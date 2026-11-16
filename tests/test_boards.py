import pytest
from werkzeug.exceptions import NotFound

from tablerito import boards


def test_starts_with_the_sample_board(app):
    assert boards.board.name == "Curso Cloud-Native"
    todo, doing, done = boards.board.lists[:3]
    assert [todo.name, doing.name, done.name] == ["Por hacer", "Haciendo", "Hecho"]
    assert [card.title for card in todo.cards] == [
        "Meter el Tablerito en un contenedor",
        "Armarle un pipeline",
    ]
    assert [card.title for card in doing.cards] == ["Encontrar los problemas del Tablerito"]
    assert [card.title for card in done.cards] == ["Leer los 12 factores"]


def test_moves_a_card_to_another_list():
    source = boards.create_list("Packing")
    target = boards.create_list("Moved")
    card = boards.create_card(source.id, "Pack the books")

    boards.move_card(card.id, target.id)

    assert source.cards == []
    assert target.cards == [card]


def test_a_card_that_does_not_exist_gives_404():
    with pytest.raises(NotFound):
        boards.find_card(999999)
