import telebot
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot import TeleBot

bot = telebot.TeleBot("8084719643:AAFz-YHKnjo81CGdIkNb1G5zpoxSJ7Kq6Cg")

@bot.message_handler(commands=["start"])
def nana(message):
    with open("obuchalka.json", "r") as file:
        bd = json.load(file)
    if str(message.chat.id) not in bd:

        bd[str(message.chat.id)] = {"progress": 0, "nickname": message.from_user.username}
        bot.send_message(message.chat.id, "Привет! Введи свой ник")
        with open("obuchalka.json", "w") as file:
            json.dump(bd, file)
    buttons = ReplyKeyboardMarkup()
    q = KeyboardButton("/Question")
    p = KeyboardButton("/Progress")
    buttons.add(q, p)
    bot.send_message(message.chat.id, "Хочешь начать обучение?", reply_markup=buttons)
@bot.message_handler(commands=["Question"])
def quest(message):
    with open("obuchalka.json", "r") as file:
        bd = json.load(file)
    progress = bd[str(message.chat.id)]["progress"]
    with open("python_questions_100.json", "r", encoding="utf-8") as file:
        questionbd = json.load(file)
        questionnumber = questionbd[str(progress)]
        questions = questionnumber["question"]
        variants = questionnumber['options']
        answer = questionnumber['answer']

    buttons1 = ReplyKeyboardMarkup()
    a1 = KeyboardButton(variants[0])
    a2 = KeyboardButton(variants[1])
    a3 = KeyboardButton(variants[2])
    a4 = KeyboardButton(variants[3])

    buttons1.add(a1, a2, a3, a4)
    bot.send_message(message.chat.id, f"{questions}",reply_markup=buttons1)
@bot.message_handler(commands=["Progress"])
def prog(message):
    with open("obuchalka.json", "r") as file:
        bd = json.load(file)
    progress = bd[str(message.chat.id)]["progress"]
    bot.send_message(message.chat.id, f"Твой текущий уровень: {progress}")
@bot.message_handler(content_types=["text"])
def playeransw(message):
    playeranswer = message.text
    with open("obuchalka.json", "r") as file:
        bd = json.load(file)
    progress = bd[str(message.chat.id)]["progress"]
    with open("python_questions_100.json", "r", encoding="utf-8") as file:
        questionbd = json.load(file)
        questionnumber = questionbd[str(progress)]
        questions = questionnumber["question"]
        variants = questionnumber['options']
        answer = questionnumber['answer']
        explain = questionnumber["explanation"]
    if playeranswer in variants:
        if playeranswer == answer:
            bot.send_message(message.chat.id, "Правильно")

            bd[str(message.chat.id)]["progress"] += 1
            print(bd)
            with open("obuchalka.json", "w") as file:
                json.dump(bd, file)
            quest(message)
        else:
            bot.send_message(message.chat.id, "Неправильно")
            buttonss = ReplyKeyboardMarkup()
            q1 = KeyboardButton("/Question")
            buttonss.add(q1)
            bot.send_message(message.chat.id, f"Подсказка: {explain}", reply_markup=buttonss)












bot.polling()