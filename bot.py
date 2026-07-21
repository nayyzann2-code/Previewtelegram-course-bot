from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

TOKEN = "8930481030:AAESGgpg4aEzGgCIvxIq85O9WGiFmOkojCM"
OWNER = "https://t.me/naywww01"

ALL_COURSES = {
    "flash": {
        "title": "The Flash (2014)",
        "videos": {
            1: "AAMCBQADGQEDXlV_al9eVk62LzCTrKjv_7BEv0WtD84AAiQeAAKFy4FUXJNsFXuqRPEBAAdtAAM9BA",
            2: "AAMCBQADGQEDXl5Qal9l8QAB-eBpKsJe-DECTOQgKQ77AAIlHgAChcuBVK49jZTQRMVjAQAHbQADPQQ",
            3: "AAMCBQADGQEDXl5-al9mFiIMkV1nc2RucvmJodK_ULoAAiYeAAKFy4FUNRtZ8dDMvisBAAdtAAM9BA",
            4: "AAMCBQADGQEDXl8-al9m0URt8_QaItigKtAt9NYDt-IAAiseAAKFy4FUtGnma9kwiGUBAAdtAAM9BA",
            5: "AAMCBQADGQEDXl9Nal9m22u3eqv_ckXtOZQcONYNa0AAAtcjAAJZxHhUy55L6Rw8zuoBAAdtAAM9BA",
        }
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    
    if args:
        payload = args[0]
        try:
            course_id, part_num = payload.split("_")
            part_num = int(part_num)
            
            if course_id in ALL_COURSES:
                course = ALL_COURSES[course_id]
                if 1 <= part_num <= 5 and part_num in course["videos"]:
                    video_id = course["videos"][part_num]
                    await update.message.reply_text(f"✅ {course['title']} (S01Ep0{part_num})")
                    await update.message.reply_video(video=video_id)
                    return
                else:
                    await update.message.reply_text(
                        "⚠️ အပိုင်း 6 မှစ၍ Free မဟုတ်တော့ပါ။\n\n"
                        "ဆက်လက်ကြည့်ရှုရန် **မန်ဘာဝင်ရန်** လိုအပ်ပါသည်။ "
                        f"မန်ဘာဝင်ရန် Owner ကို ဆက်သွယ်ပါ 👉 {OWNER}"
                    )
                    return
        except ValueError:
            pass

    keyboard = []
    for cid, course in ALL_COURSES.items():
        keyboard.append([InlineKeyboardButton(course["title"], callback_data=f"select_{cid}")])
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎬 ကြည့်ရှုလိုသော ဇာတ်ကား (သို့မဟုတ်) ခေါင်းစဉ်ကို ရွေးချယ်ပါ -",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith("select_"):
        _, course_id = data.split("_")
        course = ALL_COURSES[course_id]
        
        keyboard = []
        for part_num in course["videos"].keys():
            keyboard.append([InlineKeyboardButton(f"S01Ep0{part_num}", callback_data=f"c_{course_id}_p_{part_num}")])
            
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            f"📂 **{course['title']}**\nကြည့်ရှုလိုသည့် အပိုင်းကို ရွေးပါ -", 
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    elif data.startswith("c_"):
        _, course_id, _, part_num = data.split("_")
        part_num = int(part_num)
        
        course = ALL_COURSES[course_id]
        if 1 <= part_num <= 5 and part_num in course["videos"]:
            video_id = course["videos"][part_num]
            await query.message.reply_text(f"✅ {course['title']} (S01Ep0{part_num})")
            await query.message.reply_video(video=video_id)

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
