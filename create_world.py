import sqlite3
import sys
from os.path import isfile


def main():
    if isfile('world.db'):
        return

    # Initiating connection
    dbconn = sqlite3.connect('world.db')
    with dbconn:
        cursor = dbconn.cursor()
        # Initiating tables
        cursor.execute('CREATE TABLE workers(id INTEGER PRIMARY KEY, name TEXT NOT NULL, status TEXT NOT NULL)')
        cursor.execute('CREATE TABLE resources(name TEXT PRIMARY KEY, amount INTEGER NOT NULL)')
        cursor.execute('CREATE TABLE tasks(id INTEGER PRIMARY KEY, \
                        task_name TEXT NOT NULL, \
                        worker_id INTEGER REFERENCES workers(id), \
                        time_to_make INTEGER NOT NULL, \
                        resource_name TEXT NOT NULL, \
                        resource_amount INTEGER NOT NULL)')
        # Parsing the data
        config = sys.argv[1]
        with open(config) as f:
            for line in f:
                record = line.split(',')
                record[len(record) - 1] = record[len(record) - 1][:-1]
                if len(record) == 2:
                    # Insert into resources
                    cursor.execute('INSERT INTO resources (name, amount) VALUES(?,?)', (record[0], record[1]))
                elif len(record) == 3:
                    # Insert into workers
                    cursor.execute('INSERT INTO workers (id, name, status) VALUES(?,?,?)',
                                   (record[1], record[2], 'idle'))
                else:
                    # Insert into workers
                    cursor.execute(
                        'INSERT INTO tasks(task_name, worker_id, time_to_make, resource_name, resource_amount) VALUES(?,?,?,?,?)',
                        (record[0], record[1], record[4], record[2], record[3]))
            dbconn.commit()


if __name__ == '__main__':
    main()
