from flask import Flask, request, redirect, render_template, session, url_for
import sqlite3

app = Flask(__name__, template_folder="templates")
app.secret_key = "supersecretkey123"


def get_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def add_column_if_missing(cursor, table_name, column_name, column_definition):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]
    if column_name not in columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}")


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            leader_id INTEGER,
            archived INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (leader_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'offen',
            assigned_user_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (assigned_user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS project_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            UNIQUE(project_id, user_id),
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    default_users = [
        ("admin", "admin", "admin"),
        ("leiter", "leiter", "projektleiter"),
        ("mitarbeiter", "mitarbeiter", "mitarbeiter"),
        ("benutzer", "benutzer", "benutzer")
    ]

    for username, password, role in default_users:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role)
            )

    conn.commit()
    conn.close()


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None

    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user


def is_logged_in():
    return "user_id" in session


def is_project_member(project_id, user_id):
    conn = get_connection()
    member = conn.execute(
        "SELECT * FROM project_members WHERE project_id = ? AND user_id = ?",
        (project_id, user_id)
    ).fetchone()
    conn.close()
    return member is not None


def can_access_project(user, project):
    if user["role"] == "admin":
        return True
    if project["leader_id"] == user["id"]:
        return True
    if is_project_member(project["id"], user["id"]):
        return True
    return False


def can_manage_project(user, project):
    return user["role"] == "admin" or project["leader_id"] == user["id"]


