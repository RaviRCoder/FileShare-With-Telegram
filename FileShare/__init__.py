from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import DB
import random
import string
import json
from config import file_share_bot_usrname, user_db, data_db, admin_channel_username


filedata = []
bot_username = file_share_bot_usrname


class FileShareBot:
    def __init__(self, BOT_TOKEN, API_ID, API_HASH):
        self.app = Client(name="FileShareBot", bot_token=BOT_TOKEN,
                          api_id=API_ID, api_hash=API_HASH)
        self.app.set_parse_mode(enums.ParseMode.MARKDOWN)

        @self.app.on_message(filters.command("start"))
        def start(client, message):

            chat_id = message.chat.id
            DB(f"{user_db}").createUser(chatid=chat_id, username=message.chat.username if message.chat.username else None,
                                        large_photo_id=message.chat.photo.big_file_id if message.chat.photo else None, small_photo_id=message.chat.photo.small_file_id if message.chat.photo else None)
            if "get_" in message.text:
                try:
                    # If chat_id is present in the list.
                    if self.CheckChatMembers(chat_id) == True:
                        dtext = message.text.replace(
                            '/start ', '').replace("get_", '').split("_")
                        data = json.loads(
                            DB(f'{data_db}/chatid_{dtext[0]}/{dtext[1]}').Read())
                        if "type" in data.keys():
                            self.upload_to_telegram(data, chat_id)
                        else:
                            for da in data:
                                self.upload_to_telegram(data[da], chat_id)

                    else:  # If chat_id isn't present in the list.
                        self.app.send_message(chat_id, text=f"👋 Hello there, {message.chat.first_name}!\n\n🚀 Ready to Joined Developer Channel.\n\n🔗 Simply tap the ✅ button to get started and continue the exciting journey.", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton("✅ Join", url="https://telegram.me/RaviRCoder"), InlineKeyboardButton(
                                    "Start", callback_data=f"JoinedCheckUser")],
                            ]
                        ))
                except:

                    message.reply_text(
                        "❌ This is Not a correct url!", quote=True)
            else:
                message.reply_text(
                    "👋 Greetings, I'm your friendly bot here to assist you!\n\n🌟 **/start** - Your gateway to an exciting journey with our friendly bot. Let's explore\n\n!📎 **/getlink** - Discover the magic of effortless file sharing. Get the file share bot link now and start sharing in style. 🪄📤")

        @self.app.on_message(filters.command("info"))
        def info(client, message):
            message.reply_text(
                f"Hey,{message.chat.first_name} \n\n This bot is made to share your files with telegram Unlimited Space using link.\n\n Developer : [RaviRCoder](https://telegram.me/RaviRCoder) \n Library : [Pyrogram](https://docs.pyrogram.org) \n GitHub : [Telegram Automation](https://github.com/RaviRCoder/AutoMate_Telegram)\nDon't Forget to give me star⭐⭐.", quote=True)

        @self.app.on_message()
        def mess(client, message):
            global filedata
            chatid = message.chat.id
            if message.document != None:
                fdata = {chatid: [{
                    "type": "document",
                    "fileid": message.document.file_id,
                    "fileName": message.document.file_name,
                    "fileSize": message.document.file_size,
                    "thumb": message.document.thumbs[0].file_id if message.document.thumbs else None
                }]}
                if len(filedata) == 0:
                    filedata.append(fdata)
                else:
                    for i in filedata:
                        if chatid not in i.keys():
                            filedata.append(fdata)
                        else:
                            i[chatid].append(fdata[chatid][0])

            elif message.video != None:
                fdata = {chatid: [{
                    "type": "video",
                    "fileid": message.video.file_id,
                    "fileName": message.video.file_name,
                    "fileSize": message.video.file_size,
                    "thumb": message.video.thumbs[0].file_id if message.video.thumbs else None
                }]}

                if len(filedata) == 0:
                    filedata.append(fdata)
                else:
                    for i in filedata:
                        if chatid not in i.keys():
                            filedata.append(fdata)
                        else:
                            i[chatid].append(fdata[chatid][0])

            elif message.text == "/getlink":

                dg = ''.join(random.choice(string.digits)
                             for _ in range(10))
                chatid = message.chat.id
                message_id = message.id
                filedat = [i if chatid in i.keys(
                ) else None for i in filedata]
                file_data = [item[chatid]
                             for item in filedat if item is not None][0]
                if len(file_data) == 1:
                    db = DB(f'{data_db}').defult_save(chatid, file_data[0])
                    filedata = []

                    # message.reply_text(
                    #     ,quote=True)
                    self.app.send_message(chatid, text="✅✅ **Your link is ready click on `share` button**", reply_to_message_id=message_id, reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("🔗 Share", url=f"https://telegram.me/share/url?url=http://telegram.me/{bot_username}?start=get_{chatid}_{db['name']}")]]))
                elif len(file_data) > 1:
                    for i in file_data:
                        db = DB(f'{data_db}').folder_save(chatid, i, dg)
                    self.app.send_message(chatid, text="✅✅ **Your link is ready click on `share` button**", reply_to_message_id=message_id, reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("🔗 Share", url=f"https://telegram.me/share/url?url=http://telegram.me/{bot_username}?start=get_{chatid}_{dg}")]]))
                    filedata = []

        @self.app.on_callback_query()
        def callback_handle(client, callback_query):
            data = callback_query.data

            if data == "JoinedCheckUser":
                chat_id = callback_query.from_user.id
                text = callback_query.message.reply_to_message.text
                message_id = callback_query.message.id
                try:
                    # If chat_id is present in the list.
                    if self.CheckChatMembers(chat_id=chat_id) == True:
                        self.app.delete_messages(
                            chat_id, message_ids=[message_id])
                        callback_query.answer(text="Checked! You have joined✅")
                        dtext = text.replace(
                            '/start ', '').replace("get_", '').split("_")
                        data = json.loads(
                            DB(f'{data_db}/chatid_{dtext[0]}/{dtext[1]}').Read())
                        if "type" in data.keys():
                            self.upload_to_telegram(data, chat_id)
                        else:
                            for da in data:
                                self.upload_to_telegram(data[da], chat_id)

                    else:  # If chat_id isn't present in the list.
                        callback_query.answer(
                            text="Checked! You haven't joined✅")

                except:
                    self.app.send_message(chat_id=chat_id, text="❌ This is Not a correct url!",
                                          reply_to_message_id=callback_query.message.reply_to_message_id)

    def start(self):
        self.app.run()

    # get channel members and stored their chat ids to a list
    def CheckChatMembers(self, chat_id):
        members_chat_ids = [
            member.user.id for member in self.app.get_chat_members(admin_channel_username)]
        if chat_id in members_chat_ids:
            return True
        else:
            return False

    # Send Files to Telegram using File_id
    def upload_to_telegram(self, data, chat_id):
        filename = data["fileName"]
        fileSize = data["fileSize"]
        fileId = data["fileid"]
        Selected_Type = data["type"]
        if Selected_Type == "document":
            self.app.send_document(
                chat_id, fileId, caption=f'📖 **Title:** "`{filename}`"\n\n📏 **Size:** `{self.bytes_to_readable(fileSize)}`')
        elif Selected_Type == "video":
            self.app.send_video(
                chat_id, fileId, caption=f'📖 **Title:** "`{filename}`"\n\n📏 **Size:** `{self.bytes_to_readable(fileSize)}`')
        elif Selected_Type == "photo":
            self.app.send_photo(
                chat_id, fileId, caption=f'📖 **Title:** "`{filename}`"\n\n📏 **Size:** `{self.bytes_to_readable(fileSize)}`')

    def bytes_to_readable(self, bytes, decimal_places=2):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                break
            bytes /= 1024.0
        return f"{bytes:.{decimal_places}f} {unit}"
