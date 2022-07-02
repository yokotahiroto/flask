from email_validator import validate_email, EmailNotValidError
# Flaskクラスをimportする
from flask import (
    Flask,
    current_app,
    g,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    make_response,
    session
)
import logging
import os
from flask_mail import Mail, Message
from flask_debugtoolbar import DebugToolbarExtension
#response = make_response(render_template("contact.html"))

# keyを指定する
#username = request.cookies.get("username")
#response.delete_cookie("username")
# keyとvalueをセットする
#response.set_cookie("username", "ichiro")

# セッションへ値を設定する
#session["username"] = "ichiro"
# セッションから値を取得する
#username = session["username"]
# セッションから値を削除する
#session.pop("username", None)

# Flaskクラスをインスタンス化する
app = Flask(__name__)
# SECRET_KEYを追加する
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"
# ログレベルを設定する
app.logger.setLevel(logging.DEBUG)
# リダイレクトを中断しないようにする
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# DebugToolbarExtensionにアプリケーションをセットする
toolbar = DebugToolbarExtension(app)
# Mailクラスのコンフィグを追加する
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# flask-mail拡張を登録する
mail = Mail(app)

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
    # レスポンスオブジェクトを取得する
    response = make_response(render_template("contact.html"))
    # クッキーを設定する
    response.set_cookie("flaskbook key", "flaskbook value")
    # セッションを設定する
    session["username"] = "ichiro"
    # レスポンスオブジェクトを返す
    return response
    #return render_template("contact.html")

@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # メールを送る(最後に実装)
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        send_email(
            email, "問い合わせありがとうございました。", "contact_mail",
            username=username,
            description=description,
        )

        # 入力チェック
        is_valid = True

        if not username:
            flash("ユーザー名は必須です")
            is_valid = False

        if not email:
            flash("メールアドレスは必須です")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください")
            is_valid = False

        if not description:
            flash("問い合わせ内容は必須です")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))
        # メールを送る(最後に実装)

        # 問い合わせ完了エンドポイントへリダイレクトする
        flash("問い合わせありがとうございました。")
        # contactエンドポイントへリダイレクトする
        return redirect(url_for("contact_complete"))
    return render_template("contact_complete.html")

def send_email(to, subject, template, **kwargs):
    """メールを送信する関数"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)