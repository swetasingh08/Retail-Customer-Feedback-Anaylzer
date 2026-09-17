import os
import mysql.connector
from mysql.connector import Error

SCHEMA_FILE = os.path.join(
    os.path.dirname(__file__),
    "schema.sql"
)


def get_config():
    """Return database configuration."""

    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", 3307)),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "MyNewPassword"),
        "database": os.getenv(
            "DB_NAME",
            "retail_feedback_db"
        )
    }


def init_db():
    """
    Create the database and initialize tables
    using schema.sql.
    """

    config = get_config()

    try:
        # ---------------------------------------
        # Connect to MySQL server
        # ---------------------------------------

        conn = mysql.connector.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            auth_plugin="mysql_native_password",
            connection_timeout=3
        )

        cursor = conn.cursor()

        # ---------------------------------------
        # Create database
        # ---------------------------------------

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{config['database']}`"
        )

        cursor.execute(
            f"USE `{config['database']}`"
        )

        # ---------------------------------------
        # Read schema.sql
        # ---------------------------------------

        if not os.path.exists(SCHEMA_FILE):
            print(
                f"Warning: {SCHEMA_FILE} not found."
            )
            cursor.close()
            conn.close()
            return False

        with open(
            SCHEMA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            schema = file.read()

        # ---------------------------------------
        # Execute SQL statements
        # ---------------------------------------

        statements = schema.split(";")

        for statement in statements:

            statement = statement.strip()

            if statement:
                cursor.execute(statement)

        conn.commit()

        print("Database initialized successfully!")

        cursor.close()
        conn.close()

        return True

    except Error as e:

        print(
            f"Error initializing database: {e}"
        )

        return False


def get_connection():
    """
    Create and return a connection to the
    retail_feedback_db database.
    """

    config = get_config()

    try:

        connection = mysql.connector.connect(
            host=config["host"],
            port=config["port"],
            database=config["database"],
            user=config["user"],
            password=config["password"],
            auth_plugin="mysql_native_password",
            connection_timeout=3
        )

        if connection.is_connected():
            return connection

    except Error as e:

        print(
            f"Database connection error: {e}"
        )

    return None


def close_connection(connection):
    """Safely close the database connection."""

    if connection and connection.is_connected():
        connection.close()


# =============================================
# TEST
# =============================================

if __name__ == "__main__":

    print("=" * 50)
    print("RETAIL FEEDBACK ANALYZER - DATABASE TEST")
    print("=" * 50)

    # Initialize database
    if init_db():

        # Test connection
        connection = get_connection()

        if connection:

            print(
                "Database connected successfully!"
            )

            print(
                f"Database: {connection.database}"
            )

            close_connection(connection)

            print(
                "Database connection closed."
            )

        else:

            print(
                "Database connection failed."
            )

    else:

        print(
            "Database initialization failed."
        )
