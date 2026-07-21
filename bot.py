import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

# Log များကို စစ်ဆေးရန် (Error ရှိမရှိ ကြည့်ရန်)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TOKEN = "8954957485:AAEZbI58ShdA6r1lNecuPBiGCe5ym2XKe4s"
OWNER = "https://t.me/naywww01"

# 📂 ခေါင်းစဉ် ၁၀ ခုစာအတွက် ဗီဒီယို File ID များ
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
    },
    "spiderman": {
        "title": "Spider-Man",
        "videos": {
            1: "File ID ထည့်ရန်",
            2: "File ID ထည့်ရန်",
            3: "File ID ထည့်ရန်",
            4: "File ID ထည့်ရန်",
            5: "File ID ထည့်ရန်",
            6: "File ID ထည့်ရန်",
        }
    },
    "batman": {
        "title": "The Batman",
        "videos": {
            1: "File ID ထည့်ရန်",
            2: "File ID ထည့်ရန်",
            3: "File ID ထည့်ရန်",
            4: "File ID ထည့်ရန်",
            5: "File ID ထည့်ရန်",
            6: "File ID ထည့်ရန်",
        }
    },
    "ironman": {
        "title": "Iron Man",
        "videos": {
            1: "File ID ထည့်ရန်",
            2: "File ID ထည့်ရန်",
            3: "File ID ထည့်ရန်",
            4: "File ID ထည့်ရန်",
            5: "File ID ထည့်ရန်",
            6: "File ID ထည့်ရန်",
        }
    },
    "thor": {
        "title": "Thor",
        "videos": {
            1: "File ID ထည့်ရန်",
            2: "File ID ထည့်ရန်",
            3: "File ID ထည့်ရန်",
            4: "File ID ထည့်ရန်",
            5: "File ID ထည့်ရန်",
            6: "File ID ထည့်ရန်",
        }
    },
    "captain": {
        "title": "Captain America",
        "videos": {
            1: "File ID ထည့်ရန်",
            2: "File ID ထည့်ရန်",
            3: "File ID ထည့်ရန်",
            4: "File ID ထည့်ရန်",
            5: "File ID ထည့်ရန်",
            6: "File ID ထည့်ရန်",
        }
    },
    "superman": {
        "title": "Superman",
        "videos": {
            1: "File ID ထည့်ရန်",
            2: "File ID ထည့်ရန်",
            3: "File ID ထည့်ရန်",
            4: "File ID ထည့်ရန်",
            5: "File ID ထည့်ရန်",
            6: "File ID ထည့်ရန်",
        }
    },
    "avengers": {
        "title": "Avengers",
        "videos": {
            1: "File ID ထည့်ရန်",
            2: "File ID ထည့်ရန်",
            3: "File ID ထည့်ရန်",
            4: "File ID ထည့်ရန်",
            5: "File ID ထည့်ရန်",
            6: "File ID ထည့်ရန်",
        }
    },
    "matrix": {
        "title": "The Matrix",
        "videos": {
            1: "File ID ထည့်ရန်",
            2: "File ID ထည့်ရန်",
            3: "File ID ထည့်ရန်",
            4: "File ID ထည့်ရန်",
            5: "File ID ထည့်ရန်",
            6: "File ID ထည့်ရန်",
        }
    },
    "avatar": {
        "title": "Avatar",
        "videos": {
            1: "File ID ထည့်ရန်",
            2: "File ID ထည့်ရန်",
            3: "File ID ထည့်ရန်",
            4: "File ID ထည့်ရန်",
            5: "File ID ထည့်ရန်",
            6: "File ID ထည့်ရန်",
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
                if part_num in course["videos"]:
                    video_id = course["videos"][part_num]
                    await update.message.reply_text(f"✅ {course['title']} (S01Ep0{part_num})")
                    await update.message.reply_video(video=video_id)
                    return
                else:
                    await update.message.reply_text(
                        "⚠️ ဤအပိုင်းအတွက် ဗီဒီယို မရှိသေးပါ။\n\n"
                        f"ဆက်လက်ကြည့်ရှုရန် Owner ကို ဆက်သွယ်ပါ 👉 {OWNER}"
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
        if part_num in course["videos"]:
            video_id = course["videos"][part_num]
            # File ID နေရာမှာ စာသားအမှန်မဟုတ်ဘဲ "File ID ထည့်ရန်" ဖြစ်နေရင် သတိပေးချက်ပြမယ်
            if "File ID" in str(video_id):
                await query.message.reply_text("⚠️ ဤအပိုင်းအတွက် ဗီဒီယို File ID ထည့်ရန် ကျန်သေးသည်။")
            else:
                await query.message.reply_text(f"✅ {course['title']} (S01Ep0{part_num})")
                await query.message.reply_video(video=video_id)

def main():
    # Bot ကို စတင် Run မည့် အဓိက အပိုင်း
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Bot ကို စတင်လည်ပတ်စေခြင်း
    application.run_polling()

if __name__ == "__main__":
    main()
