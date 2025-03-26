import sqlite3

def create_tables():
    """Creates the necessary database tables."""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    # Staging table (Cart/Temporary Storage)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS staging (
            stage_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            stock_code TEXT,
            description TEXT,
            quantity INTEGER,
            unit_price REAL,
            added_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            total_amount REAL,
            order_status TEXT DEFAULT 'pending'
        )
    ''')

    # Order items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            stock_code TEXT,
            description TEXT,
            quantity INTEGER,
            unit_price REAL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully.")