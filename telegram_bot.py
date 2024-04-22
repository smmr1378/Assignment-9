import random
import telebot
from telebot import types
from telebot import REPLY_MARKUP_TYPES
from telebot.types import Message
from datetime import datetime
import gtts
import qrcode

number_of_guesses = 0

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

bot = telebot.TeleBot("7147019989:AAEmjU97Tk1QVS2ShYyioQPH3hP1gVLjcOM",parse_mode=None)

@bot.message_handler(commands=['/start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome")


@bot.message_handler(commands=['/Help💊'])
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

@bot.message_handler(commands=['/Qr code'])
def send_qrcode(message):
    bot.reply_to(message,"Give me what ever you want and i will give you a Qr code")
    user_input = input("Give me what ever you want but use (,) between your information ")
    x = qrcode.make(user_input)
    x.save("my_Qrcode.png")

@bot.message_handler(commands=['/Voice🔊'])
def send_voice(message):
    bot.reply_to(message,"Convert a eng sentence to Voice")

    user_text = input("enter your english text: ")
    voice_sound = gtts.gTTS(user_text, lang='en')
    voice_sound.save('english voice.mp3')