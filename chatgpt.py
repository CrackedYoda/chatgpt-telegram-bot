import logging
import os
import telebot
from telebot import types, util # imported telebot from pyTelegramBotAPI
from telebot import custom_filters #imported the custom text filter from telebot library 
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI(api_key = os.getenv("GPT_KEY"))
 

def gpt(prompt):
  completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": prompt}
  ]
  )
  return (completion.choices[0].message.content)
  
 
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



TELEGRAM_API_Key = os.getenv("TELEGRAM_API_Key")

bot = telebot.TeleBot(TELEGRAM_API_Key) #initiated the telebot with my API keys


@bot.message_handler(commands=['start'])  #made a ""start"" text handler with the COMMAND method. Refer to Docs
def welcome_message(message):#a function that takes one parameter which is the ""message"" just right under the handler is how pyTelegramBotAPI deals with info
    bot.reply_to(message,"welcome to yoda chatGptBot")

@bot.message_handler(commands=['help'])
def help_handler(message):
  bot.send_message(message.chat.id,"this is a bot that makes use of chatgpt model. ask any question or start a conversation")

@bot.message_handler(content_types=['document', 'audio','photo','voice'])
def handle_docs_audio(message):
	bot.send_message(message.chat.id,'this is not a text') #when sending a message you nedd to add a chat id


nsfw_words = ['sex', 'porn', 'dick','pussy']
        
        
@bot.message_handler(func=lambda message: True)
def main(message):
    if any(word in message.text.lower() for word in nsfw_words):
        # Get the chat ID and message ID
        chat_id = message.chat.id
        try:
            bot.send_message(chat_id, "NSFW WORD🔨")
        except Exception as e:
            print(f"Error sending NSFW message alert: {e}")
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        response = gpt(message.text)
        if len(response) > 5000:
            splitted_text = util.split_string(response, 3000)
            for text in splitted_text:
                print(text)
                bot.reply_to(message, text)
        else:
            print(response)
            bot.reply_to(message, response)

     
                 
     

bot.add_custom_filter(custom_filters.TextMatchFilter()) #added the text match filter
bot.add_custom_filter(custom_filters.TextStartsFilter())

bot.infinity_polling()


  

  
