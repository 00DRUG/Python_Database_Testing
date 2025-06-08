import sqlite3
import os
import pytest
from Testing.DB_testing_features import clone_database, mode_a_randomize, mode_b_randomize

@pytest.fixture
def test_db(DB_NAME):
    temp_db_path = clone_database(DB_NAME)
    conn = sqlite3.connect(temp_db_path)
    yield conn
    conn.close()
    os.remove(temp_db_path)

def test_mode_a_randomizes_one_component(test_db):
    cursor = test_db.cursor()
    cursor.execute("SELECT ship, weapon, hull, engine FROM ships")
    before = {row[0]: row[1:] for row in cursor.fetchall()}

    mode_a_randomize(test_db)

    cursor.execute("SELECT ship, weapon, hull, engine FROM ships")
    after = {row[0]: row[1:] for row in cursor.fetchall()}

    changed = sum(1 for ship in before if before[ship] != after[ship])
    assert changed > 0, "No ship components were changed in Mode A"

def test_mode_b_randomizes_component_parameters(test_db):
    cursor = test_db.cursor()
    cursor.execute("SELECT * FROM weapons")
    weapons_before = cursor.fetchall()

    mode_b_randomize(test_db)

    cursor.execute("SELECT * FROM weapons")
    weapons_after = cursor.fetchall()

    changed = any(b != a for b, a in zip(weapons_before, weapons_after))
    assert changed, "No weapon parameter was changed in Mode B"
