import Tkinter as Tk
import functions
from random import shuffle
import sqlite3
import subprocess
import ConfigParser


# ROOT
root = Tk.Tk()
root.title("Best of Bronze")


# CONFIG
config = ConfigParser.ConfigParser()
config.read("cfg/config.cfg")

PATH = config.get("GAME_PATH", "path")


# VARIABLES
#cmddir = r"C:\Riot Games\League of Legends\RADS\solutions\lol_game_client_sln\releases\0.0.1.88\deploy"
cmdparts = ["League of Legends.exe", "8394", "LoLLauncher.exe", "", "spectator spectator.euw1.lol.riotgames.com:80"]
command = ""

border_width = int(config.get("BORDERWIDTH", "width"))
API_KEY = config.get("API_KEY", "key")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()	 #screen data

midframe_height = screen_height - screen_height/10 - screen_height/5 	#compute midframe height
midframe_canvas_height = (midframe_height/5)-2*border_width-2 	#compute midframe canvas height

root.state("zoomed") 	#window starts 'maximized'

ingame_time = Tk.StringVar()
ingame_time.set("Game Length")	#ingame time str variable 

game_type = Tk.StringVar()
game_type.set("")	#gametype str variable

playerlist = [] 
iteration = -1 
canvas_text = []

for i in range(0,10):
	canvas_text.append(Tk.StringVar())		#fil canvas_text with str variables
for i in range(0,10):
	canvas_text[i].set("Player " + str(i+1))


# READ IN PLAYERS
sqlConnection = sqlite3.connect("bronzeplayers.sql")	#build sql connection
sqlCursor = sqlConnection.cursor()
sqlCursor.execute("select name from players")
playerlist = sqlCursor.fetchall()

shuffle(playerlist)	#shuffle playerlist for enhanced experience




# FUNCTIONS
	#search
def search():
	game_type.set("")
	root.update()

	global iteration
	global canvas_text
	game_switch = 1
	
	
	content = None
	while content is None:
		iteration += 1
		if iteration >= len(playerlist):
			game_type.set("KEINE SPIELER GEFUNDEN")
			GameTypeLabel.update_idletasks()
			
		if game_switch:
			game_switch = 0
			game_type.set("SEARCHING...")
			GameTypeLabel.update_idletasks()
			GameTypeLabel.update_idletasks()
			GameTypeLabel.update_idletasks()
		else:
			game_switch = 1
			game_type.set("SEARCHING..")
			GameTypeLabel.update_idletasks()
			GameTypeLabel.update_idletasks()
			GameTypeLabel.update_idletasks()
			
		if functions.fetchcontent(playerlist[iteration][0].encode('utf-8')):
			break;
	player_name = playerlist[iteration][0].encode('utf-8')
	[gamedata, ranklist, champIdList] = functions.findSpecDataById(functions.findIdByName(player_name))
	
	# DEBUG
	print champIdList
	
	# UPDATE SPEC URL
	cmdparts.extend(gamedata)
	cmdparts.append("EUW1")

	# UPDATE LABELS
	for i in range(0,10):
		canvas_text[i].set(ranklist[i])
	# UPDATE GAMETIME
	game_time_short = gamedata[2]
	if game_time_short <= 60:
		ingame_time.set("not yet started")
	else:
		ingame_time.set(str(game_time_short/60)+ " Minuten")
	# UPDATE GAMEMODE
	game_type.set("Ranked Game by " + player_name)
	return 0




#watch
def watch():
	global iteration
	if iteration is 0:
		return 0
	
	lastpart = "\"" + str(cmdparts[4]) + " " + str(cmdparts[6]) + " " + str(cmdparts[5]) + " " + str(cmdparts[8]) + "\""
	command = "cmd /C start \"LoL\" " + "\"" + str(cmdparts[0]) + "\"" + " " + "\"" + str(cmdparts[1]) + "\"" + " " + "\"" + str(cmdparts[2]) + "\"" + " " + "\"" + str(cmdparts[3]) + "\"" + " " + str(lastpart)
	
	subprocess.Popen(command, shell=False, cwd=PATH)
	
	return 0



