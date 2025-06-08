import sqlite3


def create_connection():
    try:
        conn = sqlite3.connect('Fleet_main.db')
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS weapons (
            weapon TEXT PRIMARY KEY,
            reload_speed INTEGER,
            rotational_speed INTEGER,
            diameter INTEGER,
            power_volley INTEGER,
            count INTEGER
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS hulls (
            hull TEXT PRIMARY KEY,
            armor INTEGER,
            type INTEGER,
            capacity INTEGER
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS engines (
            engine TEXT PRIMARY KEY,
            power INTEGER,
            type INTEGER
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ships (
            ship TEXT PRIMARY KEY,
            weapon TEXT,
            hull TEXT,
            engine TEXT,
            FOREIGN KEY (weapon) REFERENCES weapons(weapon),
            FOREIGN KEY (hull) REFERENCES hulls(hull),
            FOREIGN KEY (engine) REFERENCES engines(engine)
        )
        ''')
        conn.commit()
        print("Database created successfully.")
    except sqlite3.Error as e:
        print("Database connection error.Error:" + e)
    finally:
        conn.close()
