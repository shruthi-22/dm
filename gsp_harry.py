# GSP mining

def search_sequence_util(sequences, input_sequence):
    if len(sequences) == 0 or len(input_sequence) == 0:
        return 0
    results = []
    for i,sequence in enumerate(sequences):
        result = 0
        if input_sequence[0] in sequence:
            result += 1
            if len(sequences) > 1 and len(input_sequence) > 1:
                result += search_sequence_util(sequences[i+1:], input_sequence[1:])
        results.append(result)
    return max(results)

def search_different_subsequences(data, input_sequence):
    result = 0
    for sequence in data:
        r = search_sequence_util(sequence, input_sequence)
        if r >= len(input_sequence):
            result += 1
    return result

data, support_cnt = [
    [ ['a', 'b'], ['c'],['f','g'],['g'],['e']], 
    [ ['a','d'], ['c'], ['b'], ['a','b','e','f']], 
    [ ['a'],['b'],['f','g'],['e']], 
    [ ['b'],['f','g'] ]
], 2

unique_elements = set()
for s in data:
    for row in s:
        for element in row:
            unique_elements.add(element)
unique_elements = list(unique_elements)
unique_elements.sort()

print('\n\nFreq-1-itemset')
for element in unique_elements:
    print(f"{element} -> {search_different_subsequences(data, element)}")

print('\n\nFreq-2-itemset')
for element1 in unique_elements:
    for element2 in unique_elements:
        print(f"{element1},{element2} -> {search_different_subsequences(data, [element1, element2])}")
# print(search_different_subsequences(data,['a','a']))

print('\n\nFreq-3-itemset-within-same-subsequence')
freq_2_same_subset = {}
for element1 in unique_elements:
    for element2 in unique_elements:
        for element3 in unique_elements:
            for sequence in data:
                res = search_different_subsequences(sequence, [element1, element2, element3])
                freq_2_same_subset[f"{element1}{element2}{element3}"] = res
                if res > 0:
                    print(f"{element1},{element2},{element3} -> {res}")
