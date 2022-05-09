from collections import defaultdict, Counter
from itertools import permutations
import pandas as pd

def get_count(data, input_set):
	data['items'] = [set(items) for items in data['items']]
	result = 0
	for i,row in data.iterrows():
		freq = row['items'].intersection(input_set)
		if len(freq) == len(input_set):
			result += 1
	return result

min_support, confidence = 3, 0.8
data = pd.read_csv("data.csv", names=['t_id', 'items'])
data['items'] = [entry.split(';') for entry in data['items']]

all_transaction_items = []
for item in data['items']:
    all_transaction_items.extend(item)

freq_1_itemset = Counter(all_transaction_items)
filtered_items = defaultdict(list)

for item,count in freq_1_itemset.items():
    if count >= min_support:
        filtered_items[count].append(item)

sorted_frequencies = list(filtered_items.keys())
sorted_frequencies.sort(reverse=True)

rearraged_transactions = pd.DataFrame({})
sorted_items_on_ranking = []

for frequency in sorted_frequencies:
    sorted_items_for_current_frequency = filtered_items[frequency]
    sorted_items_for_current_frequency.sort()
    for item in sorted_items_for_current_frequency:
        sorted_items_on_ranking.append(item)


for i,transaction in data.iterrows():
    rearranged_items = []
    for item_count in sorted_frequencies:
        sorted_items_for_current_frequency = filtered_items[item_count]
        sorted_items_for_current_frequency.sort()
        for item in sorted_items_for_current_frequency:
            for current_item in transaction['items']:
                if current_item == item:
                    rearranged_items.append(current_item)
    rearraged_transactions = rearraged_transactions.append({
        't_id': transaction['t_id'],
        'items': rearranged_items
    }, ignore_index=True)

print(f"Rearranged items in transaction:\n{rearraged_transactions}")

frequent_pattern_tree = {}
for i,transaction in rearraged_transactions.iterrows():
    temp = frequent_pattern_tree
    for item in transaction['items']:
        if item not in temp:
            temp[item] = {}
        temp = temp[item]
print(frequent_pattern_tree)
