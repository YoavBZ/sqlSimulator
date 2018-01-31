import sqlite3


def main():
    # Initiating connection
    dbconn = sqlite3.connect('world.db')
    with dbconn:
        cursor = dbconn.cursor()
        cursor.execute(
            'SELECT id,task_name,worker_id,resource_name,resource_amount FROM tasks WHERE tasks.time_to_make>0')
        tasks = cursor.fetchall()
        working_map = {}
        while len(tasks) != 0:
            # Starting/continuing tasks
            for task in tasks:
                # Checking if time_to_make isn't 0 (in this iteration)
                cursor.execute('SELECT time_to_make FROM tasks WHERE tasks.id=?', [task[0], ])
                time_to_make = cursor.fetchone()[0]
                if time_to_make > 0:
                    cursor.execute('SELECT id,name,status FROM workers WHERE id=?', [task[2], ])
                    worker = cursor.fetchone()
                    if worker[2] == 'idle':
                        print(worker[1], 'says: work work')
                        working_map[worker[0]] = task[0]
                        # cursor.execute('SELECT amount FROM resources WHERE name=?', [task[3]])
                        # amount=cursor.fetchone();
                        cursor.execute('UPDATE resources SET amount=(amount-?) WHERE name=(?)', [task[4], task[3], ])
                        cursor.execute('UPDATE workers SET status=? WHERE id=?', ['busy', worker[0], ])
                    elif working_map[worker[0]] == task[0]:
                        print(worker[1], 'is busy', task[1], '...')
                        cursor.execute('UPDATE tasks SET time_to_make=(time_to_make-1) WHERE id=(?)', [task[0], ])
                dbconn.commit()

            # Finishing tasks
            for task in tasks:
                cursor.execute('SELECT name FROM workers WHERE workers.id=?', [task[2], ])
                worker_name = cursor.fetchone()[0]
                cursor.execute('SELECT time_to_make FROM tasks WHERE tasks.id=?', [task[0], ])
                time_to_make = cursor.fetchone()[0]
                if time_to_make == 0:
                    if working_map[task[2]] == task[0]:
                        print(worker_name, 'says: All Done!')
                        cursor.execute('UPDATE workers SET status=? WHERE id=?', ['idle', task[2], ])
                        del working_map[task[2]]
                dbconn.commit()
            cursor.execute(
                'SELECT id,task_name,worker_id,resource_name,resource_amount FROM tasks WHERE tasks.time_to_make>0')
            tasks = cursor.fetchall()


if __name__ == '__main__':
    main()