# FRAMES
TopFrame = Tk.Frame(width = screen_width, height = screen_height/10, bg = "white", bd = border_width, relief="ridge")
MidFrameLeft = Tk.Frame(width = screen_width/2-8, height = midframe_height, bg = "white", bd = 2, relief="ridge")
MidFrameRight = Tk.Frame(width = screen_width/2-8, height = midframe_height, bg = "white", bd = 2, relief="ridge")
SearchFrame = Tk.Frame(width = screen_width/3, height = screen_height/5, bg = "black", bd = border_width, relief="ridge")
WatchFrame = Tk.Frame(width = screen_width/3, height = screen_height/5, bg = "black", bd = border_width, relief="ridge")
ExitFrame = Tk.Frame(width = screen_width/3, height = screen_height/5, bg = "black", bd = border_width, relief="ridge")



# BUTTONS
# graphics
SearchButtonGraphic = Tk.PhotoImage(file="img/SearchGameGraphic.gif")
WatchButtonGraphic = Tk.PhotoImage(file="img/WatchGameGraphic.gif")
ExitButtonGraphic = Tk.PhotoImage(file="img/ExitGameGraphic.gif")



# instances
SearchButton = Tk.Button(SearchFrame, image = SearchButtonGraphic, command=search, width = 196, height = 91, bd = 0)
WatchButton = Tk.Button(WatchFrame, image = WatchButtonGraphic, command=watch, width = 196, height = 91, bd = 0)
ExitButton = Tk.Button(ExitFrame, image = ExitButtonGraphic, command=quit, width = 196, height = 91, bd = 0)



# CANVAS
MidFrameCanvas0 = Tk.Canvas(MidFrameLeft, width = screen_width/2, height = midframe_canvas_height, bg = "white", bd = 2, relief="ridge")
MidFrameCanvas1 = Tk.Canvas(MidFrameLeft, width = screen_width/2, height = midframe_canvas_height, bg = "white", bd = 2, relief="ridge")
MidFrameCanvas2 = Tk.Canvas(MidFrameLeft, width = screen_width/2, height = midframe_canvas_height, bg = "white", bd = 2, relief="ridge")
MidFrameCanvas3 = Tk.Canvas(MidFrameLeft, width = screen_width/2, height = midframe_canvas_height, bg = "white", bd = 2, relief="ridge")
MidFrameCanvas4 = Tk.Canvas(MidFrameLeft, width = screen_width/2, height = midframe_canvas_height, bg = "white", bd = 2, relief="ridge")
MidFrameCanvas5 = Tk.Canvas(MidFrameRight, width = screen_width/2, height = midframe_canvas_height, bg = "white", bd = 2, relief="ridge")
MidFrameCanvas6 = Tk.Canvas(MidFrameRight, width = screen_width/2, height = midframe_canvas_height, bg = "white", bd = 2, relief="ridge")
MidFrameCanvas7 = Tk.Canvas(MidFrameRight, width = screen_width/2, height = midframe_canvas_height, bg = "white", bd = 2, relief="ridge")
MidFrameCanvas8 = Tk.Canvas(MidFrameRight, width = screen_width/2, height = midframe_canvas_height, bg = "white", bd = 2, relief="ridge")
MidFrameCanvas9 = Tk.Canvas(MidFrameRight, width = screen_width/2, height = midframe_canvas_height, bg = "white", bd = 2, relief="ridge")



# LABELS
IngameTimeLabel = Tk.Label(TopFrame, font="Times 16 bold", textvariable = ingame_time, bg = "white", fg = "black")
GameTypeLabel = Tk.Label(TopFrame, font="Times 24 bold", textvariable = game_type, bg = "white", fg = "black")



# TEXT IN CANVAS
MidFrameCanvas0PlayerRank = Tk.Label(textvariable = canvas_text[0] , fg = "black", font = "times 24 italic", bg = "white")
MidFrameCanvas0.create_window(10,midframe_canvas_height/2, anchor = "w", window = MidFrameCanvas0PlayerRank)

MidFrameCanvas1PlayerRank = Tk.Label(textvariable = canvas_text[1] , fg = "black", font = "times 24 italic", bg = "white")
MidFrameCanvas1.create_window(10,midframe_canvas_height/2, anchor = "w", window = MidFrameCanvas1PlayerRank)

