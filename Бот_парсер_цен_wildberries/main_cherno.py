import time
from selenium import webdriver
from selenium.webdriver import Chrome
from time import sleep
import telebot

token = "TOKEN"
articles = []

def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def send_message(message):
        bot.send_message(message.chat.id, "Привет, друг! Введи нужные артикли через пробел.")

    @bot.message_handler(content_types=["text"])
    def send_text(message):  
        try:
            arts = message.text.split(" ")
            for art in arts:
                articles.append(art)

            for article in articles:
                url = f'https://www.wildberries.ru/catalog/{article}/detail.aspx?targetUrl=XS' 
                bot.send_message(message.chat.id, url)

                options = webdriver.ChromeOptions()
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36")

                browser = Chrome('Project_14 Основа\Selenium\Chrome\chromedriver.exe', options=options)

                browser.get(url)
                time.sleep(3)

                try:
                    price = browser.find_element_by_class_name('price-block__old-price').text
                except:
                    price = browser.find_element_by_class_name('price-block__final-price').text

                bot.send_message(
                    message.chat.id,
                    f"Price: {price}"
                )
            articles.clear()
        except:
            bot.send_message(
                message.chat.id,
                "Damn... Something was wrong"
            )
            articles.clear()

    bot.polling()
    
if __name__ == '__main__':
    telegram_bot(token)