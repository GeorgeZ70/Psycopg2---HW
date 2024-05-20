import psycopg2    
def create_db(conn):    
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE clientsphone;
        """)
        cur.execute("""
        DROP TABLE client;
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) NOT NULL ,
            last_name VARCHAR(70) NOT NULL ,
            email VARCHAR(70) UNIQUE NOT NULL
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clientsphone(
            client_id INTEGER REFERENCES client(id) , phone VARCHAR(20) UNIQUE
            
        );   
        """)
        
        conn.commit()
        
        
with psycopg2.connect(database="clients", user="postgres", password = "postgres") as conn:  
    create_db(conn)  


def get_client_id(cursor,email: str) -> int:
    cursor.execute("""SELECT id from client WHERE email = %s;
                   """, (email,))
    return cursor.fetchone()[0]

                       
def add_client(conn, name: str, surname: str, mail: str, phones: list=None): 
    with conn.cursor() as cur:
        data = (name, surname, mail)
        cur.execute(""" INSERT INTO client(first_name, last_name, email) VALUES(%s, %s, %s) ;
                    """, data)
        
        conn.commit()
        for phone in phones:
            cur.execute(""" INSERT INTO clientsphone(client_id, phone) VALUES(%s, %s) ;
                  """, (get_client_id(cur, mail), phone))
    conn.commit()

        
def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute(""" INSERT INTO clientsphone(client_id, phone) VALUES(%s, %s) ;
                  """, (client_id, phone))
    conn.commit()
 
    
def change_client(conn, client_id, name=None, surname=None, mail=None, phones: list=None):
    with conn.cursor() as cur:
        if name != None:
            cur.execute(""" UPDATE client SET first_name=%s WHERE id = %s;
                    """, (name, client_id))
        if surname != None:
            cur.execute(""" UPDATE client SET last_name=%s WHERE id = %s;
                    """, (surname, client_id))  
        if mail != None:
            cur.execute(""" UPDATE client SET email=%s WHERE id = %s;
                    """, (mail, client_id))
        
        cur.execute(""" DELETE from clientsphone WHERE client_id = %s;
                    """, (client_id,))
        if phones != None:    
            for phone in phones:
                cur.execute(""" INSERT  INTO clientsphone(client_id, phone) VALUES(%s, %s) ;
                  """, (client_id, phone))
            
        conn.commit()
    
    
def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute(""" DELETE from clientsphone WHERE client_id = %s AND phone = %s;
                    """, (client_id,phone))    
        conn.commit()
        
        
def delete_client(conn, client_id):
    with conn.cursor() as cur:
           
        cur.execute(""" DELETE from clientsphone WHERE client_id = %s;
                    """, (client_id,))
        cur.execute(""" DELETE from client WHERE id = %s ;
                    """, (client_id,))
        conn.commit()
        
        
def find_client(conn, name=None, surname=None, mail=None, phone=None): 
    if name != None and surname != None:
        with conn.cursor() as cur:        
            cur.execute(""" SELECT * from client WHERE first_name = %s AND last_name = %s;
            """, (name, surname))
            if cur.fetchone() == None:
                print("Клиент не найден")
                return
            else:
                cur.execute(""" SELECT * from client WHERE first_name = %s AND last_name = %s;
            """, (name, surname))
                found_id = cur.fetchone()[0]
                cur.execute(""" SELECT * from client WHERE first_name = %s AND last_name = %s;
            """, (name, surname))
                print(cur.fetchone())
            cur.execute(""" SELECT * from client WHERE first_name = %s AND last_name = %s;
            """, (name, surname))    
            cur.execute(""" SELECT phone from clientsphone WHERE client_id = %s;
            """, (found_id,))
            print(cur.fetchall())            
    elif mail != None:
        with conn.cursor() as cur:
            cur.execute(""" SELECT * from client WHERE email = %s ;
                """, (mail,))
            if cur.fetchone() == None:
                print("Клиент не найден")
                return
            else:
                cur.execute(""" SELECT * from client WHERE email = %s ;
                """, (mail,))
                print(cur.fetchone())
                cur.execute(""" SELECT phone from clientsphone WHERE client_id = %s;
                """, (get_client_id(cur,mail),))
                print(cur.fetchall())
    elif phone != None:
        with conn.cursor() as cur:
            cur.execute(""" SELECT client_id from clientsphone WHERE phone = %s;
            """, (phone,))
            if cur.fetchone() == None:
                print("Клиент не найден")
                return
            else:
                cur.execute(""" SELECT client_id from clientsphone WHERE phone = %s;
                """, (phone,))
                found_id = cur.fetchone()[0]
                cur.execute(""" SELECT * from client WHERE id = %s ;
                """, (found_id,))
                print(cur.fetchone())
                cur.execute(""" SELECT phone from clientsphone WHERE client_id = %s;
                """, (found_id,))
                print(cur.fetchall())
    else :
        print ("Введите имя с фамилией или адрес электронной почты или номер телефона")
            
        
    
       
add_client(conn, 'John', 'Smith','johnsmith2002@gmail.com',['14672523438', '28574639841'])
add_client(conn, 'Mary', 'Butler','marybutler@yahoo.com', ['13584950982'] )
add_phone(conn, 2, '13760898678')
change_client(conn, 2, phones = ['18459783680', '16453907980'])
delete_phone(conn, 2, '16453907980')
delete_client(conn, 1)
find_client(conn, 'Mary', 'Butler')
find_client(conn, mail='marybutler@yahoo.com')
find_client(conn, phone='18459783680')
find_client(conn,'Mary')
find_client(conn, phone= '123456789')
