
import sqlite3
from datetime import datetime

DB = "helpdesk.db"

def setup():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee TEXT NOT NULL,
                issue TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT DEFAULT 'Open',
                created_at TEXT NOT NULL
            )
        """)

def create_ticket():
    print("\n--- CREATE SUPPORT TICKET ---")
    employee = input("Employee name: ").strip()
    issue = input("Describe the issue: ").strip()

    if not employee or not issue:
        print("Name and issue cannot be empty.")
        return

    print("1. Low")
    print("2. Medium")
    print("3. High")
    choice = input("Choose priority (1-3): ")

    priorities = {
        "1": "Low",
        "2": "Medium",
        "3": "High"
    }

    if choice not in priorities:
        print("Invalid priority.")
        return

    with sqlite3.connect(DB) as conn:
        cursor = conn.execute("""
            INSERT INTO tickets
            (employee, issue, priority, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            employee,
            issue,
            priorities[choice],
            datetime.now().isoformat(timespec="seconds")
        ))
        print(f"Ticket #{cursor.lastrowid} created!")

def view_tickets():
    with sqlite3.connect(DB) as conn:
        tickets = conn.execute("""
            SELECT id, employee, issue, priority, status
            FROM tickets ORDER BY id DESC
        """).fetchall()

    print("\n--- ALL SUPPORT TICKETS ---")

    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        print(f"\nTicket ID: {ticket[0]}")
        print(f"Employee: {ticket[1]}")
        print(f"Issue: {ticket[2]}")
        print(f"Priority: {ticket[3]}")
        print(f"Status: {ticket[4]}")

def resolve_ticket():
    view_tickets()

    try:
        ticket_id = int(input("\nTicket ID to resolve: "))
    except ValueError:
        print("Enter a valid number.")
        return

    with sqlite3.connect(DB) as conn:
        cursor = conn.execute("""
            UPDATE tickets SET status = 'Resolved'
            WHERE id = ? AND status = 'Open'
        """, (ticket_id,))

        if cursor.rowcount:
            print("Ticket successfully resolved!")
        else:
            print("No matching open ticket found.")

def main():
    setup()

    while True:
        print("\n===== IT HELP DESK SYSTEM =====")
        print("1. Create Ticket")
        print("2. View Tickets")
        print("3. Resolve Ticket")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            create_ticket()
        elif choice == "2":
            view_tickets()
        elif choice == "3":
            resolve_ticket()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
