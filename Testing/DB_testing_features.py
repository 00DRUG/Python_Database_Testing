import sqlite3
import shutil
import tempfile
import os
import random


def random_int():
    return random.randint(1, 20)


def clone_database(DB_NAME):
    temp_dir = tempfile.mkdtemp()
    temp_db_path = os.path.join(temp_dir, "Fleet_test.db")
    shutil.copy(DB_NAME, temp_db_path)
    return temp_db_path


def mode_a_randomize(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT ship FROM ships")
    ships = cursor.fetchall()

    for (ship,) in ships:
        component = random.choice(['weapon', 'hull', 'engine'])

        if component == 'weapon':
            cursor.execute("SELECT weapon FROM weapons ORDER BY RANDOM() LIMIT 1")
            new_value = cursor.fetchone()[0]
            cursor.execute("UPDATE ships SET weapon = ? WHERE ship = ?", (new_value, ship))

        elif component == 'hull':
            cursor.execute("SELECT hull FROM hulls ORDER BY RANDOM() LIMIT 1")
            new_value = cursor.fetchone()[0]
            cursor.execute("UPDATE ships SET hull = ? WHERE ship = ?", (new_value, ship))

        elif component == 'engine':
            cursor.execute("SELECT engine FROM engines ORDER BY RANDOM() LIMIT 1")
            new_value = cursor.fetchone()[0]
            cursor.execute("UPDATE ships SET engine = ? WHERE ship = ?", (new_value, ship))

    conn.commit()


def mode_b_randomize(conn):
    cursor = conn.cursor()

    # Weapons
    cursor.execute("SELECT weapon FROM weapons")
    for (weapon,) in cursor.fetchall():
        column = random.choice(['reload_speed', 'rotational_speed', 'diameter', 'power_volley', 'count'])
        cursor.execute(f"UPDATE weapons SET {column} = ? WHERE weapon = ?", (random_int(), weapon))

    # Hulls
    cursor.execute("SELECT hull FROM hulls")
    for (hull,) in cursor.fetchall():
        column = random.choice(['armor', 'type', 'capacity'])
        cursor.execute(f"UPDATE hulls SET {column} = ? WHERE hull = ?", (random_int(), hull))

    # Engines
    cursor.execute("SELECT engine FROM engines")
    for (engine,) in cursor.fetchall():
        column = random.choice(['power', 'type'])
        cursor.execute(f"UPDATE engines SET {column} = ? WHERE engine = ?", (random_int(), engine))

    conn.commit()
