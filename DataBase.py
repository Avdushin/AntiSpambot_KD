import psycopg2
from config import user, password, host, port, database

def base_connect():
    try:
        connection = psycopg2.connect(
                user=user, 
                password=password,
                host=host, 
                port=port,
                database=database
            )

        connection.autocommit = True
        return connection
    except:
        print("[info data base] Error conect")

def start(connection = base_connect()) -> None:
    with connection.cursor() as cursor:
        cursor.execute("""CREATE TABLE IF NOT EXISTS client(id_user varchar(40), chat_id varchar(20), payment TEXT, bot_num varchar(20))""")
        print("[info data base] The table has been created")
        

def insert_data(connection = base_connect(), data = [None, None, None]) -> None:
    with connection.cursor() as cursor:
        print(data)
        cursor.execute(f"""SELECT COUNT(*) FROM client WHERE id_user = '{data[0]}';""")
        num = cursor.fetchall()
        cursor.execute(f"""INSERT INTO client(id_user, chat_id, payment, bot_num) VALUES ({data[0]}, {data[1]},'{data[2]}', '{int(num[0][0])+ 1}')""")
        
def insert_update(connection = base_connect(), data = [None, None, None, None]) -> None:
    with connection.cursor() as cursor:
        cursor.execute(f"""UPDATE client SET payment = '{data[2]}' WHERE id_user = '{data[0]}' AND chat_id = '{data[1]}' AND bot_num = '{data[3]}';""")

def update_all(connection = base_connect(), data = [None, None]) -> None:
    with connection.cursor() as cursor:
        cursor.execute(f"""UPDATE client SET payment = '{data[1]}' WHERE id_user = '{data[0]}';""")


def get_data(connection = base_connect(), id= None) -> None:
    result = None
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM client WHERE id_user = '{id}'""")
        result = cursor.fetchall()
    return result


def pass_men(connection = base_connect(), chat_id=None):
    result = None
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT payment FROM client WHERE chat_id = '{chat_id}' LIMIT 1;  """)
        result = cursor.fetchall()
    if len(result) > 0:
        return result[0][0]
    else:
        return "1000-1-1"