import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import random
import logging

bot = telegram.Bot(token = '672161416:AAF1Ln4gg_J4QH2nS9pDpLT-H6x_gsrYJW8')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

##global_update = None
last = ''
score = 0
count = 0

def ask(update, context):
    global last
    chat_id = update.message.chat_id
    variants = ['Beyond the boundary', 'Charlotte', 'Your name', 'Plastic memories']
    rnd = random.randint(0, 3)
##    bot.send_photo(chat_id=chat_id, photo=open('/home/tukan-king/Pictures/{}.jpg'.format(variants[rnd]), 'rb'))
    last = variants[rnd]
    keyboard = [
        [InlineKeyboardButton('Beyond the boundary', callback_data = 'Beyond the boundary'), InlineKeyboardButton('Charlotte', callback_data = 'Charlotte')],
        [InlineKeyboardButton('Your name', callback_data = 'Your name'), InlineKeyboardButton('Plastic memories', callback_data = 'Plastic memories')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def start(update, context):
##    global_update = update
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome to Anime Quiz. Let's start :)")
    ask(update, context)
##    variants = ['Beyond the boundary', 'Charlotte', 'Your name', 'Plastic memories']
##    rnd = random.randint(0, 3)
##    bot.send_photo(chat_id=chat_id, photo=open('/home/tukan-king/Pictures/{}.jpg'.format(variants[rnd]), 'rb'))
##    keyboard = [
##        [InlineKeyboardButton('Beyond the boundary', callback_data = 'Beyond the boundary'), InlineKeyboardButton('Charlotte', callback_data = 'Charlotte')],
##        [InlineKeyboardButton('Your name', callback_data = 'Your name'), InlineKeyboardButton('Plastic memories', callback_data = 'Plastic memories')]
##    ]
##    reply_markup = InlineKeyboardMarkup(keyboard)
##    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def user_result(update, context):
    global score
    global count
    query = update.callback_query
    count += 1
    if(last == query.data):
        score += 1
    query.edit_message_text(text="You chose: {} \nThe answer is: {} \nThe score is {}/{} \nDo you want to /continue ? \nOr /clear ?".format(query.data, last, score, count))

##    global_update.message.reply_text('Do you want to /continue ?')

def clear(update, context):
    global count
    global score
    count = 0
    score = 0
    update.message.reply_text(text="The score is {}/{} \nDo you want to /continue ? \nOr /clear ?".format(score, count))
    
def main():
    updater = Updater(token="672161416:AAF1Ln4gg_J4QH2nS9pDpLT-H6x_gsrYJW8", use_context=True)
    dispatcher = updater.dispatcher
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('continue', ask))
    updater.dispatcher.add_handler(CommandHandler('clear', clear))
    updater.dispatcher.add_handler(CallbackQueryHandler(user_result))
    updater.start_polling()
    ##updates = bot.get_updates()
main()
