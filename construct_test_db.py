import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()

c.execute( ''' CREATE TABLE Production( process VARCHAR(10),
    date VARCHAR(50), origin VARCHAR(10),
    operator VARCHAR(20), labor TINYINT(3),
    lbsIn SMALLINT(5), lbsOut SMALLINT(5), batch TINYINT(4) ); ''')
 
c.execute( ''' CREATE TABLE Employee(
    ID INTEGER PRIMARY KEY, name VARCHAR(20), active INTEGER ); ''' )

employeeinfo = [(2, 'Stanley', 1),
                (3, 'Kyle', 1),
                (4, 'Clark', 1),
                (5, 'Ray', 0),
                (6, 'Bion', 1),
                ]

c.executemany( ' INSERT INTO Employee VALUES (?, ?, ?) ', employeeinfo )

conn.commit()

conn.close()