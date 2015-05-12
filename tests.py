import sqlite3
import updateInfos
import urllib2
import json
import ConfigParser



conn = sqlite3.connect("bronzeplayers.sql")
c = conn.cursor()

c.execute("select * from players")

tmp = c.fetchall()

print len(tmp)