import random
import telebot
from telebot import types
from datetime import datetime
import jdatetime as jdate
import gtts
import qrcode
import os

# Initialize global variables and the bot
number_of_guesses = 0
user_states = {}
my_keyboard = types.ReplyKeyboardMarkup(row_width=3)
keys = ["/start", "/Game😃", "/Age✌", "/Voice🔊", "/Max", "/argmax", "/Qrcode", "/Help💊"]
my_keyboard.add(*(types.KeyboardButton(k) for k in keys))

bot = telebot.TeleBot("7147019989:AAEmjU97Tk1QVS2ShYyioQPH3hP1gVLjcOM", parse_mode=None)  # Replace with your actual token

# Define command handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}, welcome to your friendly BOT. Please select your request from the menu", reply_markup=my_keyboard)

@bot.message_handler(commands=['Help💊'])
def send_help(message):
    help_text = (
        "📌 /start: Greet with the user's name.\n"
        "📌 /Game😃: Guess a random number game.\n"
        "📌 /Age✌: Calculate your age.\n"
        "📌 /Voice🔊: Convert an English sentence to voice.\n"
        "📌 /Max Number: Find the maximum number.\n"
        "📌 /Max index: Find the index of the max number.\n"
        "📌 /Qr code: Make a QR code from the input text.\n"
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['Game😃'])
def start_game_handler(message):
    start_game(message.chat.id)

def start_game(chat_id):
    user_states[chat_id] = {"game": {"playing": True, "number": random.randint(1, 100), "guesses": 0}}
    game_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    game_keyboard.add(types.KeyboardButton("New Game 🔄"))
    bot.send_message(chat_id, "Game started! Guess a number between 1 and 100.", reply_markup=game_keyboard)

@bot.message_handler(func=lambda message: message.text == "New Game 🔄")
def new_game_handler(message):
    start_game(message.chat.id)

@bot.message_handler(func=lambda message: message.text.isdigit())
def handle_guess(message):
    chat_id = message.chat.id
    if chat_id in user_states and user_states[chat_id]["game"]["playing"]:
        guess = int(message.text)
        number = user_states[chat_id]["game"]["number"]
        user_states[chat_id]["game"]["guesses"] += 1

        if guess < number:
            bot.send_message(chat_id, "Higher!")
        elif guess > number:
            bot.send_message(chat_id, "Lower!")
        else:
            bot.send_message(chat_id, f"Congratulations! You guessed the number in {user_states[chat_id]['game']['guesses']} guesses.")
            user_states[chat_id]["game"]["playing"] = False
    else:
        bot.send_message(chat_id, "Please start a new game using /Game😃.")
    
@bot.message_handler(commands=['Voice🔊'])
def send_voice(message):
    msg = bot.reply_to(message, "Enter the English text you want to convert to voice.")
    bot.register_next_step_handler(msg, generate_voice)

def generate_voice(message):
    user_text = message.text
    voice_sound = gtts.gTTS(user_text, lang='en')
    voice_file_path = "voice.mp3"
    voice_sound.save(voice_file_path)
    with open(voice_file_path, "rb") as voice_file:
        bot.send_voice(message.chat.id, voice_file)
    os.remove(voice_file_path)

@bot.message_handler(commands=['Age✌'])
def ask_for_birthdate(message):
    bot.send_message(message.chat.id, "Please enter your birthdate in Shamsi (Hijri Shamsi) format as: (YYYY/MM/DD).")

@bot.message_handler(func=lambda message: "/" in message.text and len(message.text.split("/")) == 3)
def calculate_age(message):
    try:
        birthdate = message.text.split("/")
        birthdate = jdate.date(int(birthdate[0]), int(birthdate[1]), int(birthdate[2]))
        today = jdate.date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        bot.send_message(message.chat.id, f"You are {age} years old.")
    except Exception as e:
        bot.send_message(message.chat.id, "Invalid date format. Please enter in YYYY/MM/DD format.")

@bot.message_handler(commands=['max'])
def max_command_handler(message):
    msg = bot.reply_to(message, "لطفاً یک آرایه از اعداد را وارد کنید، جدا شده با کاما.")
    bot.register_next_step_handler(msg, find_max)

def find_max(message):
    try:
        number_list = [int(num) for num in message.text.split(',')]
        max_number = max(number_list)
        bot.send_message(message.chat.id, f"بزرگترین مقدار در آرایه: {max_number}")
    except Exception as e:
        bot.send_message(message.chat.id, "لطفاً اعداد را به درستی وارد کنید، جدا شده با کاما.")

@bot.message_handler(commands=['argmax'])
def argmax_command_handler(message):
    msg = bot.reply_to(message, "لطفاً یک آرایه از اعداد را وارد کنید، جدا شده با کاما.")
    bot.register_next_step_handler(msg, find_argmax)

def find_argmax(message):
    try:
        number_list = [int(num) for num in message.text.split(',')]
        max_number = max(number_list)
        argmax_index = number_list.index(max_number)
        bot.send_message(message.chat.id, f"اندیس بزرگترین مقدار در آرایه: {argmax_index}")
    except Exception as e:
        bot.send_message(message.chat.id, "لطفاً اعداد را به درستی وارد کنید، جدا شده با کاما.")
@bot.message_handler(commands=['Qrcode'])
def generate_qrcode(message):
    msg = bot.reply_to(message, "Please enter the text you want to convert to a QR code.")
    bot.register_next_step_handler(msg, process_qrcode_input)

def process_qrcode_input(message):
    input_text = message.text
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(input_text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save("qrcode.png")
    with open("qrcode.png", "rb") as qr_file:
        bot.send_photo(message.chat.id, qr_file)
    os.remove("qrcode.png")

@bot.message_handler(commands=['Max'])
def max_command_handler(message):
    msg = bot.reply_to(message, "لطفاً اعداد را به درستی وارد کنید، جدا شده با کاما.")
    bot.register_next_step_handler(msg, find_max)

def find_max(message):
    try:
        number_list = [int(num) for num in message.text.split(',')]
        max_number = max(number_list)
        bot.send_message(message.chat.id, f"The maximum value in the list is: {max_number}")
    except Exception as e:
        bot.send_message(message.chat.id, "Please enter numbers separated by commas.")
bot.infinity_polling()
