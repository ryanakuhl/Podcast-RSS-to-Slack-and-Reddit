# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 11:00:26 2018

@author: ryan-kuhl
"""

import praw
import feedparser
from datetime import datetime
from datetime import timedelta
import time
import timestring
from slackclient import SlackClient
from tkinter import messagebox

#PRAW login
#see progur.com/2016/09/how-to-create-reddit-bot-using-praw4.html to learn how to get these fields
reddit = praw.Reddit(user_agent='#', client_id='#', client_secret='#', username='#', password='#')
 
#get Slack bot user token https://api.slack.com/bot-users                     
def posted():
	reddit.subreddit('INSERT SUBREDDIT TO POST TO').submit(title,url=link).reply(summary)
	SLACK_TOKEN = "#"
	sc = SlackClient(SLACK_TOKEN)
	desc = "\n"+title+"\n"+summary+"\n"+link
	sc.api_call("chat.postMessage", channel='#INSERT CHANNEL OF SLACK TO POST TO', text=desc, username='INSERT USERNAM')
	time.sleep(25*60*60)
    
def checkreddit():
    subreddit = reddit.subreddit('obdm')
    for submission in subreddit.new(limit=1):
      old = submission.title
      if old == title:
        message = "Looks like the episode released within the past day is already published.\nGoing to snooze for 24 hours.\nRSS:\n"+title+"\nReddit:\n"+old
        messagebox.showinfo("TITLE", message)
        time.sleep(25*60*60)
      else:
        b = messagebox.askquestion("Alpha One Command Center ","New episode detected. Would you like to publish?\n"+title)
        if b == "yes":
          posted()
        elif b == "no":
          time.sleep(60*60)
    
while reddit != None:
  #get feed
  d = feedparser.parse('http://ourbigdumbmouth.libsyn.com/rss')
  #pull and convert to time
  published = timestring.Date(d.modified)
  #get current time minus 24hours to hunt for new episode
  present = datetime.now() + timedelta(hours=23)
  title = d.entries[0].title
  link = d.entries[0].link
  summary = d.entries[0].summary
  #cleans, strips social media
  summary = summary.split('</p>', 1)[0]
  summary = summary.replace('<p>','')
  summary = summary.replace('<br />','\n\n')
  if present > published:
    checkreddit()
