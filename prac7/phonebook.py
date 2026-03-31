import psycopg2
import csv
from connect import connect

def create_table():
    command = """CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                phone VARCHAR(20) NOT NULL
            );"""
    cur.execute(command)
    con.commit()

def insert_contact(name, phone):
    command = "INSERT INTO contacts(name, phone) VALUES(%s, %s)"
    cur.execute(command, (name, phone))
    con.commit()

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    insert_contact(name, phone)
    print(f"Added: {name} - {phone}")

def insert_from_csv(csv_file):
    command = "INSERT INTO contacts(name, phone) VALUES(%s, %s)"
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            name, phone = row
            cur.execute(command, (name, phone))
    con.commit()
    print(f"Imported contacts from {csv_file}")

# --- SELECT ---

def get_all_contacts():
    command = "SELECT * FROM contacts ORDER BY name"
    cur.execute(command)
    return cur.fetchall()

def search_contacts(pattern):
    command = "SELECT * FROM contacts WHERE name ILIKE %s OR phone ILIKE %s"
    like_pattern = f"%{pattern}%"
    cur.execute(command, (like_pattern, like_pattern))
    return cur.fetchall()

def search_contacts(cur, name=None, phone=None, prefix=None):
    query = "SELECT * FROM contacts WHERE 1=1"
    params = []

    if name:
        query += " AND name ILIKE %s"
        params.append(f"%{name}%")

    if phone:
        query += " AND phone = %s"
        params.append(phone)

    if prefix:
        query += " AND phone LIKE %s"
        params.append(prefix + "%")

    cur.execute(query, tuple(params))
    return cur.fetchall()

# --- UPDATE ---

def update_phone(name, new_phone):
    command = "UPDATE contacts SET phone = %s WHERE name = %s"
    cur.execute(command, (new_phone, name))
    con.commit()
    print(f"Updated {cur.rowcount} row(s)")

def update_name(phone, new_name):
    command = "UPDATE contacts SET name = %s WHERE phone = %s"
    cur.execute(command, (new_name, phone))
    con.commit()
    print(f"Updated {cur.rowcount} row(s)")

# --- DELETE ---

def delete_by_name(name):
    command = "DELETE FROM contacts WHERE name = %s"
    cur.execute(command, (name,))
    con.commit()
    print(f"Deleted {cur.rowcount} row(s)")

def delete_by_phone(phone):
    command = "DELETE FROM contacts WHERE phone = %s"
    cur.execute(command, (phone,))
    con.commit()
    print(f"Deleted {cur.rowcount} row(s)")

# --- Main menu ---

def print_contacts(contacts):
    if not contacts:
        print("  (no contacts)")
        return
    for c in contacts:
        print(f"  [{c[0]}] {c[1]} - {c[2]}")

def main():
    global con , cur
    con, cur = connect()

    create_table()

    while True:
        print("\n--- PhoneBook ---")
        print("1. Show all contacts")
        print("2. Add contact (console)")
        print("3. Import from CSV")
        print("4. Search")
        print("5. Update phone by name")
        print("6. Update name by phone")
        print("7. Delete by name")
        print("8. Delete by phone")
        print("9. Query contacts with filters")
        print("0. Exit")

        choice = input("\nChoice: ")

        if choice == "1":
            print_contacts(get_all_contacts())
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            filename = input("CSV file path: ")
            insert_from_csv(filename)
        elif choice == "4":
            pattern = input("Search: ")
            print_contacts(search_contacts(pattern))
        elif choice == "5":
            name = input("Name: ")
            new_phone = input("New phone: ")
            update_phone(name, new_phone)
        elif choice == "6":
            phone = input("Phone: ")
            new_name = input("New name: ")
            update_name(phone, new_name)
        elif choice == "7":
            name = input("Name: ")
            delete_by_name(name)
        elif choice == "8":
            phone = input("Phone: ")
            delete_by_phone(phone)
        elif choice == "9":
            name = input("Name (enter to skip): ")
            phone = input("Phone (enter to skip): ")
            prefix = input("Prefix (enter to skip): ")
            results = search_contacts(
                cur,
                name=name if name else None,
                phone=phone if phone else None,
                prefix=prefix if prefix else None
            )
            print_contacts(results)
        elif choice == "0":
            break
        else:
            print("Invalid choice")

    con.close()
    cur.close()
    print("Goodbye!")

if __name__ == "__main__":
    main()