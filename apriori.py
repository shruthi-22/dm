from itertools import combinations

def association_rule_mining(frequent_pattern, all_item_set, supp_cnt_pattern):
    association_rule = {}
    for i in range(1,len(frequent_pattern)):
        temp  = list(combinations(frequent_pattern,i))
        for i in temp:
            rule_left = "".join(i)
            rule_right = "".join(set(frequent_pattern) - set(rule_left))
            association_rule[str(rule_left)+" -> "+ str(rule_right)] = round((supp_cnt_pattern / all_item_set[len(rule_left)][rule_left]),2)*100
    return association_rule  

def joinOperation(item_set1, item_set2):
    if (len(item_set1)==1 and len(item_set2)==1):

        return item_set1+item_set2
    elif(item_set1[:-1] == item_set2[:-1]):

        item_set_string = item_set1 + item_set2[-1]
        return "".join(sorted(item_set_string))
    else:
        return ""  


def itemSet(trans_db, previous_item_set, item_set_cnt, min_supp):

    if(item_set_cnt==1):
        item_set={}
        for i in trans_db:
            for j in trans_db[i]:
                if j in item_set:
                    item_set[j]+=1
                else:
                    item_set[j]=1
        temp = {}
        for i in item_set:
            if item_set[i]>=min_supp:
                temp[i] = item_set[i]            
        return temp            
    else:
        item_set = {}
        temp = list(combinations(previous_item_set.keys(), 2))
        for i in temp:
            item_set_string = joinOperation(i[0],i[1])
            if(item_set_string!=""):
                for i in trans_db:
                    if(set(item_set_string).issubset(set(trans_db[i]))):
                        item_set_string = "".join(sorted(item_set_string))
                        if item_set_string in item_set:
                            item_set[item_set_string]+=1
                        else:
                            item_set[item_set_string]=1
        temp = {}
        for i in item_set:
            if item_set[i]>=min_supp:
                temp[i] = item_set[i]            
        return temp                         



# main - get input
min_supp = int(input("Enter the minimum support : "))
n = int(input("Enter num of transactions : "))
trans_db = {}
for i in range(n):
    transaction = str(input("Enter the transaction "+ str(i+1)+ " : "))
    trans_db[i+1] = transaction.split(" ")


item_set={0,0}
all_item_set={0:0} 
frequent_item_set = {}
item_set_cnt=1   

# previous_db = {'a': 2, 'c': 3, 'd': 1, 'e': 4, 'b': 3}

while(len(item_set)!=0):
    item_set = itemSet(trans_db, all_item_set[item_set_cnt-1], item_set_cnt, min_supp)
    print("\n" + str(item_set_cnt) + " item set : \n" + str(item_set))
    if(len(item_set)>0):
        all_item_set[item_set_cnt] = item_set
        frequent_item_set  = item_set
    item_set_cnt+=1
    
print("All item set : ", str(all_item_set))       
print("The highest frequent pattern is : ", [value for value in frequent_item_set]) 


for i in frequent_item_set:
   print("assotiation rule", association_rule_mining(i,all_item_set, frequent_item_set[i]))
