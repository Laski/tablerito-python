import itertools
import logging

from flask import abort

from tablerito import notifications
from tablerito.model import Board, Card, CardList
from tablerito.notifications import Notification

log = logging.getLogger(__name__)

board = Board("Curso Cloud-Native")
ids = itertools.count(1)


def seed_sample_board() -> None:
    todo = create_list("Por hacer")
    doing = create_list("Haciendo")
    done = create_list("Hecho")
    create_card(done.id, "Leer los 12 factores")
    create_card(doing.id, "Encontrar los problemas del Tablerito")
    create_card(todo.id, "Meter el Tablerito en un contenedor")
    create_card(todo.id, "Armarle un pipeline")
    log.info("Sample board loaded")


def create_list(name: str) -> CardList:
    card_list = CardList(next(ids), name)
    board.lists.append(card_list)
    return card_list


def create_card(list_id: int, title: str) -> Card:
    card = Card(next(ids), title)
    _find_list(list_id).cards.append(card)
    return card


def move_card(card_id: int, target_list_id: int) -> None:
    target = _find_list(target_list_id)
    card = find_card(card_id)
    for card_list in board.lists:
        if card in card_list.cards:
            card_list.cards.remove(card)
    target.cards.append(card)
    notifications.notify(Notification(f'La tarjeta "{card.title}" pasó a {target.name}'))


def find_card(card_id: int) -> Card:
    for card_list in board.lists:
        for card in card_list.cards:
            if card.id == card_id:
                return card
    abort(404, f"Card {card_id} not found")


def _find_list(list_id: int) -> CardList:
    for card_list in board.lists:
        if card_list.id == list_id:
            return card_list
    abort(404, f"List {list_id} not found")
