from flask import Flask, render_template
from markdown import markdown

app = Flask(__name__)


@app.route("/")
def index():
    # Exemple de texte en Markdown avec une équation mathématique
    content = """
# Ceci est un titre

Voici une équation mathématique :

$$ E = mc^2 $$

Et un peu de texte en **gras** et *italique*.

Un image


    """
    # Convertir le markdown en HTML
    content_html = markdown(content, extensions=["extra", "codehilite"])

    return render_template("index.html", content=content_html)


if __name__ == "__main__":
    app.run(debug=True)
