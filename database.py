import sqlite3

def init_db():
    conn = sqlite3.connect("bus_management.db")
    cursor = conn.cursor()
    
    # Create Routes Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS routes (
            route_id TEXT PRIMARY KEY,
            route_name TEXT,
            bus_no TEXT,
            driver_name TEXT,
            capacity INTEGER
        )
    ''')
    
    # Create Students Registration Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT,
            department TEXT,
            route TEXT,
            stop TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")