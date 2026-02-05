# GratitudeOps

<p align="center">
  <img src="https://raw.githubusercontent.com/CybersecurityMom/gratitudeops/main/docs/screenshots/GratitudeOps-GitHub-Banner.png" alt="GratitudeOps banner" width="1280">
</p>

A project by AQ’s Corner, LLC  
Project Steward: Aqueelah Emanuel  
Design Principle: Community is infrastructure.

GratitudeOps is a simple, local-first database tool for tracking support, gratitude, and reciprocity. It is designed to help you intentionally remember the people who showed up for you and how they helped, while keeping that data private on your own computer.

This project was built in honor of the people who supported me and my business during moments of uncertainty, especially post layoff, through time, financial support, introductions, shared reputation, and quiet advocacy. GratitudeOps exists to remember that support with intention and to create space to return opportunity when capacity allows.

You can use this as a private database for yourself, or you can publish your own fork as a public template. Use it your way.

---

## What this project is (and is not)

GratitudeOps is:
- A local command-line application
- A personal or private database you control
- A public template you can fork and adapt

GratitudeOps is not:
- A hosted service
- A cloud app
- A shared database
- A social platform

Your data stays on your machine unless you choose otherwise.

---

## Tech stack

- Python 3
- SQLite (local database file)
- Visual Studio Code
- Terminal / command line interface

There are no external dependencies and no internet connection required.

---

## Screenshots

### Menu

![GratitudeOps menu](docs/screenshots/01-menu1.png)

![GratitudeOps menu](docs/screenshots/sample_menu.png)


## Quick start

1. Open a terminal in this folder
2. Run this

python3 gratitudeops.py

3. Pick menu options and add people and support events

## Your data stays local

This app creates a local database file on your computer.

Default database file name: gratitudeops_local.db

Do not upload database files to GitHub. The repo includes a .gitignore to help prevent accidental commits.

## Optional: choose a custom database file name

You can set a custom database file name like this

GRATITUDEOPS_DB=my_private_gratitude.db python3 gratitudeops.py

## Credit

Created by Aqueelah Emanuel through AQ’s Corner, LLC.

If you share or fork this project, keep the attribution.
