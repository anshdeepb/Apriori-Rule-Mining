import csv as csv
import math as math
from collections import defaultdict
from itertools import combinations

def generate_item_sets(num_items, count_list):
    for item in items:
        for combination in combinations(item, num_items):
            combination = tuple(sorted(combination))
            count_list[combination] += 1

    return count_list

def generate_association_rules(all_frequent_items):

    confident_items = {}

    for key, value in all_frequent_items.items():
        items = list(key)

        for i in range(1, len(items)):
            for left_side in combinations(items, i):
                left_side = tuple(sorted(left_side))
                left_side_support = all_frequent_items.get(left_side)

                right_side = list(set(items) - set(left_side))
                right_side = tuple(right_side)

                if left_side_support is None:
                    continue

                if len(right_side) == 0:
                    continue

                support = round(value/len(data), 2)
                confidence = round(value / left_side_support, 2)

                if confidence >= min_conf:
                    confident_items[(left_side, right_side)] = (confidence, support)

    return confident_items

# reading the dataset

data = []

with open('Play_Tennis_Data_Set.csv', "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        data.append(row)

# inputs

min_sup = float(input("Enter the minimum support threshold: ")) * len(data)
min_sup = math.ceil(min_sup)
min_conf = float(input("Enter the minimum confidence threshold: "))

items = [] #stores the number of different types of items in the dataset

for row in data:
    row_items = []

    for key, value in row.items():
        row_items.append((key, value))
    items.append(row_items)

all_frequent_items = {}

# Generic to allow the use of any dataset to generate appropriate frequent item sets

num_items = 0
while num_items < len(items):
    item_counts = defaultdict(int)
    item_counts = generate_item_sets(num_items, item_counts)

    item_set = defaultdict(int)

    for col, row in item_counts.items():
        if row >= min_sup:
            item_set[col] = row

    all_frequent_items.update(item_set)
    num_items += 1

# acquiring the items selected based on confidence values and the confidence threshold

confident_items = generate_association_rules(all_frequent_items)

# formatting of the Rules into Rules.txt

with open("Rules.txt", "w") as file:
    count = 1

    for (left, right), (confidence, support) in confident_items.items():
        left_items = []
        for key, value in left:
            left_items.append(key + "=" + str(value))
        left_string = ", ".join(left_items)

        right_items = []
        for key, value in right:
            right_items.append(key + "=" + str(value))
        right_string = ", ".join(right_items)

        file.write("Rule#" + str(count) + ": {" + left_string + " => " + right_string + "}")
        file.write("\n")
        file.write("(Support:" + str(support) + ", Confidence:" + str(confidence) + ")")
        file.write("\n\n")
        count += 1