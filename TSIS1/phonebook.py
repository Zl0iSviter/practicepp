import csv
import json
import sys
from datetime import datetime,date
from connect import connect

PAGE_SIZE = 5   # rows per page for paginated views


def _fmt_row(row) -> str:

    cid, name, email, birthday, grp, phones, created = row
    parts = [f"[{cid}] {name}"]
    if grp:
        parts.append(f"  Group   : {grp}")
    if email:
        parts.append(f"  E-mail  : {email}")
    if birthday:
        parts.append(f"  Birthday: {birthday}")
    if phones:
        parts.append(f"  Phones  : {phones}")
    parts.append(f"  Added   : {created.strftime('%Y-%m-%d') if created else '-'}")
    return "\n".join(parts)


def _input_date(prompt: str):

    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date – skipping birthday.")
        return None


def _pick_group(conn) -> int | None:

    cur = conn.cursor()
    cur.execute("SELECT id, name FROM groups ORDER BY id")
    groups = cur.fetchall()
    print("  Groups:")
    for gid, gname in groups:
        print(f"    {gid}. {gname}")
    raw = input("  Choose group number (or leave blank): ").strip()
    if not raw:
        return None
    try:
        chosen_id = int(raw)
        if any(g[0] == chosen_id for g in groups):
            return chosen_id
    except ValueError:
        pass
    print(" Unknown choice – no group assigned.")
    return None


def add_contact():

    conn = connect()
    cur = conn.cursor()

    name = input("Name: ").strip()
    if not name:
        print(" Name cannot be empty.")
        conn.close()
        return

    email    = input("E-mail (optional): ").strip() or None
    birthday = _input_date("Birthday YYYY-MM-DD (optional): ")
    group_id = _pick_group(conn)

    cur.execute(
        "INSERT INTO contacts(name, email, birthday, group_id) VALUES (%s,%s,%s,%s) RETURNING id",
        (name, email, birthday, group_id)
    )
    contact_id = cur.fetchone()[0]


    while True:
        phone = input("Phone number (leave blank to stop): ").strip()
        if not phone:
            break
        ptype = input("  Type (home/work/mobile) [mobile]: ").strip().lower() or "mobile"
        if ptype not in ("home", "work", "mobile"):
            ptype = "mobile"
        cur.execute(
            "INSERT INTO phones(contact_id, phone, type) VALUES (%s,%s,%s)",
            (contact_id, phone, ptype)
        )

    conn.commit()
    conn.close()
    print(f"✓ Contact '{name}' added (id={contact_id}).")


