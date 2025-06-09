from Extensions.DB_Creator import create_connection
from Extensions.DB_Handler import populate_database

DB_NAME = 'Fleet_main.db'


def main():
    create_connection()
    populate_database(DB_NAME)


if __name__ == '__main__':
    main()
