import csv
from dataclasses import dataclass, field
from random import random, choice
from typing import NamedTuple, Dict, Iterable, Iterator

from pool import CreatureSource, CreatureMutator, CreatureEvaluator


class FoodItem(NamedTuple):
    name: str
    kcal_per_serving: int
    cost_per_serving: int

    @classmethod
    def from_raw(cls, name: str, kcal: str, cost: str):
        return FoodItem(name, int(kcal), int(cost))


@dataclass
class Diet:
    food_items: Dict[FoodItem, int] = field(default_factory=dict)

    def __iter__(self) -> Iterator[FoodItem]:
        return iter(self.food_items.keys())

    def add(self, item: FoodItem, servings=1):
        self.food_items[item] = self.food_items.get(item, 0) + servings

    def remove(self, item: FoodItem):
        self.food_items.pop(item)

    def total_calories(self):
        total = 0
        for item, servings in self.food_items.items():
            total += item.kcal_per_serving * servings
        return total

    def total_cost(self):
        total = 0
        for item, servings in self.food_items.items():
            total += item.cost_per_serving * servings
        return total

    def is_empty(self) -> bool:
        return len(self.food_items) == 0

    def copy(self) -> 'Diet':
        new_diet = Diet()
        for food_item, servings in self.food_items.items():
            new_diet.add(food_item, servings)
        return new_diet


class DietSource(CreatureSource[Diet]):

    def get_random(self) -> Diet:
        return Diet()


def probability(p: float):
    return random() < p


class DietMutator(CreatureMutator[Diet]):

    def __init__(self, food_items: Iterable[FoodItem], mutation_rate=0.05):
        self._food_items = list(food_items)
        self._mutation_rate = mutation_rate

    def get_mutated(self, creature: Diet) -> Diet:
        new_diet = creature.copy()
        if probability(self._mutation_rate):
            self._remove_random_food_item_from(new_diet)
        if probability(self._mutation_rate):
            self._add_random_food_item_to(new_diet)
        return new_diet

    def _add_random_food_item_to(self, diet: Diet):
        diet.add(choice(self._food_items))

    def _remove_random_food_item_from(self, diet: Diet):
        if diet.is_empty():
            return

        diet.remove(choice(list(diet)))


class DietEvaluator(CreatureEvaluator[Diet]):

    def __init__(self, target_total_kcal: int, target_cost: int):
        self._target_total_kcal = target_total_kcal
        self._target_cost = target_cost

    def evaluate(self, creature: Diet) -> float:
        return (
            self._calorie_efficiency(creature)
            * self._cost_efficiency(creature)
        )

    def _calorie_efficiency(self, diet: Diet) -> float:
        calorie_difference = self._target_total_kcal - diet.total_calories()
        return self._safe_inverse(calorie_difference)

    def _cost_efficiency(self, diet: Diet) -> float:
        cost_difference = diet.total_cost() - self._target_cost
        return self._safe_inverse(max(0, cost_difference))

    @staticmethod
    def _safe_inverse(x: float) -> float:
        return 1 / (1 + abs(x))


def items_from_csv(filename: str) -> Iterable[FoodItem]:
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)

        for row_number, data in enumerate(reader, start=1):
            try:
                yield FoodItem.from_raw(*data)
            except ValueError as cause:
                raise ValueError(
                    f"Can't convert row {row_number} of '{filename}': {cause}")


def print_diet(diet: Diet):
    for food_item, servings in diet.food_items.items():
        calories = food_item.kcal_per_serving * servings
        cost = food_item.cost_per_serving * servings
        print(f"{servings} {food_item.name} = {calories} kcal, ${cost}")
    print()
    print(f"Total kcalories: {diet.total_calories()}")
    print(f"Total cost: {diet.total_cost()}")
