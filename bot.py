
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

TOKEN = "7923271549:AAGEsVR-DgrT1oaBEFa-AxUr56owHguxZ3w"

questions = [
    {
        "question": "1) Какой завод в Ленинградской области в начале войны производил шифровальные машины?",
        "options": ["329", "712", "209", "305"],
        "correct": "209"
    },
    {
        "question": "2) Кто взломал шифровальную машину немецкой армии «Энигма»?",
        "options": ["Алан Тьюринг", "Джон фон Нейман", "Чарльз Бэббидж", "Клод Шеннон"],
        "correct": "Алан Тьюринг"
    },
    {
        "question": "3) Участник разработки засекреченной телефонной линии, автор книги «В круге третьем»",
        "options": ["В.А. Котельников", "К.Ф. Калачёв", "И.С. Нейман", "Н.Н. Найденов"],
        "correct": "К.Ф. Калачёв"
    },
    {
        "question": "4) Какая лаборатория изготовила прототип аппарата «Соболь-П»?",
        "options": [
            "Кучинская радиолаборатория НКВД",
            "Ленинградский физико-технический институт",
            "Ленинградская радиолаборатория НКВД",
            "Лаборатория Владимира Котельникова"
        ],
        "correct": "Лаборатория Владимира Котельникова"
    },
    {
        "question": "5) Кто осуществлял политический контроль над почтовой корреспонденцией?",
        "options": [
            "Подразделение военной цензуры",
            "НКВД",
            "НКГБ",
            "ГУГБ"
        ],
        "correct": "НКВД"
    },
    {
        "question": "6) Кому принадлежат слова «Хорошая работа шифровальщиков помогла выиграть не одно сражение»?",
        "options": [
            "К.К. Рокоссовский",
            "Р. Я. Малиновский",
            "Г.К. Жуков",
            "С.М. Буденный"
        ],
        "correct": "Г.К. Жуков"
    },
    {
        "question": "7) В каком году была запущена в серийное производство шифровальная машина К-37 «Кристалл»?",
        "options": ["1938", "1939", "1941", "1942"],
        "correct": "1939"
    },
    {
        "question": "8) Кем была разработана шифровальная машина М-101 «Изумруд»?",
        "options": [
            "Н.М. Шарыгин, М.С. Козлов под руководством И. П. Волоска.",
            "Н.В. Рытов",
            "В.А. Котельников",
            "К.Ф. Калачёв"
        ],
        "correct": "Н.М. Шарыгин, М.С. Козлов под руководством И. П. Волоска."
    },
    {
        "question": "9) За создание какой шифровальной машины была присуждена Сталинская премия 3 степени?",
        "options": ["К-37 «Кристал»", "М-100 «Спектр»", "М-101 «Изумруд»", "Соболь-П"],
        "correct": "М-101 «Изумруд»"
    },
    {
        "question": "10) Какой аппарат использовался для голосового шифрования в годы ВОВ?",
        "options": ["К-37 «Кристал»", "М-100 «Спектр»", "М-101 «Изумруд»", "Соболь-П"],
        "correct": "Соболь-П"
    }
]

QUIZ = range(1)
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"score": 0, "current": 0}
    await update.message.reply_text("Начинаем тест заново!")
    await send_question(update, context)
    return QUIZ

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await start(update, context)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = user_data[user_id]
    index = data["current"]

    if index >= len(questions):
        await update.message.reply_text(
            f"Тест завершён! Правильных ответов: {data['score']} из {len(questions)}\n\n"
            f"Чтобы пройти тест снова, введите /start."
        )
        return ConversationHandler.END

    if index == 9:
        await update.message.reply_text(
            "Остался последний вопрос, а сейчас подпишись на наш телеграмм канал t.me/bronislav56, там много интересной информации",
            disable_web_page_preview=True
        )

    q = questions[index]
    markup = ReplyKeyboardMarkup([[opt] for opt in q["options"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(q["question"], reply_markup=markup)
    return QUIZ

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    answer = update.message.text
    current_q = questions[user_data[user_id]["current"]]
    
    if answer == current_q["correct"]:
        user_data[user_id]["score"] += 1
        feedback = "✅ Правильно!"
    else:
        feedback = f"❌ Неправильно. Правильный ответ: {current_q['correct']}"

    await update.message.reply_text(feedback)
    
    user_data[user_id]["current"] += 1
    return await send_question(update, context)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выход из теста.")
    return ConversationHandler.END

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    quiz_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            QUIZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(quiz_handler)
    app.add_handler(CommandHandler("restart", restart))
    app.add_handler(CommandHandler("cancel", cancel))

    app.run_polling()
