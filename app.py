import os
from flask import Flask, render_template, request, redirect, session, flash, url_for
from dotenv import load_dotenv
from stytch import Client

load_dotenv()
print("FLASK_SECRET", os.getenv("FLASK_SECRET"))

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET")

stytch = Client(
    project_id=os.getenv("STYTCH_PROJECT_ID"),
    secret=os.getenv("STYTCH_SECRET"),
    environment="test",         # change to "live" when ready
)

REDIRECT_URL = os.getenv("REDIRECT_URL")

# ------------- helpers -------------
def logged_in():
    return "user" in session

# ------------- routes -------------
@app.route("/")
def home():
    if not logged_in():
        return redirect(url_for("login"))
    return render_template("index.html", user=session["user"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        # Fire the magic-link
        stytch.magic_links.email.login_or_create(
            email=email,
            login_magic_link_url=REDIRECT_URL,
            signup_magic_link_url=REDIRECT_URL,
        )
        flash("Check your e-mail for the magic link!")
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/authenticate")
def authenticate():
    """Landing page for the magic-link redirect."""
    token = request.args.get("token")
    if not token:
        flash("Missing token"); return redirect(url_for("login"))

    resp = stytch.magic_links.authenticate(token=token)  # ⬅ verifies & consumes
    # Save whatever you care about from Stytch’s response
    session["user"] = {
        "user_id": resp.user_id,
        "email": resp.email,
        "last_login": resp.user.last_seen_at,
        # add more fields as you enable them (name, phone, etc.)
    }
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out!")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
