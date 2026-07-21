from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8930481030:AAESGgpg4aEzGgCIvxIq85O9WGiFmOkojCM"
OWNER = "https://t.me/naywww01"

# 📂 ခေါင်းစဉ်များနှင့် အပိုင်းများ (အပိုင်း ၁ မှ ၆ အထိ File ID များကို ဤနေရာတွင် ထည့်ပါ)
ALL_COURSES = {
    "1": {
        "title": "ပထမခေါင်းစဉ်အမည် (ဥပမာ- Python Basic)",
        "videos": {
            1: "အပိုင်း ၁ ရဲ့ File ID ကို ဤနေရာတွင် ထည့်ပါ",
            2: "အပိုင်း ၂ ရဲ့ File ID ကို ဤနေရာတွင် ထည့်ပါ",
            3: "အပိုင်း ၃ ရဲ့ File ID ကို ဤနေရာတွင် ထည့်ပါ",
            4: "အပိုင်း ၄ ရဲ့ File ID ကို ဤနေရာတွင် ထည့်ပါ",
            5: "အပိုင်း ၅ ရဲ့ File ID ကို ဤနေရာတွင် ထည့်ပါ",
            6: "အပိုင်း ၆ ရဲ့ File ID ကို ဤနေရာတွင် ထည့်ပါ",
        }
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    
    # Review လင့်ခ်ကနေ နှိပ်လာရင် (ဥပမာ ?start=1_1)
    if args:
        payload = args[0]
        try:
            course_id, part_num = payload.split("_")
            part_num = int(part_num)
            
            if course_id in ALL_COURSES:
                course = ALL_COURSES[course_id]
                # အပိုင်း ၁ မှ ၆ အတွင်း ဖြစ်မှသာ ဗီဒီယိုပြမည်
                if 1 <= part_num <= 6 and part_num in course["videos"]:
                    video_id = course["videos"][part_num]
                    await update.message.reply_text(f"✅ {course['title']} (အပိုင်း {part_num})")
                    await update.message.reply_video(video=video_id)
                    return
                else:
                    # အပိုင်း ၇ နှင့်အထက်ဆိုလျှင် မန်ဘာဝင်ရန် ပြမည်
                    await update.message.reply_text(
                        "⚠️ အပိုင်း 7 မှစ၍ Free မဟုတ်တော့ပါ။\n\n"
                        "ဆက်လက်ကြည့်ရှုရန် **မန်ဘာဝင်ရန်** လိုအပ်ပါသည်။ "
                        f"မန်ဘာဝင်ရန် Owner ကို ဆက်သွယ်ပါ 👉 {OWNER}"
                    )
                    return
        except ValueError:
            pass

    # ပုံမှန် /start နှိပ်လာလျှင်
    await update.message.reply_text(
        "📚 သင်ခန်းစာများ ရှာဖွေရန် ကြိုဆိုပါတယ်။\n\n"
        "လိုချင်သော **ခေါင်းစဉ်နံပါတ် (သို့မဟုတ်) အမည်** ကို ရိုက်ထည့်ပေးပါ။\n"
        "(ဥပမာ - `1` ဟု ရိုက်ထည့်ပါ)"
    )

async def search_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query_text = update.message.text.strip()
    
    if query_text in ALL_COURSES:
        course = ALL_COURSES[query_text]
        
        keyboard = []
        for part_num in course["videos"].keys():
            keyboard.append([InlineKeyboardButton(f"အပိုင်း {part_num}", callback_data=f"c_{query_text}_p_{part_num}")])
            
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"📂 **{course['title']}**\nကြည့်ရှုလိုသည့် အပိုင်းကို ရွေးပါ -", 
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("❌ ထိုခေါင်းစဉ်ကို မတွေ့ရှိရပါ၊ မှန်ကန်သော နံပါတ်ကို ပြန်လည်ရိုက်ထည့်ပါ။")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    if data.startswith("c_"):
        _, course_id, _, part_num = data.split("_")
        part_num = int(part_num)
        
        course = ALL_COURSES[course_id]
        if 1 <= part_num <= 6 and part_num in course["videos"]:
            video_id = course["videos"][part_num]
            await query.message.reply_text(f"✅ {course['title']} (အပိုင်း {part_num})")
            await query.message.reply_video(video=video_id)
        else:
            await query.message.reply_text(
                "⚠️ အပိုင်း 7 မှစ၍ Free မဟုတ်တော့ပါ။\n\n"
                "ဆက်လက်ကြည့်ရှုရန် **မန်ဘာဝင်ရန်** လိုအပ်ပါသည်။ "
                f"မန်ဘာဝင်ရန် Owner ကို ဆက်သွယ်ပါ 👉 {OWNER}"
            )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_course))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
