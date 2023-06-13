from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Sequence
from enum import Enum
import re


class DishCategory(Enum):
    DESSERT = "dessert"
    CHICKEN = "chicken"
    BEEF = "beef"
    VEGAN = "vegan"
    LAMB = "lamb"
    PORK = "pork"  # pork / gammon
    FISH = "fish"  # fish / plaice / cod
    UNKNOWN = "unknown"

    @property
    def emoji(self) -> str:
        match self:
            case self.CHICKEN:
                return "🐔"
            case self.BEEF:
                return "🐂"
            case self.LAMB:
                return "🐑"
            case self.PORK:
                return "🐷"
            case self.FISH:
                return "🐟"
            case self.DESSERT:
                return "🍰"
            case self.VEGAN:
                return "🥬"
            case self.UNKNOWN:
                return "❓"


@dataclass
class Dish:
    name: str
    price: float

    @property
    def category(self) -> DishCategory:
        tokens = re.sub(r"\W+", " ", self.name.lower()).split(" ")

        keywords = [
            (DishCategory.CHICKEN, ["chicken"]),
            (DishCategory.BEEF, ["beef"]),
            (DishCategory.LAMB, ["lamb"]),
            (DishCategory.PORK, ["pork", "gammon"]),
            (DishCategory.FISH, ["fish", "plaice", "cod"]),
            (DishCategory.DESSERT, ["cake", "dessert"]),
            (DishCategory.VEGAN, ["vegetable"]),
        ]

        for cat, kws in keywords:
            if any(map(lambda w: w in kws, tokens)):
                return cat

        return DishCategory.UNKNOWN

    def display(self) -> str:
        return f"{self.category.emoji} {self.name}: £{self.price}"


def display_dishes(d: Sequence[Dish]) -> str:
    return "\n".join(map(lambda d: d.display(), d))


class DataSource(ABC):
    @property
    def name(self) -> str:
        pass

    @property
    def link(self) -> Optional[str]:
        return None

    @abstractmethod
    def get_lunch(self) -> Sequence[Dish]:
        pass

    @abstractmethod
    def get_dinner(self) -> Sequence[Dish]:
        pass
