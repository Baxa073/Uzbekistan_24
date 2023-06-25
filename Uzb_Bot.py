# -*- coding: utf-8 -*-
"""
Created on Tue May 23 16:56:08 2023

@author: buxor
"""


import telebot
import feedparser
import random
import time
from googleapiclient.discovery import build
from telebot import types

# Telegram bot tokenini o'zgartiring
TOKEN = '6193523506:AAHvjWH7gFfzbO2n7Ellks3ZLcJbhqr5Y48'

bot = telebot.TeleBot(TOKEN)

# YouTube API so'rovnoma uchun API kalitini o'zgartiring
YOUTUBE_API_KEY = 'AIzaSyC_xnKE_xLt7rgHlFdKqGz_9s12QpJo-io'

# YouTube API ni ishga tushiring
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def fetch_news(url):
    feed = feedparser.parse(url)
    if feed.entries:
        random_article = random.choice(feed.entries)
        title = random_article.title
        description = random_article.summary
        link = random_article.link
        return f"<b>{title}</b>\n\n{description}\n\nBatafsil: {link}"
    else:
        return "Yangiliklarni yuklashda xatolik yuz berdi. Iltimos, keyinroq qaytadan urinib ko'ring."


def fetch_news(url):
    feed = feedparser.parse(url)
    news_list = []
    for entry in feed.entries:
        title = entry.title
        description = entry.summary
        link = entry.link
        news_list.append(f"<b>{title}</b>\n\n{description}\n\nBatafsil: {link}")
    return news_list

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Assalomu alaykum! Men yangiliklar va media materiallari qo'llab-quvvatlovchi botman.")

@bot.message_handler(commands=['news'])
def news(message):
    rss_url = 'https://kun.uz/rss'
    news_list = fetch_news(rss_url)
    for news_item in news_list:
        bot.send_message(message.chat.id, news_item, parse_mode='HTML')
        time.sleep(1)  # 1 sekund kutamiz yangi yangiliklar orasida

@bot.message_handler(commands=['media'])
def media(message):
    video_request = youtube.search().list(q='kun.uz', part='snippet', maxResults=10, type='video').execute()
    video_items = video_request.get('items', [])

    if video_items:
        random_video = random.choice(video_items)
        video_id = random_video['id']['videoId']
        video_title = random_video['snippet']['title']

        video_message = f"Kun.uz video: <b>{video_title}</b>\nhttps://www.youtube.com/watch?v={video_id}"
        bot.reply_to(message, video_message, parse_mode='HTML')
    else:
        bot.reply_to(message, "Media materiallari yuklanirken xatolik yuz berdi. Iltimos, keyinroq qaytadan urinib ko'ring.")

bot.polling()
