import logging

from flask import Flask, redirect, render_template, request, url_for

from tablerito import attachments, boards, config
from tablerito.notifications import notifications


def create_app() -> Flask:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-5s %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(), logging.FileHandler("tablerito.log", encoding="utf-8")],
    )
    notifications.wait_until_available()
    boards.seed_sample_board()

    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = config.ATTACHMENT_LIMIT

    @app.get("/")
    def show_board():
        return render_template("board.html", board=boards.board)

    @app.post("/lists/<int:list_id>/cards")
    def create_card(list_id: int):
        boards.create_card(list_id, request.form["title"])
        return redirect(url_for("show_board"))

    @app.post("/cards/<int:card_id>/move")
    def move_card(card_id: int):
        boards.move_card(card_id, int(request.form["list_id"]))
        return redirect(url_for("show_board"))

    @app.post("/cards/<int:card_id>/attachments")
    def attach(card_id: int):
        file = request.files["file"]
        if file.filename:
            card = boards.find_card(card_id)
            card.attachments.append(attachments.save(card_id, file))
        return redirect(url_for("show_board"))

    @app.get("/attachments/<name>")
    def download(name: str):
        return attachments.download(name)

    return app
