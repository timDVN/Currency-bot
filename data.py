import log
import sqlite3


def init_db():
    log.logger.debug("Function: init_db. (data.py)")
    with sqlite3.connect('Data.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS currency(
                reduction VARCHAR({len('BYN')}),
                rate VARCHAR(255)
        )''')
        cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS mailing(
                        id VARCHAR(255),
                        reduction VARCHAR({len('BYN')})
                )''')
        conn.commit()


def clear_currency_table():
    log.logger.debug("Function: clear_currency_table. (data.py)")
    with sqlite3.connect('Data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS currency')
        cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS currency(
                        reduction VARCHAR({len('BYN')}),
                        rate VARCHAR(255)
                )''')
        conn.commit()


def add_currency(redact: str, rate_new: str):  # add rate and currency to "currency" table
    log.logger.debug(f"Function: add_currency,  reduction = {redact}, rate = {rate_new}. (data.py)")
    with sqlite3.connect('Data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO currency (reduction, rate) VALUES (?,?)', (redact, rate_new))
        conn.commit()


def add_recipient(chat_id: str, reduction: str):
    log.logger.debug(f"Function: add_recipient, chat_id = {chat_id}, reduction = {reduction}. (data.py)")
    with sqlite3.connect('Data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO mailing (id, reduction) VALUES (?,?)', (chat_id, reduction))
        conn.commit()


def remove_recipient(chat_id: str, reduction: str):
    log.logger.debug(f"Function: remove_recipient, chat_id = {chat_id}, reduction = {reduction}. (data.py)")
    with sqlite3.connect('Data.db') as conn:
        query = 'DELETE FROM mailing  WHERE id = ?  AND reduction = ?'
        cursor = conn.cursor()
        cursor.execute(query, (chat_id, reduction))
        conn.commit()


def list_of_recipients():
    log.logger.debug("Function: list_of_recipients. (data.py)")
    with sqlite3.connect('Data.db') as conn:
        query = 'SELECT id FROM mailing'
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def list_of_currencies(chat_id: str):
    log.logger.debug("Function: list_of_currencies. (data.py)")
    with sqlite3.connect('Data.db') as conn:
        query = f'SELECT reduction FROM mailing WHERE id = {chat_id} '
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def currencies_in_db():  # return list of currencies from "currency" table
    log.logger.debug("Function: currencies_in_db. (data.py)")
    with sqlite3.connect('Data.db') as conn:
        query = 'SELECT reduction[0] FROM currency'
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def compare(new_rate: str, redact: str):
    log.logger.debug(f"Function: compare, new_rate = {new_rate}, redact = {redact} (data.py)")
    with sqlite3.connect('Data.db') as conn:
        query = 'SELECT rate FROM currency WHERE reduction = ? '
        cursor = conn.cursor()
        cursor.execute(query, (redact,))
        old_rate = float(cursor.fetchone()[0])
        diff = float(new_rate) - old_rate
        if diff >= 0:  # if currency became more expensive
            res = f'(+{diff})'
        else:  # if currency became cheaper
            res = f'({diff})'
        return res