MidFrameCanvas2PlayerRank = Tk.Label(textvariable = canvas_text[2] , fg = "black", font = "times 24 italic", bg = "white")
MidFrameCanvas2.create_window(10,midframe_canvas_height/2, anchor = "w", window = MidFrameCanvas2PlayerRank)

MidFrameCanvas3PlayerRank = Tk.Label(textvariable = canvas_text[3] , fg = "black", font = "times 24 italic", bg = "white")
MidFrameCanvas3.create_window(10,midframe_canvas_height/2, anchor = "w", window = MidFrameCanvas3PlayerRank)

MidFrameCanvas4PlayerRank = Tk.Label(textvariable = canvas_text[4] , fg = "black", font = "times 24 italic", bg = "white")
MidFrameCanvas4.create_window(10,midframe_canvas_height/2, anchor = "w", window = MidFrameCanvas4PlayerRank)

MidFrameCanvas5PlayerRank = Tk.Label(textvariable = canvas_text[5] , fg = "black", font = "times 24 italic", bg = "white")
MidFrameCanvas5.create_window(10,midframe_canvas_height/2, anchor = "w", window = MidFrameCanvas5PlayerRank)

MidFrameCanvas6PlayerRank = Tk.Label(textvariable = canvas_text[6] , fg = "black", font = "times 24 italic", bg = "white")
MidFrameCanvas6.create_window(10,midframe_canvas_height/2, anchor = "w", window = MidFrameCanvas6PlayerRank)

MidFrameCanvas7PlayerRank = Tk.Label(textvariable = canvas_text[7] , fg = "black", font = "times 24 italic", bg = "white")
MidFrameCanvas7.create_window(10,midframe_canvas_height/2, anchor = "w", window = MidFrameCanvas7PlayerRank)

MidFrameCanvas8PlayerRank = Tk.Label(textvariable = canvas_text[8] , fg = "black", font = "times 24 italic", bg = "white")
MidFrameCanvas8.create_window(10,midframe_canvas_height/2, anchor = "w", window = MidFrameCanvas8PlayerRank)

MidFrameCanvas9PlayerRank = Tk.Label(textvariable = canvas_text[9] , fg = "black", font = "times 24 italic", bg = "white")
MidFrameCanvas9.create_window(10,midframe_canvas_height/2, anchor = "w", window = MidFrameCanvas9PlayerRank)



# GRIDDING
# frames
TopFrame.grid(row = 0, column = 0, columnspan = 6)
MidFrameLeft.grid(row = 1, column = 0, columnspan = 3)
MidFrameRight.grid(row = 1, column = 3, columnspan = 3)
SearchFrame.grid(row = 2, column = 0, columnspan = 2)
WatchFrame.grid(row = 2, column = 2, columnspan = 2)
ExitFrame.grid(row = 2, column = 4, columnspan = 2)



# TopFrame
GameTypeLabel.place(rely = 0.5, relx = 0.5, anchor = "center")
IngameTimeLabel.pack(side="right")



# MidFrameLeft
MidFrameCanvas0.grid()
MidFrameCanvas1.grid()
MidFrameCanvas2.grid()
MidFrameCanvas3.grid()
MidFrameCanvas4.grid()



# MidFrameRight
MidFrameCanvas5.grid()
MidFrameCanvas6.grid()
MidFrameCanvas7.grid()
MidFrameCanvas8.grid()
MidFrameCanvas9.grid()



# SearchFrame
SearchButton.place(relx=0.5, rely=0.375, anchor="center")

# WatchFrame
WatchButton.place(relx=0.5, rely=0.375, anchor="center")

# ExitFrame
ExitButton.place(relx=0.5, rely=0.375, anchor="center")



# options
TopFrame.grid_propagate(False)
TopFrame.pack_propagate(False)
TopFrame.rowconfigure(0, weight=1)
TopFrame.columnconfigure(0, weight = 1)
SearchFrame.pack_propagate(False)
MidFrameLeft.grid_propagate(False)
MidFrameLeft.columnconfigure(0, weight=1)


# DEBUG

# MAINLOOP
root.mainloop()