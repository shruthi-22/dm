
def get_data():
    return [[1,'<a(abc)(ac)d(cf)>'],
            [2,'<(ad)c(bc)(ae)>'],
            [3,'<(ef)(ab)(df)cb>'],
            [4,'<eg(af)cbc>']]

min_support=2

data=get_data()
database=[]

for sid,trans in data:
    eid=1
    cur,open='',False
    for c in trans[1:-1]:
        if(c=='('):
            open=True
        elif(c==')'):
            database.append([sid,eid,cur])
            cur,eid,open='',eid+1,False
        elif(open):
            cur+=c
        else:
            database.append([sid,eid,c])
            eid+=1

items=[]
for _,trans in data:
    for c in trans[1:-1]:
        if(c not in items and c not in '()'):
            items.append(c)

c1={}
for i in items:
    c1[i]=[]
    for sid,eid,trans in database:
        if(i in trans):
            c1[i].append([sid,eid])

print('Candidate for length 1')
for i in c1:
    print(i,c1[i])
    
l1={}
for i in c1:
    if(len(c1[i])>=min_support):
        l1[i]=c1[i]

print('Freq of length 1')
for i in l1:
    print(i,l1[i])

def stage_k(l_last):
    keys=list(l_last.keys())
    n=len(keys)
    
    ck={}
    for i in range(n):
        for j in range(n):
            if(i!=j and keys[i][1:]==keys[j][:-1]):
                cur_key=keys[i][0]+keys[i][1:]+keys[j][-1]
                for rowi in l_last[keys[i]]:
                    for rowj in l_last[keys[j]]:
                        if(rowi[0]==rowj[0] and rowi[2:]==rowj[1:-1] and rowi[1]<rowj[-1]):
                            if(cur_key not in ck):
                                ck[cur_key]=[]
                                
                            ck[cur_key].append(rowi+[rowj[-1]])
    lk={}
    for i in ck:
        if(len(ck[i])>=min_support):
            lk[i]=ck[i]
    
    return ck,lk

l_last=l1
for i in range(2,1000):
    print()
    
    ci,li=stage_k(l_last)
    
    print('C'+str(i))
    for itm,val in ci.items():
        print(itm,":",val)
        
    if(not li):
        break
    print()
    print('L%d' %(i))
    for itm,val in li.items():
        print(itm,":",val)
        
    print()
    l_last=li
                            
