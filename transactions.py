from db import get_connection

def save_transaction(total):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (total) VALUES (%s)", (total,))
    conn.commit()
    conn.close()