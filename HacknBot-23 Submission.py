import logging
import csv
from telegram import (
    KeyboardButton,
    KeyboardButtonPollType,
    Poll,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ForceReply
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PollAnswerHandler,
    PollHandler,
    filters,
    CallbackQueryHandler,
    ConversationHandler,
    ApplicationBuilder,
    
)




logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



class Player():
    def __init__(self, username):
        self.username = username
        self.angel = None
        self.mortal = None
        self.chat_id = None


## Copy the path of your cvs file here after downloading it
myfile = 'C:/Users/dotco/OneDrive/Documents/Python_projects/python-telegram-bot-master/am.csv'
EXPECT_BUTTON_CLICK = 0

players = {}


def loadPlayers(players):
    with open(myfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            else:
                playerName = row[0].strip()
                the_player = Player(playerName)
                angelName = row[2].strip()
                mortalName = row[1].strip()
                print(angelName)
                players[playerName] = the_player
                players[playerName].angel = angelName
                players[playerName].mortal = mortalName
                line_count += 1

loadPlayers(players)
print(players)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player_username = update.effective_chat.username
    player_id = update.effective_chat.id ## int form
    players[player_username].chat_id = player_id
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to STRIX's very ownnnnnnnn ANGEL & MORTAL bots" + " Your chat id is " + str(player_id) + " and your username is " + player_username)



async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message ='Andrew sent: ' + ' '.join(context.args)
    await context.bot.send_message(chat_id = 496326176, text=message)

async def sendMortal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('sendMortal function currently utilized!')
    name = update.message.text
    await update.message.reply_text(f'You have sent your mortal:' + name)
    message = 'Angel said: ' + name
    mortal_chat_id = players[players[update.effective_chat.username].mortal].chat_id
    await context.bot.send_message(chat_id = mortal_chat_id, text=message)

async def sendAngel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('sendAngel function currently utilized!')
    name = update.message.text
    await update.message.reply_text(f'You have sent your angel:' + name)
    message = 'Mortal said: ' + name
    mortal_chat_id = players[players[update.effective_chat.username].angel].chat_id
    await context.bot.send_message(chat_id = mortal_chat_id, text=message)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Name Conversation cancelled by user. Bye. Send /chat to start again')
    return ConversationHandler.END

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """To start the chats with mortal and angel"""
    options = []
    options.append(InlineKeyboardButton(text='Mortal', callback_data='1'))
    options.append(InlineKeyboardButton(text='Angel', callback_data='2'))
    reply_markup = InlineKeyboardMarkup([options])
    await context.bot.send_message(chat_id=get_chat_id(update, context), text='Who would you like to send to?', reply_markup=reply_markup)
    return EXPECT_BUTTON_CLICK

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    # query.data is 1 if mortal and 2 if angel
    print(query.data)
    if int(query.data) == 1:
        # it is mortal
        await update.callback_query.message.reply_text(text='Texting Mortal!')
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send your message', reply_markup=ForceReply())
        return int(query.data)

    elif int(query.data) == 2:
        # it is angel
        await update.callback_query.message.reply_text(text='Texting Angel!')
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send your message', reply_markup=ForceReply())
        return int(query.data)


    
    


def get_chat_id(update, context):
    chat_id = -1

    if update.message is not None:
        # text message
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        # callback message
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        # answer in Poll
        chat_id = context.bot_data[update.poll.id]

    return chat_id

  


if __name__ == "__main__":
    application = ApplicationBuilder().token('5970865865:AAGQcH5a6XuxnTBmW4FAuGqOn6i1s-SsYeE').build()
    ##handlers
    start_handler = CommandHandler('start', start)
    forward_handler = CommandHandler('forward', forward)
    sendMortal_handler = CommandHandler('sendMortal', sendMortal)
    sendAngel_handler = CommandHandler('sendAngel', sendAngel)
    chat_handler = CommandHandler('chat', chat)
    test_handler = CommandHandler('test', test)


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('chat', chat)],
        states={
            # 'Mortal': [MessageHandler(test)],
            0: [CallbackQueryHandler(test)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, sendMortal)],
            # 1: [CallbackQueryHandler(sendMortal)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, sendAngel)]
        }, 
        fallbacks=[CommandHandler('cancel', cancel)])


    ##add handlers
    application.add_handler(start_handler)
    application.add_handler(forward_handler)
    application.add_handler(sendMortal_handler)
    application.add_handler(sendAngel_handler)
    application.add_handler(conv_handler)
    application.add_handler(chat_handler)
    application.add_handler(test_handler)
    application.run_polling()


  
  

  

