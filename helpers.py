from functools import wraps
from flask import Flask, redirect, render_template, request, url_for, session
from flask_session import Session
import feedparser
import requests
from bs4 import BeautifulSoup

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def newsParse(league):
    url = 'https://www.espn.com/espn/rss/' + league + '/news'

    def seperate_description_and_image(s):
        if '\n' in s:
            return s.rsplit('\n', 1)
        else:
            return [s, ""]

    response = requests.get(url)
    raw = response.text
    raw = raw.replace("</description><image>", "\n")
    raw = raw.replace(".jpg]]></image>", ".jpg]]>\n</description>")
    
    parser = feedparser.parse(raw)

    newsInfo = []
    for entry in parser.entries:
        try:
            newEntry = {
            'title': entry.title,
            'description': seperate_description_and_image(entry.description)[0],
            'image': seperate_description_and_image(entry.description)[1],
            'link': entry.link,
            'date': entry.published_parsed,
            'displayDate': entry.published
            }
            newsInfo.append(newEntry)
        except AttributeError:
            continue
    
    return newsInfo
