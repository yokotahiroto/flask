# Flaskクラスをimportする
from flask import Flask, render_template, request, url_for, redirect# Flaskクラスをインスタンス化する
app = Flask(__name__)
# URLと実行する関数をマッピングする
@app.route("/")
def index():
    return "Hello, Flaskbook!"

@app.route("/hello/<name>",
methods=["GET"],
endpoint="hello-endpoint")
def hello(name):
    return f"Hello,{name}!"

@app.route("/name/<name>")
def show_name(name):
    # 変数をテンプレートエンジンに渡す
    return render_template("index.html", name=name)

with app.test_request_context():
    #/
    print(url_for("index"))
    # /hello/world
    print(url_for("hello-endpoint", name="world"))
    # /name/ichiro?page=ichiro
    print(url_for("show_name", name="ichiro", page="1"))

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # メールを送る(最後に実装)
        # contactエンドポイントへリダイレクトする
        return redirect(url_for("contact_complete"))
    return render_template("contact_complete.html")