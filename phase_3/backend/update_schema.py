import sqlite3
from datetime import datetime

def update_database_schema():
    """Update the database schema to add new columns for the enhanced Todo app."""
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # Add the new columns to the item table
    try:
        # Add completed column (default False)
        cursor.execute("ALTER TABLE item ADD COLUMN completed BOOLEAN DEFAULT 0;")
        print("Added 'completed' column to item table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Column 'completed' already exists")
        else:
            print(f"Error adding 'completed' column: {e}")

    try:
        # Add priority column (default 'medium')
        cursor.execute("ALTER TABLE item ADD COLUMN priority TEXT DEFAULT 'medium';")
        print("Added 'priority' column to item table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Column 'priority' already exists")
        else:
            print(f"Error adding 'priority' column: {e}")

    try:
        # Add category column (default NULL)
        cursor.execute("ALTER TABLE item ADD COLUMN category TEXT;")
        print("Added 'category' column to item table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Column 'category' already exists")
        else:
            print(f"Error adding 'category' column: {e}")

    try:
        # Add due_date column (default NULL)
        cursor.execute("ALTER TABLE item ADD COLUMN due_date DATETIME;")
        print("Added 'due_date' column to item table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Column 'due_date' already exists")
        else:
            print(f"Error adding 'due_date' column: {e}")

    try:
        # Add recurring column (default NULL)
        cursor.execute("ALTER TABLE item ADD COLUMN recurring TEXT;")
        print("Added 'recurring' column to item table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Column 'recurring' already exists")
        else:
            print(f"Error adding 'recurring' column: {e}")

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database schema update completed!")

if __name__ == "__main__":
    update_database_schema()