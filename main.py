import shelve
import requests
import telegram.ext
from telegram import *
from threading import Timer
from time import sleep

api_key = '5055335035:AAG3s1i6tGyQhJyv0197Xl3j8CY9CAUzhDI'
api_key_dev = "2121277949:AAGnsnht0fJVh_zrsybJdpuc9TgJn6YOo5c"
pol_key = "SIZEEU48BVGR4U9UHWQ8S5DXT8N9IMMZ8V"
add = ["0x06761b0097c5f658bd368b453b330f7e26a5ea7e","0xc5becc7e77144670de0c52896e87bd041e93d93e","0x74d1297985f921f08775451769add005dff1c1d3","0xd8f4c502b80d084bd53a91800947c5c0483f640f","0x06fe965cf71a8c4d9c1fc5865e2a82fff5b87ad9","0x7f8cb1b15bd8b405c7a2bd631ed323da72409f04","0x3bf228ba3fcbcc1ee7f367bfd2b8ecadb98cd8b4"]
print("Bot running in tg")
ShelfFile = shelve.open('shelf')

for i in add:
    ShelfFile[i]=''

ShelfFile.close()
updater = telegram.ext.Updater(api_key)
disp = updater.dispatcher

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def outputMessage(data):
    return '''
    <b>{}</b>\nbought or minted this:\n\n<b>Contract address:</b> {}\n<b>NFT Name:</b> {}\n<b>URL:</b> {}\n 
    '''.format(data['from'],data['contractAddress'],data['tokenName'],'https://opensea.io/{}'.format(data['tokenName']))    

def printit (update,context):
    message = ""
    for i in add:
        print("running")
        ShelfFile = shelve.open('shelf')
        url = '''https://api.polygonscan.com/api?module=account&action=tokennfttx&address={}&startblock=0&endblock=99999999&page=1&sort=asc&apikey={}'''.format(i,pol_key)# print(url)
        page = requests.get(url)
        res = page.json()
        results = res['result']
        chosenData =results[len(results)-1]

        if(ShelfFile[i] != chosenData['tokenID']):
            ShelfFile[i]=chosenData['tokenID']
            ShelfFile.close()
            message += outputMessage(chosenData)
            message +="\n\n\n"
            # real_balance = str("{0:.2f}".format(float(res['result'])/math.pow(10,18)))+" Matic"
            # update.message.reply_text(real_balance)
    if(len(message)>0):
        update.message.reply_text(message,parse_mode=ParseMode.HTML)

def startList(update,context):
    update.message.reply_text("Fetching updates")
    rt = RepeatedTimer(60.0, printit, update,context) # it auto-starts, no need of rt.start()

disp.add_handler(telegram.ext.CommandHandler("start",startList))


updater.start_polling()
updater.idle()
