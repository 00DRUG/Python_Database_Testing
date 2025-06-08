import sqlite3
import random


def random_int():
    return random.randint(1, 20)


def populate_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Insert weapons
    for i in range(1, 21):
        cursor.execute('''
            INSERT INTO weapons (weapon, reload_speed, rotational_speed, diameter, power_volley, count)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            f"Weapon-{i}",
            random_int(),
            random_int(),
            random_int(),
            random_int(),
            random_int()
        ))

    # Insert hulls
    for i in range(1, 6):
        cursor.execute('''
            INSERT INTO hulls (hull, armor, type, capacity)
            VALUES (?, ?, ?, ?)
        ''', (
            f"Hull-{i}",
            random_int(),
            random_int(),
            random_int()
        ))

    # Insert engines
    for i in range(1, 7):
        cursor.execute('''
            INSERT INTO engines (engine, power, type)
            VALUES (?, ?, ?)
        ''', (
            f"Engine-{i}",
            random_int(),
            random_int()
        ))

    # Insert ships
    for i in range(1, 201):
        weapon_name = f"Weapon-{random.randint(1, 20)}"
        hull_name = f"Hull-{random.randint(1, 5)}"
        engine_name = f"Engine-{random.randint(1, 6)}"

        cursor.execute('''
            INSERT INTO ships (ship, weapon, hull, engine)
            VALUES (?, ?, ?, ?)
        ''', (
            f"Ship-{i}",
            weapon_name,
            hull_name,
            engine_name
        ))

    conn.commit()
    conn.close()
    print("Database populated successfully.")
