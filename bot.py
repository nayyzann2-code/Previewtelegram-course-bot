import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, BotCommand
from telegram.ext import ApplicationBuilder, ContextTypes, CallbackQueryHandler, MessageHandler, filters, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

MOVIES = {
    "1. The Flash (2014)": (
        "Season 1 to 9", 
        "AgACAgUAAxkBAAEguTZqYDpsIxym5LL1imj09cHLuhpPCQACoxJrG-62aFUXfew0CMQ-UQEAAwIAA3cAAz0E", 
        ("BAACAgUAAxkBAAEgubBqYFc8zCBAF0q4TGoZwX3xHLSX1AACJB4AAoXLgVRxAUNrR-eL_z0E", "BAACAgUAAxkBAAEgullqYGxRVOwVCisP1T14wkwpTeDrAwACJR4AAoXLgVSvbOSV-SlXHD0E", "BAACAgUAAxkBAAEguqtqYH1JKVaAc4r3m1D_TSEGpRLRrQACJh4AAoXLgVTZ9Tnit771Sz0E", "BAACAgUAAxkBAAEguqxqYH1JCxkERguduVwRuf7HDAb2-gACKx4AAoXLgVRTok4Dly278z0E", "BAACAgUAAxkBAAEguq1qYH1JMSEgt1ePqSHRuT58A0J94wAC1yMAAlnEeFT7fXUpjRcYMD0E", "")
    ),
    "2. Spider-Man": (
        "Season 1", 
        "https://i.imgur.com/YourPoster2.jpg", 
        ("EP1_FILE_ID", "EP2_FILE_ID", "EP3_FILE_ID", "EP4_FILE_ID", "EP5_FILE_ID", "EP6_FILE_ID")
    ),
    "3. Wednesday": (
        "Season 1", 
        "https://i.imgur.com/YourPoster3.jpg", 
        ("EP1_FILE_ID", "EP2_FILE_ID", "EP3_FILE_ID", "EP4_FILE_ID", "EP5_FILE_ID", "EP6_FILE_ID")
    ),
    "4. Stranger Things": (
        "Season 1 to 4", 
        "https://i.imgur.com/YourPoster4.jpg", 
        ("EP1_FILE_ID", "EP2_FILE_ID", "EP3_FILE_ID", "EP4_FILE_ID", "EP5_FILE_ID", "EP6_FILE_ID")
    ),
    "5. Money Heist": (
        "Season 1 to 5", 
        "https://i.imgur.com/YourPoster5.jpg", 
        ("EP1_FILE_ID", "EP2_FILE_ID", "EP3_FILE_ID", "EP4_FILE_ID", "EP5_FILE_ID", "EP6_FILE_ID")
    ),
    "6. Loki": (
        "Season 1 to 2", 
        "https://i.imgur.com/YourPoster6.jpg", 
        ("EP1_FILE_ID", "EP2_FILE_ID", "EP3_FILE_ID", "EP4_FILE_ID", "EP5_FILE_ID", "EP6_FILE_ID")
    ),
    "7. Batman": (
        "Movie Collection", 
        "https://i.imgur.com/YourPoster7.jpg", 
        ("EP1_FILE_ID", "EP2_FILE_ID", "EP3_FILE_ID", "EP4_FILE_ID", "EP5_FILE_ID", "EP6_FILE_ID")
    ),
    "8. Superman": (
        "Movie Collection", 
        "https://i.imgur.com/YourPoster8.jpg", 
        ("EP1_FILE_ID", "EP2_FILE_ID", "EP3_FILE_ID", "EP4_FILE_ID", "EP5_FILE_ID", "EP6_FILE_ID")
    ),
    "9. Avengers": (
        "Movie Collection", 
        "https://i.imgur.com/YourPoster9.jpg", 
        ("EP1_FILE_ID", "EP2_FILE_ID", "EP3_FILE_ID", "EP4_FILE_ID", "EP5_FILE_ID", "EP6_FILE_ID")
    ),
    "10. Iron Man": (
        "Movie Collection", 
        "https://i.imgur.com/YourPoster10.jpg", 
        ("EP1_FILE_ID", "EP2_FILE_ID", "EP3_FILE_ID", "EP4_FILE_ID", "EP5_FILE_ID", "EP6_FILE_ID")
    ),
}

