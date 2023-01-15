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
    TypeHandler
    
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

# obj = Player("Iannnnmn")
# objtwo = Player("ugchong")
# objthree = Player("andrew250402")

# obj.angel = objtwo
# obj.mortal = objthree

# objtwo.mortal = obj
# objtwo.angel = objthree

# objthree.mortal = objtwo
# objthree.angel = obj

##Copy the path of your csv file here
myfile = 'C:/Users/dotco/OneDrive/Documents/Python_projects/python-telegram-bot-master/am.csv'
#players = {'Iannnnmn': obj, "ugchong": objtwo, "andrew250402": objthree}
EXPECT_BUTTON_CLICK = 0

players = {}


def loadPlayers(players):
    """
    Load player data from CSV

    Parameters:
        players (collections.defaultdict): Dictionary with usernames as keys and Player objects as values
    """

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
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to STRIX 👼👦 bot, I am THE messenger for you angels and mortals 😊 "  + " key /Chat to start chatting away! 🤩 To stop your chat key /Cancel, remember you can't text both your mortal and angel concurrently, teehee have fun! ") 

# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

#async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    message ='Andrew sent: ' + ' '.join(context.args)
#4    await context.bot.send_message(chat_id = 496326176, text=message)

async def sendMortal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('sendMortal function currently utilized!')
    name = update.message.text
    sticker = update.message.sticker
    print(update.message.sticker)
    mortal_chat_id = players[players[update.effective_chat.username].mortal].chat_id
    if sticker is not None:
        await context.bot.send_sticker(chat_id = mortal_chat_id, sticker=sticker)
    else:
        await update.message.reply_text(f'You have sent your mortal: ' + name)
        # message = 'Angel said: ' + ' '.join(context.args)
        message = 'Angel said: ' + name
        await context.bot.send_message(chat_id = mortal_chat_id, text=message)
        # return ConversationHandler.END

async def sendAngel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('sendAngel function currently utilized!')
    name = update.message.text
    sticker = update.message.sticker
    mortal_chat_id = players[players[update.effective_chat.username].mortal].chat_id
    if sticker is not None:
        await context.bot.send_sticker(chat_id = mortal_chat_id, sticker=sticker)
    else:
        await update.message.reply_text(f'You have sent your angel: ' + name)
        # message = 'Mortal said: ' + ' '.join(context.args)
        message = 'Mortal said: ' + name
        await context.bot.send_message(chat_id = mortal_chat_id, text=message)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Ending converation ... Send /chat to start again')
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
        await update.callback_query.message.reply_text(text='Texting Mortal ... ')
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send your message', reply_markup=ForceReply())
        return int(query.data)

    elif int(query.data) == 2:
        # it is angel
        await update.callback_query.message.reply_text(text='Texting Angel ... ')
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

  
# # def main():
#     """Run bot."""
#     # Create the Application and pass it your bot's token.
#     application = Application.builder().token("5970865865:AAGQcH5a6XuxnTBmW4FAuGqOn6i1s-SsYeE").build()
#     application.add_handler(CommandHandler("start", start))
#     # application.add_handler(CommandHandler("poll", poll))
#     # application.add_handler(CommandHandler("quiz", quiz))
#     # application.add_handler(CommandHandler("preview", preview))
#     # application.add_handler(MessageHandler(filters.POLL, receive_poll))
#     # application.add_handler(PollAnswerHandler(receive_poll_answer))
#     # application.add_handler(PollHandler(receive_quiz_answer))


#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler('chat', chat)],
#         states={
#             'Mortal': [MessageHandler(filters.Text, sendMortal)],
#             'Angel': [MessageHandler(filters.Text, sendAngel)]
#         }, 
#         fallbacks=[CommandHandler('cancel', cancel)],

#     )
#     application.add_handler(CommandHandler("chat", conv_handler))


#     # Run the bot until the user presses Ctrl-C
#     application.run_polling()


if __name__ == "__main__":
    application = ApplicationBuilder().token('5970865865:AAGQcH5a6XuxnTBmW4FAuGqOn6i1s-SsYeE').build()
    ##handlers
    start_handler = CommandHandler('start', start)
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    # caps_handler = CommandHandler('caps', caps)
    # forward_handler = CommandHandler('forward', forward)
    sendMortal_handler = CommandHandler('sendMortal', sendMortal)
    sendAngel_handler = CommandHandler('sendAngel', sendAngel)
    chat_handler = CommandHandler('chat', chat)
    test_handler = CommandHandler('test', test)


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('chat', chat)],
        states={
            # 'Mortal': [MessageHandler(test)],
            0: [CallbackQueryHandler(test)],
            1: [MessageHandler(filters.ALL, sendMortal)],
            # 1: [CallbackQueryHandler(sendMortal)],
            2: [MessageHandler(filters.ALL, sendAngel)]
        }, 
        fallbacks=[CommandHandler('cancel', cancel)])


    ##add handlers
    application.add_handler(start_handler)
    # application.add_handler(echo_handler)
    # application.add_handler(caps_handler)
    # application.add_handler(forward_handler)
    application.add_handler(sendMortal_handler)
    application.add_handler(sendAngel_handler)
    application.add_handler(conv_handler)
    # application.add_handler(chat_handler)
    application.add_handler(test_handler)
    application.run_polling()


  
  

  

