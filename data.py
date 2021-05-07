import sqlite3


def init_db(force: bool = False):
    with sqlite3.connect('Data.db') as conn:
        cursor = conn.cursor()
        if force:
            cursor.execute('DROP TABLE IF EXISTS currency')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS currency(
                reduction VARCHAR(255),
                rate VARCHAR(255)
        )''')
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS mailing(
                        id VARCHAR(255),
                        reduction VARCHAR(255)
                )''')
        conn.commit()


def add_pole(redact: str, rate_new: float):  # add rate and currency to "currency" table
    with sqlite3.connect('Data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO currency (reduction, rate) VALUES (?,?)', (redact, rate_new))
        conn.commit()


def add_recipient(chat_id: str, reduction: str):
    with sqlite3.connect('Data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO mailing (id, reduction) VALUES (?,?)', (chat_id, reduction))
        conn.commit()


def remove_recipient(chat_id: str, reduction: str):
    with sqlite3.connect('Data.db') as conn:
        query = 'DELETE FROM mailing  WHERE id = ?  AND reduction = ?'
        cursor = conn.cursor()
        cursor.execute(query, (chat_id, reduction))
        conn.commit()


def list_of_recipients():
    with sqlite3.connect('Data.db') as conn:
        query = 'SELECT id FROM mailing'
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def list_of_currencies(chat_id: str):
    with sqlite3.connect('Data.db') as conn:
        query = 'SELECT reduction FROM mailing WHERE id = ' + "'" + chat_id + "'"
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def compare(new_rate: str, redact: str):
    with sqlite3.connect('Data.db') as conn:
        query = 'SELECT rate FROM currency WHERE reduction =  ' + "'" + redact + "'"
        cursor = conn.cursor()
        cursor.execute(query)
        old_rate = float(cursor.fetchone()[0])
        diff = float(new_rate) - old_rate
        if diff >= 0:  # if currency became more expensive
            res = '(+' + str(diff) + ')'
        else:  # if currency became cheaper
            res = '(' + str(diff) + ')'
        return res


if __name__ == '__main__':
    init_db()
