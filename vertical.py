from itertools import combinations

def association_rule_mining(frequent_pattern, all_item_set, supp_cnt_pattern):
    association_rule = {}
    for i in range(1,len(frequent_pattern)):
        temp  = list(combinations(frequent_pattern,i))
        for i in temp:
            rule_left = "".join(i)
            rule_right = "".join(set(frequent_pattern) - set(rule_left))
            association_rule[str(rule_left)+" -> "+ str(rule_right)] = round((supp_cnt_pattern / len(all_item_set[len(rule_left)][rule_left])),2)*100

    return association_rule        
    

def joinOperation(item_set1, item_set2):
    if (len(item_set1)==1 and len(item_set2)==1):

        return item_set1+item_set2
    elif(item_set1[:-1] == item_set2[:-1]):

        item_set_string = item_set1 + item_set2[-1]
        return "".join(sorted(item_set_string))
    else:
        return ""   

def intersection(trans_item_set1, trans_item_set2):
    return [value for value in trans_item_set1 if value in trans_item_set2]




def itemSet ( trans_db, item_set, min_supp):
    if(item_set==1):
        item_set = {}
        for i in trans_db:
            for j in trans_db[i]:
                if j not in item_set:
                    item_set[j] = []
                item_set[j].append(i)
        temp = {}
        for i in item_set:
            if len(item_set[i])>=min_supp:
                temp[i] = item_set[i]

        item_set = dict(sorted(temp.items()))        
        return item_set
    else:
        item_set = {}
        temp = combinations(trans_db.keys(), 2)
        for i in list(temp):
            item_set_string = joinOperation(i[0],i[1])
            if(item_set_string!=""):
                intersection_trans = intersection(trans_db[i[0]], trans_db[i[1]])
                if(len(intersection_trans)>=min_supp):
                    item_set[item_set_string] = intersection_trans
        return item_set            






# main
min_supp = int(input("Enter the minimum support : "))
n = int(input("Enter num of transactions : "))
trans_db = {}
for i in range(n):
    transaction = str(input("Enter the transaction "+ str(i+1)+ " : "))
    trans_db[i+1] = transaction.split(" ")

#trans_db = {'123': [8, 9], '125': [1, 8]}

#print(oneItemSet(trans_db, 4, min_supp))
frequent_item_set = {}
all_item_set = {}
item_set = trans_db
item_set_cnt=1    
while(len(item_set)!=0):
    item_set = itemSet(item_set, item_set_cnt, min_supp)
    print("\n" + str(item_set_cnt) + " item set : \n" + str(item_set))
    if(len(item_set)>0):
        all_item_set[item_set_cnt] = item_set
        frequent_item_set  = item_set
    item_set_cnt+=1
    
print("All item set : ", str(all_item_set))       
print("The highest frequent pattern is : ", [value for value in frequent_item_set]) 

for i in frequent_item_set:
   print("assotiation rule", association_rule_mining(i,all_item_set, len(frequent_item_set[i])))
