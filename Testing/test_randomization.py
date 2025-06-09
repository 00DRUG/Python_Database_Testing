import pytest


def get_ship_components(conn, ship):
    cursor = conn.cursor()
    cursor.execute("SELECT weapon, hull, engine FROM ships WHERE ship = ?", (ship,))
    row = cursor.fetchone()
    if row:
        return {'weapon': row[0], 'hull': row[1], 'engine': row[2]}
    return None


def get_weapon_params(conn, weapon):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT reload_speed, rotational_speed, diameter, power_volley, count FROM weapons WHERE weapon = ?",
        (weapon,))
    return cursor.fetchone()


def get_hull_params(conn, hull):
    cursor = conn.cursor()
    cursor.execute("SELECT armor, type, capacity FROM hulls WHERE hull = ?", (hull,))
    return cursor.fetchone()


def get_engine_params(conn, engine):
    cursor = conn.cursor()
    cursor.execute("SELECT power, type FROM engines WHERE engine = ?", (engine,))
    return cursor.fetchone()


@pytest.mark.usefixtures("randomized_conn")
def test_component_integrity(original_conn, randomized_conn, ship, component, mode):
    orig_comp = get_ship_components(original_conn, ship)
    rand_comp = get_ship_components(randomized_conn, ship)

    if mode == 'a':
        orig_value = orig_comp[component]
        rand_value = rand_comp[component]
        assert orig_value == rand_value, (
            f"{ship}, {rand_value} \n"
            f"expected: {orig_value} , was {rand_value}"
        )
    else:
        if component == 'weapon':
            orig_params = get_weapon_params(original_conn, orig_comp['weapon'])
            rand_params = get_weapon_params(randomized_conn, rand_comp['weapon'])
            cols = ['reload speed', 'rotational speed', 'diameter', 'power volley', 'count']
        elif component == 'hull':
            orig_params = get_hull_params(original_conn, orig_comp['hull'])
            rand_params = get_hull_params(randomized_conn, rand_comp['hull'])
            cols = ['armor', 'type', 'capacity']
        else:  # engine
            orig_params = get_engine_params(original_conn, orig_comp['engine'])
            rand_params = get_engine_params(randomized_conn, rand_comp['engine'])
            cols = ['power', 'type']

        diffs = [
            f"\n{col}: expected {o}, was {r}"
            for col, o, r in zip(cols, orig_params, rand_params)
            if o != r
        ]
        if diffs:
            raise AssertionError(f"{ship}, {rand_comp[component]}" + " ".join(diffs))
