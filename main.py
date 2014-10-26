import csv

data_csv = []
data_csv_vektor = []
hash_row = {}
hash_column = {}
hash_matrix = {}
heur_row = {}
heur_column = {}
heur_matrix = {}

class Node():
    def __init__(self, data, row_indx):
        self.data = data        
        self.index_matr = None
        self.index_row = row_indx
        self.index_col = None
        self.heuris = None 

def separate_row(row, index_row):
    
    arr_symb = [] 
    arr_nodes = []
        
    # calculate heuris_row for each node 
    heuris_row = 0   
    n = None
    y = 0
    for symbol in row:
        try:
            sym = int(symbol) 
            arr_symb.append(sym)
            # create new node
            n = Node(sym, index_row)
            y +=1
            arr_nodes.append(n)
            data_csv_vektor.append(n)
            if not sym == 0: heuris_row += 1 
        except:
            return False
    
    hash_row[index_row] = arr_symb
    heur_row[index_row] = heuris_row     
    
    data_csv.append(arr_nodes)
                 
    return True          

def get_data(csv_path):
    result = True
    del data_csv[:]
    if not csv_path == "":
        with open(csv_path, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            ind = 0
            for row in csv_reader:
                if len(row) == 0: continue
                if not separate_row(row, ind):
                    result = False                
                ind += 1          
    return result

def save_data(path_file):    
    with open(path_file, 'w+') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_NONE, escapechar=' ', quotechar='')
        for i in range(9):
            newStr = []
            for j in range(9):
                newStr.append(str(data_csv[i][j].data) if len(newStr) == 0 else (','+str(data_csv[i][j].data)))
                
            csv_writer.writerow(newStr)
            
def get_nodeFromRange(matr_index, i, j):
    
    arr = []
    heuris_matr = 0
    if i == 2 and j == 2: #first
        i1 = 0
        j1 = 0
    elif i == 2 and j == 5:
        i1 = 0
        j1 = 3
    elif i == 2 and j == 8:
        i1 = 0
        j1 = 6  
    elif i == 5 and j == 2: #second
        i1 = 3
        j1 = 0
    elif i == 5 and j == 5:
        i1 = 3
        j1 = 3
    elif i == 5 and j == 8:
        i1 = 3
        j1 = 6 
    elif i == 8 and j == 2: #third
        i1 = 6
        j1 = 0
    elif i == 8 and j == 5:
        i1 = 6
        j1 = 3
    elif i == 8 and j == 8:
        i1 = 6
        j1 = 6          
    
    
    for x in range(i1, (i+1)):
        for y in range(j1, (j+1)):
            n = data_csv[x][y]
            n.index_matr = matr_index 
            arr.append(n)            
            if not n.data == 0: heuris_matr += 1
            
    hash_matrix[matr_index] = arr 
    heur_matrix[matr_index] = heuris_matr 

def set_columns():    
    
    matr_index = 0
    for i in range(9):
        
        heuris_col = 0
        arr_column = []        
        for j in range(9):
            
            n = data_csv[j][i] 
            arr_column.append(n.data)
            n.index_col = i
            if not n.data == 0: heuris_col += 1    
            
            if ((i+1)%3 == 0) and ((j+1)%3 == 0):                
                get_nodeFromRange(matr_index, i ,j)
                matr_index +=1
                
        hash_column[i] = arr_column
        heur_column[i] = heuris_col   

def set_heuris():
    for i in range(9):
        for j in range(9):
            n = data_csv[i][j]
            n.heuris = heur_row[n.index_row] + heur_column[n.index_col] + heur_matrix[n.index_matr]            

def check_index(i, arr):
    
    indx = -1
    try:
        indx =  arr.index(i)
    except ValueError:
        indx = -1
        
    return False if indx == -1 else True    

def check_obj_in_arr(i, arr):
    result = [a for a in arr if a.data == i]
    return False if len(result) == 0 else True    

def is_possible(x, node):
    
    colArr = hash_column[node.index_col]
    rowArr = hash_row[node.index_row]
    matrArr = hash_matrix[node.index_matr]
    
    if check_index(x, colArr) or check_index(x, rowArr) or check_obj_in_arr(x, matrArr):
        return False
    else:
        return True 

def find_resolving():
    
    data_csv_vektor.sort(cmp=None, key=lambda Node: Node.heuris, reverse=True)    
    
    not_poss = 0
    for item in data_csv_vektor:
        if item.data == 0:
            for x in range(1,10):
                poss = is_possible(x, item)
                if poss:
                    
                    item.data = x
                    
                    hash_row[item.index_row][item.index_col] = x
                    heur_row[item.index_row] = heur_row[item.index_row] + 1
                    
                    hash_column[item.index_col][item.index_row] = x
                    heur_column[item.index_col] = heur_column[item.index_col] + 1
                    
                    matr_arr = hash_matrix[item.index_matr]
                    result = [a for a in matr_arr if a.index_row == item.index_row  and a.index_col == item.index_col]
                    result[0].data = x                                   
                                     
                    heur_matrix[item.index_matr] = heur_matrix[item.index_matr]+1
                    
                    break
                                        
                else:
                    not_poss += 1 
                     
    if not_poss > 0:
        set_heuris()
        find_resolving() 
    else:
        return                     

def resolving(): 

    set_columns()
    
    set_heuris()    
    
    find_resolving()                  
                    
    
    
    
    
    
            
