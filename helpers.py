from functools import wraps
from flask import Flask, redirect, render_template, request, url_for, session
from flask_session import Session
import feedparser

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def newsParse(league):
    rss_url = 'https://www.espn.com/espn/rss/' + league + '/news'
    parser = feedparser.parse(rss_url)

    newsInfo = []

    for entry in parser.entries:
        newEntry = {
            'title': entry.title,
            'description': entry.description,
            'link': entry.link,
            'date': entry.published_parsed,
            'displayDate': entry.published
        }
        newsInfo.append(newEntry)
    return newsInfo