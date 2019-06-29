import unittest

from pool import Pool, CreatureSource, CreatureMutator, CreatureEvaluator


class MockSource(CreatureSource[int]):

    def get_random(self) -> int:
        return 0


class MockMutator(CreatureMutator[int]):

    def mutate(self, creature: int) -> int:
        return creature + 1


class MockEvaluator(CreatureEvaluator[int]):

    def evaluate(self, creature: int) -> float:
        return float(creature)


class TestPool(unittest.TestCase):

    def setUp(self):
        self.pool: Pool[int] = None

    def test_pool_size_doesnt_change_after_next_generation(self):
        self._given_pool()

        self._when_next_generation_is_created(kill_ratio=0.5)

        self._then_creature_count_equals_pool_size()

    def test_at_least_one_creature_is_killed(self):
        self._given_pool()

        self._when_next_generation_is_created(kill_ratio=0.01)

        self._then_creature_kill_count_is(1)

    def test_at_least_one_creature_is_left_alive(self):
        self._given_pool_of_size(10)

        self._when_next_generation_is_created(kill_ratio=0.99)

        self._then_creature_kill_count_is(9)

    def _given_pool_of_size(self, size: int):
        self.pool: Pool[int] = Pool(
            source=MockSource(),
            mutator=MockMutator(),
            evaluator=MockEvaluator(),
            size=size,
        )

    def _given_pool(self):
        self._given_pool_of_size(size=8)

    def _when_next_generation_is_created(self, kill_ratio):
        self.pool.next_generation(kill_ratio)

    def _then_creature_count_equals_pool_size(self):
        self.assertEqual(len(self.pool.all_creatures()), self.pool.size)

    def _then_creature_kill_count_is(self, count: int):
        new_creature_count = len(list(filter(
            lambda c: c != 0,
            self.pool.all_creatures()))
        )
        self.assertEqual(new_creature_count, count)


if __name__ == '__main__':
    unittest.main()
