correct = 0
heap = []
data_row = []
data_row_test = []

def openFile(f,alist):              # to convert the csv into list
    temp = []
    for line in f:
        words = line.split('\n')
        temp.append(words[0:])

    for line in temp:
        for data in line:
            if data == '':
                line.remove(data)
    
    for line in temp:
        for data in line:
            words = data.split(', ')
            alist.append(words[0:])

    alist.pop(0)


def gini_index(mySet):              # find the gini index
    ex, pro = [], []
    sum = 0
    for i in mySet:
        if i not in ex:
            ex.append(i)
    
    for i in ex:
        pro.append(mySet.count(i) / len(mySet))
    
    for i in pro:
        sum += i**2
    
    return 1 - sum


def discrete(dealSet, data_column):# mySet是一个数据集, dealSet包含该数据集中需要被处理的数据项的所有编号
    totGini = []
    totCrit = []
    
    for mySet in data_column[:11]:
        gini = []
        sorted_set = []
        partSet = []
        
        for i in dealSet:
            sorted_set.append(mySet[i])
        sorted_set.sort()
        
        for i in range(len(sorted_set) - 1):
            partition = (float(sorted_set[i]) + float(sorted_set[i + 1])) / 2
            small = []
            big = [] 

            for every in dealSet:
                if float(mySet[every]) <= partition:
                    small.append(data_column[11][every])
                else:
                    big.append(data_column[11][every])
            
            pro_small = len(small) / (len(small) + len(big))
            pro_big = len(big) / (len(small) + len(big))
            gini.append(gini_index(small)*pro_small + gini_index(big)*pro_big)
            partSet.append(partition)
        
        theGini = min(gini)
        totCrit.append(partSet[gini.index(theGini)])
        totGini.append(theGini)

    column = totGini.index(min(totGini))
    value = totCrit[column]
    return column, value


def build_tree(dealSet, data_column):           # building the tree to a binary heap
    global heap
    heap = [-1] + [dealSet] + 98 * [-1]
    m = 1
    while m < 16:
        for every in range(m, m * 2): 
            cur = heap[every]
            if isinstance(cur, list):
                if len(cur) > 2:
                    cur = discrete(cur, data_column)
                    small = []
                    big = []
                    for i in dealSet:
                        small.append(i) if float(data_column[cur[0]][i]) <= cur[1] else big.append(i)
                    heap[every * 2] = small
                    heap[every * 2 + 1] = big
                    heap[every] = cur
                else: 
                    supp = []
                    for each in cur:
                        supp.append(data_column[11][each])
                    
                    if supp.count('Y') > supp.count('N'):
                        heap[every] = 'Y'
                    else:
                        heap[every] = 'N'
        m *= 2
    
    for i in range(16, 32):
        if isinstance(heap[i], list):
            supp = []
            for r in heap[i]:
                supp.append(data_column[11][r])
            
            if supp.count('Y') > supp.count('N'):
                heap[i] = 'Y'
            else:
                heap[i] = 'N'
                

def test_tree(mydata, nodeNum):# 一个列表
    global correct, heap
    tar = heap[nodeNum]
    if isinstance(tar, tuple):
        if float(mydata[tar[0]]) <= tar[1]:
            test_tree(mydata, nodeNum * 2)
        else:
            test_tree(mydata, nodeNum * 2 + 1)
    
    elif isinstance(tar, str):
        if mydata[11] == tar:
            correct += 1 
           


def main():
    train = input('Please input the path address of the training data: ')
    test = input('Please input the path address of the test data: ')
    
    openFile(open(train,'r'), data_row)
    dealSet = list(range(len(data_row)))
    for line in data_row:
        if int(line[11]) > 6:
            line[11] = 'Y'
        else:
            line[11] = 'N'

    data_column = list(zip(*data_row))    
    
    build_tree(dealSet, data_column)
   
    openFile(open(test,'r'), data_row_test)
    for i in data_row_test:
        if int(i[11]) > 6:
            i[11] = 'Y'
        else:
            i[11] = 'N'

    for every_data in data_row_test:
        test_tree(every_data, 1)

    accuracy = correct/len(data_row_test)
    print('The accuracy of the decision tree is:',accuracy)

if __name__ == "__main__":
    main()

    input()             #so the program don't close immediately after finishing the task.