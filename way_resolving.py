import main, random
from nodes import Node

class new_way():
#creating a new way and copying data from the main module
    def __init__(self, value, node):
        data_csv = []
        hash_row = {}
        hash_column = {}
        hash_matrix = {}
        heur_row = {}
        heur_column = {}
        heur_matrix = {}
        not_poss = [] 
        
        for i in range(9):
            arr_nodes = []
            for j in range(9):
                n = main.data_csv[i][j]                
                new_n = Node(n.data, n.index_row, n.index_matr, n.index_col, n.heuris)
                if new_n.index_col == node.index_col and new_n.index_row == node.index_row: new_n.data = value 
                arr_nodes.append(new_n)                
                if new_n.data == 0: not_poss.append(new_n)                    
            data_csv.append(arr_nodes)
         
        matr_index = 0            
        for i in range(9):
            row = main.hash_row[i]
            arr_row = [] 
            for j in range(9):
                arr_row.append(row[j])
                if ((i + 1) % 3 == 0) and ((j + 1) % 3 == 0):                
                    get_nodeFromRange(matr_index, i , j,  data_csv, hash_matrix, heur_matrix)
                    matr_index += 1
            
            hash_row[i] = arr_row      
          
        for i in range(9):
            col = main.hash_column[i]
            arr_col = [] 
            for j in range(9):
                arr_col.append(col[j])
            
            hash_column[i] = arr_col       
       
        for i in range(9):
            heur_row[i] = main.heur_row[i]
        
        for i in range(9):
            heur_column[i] = main.heur_column[i]
         
        
        for n in not_poss:
            fill_poss_variants(n, hash_row, hash_column, hash_matrix)                
         
        change_dependents(node, value, hash_row, heur_row, hash_column, heur_column, hash_matrix, heur_matrix)
            
        self.data_csv = data_csv
        self.hash_row = hash_row
        self.hash_column = hash_column
        self.hash_matrix = hash_matrix
        self.heur_row = heur_row
        self.heur_column = heur_column
        self.heur_matrix = heur_matrix
        self.not_poss = not_poss
     
    def find_resolving(self, reverse):
        self.not_poss.sort(cmp=None, key=lambda Node: Node.heuris, reverse=True)     
        col = 0    
        for n in self.not_poss:
            random.shuffle(n.pos_variants)                                
            for x in n.pos_variants:
                if is_possible(x, n, self.hash_row, self.hash_column, self.hash_matrix):
                    n.data = x                
                    change_dependents(n, x, self.hash_row, self.heur_row, self.hash_column, self.heur_column, self.hash_matrix, self.heur_matrix)
                    col += 1            
        
        for n in self.not_poss:
            if n.data == 0: return False        
         
        return True
    
#calculating heuristic value for each cell
    def set_heuris(self):
        for i in range(9):
            for j in range(9):
                n = self.data_csv[i][j]
                if n.data ==0 :
                    fill_poss_variants(n, self.hash_row, self.hash_column, self.hash_matrix)
                n.heuris = self.heur_row[n.index_row] + self.heur_column[n.index_col] + self.heur_matrix[n.index_matr]-len(n.pos_variants)  

#creating matrices 3*3, creating hash table for matrices   
#calculating heuristic value for matrices
def get_nodeFromRange(matr_index, i, j, source, ha_matrix, he_matrix):
    
    arr = []
    heuris_matr = 0
    if i == 2 and j == 2:  # first
        i1 = 0
        j1 = 0
    elif i == 2 and j == 5:
        i1 = 0
        j1 = 3
    elif i == 2 and j == 8:
        i1 = 0
        j1 = 6  
    elif i == 5 and j == 2:  # second
        i1 = 3
        j1 = 0
    elif i == 5 and j == 5:
        i1 = 3
        j1 = 3
    elif i == 5 and j == 8:
        i1 = 3
        j1 = 6 
    elif i == 8 and j == 2:  # third
        i1 = 6
        j1 = 0
    elif i == 8 and j == 5:
        i1 = 6
        j1 = 3
    elif i == 8 and j == 8:
        i1 = 6
        j1 = 6          
    
    
    for x in range(i1, (i + 1)):
        for y in range(j1, (j + 1)):
            n = source[x][y]
            n.index_matr = matr_index 
            arr.append(n)            
            if not n.data == 0: heuris_matr += 1
            
    ha_matrix[matr_index] = arr 
    he_matrix[matr_index] = heuris_matr

#filling possible variants for each cell 
def fill_poss_variants(n, h_row, h_col, h_matr):
    n.pos_variants = []
    for x in range(1, 10):
        poss = is_possible(x, n, h_row, h_col, h_matr)
        if poss:
            n.pos_variants.append(x)

#adding new value into depending (a row, a column, a matrix) 
def change_dependents(node, x, ha_row, he_row, ha_col, he_col, ha_matr, he_matr):
    
    ha_row[node.index_row][node.index_col] = x
    he_row[node.index_row] = he_row[node.index_row] + 1
                    
    ha_col[node.index_col][node.index_row] = x
    he_col[node.index_col] = he_col[node.index_col] + 1
                    
    matr_arr = ha_matr[node.index_matr]
    result = [a for a in matr_arr if a.index_row == node.index_row  and a.index_col == node.index_col]
    result[0].data = x                                   
                                     
    he_matr[node.index_matr] = he_matr[node.index_matr] + 1

def del_x_from_pos_variants(x, n, arr):
    arr_colleg = [a for a in arr if a.index_matr == n.index_matr or a.index_row == n.index_row or a.index_col == n.index_col]
    for colleg in arr_colleg:
        if colleg == n: continue
        if x in colleg.pos_variants:
            colleg.pos_variants.remove(x)   

def check_obj_in_arr(i, arr):
    result = [a for a in arr if a.data == i]
    return False if len(result) == 0 else True

#checking, we can use this value for this cell
def is_possible(x, n, h_row, h_col, h_matr):
    
    colArr = h_col[n.index_col]
    rowArr = h_row[n.index_row]
    matrArr = h_matr[n.index_matr]
    
    if (x in colArr) or (x in rowArr) or check_obj_in_arr(x, matrArr):
        return False
    else:
        return True 



