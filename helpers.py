from functools import wraps
from flask import Flask, redirect, render_template, request, url_for, session
from flask_session import Session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
