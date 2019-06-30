# Genetic diet

Put your favorite food in, get a random diet each time.

## Output example

```
$ python make_diet.py -k 2000 -c 100 sample_items.csv
2 Cooked rice = 200 kcal, $8
5 Boiled egg = 500 kcal, $10
3 Cake = 900 kcal, $30
3 Ice cream = 390 kcal, $9

Total kcalories: 1990
Total cost: 57
```

## How to use:

```
usage: make_diet.py [-h] [-k TARGET_CALORIES] [-c TARGET_COST] [-p POPULATION]
              [-g GENERATIONS]
              csv_path

positional arguments:
  csv_path              path to CSV file with food items (name, kcal, cost)

optional arguments:
  -h, --help            show this help message and exit
  -k TARGET_CALORIES, --target-calories TARGET_CALORIES
                        desired amount of kilocalories in a diet (default is
                        2000)
  -c TARGET_COST, --target-cost TARGET_COST
                        desired total cost of a diet (default is 100)
  -p POPULATION, --population POPULATION
                        number of diets in each generation (default is 8)
  -g GENERATIONS, --generations GENERATIONS
                        number of generations on which selection will occur
                        (default is 100)
```