async def set_bot_commands(application):
    commands = [BotCommand("start", "ဇာတ်ကားများကြည့်ရန် ပင်မစာမျက်နှာသို့သွားရန်")]
    await application.bot.set_my_commands(commands)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [[KeyboardButton("/start")]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    
    keyboard = []
    for title in MOVIES.keys():
        keyboard.append([InlineKeyboardButton(f"🎬 {title}", callback_data=f"movie_{title}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # ပြန်လည်ထည့်သွင်းထားသော Welcome ပိုစတာပုံ (File ID)
    welcome_poster = "AgACAgUAAxkBAAEgueJqYFrWN-knIvOwmsOQ859SgDB3eQACUxVrG9u7CFdtu8B_Lb_nPQEAAwIAA3gAAz0E"
    
    welcome_text = (
        "✨ **ကြိုဆိုပါတယ်ခင်ဗျာ!**\n\n"
        "အောက်ပါ ဇာတ်ကားများထဲမှ ကြည့်လိုသည်များကို ရွေးချယ်နိုင်ပါသည် -"
    )

    try:
        sent_msg = await update.message.reply_photo(
            photo=welcome_poster,
            caption=welcome_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except Exception:
        sent_msg = await update.message.reply_text(
            text=welcome_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    context.job_queue.run_once(auto_delete_message, 600, data=sent_msg.chat_id)

async def auto_delete_message(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    try:
        await context.bot.delete_message(chat_id=job.data, message_id=job.message.message_id)
    except Exception:
        pass

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith("movie_"):
        movie_title = data.replace("movie_", "")
        movie_info = MOVIES.get(movie_title, ("Season 1", "https://i.imgur.com/Default.jpg", ("", "", "", "", "", "")))
        seasons = movie_info[0]
        poster_url = movie_info[1]
        ep_files = movie_info[2]
        
        caption_text = (
            f"📌 **{movie_title}**\n"
            f"📺 **Seasons:** {seasons}\n\n"
            f"✨ အခမဲ့ အပိုင်း (၁) မှ (၆) အထိ ဗီဒီယိုဖိုင်များ -"
        )
        
        try:
            sent_msg = await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=poster_url,
                caption=caption_text,
                parse_mode="Markdown"
            )
        except Exception:
            sent_msg = await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=caption_text,
                parse_mode="Markdown",
                protect_content=True
            )
        
        for index, file_id in enumerate(ep_files, start=1):
            if file_id and file_id != "EP1_FILE_ID":
                try:
                    await context.bot.send_video(
                        chat_id=query.message.chat_id,
                        video=file_id,
                        caption=f"📺 **{movie_title} - အပိုင်း ({index})**",
                        parse_mode="Markdown",
                        protect_content=True
                    )
                except Exception as e:
                    logging.error(f"Error sending video ep {index}: {e}")
                    pass
        
        keyboard = [
            [InlineKeyboardButton("🔒 အပိုင်း (၇) မှ အဆုံးထိ ကြည့်ရန် (မန်ဘာဝင်ရန် ၂၀၀၀ ကျပ် ဆက်သွယ်ရန်)", url="https://t.me/naywww01")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        try:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="✨ ဆက်လက်ကြည့်ရှုလိုပါက မန်ဘာဝင်ရန် ဆက်သွယ်နိုင်ပါသည်ခင်ဗျာ 👇",
                reply_markup=reply_markup
            )
        except Exception:
            pass
        
        if sent_msg:
            context.job_queue.run_once(auto_delete_message_by_obj, 43200, data=(sent_msg.chat_id, sent_msg.message_id))

async def auto_delete_message_by_obj(context: ContextTypes.DEFAULT_TYPE):
    chat_id, message_id = context.job.data
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "/start":
        await start(update, context)

if __name__ == '__main__':
    TOKEN = "tonkenဖြည့်ရန်"
    
    application = ApplicationBuilder().token(TOKEN).read_timeout(60).write_timeout(60).connect_timeout(60).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), text_handler))
    
    # Menu ခလုတ်သတ်မှတ်ရန်
    import asyncio
    asyncio.get_event_loop().run_until_complete(set_bot_commands(application))
    
    print("Bot is running...")
    application.run_polling(drop_pending_updates=True)
    
