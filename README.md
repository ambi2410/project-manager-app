# Project Manager App

Eine Webanwendung zur einfachen Verwaltung von Projekten, Aufgaben und Benutzern.

## Überblick

Dieses Projekt wurde entwickelt, um Arbeitsabläufe übersichtlich zu organisieren und die Verwaltung von Projekten zu erleichtern. Es bietet ein Login-System, verschiedene Rollen und eine strukturierte Oberfläche, damit Benutzer ihre Aufgaben und Projekte schnell bearbeiten können.

Die Anwendung ist einfach aufgebaut und eignet sich gut als Schul- oder Studienprojekt, da sie wichtige Grundlagen wie Benutzerverwaltung, Datenorganisation und einfache Webentwicklung kombiniert.

## Funktionen

- Benutzer-Login mit verschiedenen Rollen.
- Projekte anlegen, bearbeiten und löschen.
- Aufgaben verwalten und zuweisen.
- Übersichtliche Darstellung aller Einträge.
- Einfache und gut strukturierte Benutzeroberfläche.
- Lokale Speicherung der Daten.

## Installation

```bash
git clone <dein-repository-link>
cd <dein-projektordner>
pip install -r requirements.txt
```

## Starten

```bash
python app.py
```

## Testzugänge

- Admin: admin / admin
- Leiter: leiter / leiter
- Mitarbeiter: mitarbeiter / mitarbeiter
- Benutzer: benutzer / benutzer

## Projektstruktur

- `app.py` – Hauptdatei der Anwendung.
- `templates/` – HTML-Vorlagen für die Seiten.
- `static/` – CSS, Bilder und andere statische Dateien.
- `database.db` – Lokale Datenbank mit den gespeicherten Daten.

## Hinweise

Die Anwendung speichert alle Daten lokal auf dem Gerät.  
Wenn du Änderungen am Aufbau oder an der Datenbank machst, muss die Datei entsprechend angepasst werden.

Das Projekt wurde bewusst einfach gehalten, damit es leicht verständlich und gut erweiterbar bleibt.