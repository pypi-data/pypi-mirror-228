#---------- My Modeul----------#
import os,sys,time,random,base64,zlib,uuid,string,json,re,platfrom
try:
	import requests
except:
	os.system("pip install requests")
try:
	import bs4
except:
	os.system("pip install bs4")
#----------colour----------#
R = '\033[1;91m' #Rad
G = '\033[1;92m' #Green
Y = '\033[1;93m'  #Yellow
B = '\033[1;94m' #Blue
P = '\033[1;95m' #Pink
C = '\033[1;96m' #Cyan
W = '\033[1;97m' #White
BL = '\033[1;90m' #Black
#----------bg-color---------#
BG_R = '\033[1;41m' #Baground Rad
BG_G = '\033[1;42m' #Baground Green
BG_Y = '\033[1;43m'  #Baground Yellow
BG_B = '\033[1;44m' #Baground Blue
BG_P = '\033[1;45m' #Baground Pink
BG_C = '\033[1;46m' #Baground Cyan
BG_W = '\033[1;47m' #Baground White
#---------Reset-Color---------#
N = '\033[0m' #None Color
#----------mix-color----------#
mix_color = random.choice([R,G,Y,B,P,C,W])
#----------mix-my-module----------#
os = os.system
ts = time.sleep
rc = random.choice
rr = random.randint
op = open
pr = print
rqg = requests.get
rqp = requests.post
ses = requests.Session()
seg = ses.get
sep = ses.post
syw = sys.stdout.write
syf = sys.stdout.flush
#---------- My logo----------#
logo1 = ("""\033[38;5;46m
    ██   ██  █████  ███████  █████  ███    ██ 
    ██   ██ ██   ██ ██      ██   ██ ████   ██ 
    ███████ ███████ ███████ ███████ ██ ██  ██ 
    ██   ██ ██   ██      ██ ██   ██ ██  ██ ██ 
    ██   ██ ██   ██ ███████ ██   ██ ██   ████ \033[38;5;192m
""")
logo2 = ("""
 \033[38;5;141m╔════════════════════════════════════════════════╗
 \033[38;5;141m║     \033[38;5;192m[\033[38;5;45m✓\033[38;5;192m] \033[38;5;192mCREATED BY\033[38;5;196m   :  \033[38;5;192mASRAFUL ISLAM HASAN    \033[38;5;141m║
 \033[38;5;141m║     \033[38;5;192m[\033[38;5;45m✓\033[38;5;192m] \033[38;5;192mFACEBOK      \033[38;5;196m: \033[38;5;192m Hasa N                 \033[38;5;141m║
 \033[38;5;141m║     \033[38;5;192m[\033[38;5;45m✓\033[38;5;192m] \033[38;5;192mGITHUB       \033[38;5;196m:  \033[38;5;192mKgHasan                \033[38;5;141m║
 \033[38;5;141m║     \033[38;5;192m[\033[38;5;45m✓\033[38;5;192m] \033[38;5;192mTEAM         \033[38;5;196m:  \033[38;5;192mKST                    \033[38;5;141m║
 \033[38;5;141m╚════════════════════════════════════════════════╝
 \033[38;5;196m[\033[38;5;45m•\033[38;5;196m]\033[38;5;192m PLZ SAPPORT ME BRO....
 \033[38;5;196m[\033[38;5;45m•\033[38;5;196m]\033[38;5;192m HASAN TERMUX HELPING ZONE....
 \033[38;5;141m══════════════════════════════════════════════════""")
def linex1():
	print('\033[38;5;46m╔════════════════════════════════════════════════╗')
def linex2():
	print('\033[38;5;46m╚════════════════════════════════════════════════╝')
def linex3():
	print('\033[38;5;46m══════════════════════════════════════════════════')
	