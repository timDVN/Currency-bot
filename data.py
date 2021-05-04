import sqlite3


def init_db(force: bool = False):
    with sqlite3.connect('Data.db') as conn:
        c = conn.cursor()
        if force:
            c.execute('DROP TABLE IF EXISTS currency')

        c.execute('''
            CREATE TABLE IF NOT EXISTS currency(
                reduction VARCHAR(255),
                rate VARCHAR(255)
        )''')
        conn.commit()


def add_pole(redact: str, rate_new: float):
    with sqlite3.connect('Data.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO currency (reduction, rate) VALUES (?,?)', (redact, rate_new))
        conn.commit()


def compare(new_rate: str, redact: str):
    with sqlite3.connect('Data.db') as conn:
        query = ('SELECT rate FROM currency WHERE reduction = ') + "'" + redact + "'"
        c = conn.cursor()
        c.execute(query)
        old_rate = float(c.fetchone()[0])
        diff = float(new_rate) - old_rate
        if diff >= 0:
            res = '(+' + str(diff) + ')'
        else:
            res = '(' + str(diff) + ')'
        return res


if __name__ == '__main__':
    init_db()
