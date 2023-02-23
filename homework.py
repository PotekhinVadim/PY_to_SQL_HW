import psycopg2
from settings import PASSWORD


def create_db(conn):
    conn.execute("""
        DROP TABLE IF EXISTS phonebook;
        DROP TABLE IF EXISTS clients;
        """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            client_id SERIAL PRIMARY KEY,
            name VARCHAR (40) NOT NULL,
            surname VARCHAR(40) NOT NULL,
            email VARCHAR(40) UNIQUE NOT NULL
            );
        """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS phonebook(
            client_id INTEGER REFERENCES clients(client_id),
            phone INTEGER UNIQUE CHECK(phone >= 0)
            );
        """)
    

def add_client(conn, name, surname, email):
    conn.execute("""
    INSERT INTO clients (name, surname, email) VALUES(%s, %s, %s);
    """, (name, surname, email))
  
def add_phone(conn, client_id, phone):
    conn.execute("""
    INSERT INTO phonebook (client_id, phone) VALUES(%s, %s);
    """, (client_id, phone))

def change_client(conn, client_id, name=None, surname=None, email=None, phone=None):
    if name != None:
        conn.execute("""
        UPDATE clients SET name=%s WHERE client_id=%s
        """, (name, client_id))
    if surname != None:    
        conn.execute("""
        UPDATE clients SET surname=%s WHERE client_id=%s
        """, (surname, client_id))
    if email != None:    
        conn.execute("""
        UPDATE clients SET email=%s WHERE client_id=%s
        """, (email, client_id))
    if phone != None:    
        conn.execute("""
        UPDATE phonebook SET phone=%s WHERE client_id=%s
        """, (client_id, phone))

 
def delete_phone(conn, phone):
    conn.execute("""
    DELETE FROM phonebook WHERE phone=%s;
    """, (phone,))

def delete_client(conn, client_id):
    conn.execute("""
    DELETE FROM phonebook WHERE client_id=%s;
    """, (client_id,))

    conn.execute("""
    DELETE FROM clients WHERE client_id=%s;
    """, (client_id,))


def find_client(conn, name=None, surname=None, email=None, phone=None):
    if name != None:
        conn.execute("""
        SELECT cl.name, cl.surname, cl.email, ph.phone FROM clients AS cl
        LEFT JOIN phonebook AS ph ON cl.client_id = ph.client_id
        WHERE name=%s;
        """, (name,))
    if surname != None:
        conn.execute("""
        SELECT cl.name, cl.surname, cl.email, ph.phone FROM clients AS cl
        LEFT JOIN phonebook AS ph ON cl.client_id = ph.client_id
        WHERE surname=%s;
        """, (surname,))
    if email != None:
        conn.execute("""
        SELECT cl.name, cl.surname, cl.email, ph.phone FROM clients AS cl
        LEFT JOIN phonebook AS ph ON cl.client_id = ph.client_id
        WHERE email=%s;
        """, (email,))
    if phone != None:
        conn.execute("""
        SELECT cl.name, cl.surname, cl.email, ph.phone FROM clients AS cl
        LEFT JOIN phonebook AS ph ON cl.client_id = ph.client_id
        WHERE phone=%s;
        """, (phone,))


if __name__ == "__main__":
    with psycopg2.connect(database="hwdatabase", user="postgres", password=PASSWORD) as conn:
        with conn.cursor() as cur:
            create_db(cur)
            add_client(cur, 'Vadim', 'Potekhin', 'ara@ya.ru')
            add_client(cur, 'Natalia', 'Potekhina', 'vara@ya.ru')
            conn.commit()
            add_phone(cur, '1', '47865489')
            add_phone(cur, '1', '478634589')
            add_phone(cur, '2', '47867659')
            conn.commit()
            change_client(cur, '1', name='Badim', surname='Aqua')
            change_client(cur, '1', surname='Notekhin')
            conn.commit()
            find_client(cur, name='Badim')
            conn.commit()
            delete_phone(cur, '47865489')
            delete_client(cur, '2')
            conn.commit()
