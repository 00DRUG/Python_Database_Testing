import re

import pytest
import sqlite3
import shutil
import tempfile
import os
import random

DB_FILE = 'Fleet_main.db'


def pytest_addoption(parser):
    parser.addoption("--mode", action="store", default="a", choices=['a', 'b'], help="randomization mode")


@pytest.fixture(scope="session")
def mode(request):
    return request.config.getoption("--mode")


def random_int():
    return random.randint(1, 20)


@pytest.fixture(scope='session')
def original_conn():
    conn = sqlite3.connect(DB_FILE)
    yield conn
    conn.close()


@pytest.fixture(scope="session")
def randomized_conn(tmp_path_factory, mode):
    import shutil
    temp_dir = tmp_path_factory.mktemp("data")
    temp_db_path = temp_dir / "Fleet_test.db"
    shutil.copy(DB_FILE, temp_db_path)
    conn = sqlite3.connect(temp_db_path)

    if mode == 'a':
        mode_a_randomize(conn)
    else:
        mode_b_randomize(conn)

    yield conn
    conn.close()


def mode_a_randomize(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT ship FROM ships")
    ships = cursor.fetchall()

    for (ship,) in ships:
        component = random.choice(['weapon', 'hull', 'engine'])

        if component == 'weapon':
            cursor.execute("SELECT weapon FROM weapons ORDER BY RANDOM() LIMIT 1")
            new_val = cursor.fetchone()[0]
            cursor.execute("UPDATE ships SET weapon = ? WHERE ship = ?", (new_val, ship))
        elif component == 'hull':
            cursor.execute("SELECT hull FROM hulls ORDER BY RANDOM() LIMIT 1")
            new_val = cursor.fetchone()[0]
            cursor.execute("UPDATE ships SET hull = ? WHERE ship = ?", (new_val, ship))
        else:
            cursor.execute("SELECT engine FROM engines ORDER BY RANDOM() LIMIT 1")
            new_val = cursor.fetchone()[0]
            cursor.execute("UPDATE ships SET engine = ? WHERE ship = ?", (new_val, ship))
    conn.commit()


def mode_b_randomize(conn):
    cursor = conn.cursor()

    # Weapons params
    cursor.execute("SELECT weapon FROM weapons")
    for (weapon,) in cursor.fetchall():
        col = random.choice(['reload_speed', 'rotational_speed', 'diameter', 'power_volley', 'count'])
        cursor.execute(f"UPDATE weapons SET {col} = ? WHERE weapon = ?", (random_int(), weapon))

    # Hull params
    cursor.execute("SELECT hull FROM hulls")
    for (hull,) in cursor.fetchall():
        col = random.choice(['armor', 'type', 'capacity'])
        cursor.execute(f"UPDATE hulls SET {col} = ? WHERE hull = ?", (random_int(), hull))

    # Engines params
    cursor.execute("SELECT engine FROM engines")
    for (engine,) in cursor.fetchall():
        col = random.choice(['power', 'type'])
        cursor.execute(f"UPDATE engines SET {col} = ? WHERE engine = ?", (random_int(), engine))

    conn.commit()


def extract_number(ship_id):
    match = re.search(r'\d+', ship_id)
    return int(match.group()) if match else float('inf')


def pytest_generate_tests(metafunc):
    if 'ship' in metafunc.fixturenames and 'component' in metafunc.fixturenames:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT ship FROM ships")
        ships = [row[0] for row in cursor.fetchall()]
        conn.close()
        # sorting of the ships one by numbers
        ships = sorted(ships, key=extract_number)

        components = ['weapon', 'hull', 'engine']
        '''
        params = []
        for ship in ships:  # for random of a or b method of testing
            for comp in components:
                mode = random.choice(modes)
                params.append((ship, comp, mode))
        '''
        params = [(ship, comp) for ship in ships for comp in components]

        metafunc.parametrize(
            argnames=('ship', 'component'),
            argvalues=params,
            ids=[f"{ship}-{comp}" for ship, comp in params]
        )
