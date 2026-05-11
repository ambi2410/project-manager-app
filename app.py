from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'offen',
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    """)

    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    init_db()

    if request.method == "POST":
        if "project_name" in request.form:
            project_name = request.form["project_name"]
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO projects (name) VALUES (?)", (project_name,))
            conn.commit()
            conn.close()

        elif "task_title" in request.form:
            task_title = request.form["task_title"]
            project_id = request.form["project_id"]
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (project_id, title, status) VALUES (?, ?, ?)",
                (project_id, task_title, "offen")
            )
            conn.commit()
            conn.close()

        elif "toggle_task_id" in request.form:
            task_id = request.form["toggle_task_id"]
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
            current_status = cursor.fetchone()[0]

            new_status = "erledigt" if current_status == "offen" else "offen"
            cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
            conn.commit()
            conn.close()

        return redirect("/")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    conn.close()

    html = """
    <h1>Projekt- und Aufgabenmanagement</h1>

    <h2>Neues Projekt</h2>
    <form method="POST">
        <input type="text" name="project_name" placeholder="Projektname eingeben" required>
        <button type="submit">Projekt hinzufügen</button>
    </form>

    <h2>Neue Aufgabe</h2>
    <form method="POST">
        <input type="text" name="task_title" placeholder="Aufgabe eingeben" required>
        <select name="project_id" required>
    """

    for project in projects:
        html += f'<option value="{project[0]}">{project[1]}</option>'

    html += """
        </select>
        <button type="submit">Aufgabe hinzufügen</button>
    </form>

    <h2>Projekte mit Aufgaben und Fortschritt</h2>
    """

    for project in projects:
        project_tasks = [task for task in tasks if task[1] == project[0]]
        total_tasks = len(project_tasks)
        done_tasks = len([task for task in project_tasks if task[3] == "erledigt"])

        if total_tasks > 0:
            progress = round((done_tasks / total_tasks) * 100)
        else:
            progress = 0

        html += f"<h3>{project[1]}</h3>"
        html += f"<p>Fortschritt: {progress}% ({done_tasks} von {total_tasks} Aufgaben erledigt)</p>"
        html += "<ul>"

        if project_tasks:
            for task in project_tasks:
                html += f"""
                <li>
                    {task[2]} - Status: <strong>{task[3]}</strong>
                    <form method="POST" style="display:inline;">
                        <input type="hidden" name="toggle_task_id" value="{task[0]}">
                        <button type="submit">Status ändern</button>
                    </form>
                </li>
                """
        else:
            html += "<li>Keine Aufgaben vorhanden</li>"

        html += "</ul>"

    return html

if __name__ == "__main__":
    app.run(debug=True)