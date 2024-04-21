import os
import sys
import asyncio 
from database import db, mongodb_version
from config import Config, temp
from platform import python_version
from translation import Translation
from pyrogram import Client, filters, enums, __version__ as pyrogram_version
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument
import traceback
from pyrogram.errors import FloodWait

main_buttons = [[
        InlineKeyboardButton('Ꮻ ᴜᴘᴅᴀᴛᴇs Ꮻ', url='https://example.com'),
        InlineKeyboardButton('Ꮻ sᴜᴘᴘᴏʀᴛ Ꮻ', url='https://t.me/example.com')
        ],[
        InlineKeyboardButton('Ꮻ ʜᴇʟᴘ Ꮻ', callback_data='help'),
        InlineKeyboardButton('Ꮻ ᴀʙᴏᴜᴛ Ꮻ', callback_data='about')
        ],[
        InlineKeyboardButton('🧑‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ 🧑‍💻', user_id='25773993')
        ]]
#===================Start Function===================#

def checkIfChannel(id):
    try:
        if len(id) == 14 and (id).startswith('-'):
            channelId = int(id)
            return channelId
        else:
            return False
    except Exception as e:
        traceback.print_exc()
        
        
@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    user = message.from_user
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
    reply_markup = InlineKeyboardMarkup(main_buttons)
    jishubotz = await message.reply_sticker("CAACAgUAAxkBAAIBQGX_MIl7nlr-0GB3_X9U4HOzqz89AAKbAAPIlGQUmqlsx6XTYLceBA")
    await asyncio.sleep(2)
    await jishubotz.delete()
    text=Translation.START_TXT.format(user.mention)
    await message.reply_photo(
        photo=Config.START_PIC,
        caption=text,
        reply_markup=reply_markup,
        quote=True
    )
    
@Client.on_message(filters.private & filters.command(['delay']) & filters.user(Config.BOT_OWNER_ID))
async def delayFunc(client , message):
    try:
        delay = int(message.command[1])
        await db.setDelay(delay)
        await message.reply(f'success..')
    except Exception as e:
        print(f'Sry..I Got this err : {e}')
        await message.reply(f'Sry..I Got this err : {e}')
        
        
@Client.on_message(filters.private & filters.command(['aforward']) & filters.user(Config.BOT_OWNER_ID))
async def autoForwardCmd(bot , message):
    userId = message.from_user.id
    channelId = await bot.ask( userId, 'Send Me Your Source Channel Id..')
    channelId = checkIfChannel(channelId.text)
    if channelId:
        pass
    else:
        return await message.reply('Invalid Channel Id')
    addedIds = []
    notAddedIds = []
    await message.reply('okk')
    try:
            chnl = await bot.ask(userId , 'Send me your all channel ids in this formate :\n-100xxxxxxxxxx -100xxxxxxxxxx -100xxxxxxxxxx')
            chnls = chnl.text
            if len(chnls) <= 14:
                intId = checkIfChannel(chnls)
                if intId and (intId != channelId):
                    addedIds.append(intId)
                else:
                    return await message.reply("At-least send me one valid id 🫠And it should not be same as source channel id..")
            else:
                ids = chnls.split(' ')
                for id in ids:
                    intId = checkIfChannel(id)
                    if intId and intId != channelId:
                        addedIds.append(intId)
                    else:
                        notAddedIds.append(intId)
            isadded = await db.addAutoForwardChnl(channelId , addedIds)
            if not isadded:
                return await message.reply("Sry I failed to add channels in database..")
            if len(notAddedIds) == 0 and len(addedIds) != 0:
                await message.reply(f'All channels added succesfully...\nAdded Channels : {'\n'.join(map(str, addedIds))}')
            else :
                await message.reply(f'Ignored channels : {'\n'.join(map(str, notAddedIds))} \n\n Added Channels : {'\n'.join(map(str, addedIds))}')
    except Exception as e:
        print('err is : ' , e)
        
@Client.on_message(filters.private & filters.command(['delchannel']) & filters.user(Config.BOT_OWNER_ID))
async def deletAutoForwardCmd(bot , message):
    userId = message.from_user.id
    channelId = await bot.ask(userId , 'Send Me the Source Channel id To delete !')
    intId = checkIfChannel(channelId.text)
    if intId:
        isRemoved = await db.delAutoForwardChnl(intId)
        if isRemoved:
            return await message.reply(f'Channel ID {intId} removed successfully.')
        else:
            return await message.reply('Channel has not been added yet.')
    else:
        await message.reply("Send a valid  cahnnel id") 
#==================Restart Function==================#

@Client.on_message(filters.private & filters.command(['restart', "r"]) & filters.user(Config.BOT_OWNER_ID))
async def restart(client, message):
    msg = await message.reply_text(
        text="<i>Trying To Restarting.....</i>",
        quote=True
    )
    await asyncio.sleep(5)
    await msg.edit("<i>Server Restarted Successfully ✅</i>")
    os.execl(sys.executable, sys.executable, *sys.argv)
    
#==================Callback Functions==================#

@Client.on_callback_query(filters.regex(r'^help'))
async def helpcb(bot, query):
    await query.message.edit_text(
        text=Translation.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(
            [[
            InlineKeyboardButton('🛠️ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ 🛠️', callback_data='how_to_use')
            ],[
            InlineKeyboardButton('⚙️ sᴇᴛᴛɪɴɢs ⚙️', callback_data='settings#main'),
            InlineKeyboardButton('📊 sᴛᴀᴛs 📊', callback_data='status')
            ],[
            InlineKeyboardButton('🔙 ʙᴀᴄᴋ', callback_data='back')
            ]]
        ))

@Client.on_callback_query(filters.regex(r'^how_to_use'))
async def how_to_use(bot, query):
    await query.message.edit_text(
        text=Translation.HOW_USE_TXT,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 Back', callback_data='help')]]),
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex(r'^back'))
async def back(bot, query):
    reply_markup = InlineKeyboardMarkup(main_buttons)
    await query.message.edit_text(
       reply_markup=reply_markup,
       text=Translation.START_TXT.format(
                query.from_user.first_name))

@Client.on_callback_query(filters.regex(r'^about'))
async def about(bot, query):
    await query.message.edit_text(
        text=Translation.ABOUT_TXT.format(bot.me.mention),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 Back', callback_data='back')]]),
        disable_web_page_preview=True,
        parse_mode=enums.ParseMode.HTML,
    )

@Client.on_callback_query(filters.regex(r'^status'))
async def status(bot, query):
    users_count, bots_count = await db.total_users_bots_count()
    total_channels = await db.total_channels()
    await query.message.edit_text(
        text=Translation.STATUS_TXT.format(users_count, bots_count, temp.forwardings, total_channels, temp.BANNED_USERS ),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙 Back', callback_data='help')]]),
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )


@Client.on_message(filters.channel & filters.incoming)
async def channelAutoForward(client , message):
    try: 
        channelId = message.chat.id
        targets = await db.getChnlLists(channelId)
        if targets:
            for target in targets:
                try:
                    await message.copy(target)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception as e: 
                    print('Got this err while forwarding : ',e)
    except Exception as e:
        print(e)
        traceback.print_exc()  
