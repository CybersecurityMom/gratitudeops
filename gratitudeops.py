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
# GratitudeOps exists to remember that support with intention,
# and to return opportunity when capacity allows.
#
# Build your own private database. Keep it local. Use it your way.

PROJECT_NAME = "GratitudeOps"
PUBLIC_TEMPLATE = True
DEFAULT_DB_NAME = "gratitudeops_local.db"

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
    print(f"{PROJECT_NAME} | AQ’s Corner, LLC")
    print("Project Steward: Aqueelah Emanuel")
    print("Design Principle: Community is infrastructure.")
    print()

    if PUBLIC_TEMPLATE:
        print("Public template mode")
        print("Your data stays on your computer in a local database file.")
        print("Do not upload your database file to GitHub or share it publicly.")
        print(f"Database file in use: {DB_NAME}")
        print()


def prompt_optional(label):
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
    cur.execute("""
        INSERT INTO people
        (name, tag, specialty, contact_email, contact_phone, linkedin, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        tag,
        specialty,
        contact_email,
        contact_phone,
        linkedin,
        notes,
        datetime.now().isoformat()
    ))
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
        print("No people yet.")
        return

    print("\nPeople")
    for pid, name, tag, specialty in rows:
        details = ", ".join(filter(None, [tag, specialty]))
        print(f"{pid}. {name}" + (f" ({details})" if details else ""))
    print()


def view_person_details():
    list_people()
    person_id = input("Type the person number (id): ").strip()

    if not person_id.isdigit():
        print("Please enter a valid number.")
        return

    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, COALESCE(tag,''), COALESCE(specialty,''),
               COALESCE(contact_email,''), COALESCE(contact_phone,''),
               COALESCE(linkedin,''), COALESCE(notes,''), created_at
        FROM people
        WHERE id = ?
    """, (int(person_id),))
    row = cur.fetchone()
    conn.close()

    if not row:
        print("That person id does not exist.")
        return

    pid, name, tag, specialty, email, phone, linkedin, notes, created_at = row
    print("\nPerson details")
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
    print(f"Created: {created_at}\n")


def add_support_event():
    list_people()
    person_id = input("Type the person number (id): ").strip()

    support_type = input("Support type (intro, advice, referral, etc): ").strip()
    description = input("What exactly did they do to help: ").strip()
    impact = input("Impact level (1-5): ").strip()
    date_occurred = input("Date YYYY-MM-DD or press Enter for today: ").strip()
    evidence_link = prompt_optional("Evidence link")

    if not (person_id.isdigit() and impact.isdigit()):
        print("Person id and impact must be numbers.")
        return

    impact_int = int(impact)
    if impact_int < 1 or impact_int > 5:
        print("Impact must be between 1 and 5.")
        return

    if not date_occurred:
        date_occurred = datetime.now().date().isoformat()

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM people WHERE id = ?", (int(person_id),))
    if not cur.fetchone():
        conn.close()
        print("That person id does not exist. Add the person first.")
        return

    cur.execute("""
        INSERT INTO support_events
        (person_id, support_type, description, impact, date_occurred, evidence_link, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        int(person_id),
        support_type,
        description,
        impact_int,
        date_occurred,
        evidence_link,
        datetime.now().isoformat()
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
        print("No support events yet.")
        return

    print("\nSupport events")
    for sid, person_name, support_type, impact, date, desc, link in rows:
        print(f"{sid}. {person_name} | {support_type} | impact {impact} | {date}")
        print(f"   {desc}")
        if link:
            print(f"   Evidence: {link}")
    print()


def main_menu():
    setup_db()
    banner()

    while True:
        print()
        print("Menu (type a number and press Enter)")
        print("1. Add a person")
        print("2. List people")
        print("3. View person details")
        print("4. Add a support event")
        print("5. List support events")
        print("6. Quit")
        print()

        choice = input("Enter a menu choice (1-6): ").strip()

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
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main_menu()
