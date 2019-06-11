import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import random
import logging
import pandas as pd

MAX_TITLES_COUNT = 415

bot = telegram.Bot(token = 'TOKEN')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# global_update = None
db = pd.read_csv('anime_greater_8.csv')
last = {}
score = {}
count = {}

def get_title_from_db(index):
    return db['title_english'][index]

def get_image_from_db(index):
    return db['image_url'][index]

def ask(update, context):
    global last
    chat_id = update.message.from_user['id']
    random_indexes = [0 for i in range(4)]
    title_variants = ['' for i in range(4)]
    image_variants = ['' for i in range(4)]
    log_variants = ''
    for i in range(4):
        random_indexes[i] = random.randint(0, MAX_TITLES_COUNT)
        title_variants[i] = get_title_from_db(random_indexes[i])
        title_variants[i] = title_variants[i]
        if len(title_variants[i]) > 63:
            title_variants[i] = title_variants[i][:63]
        image_variants[i] = get_image_from_db(random_indexes[i])
        temp = image_variants[i]
        temp_arr = temp.split('/')
        temp = "https://cdn.myanimelist.net"
        for j in range(3, 7):
            temp += '/'
            temp += temp_arr[j]
        image_variants[i] = temp
        log_variants += ', '
        log_variants += title_variants[i]
    print('{} variants are {}'.format(chat_id, log_variants))
    print('')
    correct_answer = random.randint(0, 3)
    bot.send_photo(chat_id = chat_id, photo = image_variants[correct_answer])
    last[chat_id] = title_variants[correct_answer]
    keyboard = [

        [InlineKeyboardButton(title_variants[0], callback_data = title_variants[0]), InlineKeyboardButton(title_variants[1], callback_data = title_variants[1])],
        [InlineKeyboardButton(title_variants[2], callback_data = title_variants[2]), InlineKeyboardButton(title_variants[3], callback_data = title_variants[3])]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def start(update, context):
    chat_id = update.message.from_user['id']
    print('start with chat_id {}'.format(chat_id))
    print('')
    count[chat_id] = 0
    score[chat_id] = 0
    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome to Anime Quiz. Let's start :)")
    ask(update, context)

def user_result(update, context):
    global score
    global count
    query = update.callback_query
    chat_id = update.callback_query.from_user['id']
    if chat_id not in last.keys():
        last[chat_id] = 'Sorry, the answer for this question was dropped by the system (as like as your score)'
    if chat_id not in score.keys():
        score[chat_id] = 0
    if chat_id not in count.keys():
        count[chat_id] = 0
    #print(update.callback_query.from_user)
    print('{} chose {}, correct is {}'.format(chat_id, query.data, last[chat_id]))
    print('')
    if chat_id not in count.keys():
        count[chat_id] = 0
    count[chat_id] += 1
    if last[chat_id] == query.data:
        score[chat_id] += 1
    query.edit_message_text(text="You chose: {} \nThe answer is: {} \nThe score is {}/{} \nDo you want to /continue ? \nOr /clear ?".format(query.data, last[chat_id], score[chat_id], count[chat_id]))

def clear(update, context):
    global count
    global score
    chat_id = update.message.from_user['id']
    count[chat_id] = 0
    score[chat_id] = 0
    update.message.reply_text(text="The score is {}/{} \nDo you want to /continue ? \nOr /clear ?".format(score[chat_id], count[chat_id]))
    
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
