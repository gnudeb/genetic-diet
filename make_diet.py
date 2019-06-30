from argparse import ArgumentParser

from pool import Pool
from diet import DietSource, DietMutator, DietEvaluator, items_from_csv, \
    print_diet


def construct_parser() -> ArgumentParser:
    parser = ArgumentParser()

    parser.add_argument(
        "-k", "--target-calories",
        type=int,
        default=2000,
        help=(
            "desired amount of kilocalories in a diet "
            "(default is %(default)d)"
        ),
    )
    parser.add_argument(
        "-c", "--target-cost",
        type=int,
        default=100,
        help="desired total cost of a diet (default is %(default)d)"
    )
    parser.add_argument(
        "-p", "--population",
        type=int,
        default=8,
        help="number of diets in each generation (default is %(default)d)"
    )
    parser.add_argument(
        "-g", "--generations",
        type=int,
        default=100,
        help=(
            "number of generations on which selection will occur "
            "(default is %(default)d)"
        )
    )
    parser.add_argument(
        "csv_path",
        type=str,
        help="path to CSV file with food items (name, kcal, cost)",
    )

    return parser


if __name__ == '__main__':
    args = construct_parser().parse_args()

    pool = Pool(
        source=DietSource(),
        mutator=DietMutator(
            food_items=items_from_csv(args.csv_path),
            mutation_rate=0.3
        ),
        evaluator=DietEvaluator(
            target_total_kcal=args.target_calories,
            target_cost=args.target_cost,
        ),
        size=args.population,
    )

    for _ in range(args.generations):
        pool.next_generation()

    best_diet = pool.best_creature()
    print_diet(best_diet)
