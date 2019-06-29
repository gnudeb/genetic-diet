from math import floor
from random import randrange, choice, randint
from typing import TypeVar, Generic, List


Creature = TypeVar("Creature")


class CreatureSource(Generic[Creature]):

    def get_random(self) -> Creature:
        raise NotImplementedError


class CreatureMutator(Generic[Creature]):

    def mutate(self, creature: Creature) -> Creature:
        raise NotImplementedError


class CreatureEvaluator(Generic[Creature]):

    def evaluate(self, creature: Creature) -> float:
        raise NotImplementedError


class Pool(Generic[Creature]):

    def __init__(
            self,
            source: CreatureSource,
            mutator: CreatureMutator,
            evaluator: CreatureEvaluator,
            size: int,
    ):
        self._size = size
        self._creature_source: CreatureSource = source
        self._creature_mutator: CreatureMutator = mutator
        self._creature_evaluator: CreatureEvaluator = evaluator
        self._pool: List[Creature] = []

        self._populate()

    def next_generation(self, kill_ratio=0.5):
        kill_count = max(1, floor(self._size * kill_ratio))
        self._kill_bad_creatures(kill_count)
        self._repopulate_from_remaining_creatures(kill_count)

    def best_creature(self) -> Creature:
        return self._sorted_creatures()[-1]

    def all_creatures(self) -> List[Creature]:
        return self._pool

    @property
    def size(self):
        return self._size

    def _populate(self):
        for _ in range(self._size):
            self._pool.append(self._creature_source.get_random())

    def _worst_creature(self):
        return self._sorted_creatures()[0]

    def _sorted_creatures(self):
        return sorted(
            self._pool,
            key=lambda c: self._creature_evaluator.evaluate(c)
        )

    def _kill_bad_creatures(self, amount: int):
        for _ in range(amount):
            self._kill_worst_creature()

    def _kill_worst_creature(self):
        self._pool.remove(self._worst_creature())

    def _repopulate_from_remaining_creatures(self, amount: int):
        for _ in range(amount):
            self._pool.append(self._mutated(self._random_creature()))

    def _random_creature(self):
        return choice(self._pool)

    def _mutated(self, creature: Creature) -> Creature:
        return self._creature_mutator.mutate(creature)
