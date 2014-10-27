class Node():
    def __init__(self, data, row_indx, index_matr = None, index_col = None, heuris = None):
        self.data = data        
        self.index_matr = index_matr
        self.index_row = row_indx
        self.index_col = index_col
        self.heuris = heuris
        self.pos_variants = [] 