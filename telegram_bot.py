import random
import telebot
from telebot import types
from datetime import datetime
import jdatetime as jdate
import gtts
import qrcode

number_of_guesses = 0
user_states = {}
my_keyboard = types.ReplyKeyboardMarkup(row_width=3)
key1 = types.KeyboardButton("/start")
key2 = types.KeyboardButton("/Game😃")
key3 = types.KeyboardButton("/Age✌")
key4 = types.KeyboardButton("/Voice🔊")
key5 = types.KeyboardButton("/Max Number")
key6 = types.KeyboardButton("/Max index ")
key7 = types.KeyboardButton("/Qr code")
key8 = types.KeyboardButton("/Help💊")

my_keyboard.add(key1, key2, key3, key4, key5, key6, key7, key8)

bot = telebot.TeleBot("7147019989:AAEmjU97Tk1QVS2ShYyioQPH3hP1gVLjcOMnn",parse_mode=None)

def start_game(chat_id):
    user_states[chat_id] = {"game": {"playing": True, "number": random.randint(1,100), "guesses": 0}}
    game_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    game_keyboard.add(types.KeyboardButton("New Game 🔄"))
    bot.send_message(chat_id, "Game started! Guess a number between 1 and 100.", reply_markup=game_keyboard)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}, welcome to your friendly BOT, Please select your request from the menu", reply_markup=my_keyboard)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Please select your request from the menu")


@bot.message_handler(commands=['Help💊'])
def send_help(message):
    bot.reply_to(message,"im ready to help you")

    "📌 start: Greet with the users name."

    "📌 game: Guess a random number game"

    "📌 age: Calculate your age."

    "📌 voice: Convert a eng sentence to Voice."

    "📌 max: Find the maximim number"

    "📌 argmax: Find the index of the max number."

    "📌 qrcode: Make a QR code from the input text."

@bot.message_handler(commands=['Game'])
def guessing_game():
    computer_number = random.randint(10, 40)
    user_number = 0
    number_of_guesses = 0

    while True:
        user_number = int(input("Enter your guess: "))
        if computer_number == user_number:
            print("Congratulations! You guessed the correct number.")
            break
        elif computer_number > user_number:
            number_of_guesses += 1
            print("Go up")
        elif computer_number < user_number:
            number_of_guesses += 1
            print("Go down")

@bot.message_handler(commands=['Qr code'])
def send_qrcode(message):
    bot.reply_to(message,"Give me what ever you want and i will give you a Qr code")
    user_input = input("Give me what ever you want but use (,) between your information ")
    x = qrcode.make(user_input)
    x.save("my_Qrcode.png")

@bot.message_handler(commands=['Voice🔊'])
def send_voice(message):
    bot.reply_to(message,"Convert a eng sentence to Voice")

    user_text = input("enter your english text: ")
    voice_sound = gtts.gTTS(user_text, lang='en')
    bot.send_voice(message.chat.id, voice_sound)

@bot.message_handler(commands=['Age✌'])
@bot.message_handler(func=lambda message: message.text == "Age 🕵️‍♂️")
def ask_for_birthdate(message):
    bot.send_message(message.chat.id, "Please enter your birthdate in Shamsi (Hijri Shamsi) format as: (YYYY/MM/DD).")

@bot.message_handler(func=lambda message: "/" in message.text and len(message.text.split("/")) == 3)
def calculate_age(message):
    birthdate = message.text.split("/")
    birthdate = jdate.date(int(birthdate[0]), int(birthdate[1]), int(birthdate[2]))
    today = jdate.date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    bot.send_message(message.chat.id, f"You are {age} years old.")



@bot.message_handler(commands=['Max Number',"Max index"])
@bot.message_handler(func=lambda message: message.text == "Max Number" or message.text == "Max index")
def ask_for_array(message):
    user_states[message.chat.id] = {"command": message.text}
    bot.send_message(message.chat.id, "Please enter a list of numbers separated by commas, format as: (1,2,3,...).")

@bot.message_handler(func=lambda message: "," in message.text and message.chat.id in user_states)
def handle_array_commands(message):
    command = user_states[message.chat.id].get("command")
    numbers = [int(n) for n in message.text.split(',') if n.isdigit()]
    if command == "Max Number" or command == "max":
        max_value = max(numbers)
        bot.send_message(message.chat.id, f"The maximum number is: {max_value}")
    elif command == "Max index" or command == "argmax":
        max_index = numbers.index(max(numbers))
        bot.send_message(message.chat.id, f"The index of the maximum number is: {max_index+1}")

    if message.chat.id in user_states:
        del user_states[message.chat.id]

bot.infinity_polling()

