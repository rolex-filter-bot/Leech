#!/usr/bin/env python3
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.filters import command, regex

from bot import bot, LOGGER, OWNER_ID
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.button_build import ButtonMaker
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.ext_utils.bot_utils import sync_to_async, new_task


@new_task
async def driveclean(_, message):
    buttons = ButtonMaker()
    buttons.ibutton('Yes', 'gdclean clear')
    buttons.ibutton('No', 'gdclean stop')
    reply_message = await sendMessage(message, 'Do you want to Delete All your Files from GDRIVE_ID folder ?', buttons.build_menu(2))
    await auto_delete_message(message, reply_message)

@new_task
async def drivecleancb(_, query):
    message = query.message
    user_id = query.from_user.id
    data = query.data.split()
    if user_id != OWNER_ID:
        await query.answer(text="Not Owner!", show_alert=True)
        return
    if data[2] == "clean":
        await query.answer()
        drive = GoogleDriveHelper()
        msg = await sync_to_async(drive.driveclean)
        await editMessage(message, msg)
    elif data[1] == "stop":
        await query.answer()
        await editMessage(message, 'Driveclean Stopped!!')
        

bot.add_handler(MessageHandler(driveclean, filters=command('driveclean') & CustomFilters.owner))
bot.add_handler(CallbackQueryHandler(drivecleancb, filters=regex(r'^gdclean')))