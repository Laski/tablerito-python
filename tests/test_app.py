import io
from pathlib import Path

from tablerito import boards


def test_shows_the_board(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Curso Cloud-Native" in response.text


def test_creates_a_card_from_the_page(client):
    card_list = boards.create_list("From the page")

    response = client.post(f"/lists/{card_list.id}/cards", data={"title": "Try out Tablerito"})
    assert response.status_code == 302

    response = client.get("/")
    assert response.status_code == 200
    assert "Try out Tablerito" in response.text


def test_saves_and_returns_an_attachment(client):
    card_list = boards.create_list("With attachments")
    card = boards.create_card(card_list.id, "Read the contract")

    response = client.post(
        f"/cards/{card.id}/attachments",
        data={"file": (io.BytesIO(b"hello"), "contract.txt")},
    )
    assert response.status_code == 302

    name = f"{card.id}-contract.txt"
    assert card.attachments == [name]
    with client.get(f"/attachments/{name}") as response:
        assert response.status_code == 200
        assert response.data == b"hello"

    (Path("attachments") / name).unlink()


def test_a_card_or_list_that_does_not_exist_gives_404(client):
    assert client.post("/lists/999999/cards", data={"title": "Nowhere"}).status_code == 404
    card_list = boards.create_list("Existing")
    response = client.post("/cards/999999/move", data={"list_id": card_list.id})
    assert response.status_code == 404
