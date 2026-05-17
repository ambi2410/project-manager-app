# \# project-manager-app

# 

# Webbasierte Projekt- und Aufgabenverwaltung für die IU-Fallstudie. Die Anwendung wurde mit \*\*Flask\*\* und \*\*SQLite\*\* umgesetzt und unterstützt Benutzerverwaltung, Rollen, Projektmanagement, Aufgabenverwaltung sowie Fortschrittsanzeige. \[1]\[2]\[3]

# 

# \## Funktionen

# 

# Die Anwendung deckt die in der Aufgabenstellung geforderten Kernfunktionen ab. Dazu gehören Benutzerkonten mit Rollen, Projekte, Mitarbeiterzuordnung, Aufgabenbearbeitung und persistente Datenspeicherung. \[1]\[2]

# 

# \- Administrator:innen können Benutzerkonten anlegen und Rollen vergeben. \[1]

# \- Projektleiter:innen können Projekte anlegen, bearbeiten und archivieren. \[1]

# \- Projektleiter:innen können mehreren Mitarbeitenden Projekte zuordnen. \[1]

# \- Mitarbeitende können Aufgaben erstellen, bearbeiten und den Status ändern. \[1]

# \- Der Projektfortschritt wird anhand erledigter Aufgaben angezeigt. \[1]

# \- Benutzer:innen können sich an- und abmelden und sehen nur berechtigte Projekte. \[1]

# 

# \## Technologiestack

# 

# Für die Umsetzung wird ein einfacher Python-Webstack mit lokaler Datenbank verwendet. Die Daten werden dauerhaft in einer SQLite-Datenbank gespeichert. \[2]\[3]

# 

# \- Python

# \- Flask

# \- SQLite

# \- HTML

# \- CSS

# 

# \## Projektstruktur

# 

# Die Anwendung ist bewusst kompakt aufgebaut. Die zentrale Logik liegt in der Flask-Anwendung, während Templates und Styles die Oberfläche darstellen. \[3]

# 

# ```text

# project-manager-app/

# ├── app.py

# ├── database.db

# ├── requirements.txt

# ├── README.md

# ├── templates/

# │   ├── index.html

# │   └── login.html

# └── static/

# &#x20;   └── style.css

# ```

# 

# \## Installation

# 

# 1\. Repository klonen:

# &#x20;  ```bash

# &#x20;  git clone <REPOSITORY-URL>

# &#x20;  cd project-manager-app

# &#x20;  ```

# 2\. Abhängigkeiten installieren:

# &#x20;  ```bash

# &#x20;  pip install -r requirements.txt

# &#x20;  ```

# 3\. Anwendung starten:

# &#x20;  ```bash

# &#x20;  python app.py

# &#x20;  ```

# 4\. Danach die Anwendung im Browser öffnen, zum Beispiel unter `http://127.0.0.1:5000/`. Flask stellt für lokale Entwicklung einen eingebauten Entwicklungsserver bereit. \[4]

# 

# \## Standardbenutzer

# 

# Beim ersten Start werden Standardbenutzer angelegt, damit die wichtigsten Rollen direkt getestet werden können. \[5]

# 

# | Benutzername | Passwort | Rolle |

# |---|---|---|

# | admin | admin | admin |

# | leiter | leiter | projektleiter |

# | mitarbeiter | mitarbeiter | mitarbeiter |

# | benutzer | benutzer | benutzer |

# 

# \## Nutzung

# 

# Nach dem Login können je nach Rolle unterschiedliche Funktionen verwendet werden. Admins verwalten Benutzer, Projektleiter verwalten Projekte und Mitarbeiter, und Mitarbeitende bearbeiten Aufgaben innerhalb ihrer berechtigten Projekte. \[1]\[5]

# 

# Ein typischer Ablauf ist:

# \- Als Admin anmelden und Benutzer anlegen.

# \- Als Projektleiter ein Projekt erstellen.

# \- Mitarbeitende dem Projekt zuordnen.

# \- Aufgaben anlegen und Benutzern zuweisen.

# \- Aufgabenstatus ändern und Fortschritt verfolgen. \[1]

# 

# \## Persistenz

# 

# Die Anwendung speichert ihre Daten persistent in der Datei `database.db`. Dadurch bleiben Benutzer, Projekte, Zuordnungen und Aufgaben auch nach einem Neustart der Anwendung erhalten. \[2]\[3]

# 

# \## Hinweise zur Abgabe

# 

# Das öffentliche GitHub-Repository ist ein Teil der Prüfungsanforderung, und dein Screenshot zeigt bereits ein öffentliches Repository. Für die vollständige Abgabe sollten zusätzlich Dokumentation, Screenshots, Datenbankbeschreibung, Architekturdiagramm und Testnachweise ergänzt werden. \[2]\[3]

