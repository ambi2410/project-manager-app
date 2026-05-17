# Project Manager App

Eine einfache Webanwendung zur Verwaltung von Projekten, Aufgaben und Benutzern.

## Überblick

Dieses Projekt wurde entwickelt, um Projekte übersichtlich zu organisieren. Es enthält verschiedene Rollen, ein Login-System und eine einfache Verwaltung von Aufgaben und Projekten.

## Funktionen

- Benutzer-Login.
- Rollenverwaltung.
- Projekte anlegen, bearbeiten und löschen.
- Aufgaben verwalten und zuweisen.
- Übersichtliche Darstellung der Daten.

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

## Projektstruktur

- `app.py` – Hauptdatei der Anwendung.
- `templates/` – HTML-Vorlagen.
- `static/` – CSS, Bilder und andere statische Dateien.
- `database.db` – Lokale Datenbank.

## Hinweise

Die Anwendung speichert Daten lokal.  
Falls Änderungen an der Datenbank nötig sind, muss die Datei entsprechend angepasst werden.