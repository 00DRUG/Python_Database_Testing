from Extensions.DB_Creator import create_connection
from Extensions.DB_Handler import populate_database
from Testing.test_randomization import test_db

DB_NAME = 'Fleet_main.db'


def main():
    create_connection()
    populate_database()
    test_db(DB_NAME)


if __name__ == '__main__':
    main()
