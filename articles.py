from db import get_connection

def upsert_article(code, name, price):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """INSERT INTO articles (code_barre, nom, prix)
             VALUES (%s, %s, %s)
             ON DUPLICATE KEY UPDATE nom=%s, prix=%s"""

    cursor.execute(sql, (code, name, price, name, price))
    conn.commit()
    conn.close()


def delete_article(code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles WHERE code_barre = %s", (code,))
    conn.commit()
    conn.close()


def get_all_articles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT code_barre, nom, prix FROM articles")
    data = cursor.fetchall()
    conn.close()
    return data