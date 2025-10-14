import mariadb 
import sys

db_config = {
    'user': 'root',
    'password': '25849',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'project'
}
def get_connection():
    conn = None
    try:
        conn = mariadb.connect(**db_config)
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
def execute_query(query, params=None):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params )
        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            return results
        else:
            conn.commit()
            return cursor.rowcount
    except mariadb.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
if __name__ == "__main__":
    pass    