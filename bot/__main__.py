import signal
import time

from telegram.ext import CommandHandler
from bot import dispatcher, updater, botStartTime
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from .helper.telegram_helper.filters import CustomFilters
from .modules import authorize, list
from telegram import InlineKeyboardMarkup
from bot.helper.telegram_helper.bot_utils import get_readable_time
from bot.helper.telegram_helper import button_builder

def start(update, context):
    buttons = button_builder.ButtonMaker()
    buttons.buildbutton("Join Our Channel", "https://t.me/MovieClubOfficiall")
    reply_markup = InlineKeyboardMarkup(buttons.build_menu(1))
    uptime = get_readable_time((time.time() - botStartTime))
    LOGGER.info('UID: {} - UN: {} - MSG: {}'.format(update.message.chat.id,update.message.chat.username,update.message.text))
    if CustomFilters.authorized_user(update) or CustomFilters.authorized_chat(update):
        if update.message.chat.type == "private":
            sendMessage(f"Hello 😎.\n\n<b>I Can Search For Files In Nick Mirror Database & Return A List Of Matching Files With Google Drive & Index Links.\n\n- Just Send Me The File Name.\n\nI Am Also Usable In Groups Just Add Me In Any Group & Send The Below Format 👇</b>\n\n/search <b>File Name..</b>", context.bot, update)
        else:
            start_string = '\x1f<b>Hello 😎.\n\nI Can Search For Files In Nick Mirror Database & Return A List Of Matching Files With Google Drive & Index Links.\n\n- Just Send Me The File Name.</b>\x1f'

            sendMessage(start_string, context.bot, update)
    else:
        sendMarkup(
            'Hello 😎.\n\n<b>I Can Search For Files In Nick Mirror Database & Return A List Of Matching Files With Google Drive & Index Links.\n\n- Just Send Me The File Name.\n\nI Am Also Usable In Groups Just Add Me In Any Group & Send The Below Format 👇</b>\n\n/search <b>File Name..</b>',
            context.bot,
            update,
            reply_markup,
        )

botcmds = [
        (f'{BotCommands.ListCommand}','Searches files in Drive'),
    ]

def log(update, context):
    sendLogFile(context.bot, update)

def main():
    bot.set_my_commands(botcmds)
    start_handler = CommandHandler(BotCommands.StartCommand, start, run_async=True)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter, run_async=True)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(log_handler)

    updater.start_polling(drop_pending_updates=True)
    LOGGER.info("Yeah boss I'm running fine!")
    signal.signal(signal.SIGINT, exit(1))
    updater.idle()

main()
