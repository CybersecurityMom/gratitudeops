import os
import sqlite3
from datetime import datetime

# GratitudeOps
# A project by AQ’s Corner, LLC
# Project Steward: Aqueelah Emanuel
# Design Principle: Community is infrastructure.
#
# Dedication
# This project is built in honor of the people who showed up for me and my business
# during moments of uncertainty, especially post layoff, through time, financial support,
# introductions, shared reputation, and quiet advocacy.
#
# Some gave resources.
# Some gave credibility.
# Some gave belief when outcomes were unclear.
#
# GratitudeOps exists to remember that support with intention, and to return opportunity
# when capacity allows.
#
# My hope is that others use this tool to do the same.
# Build your own private database. Keep it local. Use it your way.
# Community is infrastructure.

PROJECT_NAME = "GratitudeOps"
PUBLIC_TEMPLATE = True  # Public repo template. Users run locally.
DEFAULT_DB_NAME = "gratitudeops_local.db"  # Local only. This file should never be committed.

# Allow users to choose a custom DB file name without editing code
DB_NAME = os.getenv("GRATITUDEOPS_DB", DEFAULT_DB_NAME)


def connect():
    return sqlite3.connect(DB_NAME)


def setup_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        tag TEXT,
        specialty TEXT,
        contact_email TEXT,
        contact_phone TEXT,
        linkedin TEXT,
        notes TEXT,
        created_at TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS support_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL,
        support_type TEXT NOT NULL,
        description TEXT NOT NULL,
        impact INTEGER NOT NULL,
        date_occurred TEXT NOT NULL,
        evidence_link TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (person_id) REFERENCES people(id)
    )
    """)

    conn.commit()
    conn.close()


def banner():
    print()
    print(f"{PROJECT_NAME}  |  AQ’s Corner, LLC")
    print("Project Steward: Aqueelah Emanuel")
    print("Design Principle: Community is infrastructure.")
    print()

    if PUBLIC_TEMPLATE:
        print("Public template mode")
        print("Your data stays on your computer in a local database file.")
        print("Do not upload your database file to GitHub or share it publicly.")
        print(f"Database file in use: {DB_NAME}")
        print()


def prompt_optional(label: str) -> str:
    return input(f"{label} (press Enter to skip): ").strip()


def add_person():
    name = input("Person name (or alias): ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    tag = prompt_optional("Tag (mentor, friend, vendor, etc)")
    specialty = prompt_optional("Specialty (cybersecurity, design, editing, etc)")
    contact_email = prompt_optional("Email")
    contact_phone = prompt_optional("Phone")
    linkedin = prompt_optional("LinkedIn URL")
    notes = prompt_optional("Notes")

    conn = connect()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO people
        (name, tag, specialty, contact_email, contact_phone, linkedin, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            tag,
            specialty,
            contact_email,
            contact_phone,
            linkedin,
            notes,
            datetime.now().isoformat(),
        ),
    )
    conn.commit()
    conn.close()
    print("Saved person")


def list_people():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, COALESCE(tag,''), COALESCE(specialty,'')
        FROM people
        ORDER BY id DESC
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No people yet")
        return

    print()
    print("People")
    for pid, name, tag, specialty in rows:
        bits = [b for b in [tag, specialty] if b]
        if bits:
            print(f"{pid}. {name} ({', '.join(bits)})")
        else:
            print(f"{pid}. {name}")
    print()


def view_person_details():
    list_people()
    person_id = input("Type the person number (id): ").strip()
    try:
        person_id_int = int(person_id)
    except ValueError:
        print("That was not a number")
        return

    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, COALESCE(tag,''), COALESCE(specialty,''),
               COALESCE(contact_email,''), COALESCE(contact_phone,''),
               COALESCE(linkedin,''), COALESCE(notes,''), created_at
        FROM people
        WHERE id = ?
    """, (person_id_int,))
    row = cur.fetchone()
    conn.close()

    if not row:
        print("That person id does not exist")
        return

    pid, name, tag, specialty, email, phone, linkedin, notes, created_at = row
    print()
    print("Person details")
    print(f"ID: {pid}")
    print(f"Name: {name}")
    if tag:
        print(f"Tag: {tag}")
    if specialty:
        print(f"Specialty: {specialty}")
    if email:
        print(f"Email: {email}")
    if phone:
        print(f"Phone: {phone}")
    if linkedin:
        print(f"LinkedIn: {linkedin}")
    if notes:
        print(f"Notes: {notes}")
    print(f"Created: {created_at}")
    print()


def add_support_event():
    list_people()
    person_id = input("Type the person number (id): ").strip()

    support_type = input("Support type (intro, advice, review, referral, etc): ").strip()
    description = input("What exactly did they do to help: ").strip()
    impact = input("Impact level 1 to 5: ").strip()
    date_occurred = input("Date YYYY-MM-DD or press Enter for today: ").strip()
    evidence_link = prompt_optional("Evidence link (optional)")

    if not (person_id and support_type and description and impact):
        print("Missing required info")
        return

    try:
        person_id_int = int(person_id)
        impact_int = int(impact)
        if impact_int < 1 or impact_int > 5:
            raise ValueError
    except ValueError:
        print("Person id must be a number and impact must be 1 to 5")
        return

    if not date_occurred:
        date_occurred = datetime.now().date().isoformat()

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id FROM people WHERE id = ?", (person_id_int,))
    if not cur.fetchone():
        conn.close()
        print("That person id does not exist. Add the person first.")
        return

    cur.execute("""
        INSERT INTO support_events
        (person_id, support_type, description, impact, date_occurred, evidence_link, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        person_id_int,
        support_type,
        description,
        impact_int,
        date_occurred,
        evidence_link,
        datetime.now().isoformat(),
    ))

    conn.commit()
    conn.close()
    print("Saved support event")


def list_support_events():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT se.id, p.name, se.support_type, se.impact, se.date_occurred,
               se.description, COALESCE(se.evidence_link,'')
        FROM support_events se
        JOIN people p ON p.id = se.person_id
        ORDER BY se.id DESC
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No support events yet")
        return

    print()
    print("Support events")
    for sid, person_name, support_type, impact, date_occurred, desc, link in rows:
        print(f"{sid}. {person_name} | {support_type} | impact {impact} | {date_occurred}")
        print(f"   {desc}")
        if link:
            print(f"   Evidence: {link}")
    print()


def main_menu():
    setup_db()
    banner()

    while True:
        print("Menu")
        print("1 Add person")
        print("2 List people")
        print("3 View person details")
        print("4 Add support event")
        print("5 List support events")
        print("6 Quit")

        choice = input("Pick a number: ").strip()

        if choice == "1":
            add_person()
        elif choice == "2":
            list_people()
        elif choice == "3":
            view_person_details()
        elif choice == "4":
            add_support_event()
        elif choice == "5":
            list_support_events()
        elif choice == "6":
            print("Bye")
            break
        else:
            print("Try again")


if __name__ == "__main__":
    main_menu()