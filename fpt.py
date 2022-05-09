from collections import defaultdict

def Load_data():
    return [['I1','I2','I5'],
             ['I2','I4'],
             ['I2','I3'],
             ['I1','I2','I4'],
             ['I1','I3'],
             ['I2','I3'],
             ['I1','I3'],
             ['I1','I2','I3','I5'],
             ['I1','I2','I3']]

def create_initialset(dataset):
    retDict = {}
    for trans in dataset:
        retDict[frozenset(trans)] = 1
    return retDict

class TreeNode:
    def __init__(self, Node_name,counter,parentNode):
        self.name = Node_name
        self.count = counter
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
def updateTree(itemset, FPTree, HeaderTable, count):
    if itemset[0] in FPTree.children:
        FPTree.children[itemset[0]].count+=count
    else:
        FPTree.children[itemset[0]] = TreeNode(itemset[0], count, FPTree)

        if HeaderTable[itemset[0]][1] == None:
            HeaderTable[itemset[0]][1] = FPTree.children[itemset[0]]
        else:
            update_NodeLink(HeaderTable[itemset[0]][1], FPTree.children[itemset[0]])

    if len(itemset) > 1:
        updateTree(itemset[1:], FPTree.children[itemset[0]], HeaderTable, count)

def update_NodeLink(Test_Node, Target_Node):
    while (Test_Node.nodeLink != None):
        Test_Node = Test_Node.nodeLink

    Test_Node.nodeLink = Target_Node
    
def create_FPTree(dataset, minSupport):
    HeaderTable = defaultdict(int)
    for transaction in dataset:
        for item in transaction:
            HeaderTable[item]+=dataset[transaction]
            
    for k in list(HeaderTable):
        if HeaderTable[k] < minSupport:
            del(HeaderTable[k])

    frequent_itemset = set(HeaderTable.keys())

    if len(frequent_itemset) == 0:
        return None, None

    for k in HeaderTable:
        HeaderTable[k] = [HeaderTable[k], None]

    retTree = TreeNode('Null Set',1,None)
    for itemset,count in dataset.items():
        frequent_transaction = {}
        for item in itemset:
            if item in frequent_itemset:
                frequent_transaction[item] = HeaderTable[item][0]
        if len(frequent_transaction) > 0:
            ordered_itemset = [v[0] for v in sorted(frequent_transaction.items(), key=lambda p: p[1], reverse=True)]
            updateTree(ordered_itemset, retTree, HeaderTable, count)
    return retTree, HeaderTable

def FPTree_uptransveral(leaf_Node, prefixPath):
 if leaf_Node.parent != None:
    prefixPath.append(leaf_Node.name)
    FPTree_uptransveral(leaf_Node.parent, prefixPath)

def find_prefix_path(basePat, TreeNode):
 Conditional_patterns_base = {}

 while TreeNode != None:
    prefixPath = []
    FPTree_uptransveral(TreeNode, prefixPath)
    if len(prefixPath) > 1:
        Conditional_patterns_base[frozenset(prefixPath[1:])] = TreeNode.count
    TreeNode = TreeNode.nodeLink

 return Conditional_patterns_base

def Mine_Tree(HeaderTable, minSupport, prefix, frequent_itemset):
    bigL = [v[0] for v in sorted(HeaderTable.items(),key=lambda p: p[1][0])]
    for basePat in bigL:
        new_frequentset = prefix.copy()
        new_frequentset.add(basePat)
        
        frequent_itemset.append(new_frequentset)
        Conditional_pattern_bases = find_prefix_path(basePat, HeaderTable[basePat][1])
        
        Conditional_FPTree, Conditional_header = create_FPTree(Conditional_pattern_bases,minSupport)

        if Conditional_header != None:
            Mine_Tree(Conditional_header, minSupport, new_frequentset, frequent_itemset)

initSet = create_initialset(Load_data())

min_Support_per = 0.5
min_Support=min_Support_per*len(initSet)

FPtree, HeaderTable = create_FPTree(initSet, min_Support)

frequent_itemset = []
Mine_Tree(HeaderTable, min_Support, set([]), frequent_itemset)

print("All frequent itemsets:")
print(frequent_itemset)
