import telebot
import random
from cs50 import SQL

# This telebot was written with the help of pyTelegramBotAPI library 26.02.2023
# I've used additional materials from: https://mastergroosha.github.io/telegram-tutorial/docs/lesson_01/ , https://mastergroosha.github.io/telegram-tutorial/docs/lesson_02/


bot = telebot.TeleBot("XXX")

db = SQL("sqlite:///mathbot.db")

def define_task():
	x = random.randint(2, 9)
	y = random.randint(3, 9)
	z = x*y
	db.execute("INSERT INTO history (x, y, z) VALUES (:x, :y, :z)", x=x, y=y, z=z)


@bot.message_handler(commands=["start"])
def start(m):
	define_task()
	xlist = db.execute("SELECT x FROM history")
	xl = xlist[0]
	x = xl['x']
	ylist = db.execute("SELECT y FROM history")
	yl = ylist[0]
	y = yl['y']
	bot.send_message(m.chat.id, "How much is: " + str(x) + " * " + str(y) + " ?")


def clean_task():
	db.execute("DELETE FROM history")


@bot.message_handler(content_types=["text"])
def check_answer(message):
	a = message.text.strip()
	if a.isdigit() == True:
		try:
			answer = int(a)
			r_alist = db.execute("SELECT z FROM history")
			r_al = r_alist[0]
			r_a = r_al['z']
			if answer == r_a:
				bot.send_message(message.chat.id, "Yes. Press start to continue")
				clean_task()
			else:
				bot.send_message(message.chat.id, "No. The answer is " + str(r_a) + ". Your answer was " + str(answer) + ". Press start to continue")
				clean_task()
		except:
				r_a = right_answer()
				bot.send_message(message.chat.id, "No. The answer is " + str(r_a) + ". Your answer was " + str(answer) + ". Press start to continue")
		clean_task()
	else:
		r_alist = db.execute("SELECT z FROM history")
		r_al = r_alist[0]
		r_a = r_al['z']
		bot.send_message(message.chat.id, "No. The answer is " + str(r_a) + ". Your answer was " + str(a) + ". Press start to continue")

if __name__ == '__main__':
    bot.infinity_polling()
