import csv, nodes, random  
from way_resolving import *

data_csv = []
hash_row = {}
hash_column = {}
hash_matrix = {}
heur_row = {}
heur_column = {}
heur_matrix = {}
not_poss = [] 
 
#Download data from a file 
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
            n = nodes.Node(sym, index_row)
            y += 1
            arr_nodes.append(n)
            # data_csv_vektor.append(n)
            if not sym == 0: heuris_row += 1 
        except:
            return False
    
    hash_row[index_row] = arr_symb
    heur_row[index_row] = heuris_row     
    
    data_csv.append(arr_nodes)
                 
    return True          

#download data from a file
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

def save_data(path_file, solution):   
    with open(path_file, 'w+') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_NONE, escapechar=' ', quotechar='')
        for i in range(9):
            newStr = []
            for j in range(9):
                newStr.append(str(solution[i][j].data) if len(newStr) == 0 else (',' + str(solution[i][j].data)))
                
            csv_writer.writerow(newStr)

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
            else: not_poss.append(n)    
            
            if ((i + 1) % 3 == 0) and ((j + 1) % 3 == 0):                
                get_nodeFromRange(matr_index, i , j, data_csv, hash_matrix, heur_matrix)
                matr_index += 1
                
        hash_column[i] = arr_column
        heur_column[i] = heuris_col   

def set_heuris():
    for i in range(9):
        for j in range(9):
            n = data_csv[i][j]
            if n.data ==0 :
                fill_poss_variants(n, hash_row, hash_column, hash_matrix)
            n.heuris = heur_row[n.index_row] + heur_column[n.index_col] + heur_matrix[n.index_matr]-len(n.pos_variants)

def resolving(): 

    set_columns()    
    set_heuris()   
    
    not_poss.sort(cmp=None, key=lambda Node: Node.heuris, reverse=True)
    return start_search(True)

def start_search(reverse):
    for item in not_poss:        
        random.shuffle(item.pos_variants)
        #item.pos_variants.sort(reverse=reverse)
        for x in item.pos_variants:
            way = new_way(x, item)
            result = way.find_resolving(reverse)
            if result == True: 
                return way.data_csv                 
            way = None    
                
    start_search(not reverse)                     
    
    
    
    
    
            
