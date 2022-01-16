import shelve
import requests
import telegram.ext
from telegram import *
from threading import Timer
from time import sleep

api_key = '5055335035:AAG3s1i6tGyQhJyv0197Xl3j8CY9CAUzhDI'
pol_key = "SIZEEU48BVGR4U9UHWQ8S5DXT8N9IMMZ8V"
add = "0x06761b0097c5f658bd368b453b330f7e26a5ea7e"
print("Bot running in tg")

updater = telegram.ext.Updater(api_key)
disp = updater.dispatcher

ShelfFile = shelve.open('shelf')
ShelfFile['merhi'] = ""

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
    <b>Sohyoune l zaber</b>\nbought or minted this:\n\n<b>Contract address:</b> {}\n<b>NFT Name:</b> {}\n<b>URL:</b> {}\n 
    '''.format(data['contractAddress'],data['tokenName'],'https://opensea.io/{}'.format(data['tokenName']))    

def printit (update,context):
    print("running")
    url = '''https://api.polygonscan.com/api?module=account&action=tokennfttx&address={}&startblock=0&endblock=99999999&page=1&sort=asc&apikey={}'''.format(add,pol_key)# print(url)
    page = requests.get(url)
    res = page.json()
    results = res['result']
    f = open('./write.txt','w')
    f.write(str(results[len(results)-15]))
    f.close()
    chosenData =results[len(results)-1]
    if(ShelfFile['merhi']!=chosenData['tokenID']):
        ShelfFile['merhi']=chosenData['tokenID']
        print(chosenData)
        message = outputMessage(chosenData)
        update.message.reply_text(message,parse_mode=ParseMode.HTML)
        # real_balance = str("{0:.2f}".format(float(res['result'])/math.pow(10,18)))+" Matic"
        # update.message.reply_text(real_balance)
        
def startList(update,context):
    update.message.reply_text("Fetching updates")
    rt = RepeatedTimer(180.0, printit, update,context) # it auto-starts, no need of rt.start()

disp.add_handler(telegram.ext.CommandHandler("start",startList))


updater.start_polling()
updater.idle()
