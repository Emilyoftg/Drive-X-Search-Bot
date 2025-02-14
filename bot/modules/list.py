from telegram.ext import CommandHandler
from bot.helper.drive_utils.gdriveTools import GoogleDriveHelper
from bot import LOGGER, dispatcher
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands

def list_drive(update,context):
    try:
        search = update.message.text.split(' ',maxsplit=1)[1]
        if "'"in search:
            search = search.replace("'", "\\'")
    except IndexError:
        sendMessage('<b>Follow These Steps 👇:\nSend A Keyword Along With Search Command.\nExample 👉:</b> <code>/search Uploads</code>', context.bot, update)
        return
        
    reply = sendMessage('Searching In Nick Mirror Database.....', context.bot, update)

    LOGGER.info(f"Searching: {search}")
        
    gdrive = GoogleDriveHelper(None)
    msg, button = gdrive.drive_list(search)

    editMessage(msg,reply,button)


list_handler = CommandHandler(BotCommands.ListCommand, list_drive,filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(list_handler)
