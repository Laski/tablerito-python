from dataclasses import dataclass, field


@dataclass
class Card:
    id: int
    title: str
    attachments: list[str] = field(default_factory=list)


@dataclass
class CardList:
    id: int
    name: str
    cards: list[Card] = field(default_factory=list)


@dataclass
class Board:
    name: str
    lists: list[CardList] = field(default_factory=list)
