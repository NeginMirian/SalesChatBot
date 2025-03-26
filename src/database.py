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
def add_to_staging(session_id, stock_code, description, quantity, unit_price):
    """Adds an item to the staging table."""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO staging (session_id, stock_code, description, quantity, unit_price)
        VALUES (?, ?, ?, ?, ?)
    ''', (session_id, stock_code, description, quantity, unit_price))
    conn.commit()
    conn.close()

def get_staging_items(session_id):
    """Retrieves items from the staging table for a given session."""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT stock_code, description, quantity, unit_price
        FROM staging
        WHERE session_id = ?
    ''', (session_id,))
    items = cursor.fetchall()
    conn.close()
    return items

def create_order(session_id):
    """Creates an order from the staging table."""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    # Get items from staging
    items = get_staging_items(session_id)
    if not items:
        return None  # No items in staging

    # Calculate total amount
    total_amount = sum(item[2] * item[3] for item in items)

    # Create order
    cursor.execute('''
        INSERT INTO orders (session_id, total_amount)
        VALUES (?, ?)
    ''', (session_id, total_amount))
    order_id = cursor.lastrowid

    # Move items to order_items
    for item in items:
        cursor.execute('''
            INSERT INTO order_items (order_id, stock_code, description, quantity, unit_price)
            VALUES (?, ?, ?, ?, ?)
        ''', (order_id, item[0], item[1], item[2], item[3]))

    # Clear staging
    cursor.execute('''
        DELETE FROM staging WHERE session_id = ?
    ''', (session_id,))

    conn.commit()
    conn.close()
    return order_id

def get_order_history(session_id):
    """Retrieves order history for a given session."""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT order_id, order_date, total_amount, order_status
        FROM orders
        WHERE session_id = ?
    ''', (session_id,))
    orders = cursor.fetchall()
    conn.close()
    return orders

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully.")