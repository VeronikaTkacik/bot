import logging
import telebot

# Встановлення логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація бота з використанням токену
bot = telebot.TeleBot('7097701978:AAFDodgtVT792uPEDnGLCgQVV6c5iZFm-Oo')

# Словник для зберігання транзакцій
transactions = []

# Обробник команди /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привіт! Я бот для відстеження фінансів. Ви можете додавати свої доходи та витрати.")

# Обробник команди /balance
@bot.message_handler(commands=['balance'])
def balance(message):
    total_income = sum([t['amount'] for t in transactions if t['type'] == 'income'])
    total_expense = sum([t['amount'] for t in transactions if t['type'] == 'expense'])
    current_balance = total_income - total_expense
    bot.reply_to(message, f"Загальний баланс: {current_balance} грн.")

# Обробник команди /income
@bot.message_handler(commands=['Дохід'])
def income(message):
    msg = bot.reply_to(message, "Введіть суму доходу:")
    bot.register_next_step_handler(msg, save_income)

# Функція для збереження доходу
def save_income(message):
    try:
        amount = float(message.text)
        transactions.append({'type': 'income', 'amount': amount})
        bot.reply_to(message, f"Дохід {amount} грн. успішно збережено.")
    except ValueError:
        bot.reply_to(message, "Будь ласка, введіть числове значення.")

# Обробник команди /expense
@bot.message_handler(commands=['Витрата'])
def expense(message):
    msg = bot.reply_to(message, "Введіть суму витрати:")
    bot.register_next_step_handler(msg, save_expense)

# Функція для збереження витрати
def save_expense(message):
    try:
        amount = float(message.text)
        transactions.append({'type': 'expense', 'amount': amount})
        bot.reply_to(message, f"Витрата {amount} грн. успішно збережена.")
    except ValueError:
        bot.reply_to(message, "Будь ласка, введіть числове значення.")

# Обробник команди /history
@bot.message_handler(commands=['history'])
def history(message):
    if transactions:
        history_text = "\n".join([f"{t['type'].capitalize()} {t['amount']} грн." for t in transactions])
        bot.reply_to(message, f"Історія транзакцій:\n{history_text}")
    else:
        bot.reply_to(message, "Історія транзакцій порожня.")

# Запуск бота
bot.polling()