def add_phone_to_contact():

    conn = connect()
    cur = conn.cursor()

    name  = input("Contact name: ").strip()
    phone = input("New phone number: ").strip()
    ptype = input("Type (home/work/mobile) [mobile]: ").strip().lower() or "mobile"
    if ptype not in ("home", "work", "mobile"):
        ptype = "mobile"

    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        conn.commit()
        print(f" Phone {phone} ({ptype}) added to '{name}'.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        conn.close()


def move_contact_to_group():
    conn = connect()
    cur = conn.cursor()

    name  = input("Contact name: ").strip()
    group = input("Group name: ").strip()

    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        print(f"'{name}' moved to group '{group}'.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        conn.close()


def delete_contact():

    conn = connect()
    cur = conn.cursor()

    val = input("Name or phone to delete: ").strip()

    # New contacts table
    cur.execute(
        "DELETE FROM contacts WHERE name = %s OR id IN "
        "(SELECT contact_id FROM phones WHERE phone = %s)",
        (val, val)
    )
    deleted = cur.rowcount
    cur.execute("CALL delete_user(%s)", (val,))

    conn.commit()
    conn.close()
    print(f" Deleted {deleted} contact(s) matching '{val}'.")



def search_contacts():
    conn = connect()
    cur = conn.cursor()

    query = input("Search (name / email / phone): ").strip()
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("  No results found.")
        return

    contacts: dict = {}
    for cid, name, email, birthday, grp, phone, ptype in rows:
        if cid not in contacts:
            contacts[cid] = {
                "name": name, "email": email, "birthday": birthday,
                "grp": grp, "phones": []
            }
        if phone:
            contacts[cid]["phones"].append(f"{phone} ({ptype or '?'})")

    for cid, c in contacts.items():
        print(f"\n[{cid}] {c['name']}")
        if c["grp"]:     print(f"  Group   : {c['grp']}")
        if c["email"]:   print(f"  E-mail  : {c['email']}")
        if c["birthday"]:print(f"  Birthday: {c['birthday']}")
        if c["phones"]:  print(f"  Phones  : {', '.join(c['phones'])}")


def filter_by_group():

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT name FROM groups ORDER BY name")
    groups = [r[0] for r in cur.fetchall()]
    print("Available groups:", ", ".join(groups))
    group = input("Group name: ").strip()

    offset = 0
    while True:
        cur.execute(
            "SELECT * FROM get_contacts_by_group(%s, %s, %s)",
            (group, PAGE_SIZE, offset)
        )
        rows = cur.fetchall()
        if not rows:
            print("  (no more contacts)")
            break
        for row in rows:
            cid, name, email, birthday, phones = row
            print(f"\n[{cid}] {name}")
            if email:   print(f"  E-mail  : {email}")
            if birthday:print(f"  Birthday: {birthday}")
            if phones:  print(f"  Phones  : {phones}")
        cmd = input("\n[n]ext  [p]rev  [q]uit: ").strip().lower()
        if cmd == "n":
            offset += PAGE_SIZE
        elif cmd == "p":
            offset = max(0, offset - PAGE_SIZE)
        else:
            break

    conn.close()

def show_all():
    sort_opts = {"1": "name", "2": "birthday", "3": "created_at"}
    print("Sort by:  1) Name   2) Birthday   3) Date added")
    sort_key = sort_opts.get(input("Choice [1]: ").strip(), "name")

    conn = connect()
    cur = conn.cursor()
    offset = 0

    while True:
        cur.execute("SELECT * FROM get_contacts(%s, %s, %s)", (PAGE_SIZE, offset, sort_key))
        rows = cur.fetchall()
        if not rows:
            print("  (no more contacts)")
            break
        for row in rows:
            print("\n" + _fmt_row(row))
        print(f"\n  — page {offset // PAGE_SIZE + 1} —")
        cmd = input("[n]ext  [p]rev  [q]uit: ").strip().lower()
        if cmd == "n":
            offset += PAGE_SIZE
        elif cmd == "p":
            offset = max(0, offset - PAGE_SIZE)
        else:
            break

    conn.close()


def export_json():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email,
               c.birthday::text,
               g.name AS grp,
               c.created_at::text
        FROM   contacts c
        LEFT   JOIN groups g ON g.id = c.group_id
        ORDER  BY c.name
    """)
    contacts_raw = cur.fetchall()

    out = []
    for cid, name, email, birthday, grp, created in contacts_raw:
        cur.execute(
            "SELECT phone, type FROM phones WHERE contact_id = %s ORDER BY id",
            (cid,)
        )
        phones = [{"phone": p, "type": t} for p, t in cur.fetchall()]
        out.append({
            "name": name,
            "email": email,
            "birthday": birthday,
            "group": grp,
            "phones": phones,
            "created_at": created
        })

    conn.close()

    filename = input("Output filename [contacts.json]: ").strip() or "contacts.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Exported {len(out)} contact(s) to '{filename}'.")


def import_json():

    filename = input("JSON filename [contacts.json]: ").strip() or "contacts.json"
    try:
        with open(filename, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f" File '{filename}' not found.")
        return
    except json.JSONDecodeError as e:
        print(f" Invalid JSON: {e}")
        return

    conn = connect()
    cur = conn.cursor()
    added = skipped = overwritten = 0

    for item in data:
        name     = item.get("name", "").strip()
        email    = item.get("email")
        birthday = item.get("birthday")
        group    = item.get("group")
        phones   = item.get("phones", [])

        if not name:
            continue

        # Resolve group id
        group_id = None
        if group:
            cur.execute(
                "INSERT INTO groups(name) VALUES (%s) ON CONFLICT(name) DO NOTHING",
                (group,)
            )
            cur.execute("SELECT id FROM groups WHERE name = %s", (group,))
            row = cur.fetchone()
            if row:
                group_id = row[0]

        # Check duplicate
        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()

        if existing:
            print(f"  Duplicate: '{name}'  [s]kip / [o]verwrite? ", end="")
            choice = input().strip().lower()
            if choice == "o":
                cur.execute(
                    "UPDATE contacts SET email=%s, birthday=%s, group_id=%s WHERE id=%s",
                    (email, birthday, group_id, existing[0])
                )
                cur.execute("DELETE FROM phones WHERE contact_id = %s", (existing[0],))
                contact_id = existing[0]
                overwritten += 1
            else:
                skipped += 1
                continue
        else:
            cur.execute(
                "INSERT INTO contacts(name, email, birthday, group_id) "
                "VALUES (%s,%s,%s,%s) RETURNING id",
                (name, email, birthday, group_id)
            )
            contact_id = cur.fetchone()[0]
            added += 1

        # Insert phones
        for p in phones:
            pnum  = p.get("phone", "").strip()
            ptype = p.get("type", "mobile")
            if ptype not in ("home", "work", "mobile"):
                ptype = "mobile"
            if pnum:
                cur.execute(
                    "INSERT INTO phones(contact_id, phone, type) VALUES (%s,%s,%s)",
                    (contact_id, pnum, ptype)
                )

    conn.commit()
    conn.close()
    print(f"Import done — added: {added}, overwritten: {overwritten}, skipped: {skipped}.")


def import_csv():
    filename = input("CSV filename [contacts.csv]: ").strip() or "contacts.csv"
    try:
        f = open(filename, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f" File '{filename}' not found.")
        return

    conn = connect()
    cur = conn.cursor()
    added = errors = 0

    with f:
        reader = csv.DictReader(f)
        for row in reader:
            name  = (row.get("name") or "").strip()
            phone = (row.get("phone") or "").strip()
            if not name or not phone:
                errors += 1
                continue

            ptype    = (row.get("type") or "mobile").strip().lower()
            if ptype not in ("home", "work", "mobile"):
                ptype = "mobile"
            email    = (row.get("email") or "").strip() or None
            birthday_raw = (row.get("birthday") or "").strip()
            birthday = None
            if birthday_raw:
                try:
                    birthday = datetime.strptime(birthday_raw, "%Y-%m-%d").date()
                except ValueError:
                    pass
            group    = (row.get("group") or "").strip() or None

            # Resolve / create group
            group_id = None
            if group:
                cur.execute(
                    "INSERT INTO groups(name) VALUES (%s) ON CONFLICT(name) DO NOTHING",
                    (group,)
                )
                cur.execute("SELECT id FROM groups WHERE name = %s", (group,))
                r = cur.fetchone()
                if r:
                    group_id = r[0]

            # Upsert contact
            cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
            existing = cur.fetchone()
            if existing:
                contact_id = existing[0]
                cur.execute(
                    "UPDATE contacts SET email=COALESCE(%s,email), "
                    "birthday=COALESCE(%s,birthday), group_id=COALESCE(%s,group_id) "
                    "WHERE id=%s",
                    (email, birthday, group_id, contact_id)
                )
            else:
                cur.execute(
                    "INSERT INTO contacts(name, email, birthday, group_id) "
                    "VALUES (%s,%s,%s,%s) RETURNING id",
                    (name, email, birthday, group_id)
                )
                contact_id = cur.fetchone()[0]

            cur.execute(
                "INSERT INTO phones(contact_id, phone, type) VALUES (%s,%s,%s)",
                (contact_id, phone, ptype)
            )
            added += 1

    conn.commit()
    conn.close()
    print(f"✓ CSV import done — {added} row(s) processed, {errors} skipped.")


def legacy_add(name, phone):
    conn = connect(); cur = conn.cursor()
    cur.execute("CALL upsert_user(%s, %s)", (name, phone))
    conn.commit(); conn.close()

def legacy_search(pattern):
    conn = connect(); cur = conn.cursor()
    cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
    for r in cur.fetchall(): print(r)
    conn.close()

def legacy_show(limit, offset):
    conn = connect(); cur = conn.cursor()
    cur.execute("SELECT * FROM get_phonebook(%s, %s)", (limit, offset))
    for r in cur.fetchall(): print(r)
    conn.close()

def legacy_delete(val):
    conn = connect(); cur = conn.cursor()
    cur.execute("CALL delete_user(%s)", (val,))
    conn.commit(); conn.close()

def legacy_insert_many(names, phones):
    conn = connect(); cur = conn.cursor()
    cur.execute("CALL insert_many(%s, %s)", (names, phones))
    conn.commit(); conn.close()


MENU = """
╔══════════════════════════════════════╗
║      PhoneBook v2  –  Main Menu      ║
╠══════════════════════════════════════╣
║  Contact management                  ║
║   1. Add / update contact (full)     ║
║   2. Add extra phone to contact      ║
║   3. Move contact to group           ║
║   4. Delete contact                  ║
╠══════════════════════════════════════╣
║  Search & Browse                     ║
║   5. Search (name / email / phone)   ║
║   6. Filter by group                 ║
║   7. Show all (paginated + sort)     ║
╠══════════════════════════════════════╣
║  Import / Export                     ║
║   8. Export contacts → JSON          ║
║   9. Import contacts ← JSON          ║
║  10. Import contacts ← CSV (extended)║
╠══════════════════════════════════════╣
║  Commands from prac7,8               ║
║  11. Legacy add / upsert             ║
║  12. Legacy search                   ║
║  13. Legacy show (paginated)         ║
║  14. Legacy delete                   ║
║  15. Legacy bulk insert              ║
╠══════════════════════════════════════╣
║   0. Exit                            ║
╚══════════════════════════════════════╝
"""


def main():
    actions = {
        "1":  add_contact,
        "2":  add_phone_to_contact,
        "3":  move_contact_to_group,
        "4":  delete_contact,
        "5":  search_contacts,
        "6":  filter_by_group,
        "7":  show_all,
        "8":  export_json,
        "9":  import_json,
        "10": import_csv,
        "11": lambda: legacy_add(
                  input("Name: ").strip(),
                  input("Phone: ").strip()),
        "12": lambda: legacy_search(input("Search pattern: ").strip()),
        "13": lambda: legacy_show(
                  int(input("Limit: ")),
                  int(input("Offset: "))),
        "14": lambda: legacy_delete(input("Name or phone: ").strip()),
        "15": _legacy_bulk_insert,
    }

    while True:
        print(MENU)
        choice = input("Choice: ").strip()
        if choice == "0":
            print("Bye!")
            sys.exit(0)
        action = actions.get(choice)
        if action:
            try:
                action()
            except Exception as e:
                print(f"✗ Unexpected error: {e}")
        else:
            print("✗ Unknown choice.")


def _legacy_bulk_insert():
    n = int(input("How many entries: "))
    names, phones = [], []
    for i in range(n):
        names.append(input(f"  Name {i+1}: "))
        phones.append(input(f"  Phone {i+1}: "))
    legacy_insert_many(names, phones)


if __name__ == "__main__":
    main()
