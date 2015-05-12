import sqlite3



try:
    fobj = open("bronzeplayers.txt", "r")
    
except IOError:
    print "I/O error" 




conn = sqlite3.connect("bronzeplayers.sql")
c = conn.cursor()

sql_command = """
CREATE TABLE IF NOT EXISTS players (
id int UNIQUE,
name text UNIQUE,
rank text,
note text); """

c.execute(sql_command)


for line in fobj:
    name = line[:-1].rstrip()
    c.execute("INSERT OR IGNORE INTO players VALUES (NULL, :name, NULL, NULL)", {"name": unicode(name)})
    
conn.commit()


conn.close()
    