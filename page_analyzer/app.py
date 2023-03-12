from flask import Flask, render_template, request, redirect, url_for, flash
from page_analyzer.validation import check_url
from page_analyzer.storage import URLStorage, UrlExists
from page_analyzer.message_texts import URL_ADDED_SUCCESS, URL_ALREADY_EXISTS
from dotenv import load_dotenv
from os import getenv


load_dotenv()

app = Flask(__name__)
app.storage = URLStorage(dsn=getenv("DATABASE_URL"))
app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def get_index():
    return render_template("index.html")


@app.route("/urls", methods=["POST"])
def add_url():
    url_name = request.form.get("url", None)
    error = check_url(url_name)
    if error:
        return render_template("index.html", error=error)

    try:
        url = app.storage.add(url_name)
    except UrlExists as e:
        flash(URL_ALREADY_EXISTS, category="info")
        return redirect(url_for('get_url', id=e.id))

    flash(URL_ADDED_SUCCESS, category="success")
    return redirect(url_for('get_url', id=url["id"]))


@app.route("/urls/<int:id>", methods=["GET"])
def get_url(id):
    url = app.storage.get(id)
    return render_template("url.html", url=url)


@app.route("/urls", methods=["GET"])
def get_urls():
    urls = app.storage.list()
    return render_template("urls.html", urls=urls)
