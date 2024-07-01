from flask import Flask, render_template, session, redirect, url_for
import os
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

k_CardsFolder = "./static/cards"
images = os.listdir(k_CardsFolder)


# -----------------------------------------------------------------------------
@app.route("/")
def index():
    if "seen_images" not in session:
        session["seen_images"] = []

    if len(session["seen_images"]) == len(images):
        # reset the list since all images have been seen during the session
        # TODO : save the seen_images suche that we can continue from one session to another
        session["seen_images"] = []

    remaining_images = list(set(images) - set(session["seen_images"]))
    img_file = random.choice(remaining_images)
    # print(img_file)
    session["seen_images"].append(img_file)

    return render_template("index.html", img_file=img_file)


# -----------------------------------------------------------------------------
@app.route("/next")
def next_image():
    return redirect(url_for("index"))


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
