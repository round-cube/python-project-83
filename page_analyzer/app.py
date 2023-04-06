from flask import Flask, render_template, request, redirect, url_for, flash
from page_analyzer.validation import check_url
from page_analyzer.storage import URLStorage, UrlExists, UrlNotFound
from page_analyzer.message_texts import URL_ADDED_SUCCESS, URL_ALREADY_EXISTS, URL_CHECK_SUCCESS
from dotenv import load_dotenv
from os import getenv
from page_analyzer.web import fetch_url, URLFetchError, parse_html


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
        return render_template("index.html", error=error), 422

    try:
        url = app.storage.add(url_name)
    except UrlExists as e:
        flash(URL_ALREADY_EXISTS, category="info")
        return redirect(url_for('get_url', id=e.id))

    flash(URL_ADDED_SUCCESS, category="success")
    return redirect(url_for('get_url', id=url["id"]))


@app.route("/urls/<int:id>", methods=["GET"])
def get_url(id):
    try:
        url = app.storage.get(id)
    except UrlNotFound:
        return render_template("404.html")
    return render_template("url.html", url=url)


@app.route("/urls/<int:id>/checks", methods=["POST"])
def add_url_check(id):
    try:
        url = app.storage.get(id)
    except UrlNotFound:
        return render_template("404.html")

    kwargs = {}

    try:
        response = fetch_url(url["name"])
    except URLFetchError as e:
        return render_template("url.html", url=url, error=e.text)

    kwargs["status_code"] = response.status_code
    (kwargs["h1"], kwargs["title"],
     kwargs["description"]) = parse_html(response.content)

    _ = app.storage.add_url_check(id, **kwargs)
    flash(URL_CHECK_SUCCESS, category="success")
    return redirect(url_for("get_url", id=id))


@app.route("/urls", methods=["GET"])
def get_urls():
    urls = app.storage.list()
    return render_template("urls.html", urls=urls)