@app.route("/login", methods=["GET", "POST"])
def login():
    init_db()

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        conn = get_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            return redirect(url_for("home"))
        return render_template("login.html", error="Falscher Benutzername oder falsches Passwort.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
def home():
    init_db()

    if not is_logged_in():
        return redirect(url_for("login"))

    current_user = get_current_user()
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        if "project_name" in request.form:
            project_name = request.form["project_name"].strip()
            leader_id = request.form.get("leader_id")

            if project_name and current_user["role"] in ["admin", "projektleiter"]:
                if current_user["role"] == "projektleiter":
                    leader_id = current_user["id"]

                cursor.execute(
                    "INSERT INTO projects (name, leader_id, archived) VALUES (?, ?, 0)",
                    (project_name, leader_id if leader_id else None)
                )

        elif "task_title" in request.form and "project_id" in request.form:
            task_title = request.form["task_title"].strip()
            project_id = request.form["project_id"]
            assigned_user_id = request.form.get("assigned_user_id")

            project = cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()

            if task_title and project and can_access_project(current_user, project):
                cursor.execute(
                    "INSERT INTO tasks (project_id, title, status, assigned_user_id) VALUES (?, ?, ?, ?)",
                    (project_id, task_title, "offen", assigned_user_id if assigned_user_id else None)
                )

        elif "assign_task_user_id" in request.form and "assign_task_id" in request.form:
            task_id = request.form["assign_task_id"]
            assigned_user_id = request.form["assign_task_user_id"]

            task = cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            if task:
                project = cursor.execute("SELECT * FROM projects WHERE id = ?", (task["project_id"],)).fetchone()
                if project and can_manage_project(current_user, project):
                    cursor.execute(
                        "UPDATE tasks SET assigned_user_id = ? WHERE id = ?",
                        (assigned_user_id if assigned_user_id else None, task_id)
                    )

        elif "assign_member_user_id" in request.form and "assign_member_project_id" in request.form:
            user_id = request.form["assign_member_user_id"]
            project_id = request.form["assign_member_project_id"]

            project = cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
            if project and can_manage_project(current_user, project) and user_id:
                cursor.execute(
                    "INSERT OR IGNORE INTO project_members (project_id, user_id) VALUES (?, ?)",
                    (project_id, user_id)
                )

        elif "remove_member_user_id" in request.form and "remove_member_project_id" in request.form:
            user_id = request.form["remove_member_user_id"]
            project_id = request.form["remove_member_project_id"]

            project = cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
            if project and can_manage_project(current_user, project):
                cursor.execute(
                    "DELETE FROM project_members WHERE project_id = ? AND user_id = ?",
                    (project_id, user_id)
                )

        elif "toggle_task_id" in request.form:
            task_id = request.form["toggle_task_id"]
            task = cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

            if task:
                project = cursor.execute("SELECT * FROM projects WHERE id = ?", (task["project_id"],)).fetchone()
                if project and can_access_project(current_user, project):
                    new_status = "erledigt" if task["status"] != "erledigt" else "offen"
                    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))

        elif "delete_task_id" in request.form:
            task_id = request.form["delete_task_id"]
            task = cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

            if task:
                project = cursor.execute("SELECT * FROM projects WHERE id = ?", (task["project_id"],)).fetchone()
                if project and can_manage_project(current_user, project):
                    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

        elif "archive_project_id" in request.form:
            project_id = request.form["archive_project_id"]
            project = cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()

            if project and can_manage_project(current_user, project):
                cursor.execute("UPDATE projects SET archived = 1 WHERE id = ?", (project_id,))

        elif "unarchive_project_id" in request.form:
            project_id = request.form["unarchive_project_id"]
            project = cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()

            if project and can_manage_project(current_user, project):
                cursor.execute("UPDATE projects SET archived = 0 WHERE id = ?", (project_id,))

        elif "delete_project_id" in request.form:
            project_id = request.form["delete_project_id"]
            project = cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()

            if project and current_user["role"] == "admin":
                cursor.execute("DELETE FROM tasks WHERE project_id = ?", (project_id,))
                cursor.execute("DELETE FROM project_members WHERE project_id = ?", (project_id,))
                cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))

        elif "edit_project_id" in request.form:
            project_id = request.form["edit_project_id"]
            new_project_name = request.form["new_project_name"].strip()

            project = cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
            if project and new_project_name and can_manage_project(current_user, project):
                cursor.execute("UPDATE projects SET name = ? WHERE id = ?", (new_project_name, project_id))

        elif "edit_task_id" in request.form:
            task_id = request.form["edit_task_id"]
            new_task_title = request.form["new_task_title"].strip()

            task = cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            if task:
                project = cursor.execute("SELECT * FROM projects WHERE id = ?", (task["project_id"],)).fetchone()
                if project and new_task_title and can_access_project(current_user, project):
                    cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (new_task_title, task_id))

        elif "new_username" in request.form and "new_password" in request.form and "new_role" in request.form:
            if current_user["role"] == "admin":
                new_username = request.form["new_username"].strip()
                new_password = request.form["new_password"].strip()
                new_role = request.form["new_role"].strip()

                if new_username and new_password and new_role:
                    existing = cursor.execute(
                        "SELECT * FROM users WHERE username = ?",
                        (new_username,)
                    ).fetchone()

                    if existing is None:
                        cursor.execute(
                            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                            (new_username, new_password, new_role)
                        )

        conn.commit()
        conn.close()
        return redirect(url_for("home"))

    users = cursor.execute("SELECT * FROM users ORDER BY username ASC").fetchall()
    projects_raw = cursor.execute("SELECT * FROM projects ORDER BY archived ASC, id DESC").fetchall()
    tasks_raw = cursor.execute("SELECT * FROM tasks ORDER BY id ASC").fetchall()
    member_rows = cursor.execute("""
        SELECT pm.project_id, pm.user_id, u.username
        FROM project_members pm
        JOIN users u ON pm.user_id = u.id
        ORDER BY u.username ASC
    """).fetchall()
    conn.close()

    visible_projects = [project for project in projects_raw if can_access_project(current_user, project)]

    active_projects = []
    archived_projects = []

    user_lookup = {user["id"]: user["username"] for user in users}

    for project in visible_projects:
        project_tasks = [task for task in tasks_raw if task["project_id"] == project["id"]]
        project_members = [m for m in member_rows if m["project_id"] == project["id"]]

        prepared_tasks = []
        for task in project_tasks:
            assigned_username = "Niemand"
            if task["assigned_user_id"] in user_lookup:
                assigned_username = user_lookup[task["assigned_user_id"]]

            prepared_tasks.append({
                "id": task["id"],
                "project_id": task["project_id"],
                "title": task["title"],
                "status": task["status"],
                "assigned_user_id": task["assigned_user_id"],
                "assigned_username": assigned_username
            })

        total_tasks = len(prepared_tasks)
        done_tasks = len([task for task in prepared_tasks if task["status"] == "erledigt"])
        progress = round((done_tasks / total_tasks) * 100) if total_tasks > 0 else 0

        leader_name = "-"
        if project["leader_id"] in user_lookup:
            leader_name = user_lookup[project["leader_id"]]

        project_data = {
            "id": project["id"],
            "name": project["name"],
            "leader_id": project["leader_id"],
            "leader_name": leader_name,
            "archived": project["archived"],
            "tasks": prepared_tasks,
            "members": project_members,
            "total_tasks": total_tasks,
            "done_tasks": done_tasks,
            "progress": progress
        }

        if project["archived"] == 1:
            archived_projects.append(project_data)
        else:
            archived_projects if False else active_projects.append(project_data)

    return render_template(
        "index.html",
        current_user=current_user,
        users=users,
        active_projects=active_projects,
        archived_projects=archived_projects
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)