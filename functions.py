import urllib2
import re
import json
import sqlite3
import ConfigParser


# CONFIG
config = ConfigParser.ConfigParser()
config.read("cfg/config.cfg")
 
API_KEY = config.get("API_KEY", "key")



def fetchcontent(playername):
	name = playername.replace(" ","")    
	url = "http://www.lolskill.net/game/EUW/"+name
	
	try:
		content = urllib2.urlopen(url)
		content = content.read()
	except HTTPError as e:
		print "HTTP sagt nein"
	except URLError as e:
		print "URL sagt nein"
	
	
	if content.find("is not ingame") is -1 and content.find("Ranked Solo") != -1:
		return 1
		
	return None
       
       
 
 
               
# FIND ID BY NAME      
def findIdByName(name):
	conn = sqlite3.connect("bronzeplayers.sql")
	c = conn.cursor()
	
	c.execute("select id from players where name=:name", {"name": name})
	tmp = c.fetchall()
	
	if tmp[0][0] is not None:
	    return tmp[0][0]
	
	name = name.replace(" ","")
	url = "https://euw.api.pvp.net/api/lol/euw/v1.4/summoner/by-name/" + name + "?api_key=" + API_KEY
	
	try:
		content = urllib2.urlopen(url)
		content = content.read()	
		tmp = json.loads(content)
	except HTTPError as e:
		print "HTTP sagt nein"
	except URLError as e:
		print "URL sagt nein"
		

	c.execute("UPDATE players SET id=:id WHERE name=:name", {"id": str(tmp[name]['id']), "name": name})
	
	conn.commit()
	conn.close()
	
	return str(tmp[name]['id'])
    
    
    
 
def updatePlayerInfos(summonerId, name, rank):
    conn = sqlite3.connect("bronzeplayers.sql")
    c = conn.cursor()
   
    c.execute("insert or replace into players (id, name, rank) values (:id, :name, :rank)", {"id": summonerId, "name": unicode(name), "rank": unicode(rank)})
    
    conn.commit()
    conn.close()
	
	

	
	
def deleteHighElo(summonerId, name, rank):
	conn = sqlite3.connect("bronzeplayers.sql")
	c = conn.cursor()
	
	c.execute("delete from players where name=:name and (rank=:rank1 or rank=:rank2)", {"name": name, "rank1": unicode("BRONZE IV"), "rank2": unicode("BRONZE V")})

	conn.commit()
	conn.close()
 
 
 
 
 
   
def fetchRanksOfIngamePlayers(tmp):
	idListStr = ""
	idList = []
	
	for x in range(0,10):
		idList.append(tmp[unicode("participants")][x][unicode("summonerId")])
		idListStr += str(tmp[unicode("participants")][x][unicode("summonerId")])
		idListStr += ","
    	
    
	url = "https://euw.api.pvp.net/api/lol/euw/v2.5/league/by-summoner/"+ idListStr[:-1] + "?api_key=" + API_KEY
	
	try:
		content = urllib2.urlopen(url)
		content = content.read()	
		tmp = json.loads(content)
	except HTTPError as e:
		print "HTTP sagt nein"
	except URLError as e:
		print "URL sagt nein"
	

	rankList = []
    
	for y in range(0,10):
		for x in range(0,len(tmp[unicode(str(idList[y]))][0][unicode("entries")])):
			tier = tmp[unicode(str(idList[y]))][0][unicode("tier")]
			if tmp[unicode(str(idList[y]))][0][unicode("entries")][x][unicode("playerOrTeamId")] == unicode(str(idList[y])):
				division = ""
				division = tmp[unicode(str(idList[y]))][0][unicode("entries")][x][unicode("division")]
				name = tmp[unicode(str(idList[y]))][0][unicode("entries")][x][unicode("playerOrTeamName")]
				rank = tier + " " + division
	            
				rankList.append(rank)
	            
				if tier == "BRONZE" and (division == "IV" or division == "V"):
					updatePlayerInfos(idList[y], name, rank)
					
				else:
					deleteHighElo(idList[y], name, rank)
	            
	return rankList
    
    
    
       
def findSpecDataById(id):
	champIdList = []
	url = "https://euw.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/EUW1/"+str(id)+"?api_key=" + API_KEY
	
	try:
		content = urllib2.urlopen(url)
		content = content.read()		
		tmp = json.loads(content)
	except HTTPError as e:
		print "HTTP sagt nein"
	except URLError as e:
		print "URL sagt nein"
		
	
	gameId = tmp[unicode("gameId")]
	gameLength = tmp[unicode("gameLength")]
	encKey = tmp[unicode("observers")][unicode("encryptionKey")]
	
	for i in range(0,10):
		champIdList.append(tmp[unicode("participants")][i][unicode("championId")])
	
	rankList = fetchRanksOfIngamePlayers(tmp)
	
	value = []
	value.append(gameId)
	value.append(encKey)
	value.append(gameLength)
	return value, rankList, champIdList
