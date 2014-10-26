import main, tkFileDialog, tkMessageBox
from Tkinter import *
import time
import sys

sys.setrecursionlimit(100000000)

def choosing_file():
    file = tkFileDialog.askopenfile(parent=root, filetypes = [('','*.csv')], mode='rb',title='Choose a file')
    if file != None:        
        tbPath.configure(state='normal')
        tbPath.delete(0, END)
        tbPath.insert(0, file.name)
        tbPath.configure(state='disabled')

def download_data():
    csv_path = tbPath.get()
    
    if len(csv_path) == 0: 
        tkMessageBox.showinfo('Error.','Path for a csv file is empty!')
        return
    
    result = main.get_data(csv_path)
    
    if result and len(main.data_csv) != 0:
        draw_board(50, 70)
    
        #add button for starting resolving
        btResolve = Button(root, text ='Resolve', command = start_resolving, height=1, width=80);
        btResolve.place(x=245,y=150, width = 80) 
    else:
        tkMessageBox.showinfo('Error.','Could not load data.')       

def save_data():
    file = tkFileDialog.asksaveasfile(parent=root, filetypes = [('','*.csv')], mode='w',title='Choose a file')
    if file != None:
        main.save_data(file.name)
        tkMessageBox.showinfo('Info.','Saving was success.') 

def start_resolving():
    
#     start = time.time()    
        
    main.resolving()
#     stop = time.time() 
#     
#     dimer_data.set('Time - '+str(stop-start))
    
    
    draw_board(340, 70)
    #add button for save result
    btSave = Button(root, text ='Save', command = save_data, height=1, width=80);
    btSave.place(x=245,y=190, width = 80)       

def draw_board(x_start, y_start):
    x = x_start
    y = y_start
    for i in range(9):
        x = x_start
        for j in range(9):
            n = main.data_csv[i][j]
            var = StringVar()
            if n.data == 0:
                cell = Label(root, textvariable = var, bd = 3, relief=SUNKEN)
            else:
                cell = Label(root, textvariable = var, bd = 3, relief=SUNKEN, background = 'white')
                var.set(str(n.data))           
            
            cell.pack(side=LEFT)
            cell.place(x = x,y = y, width = 20)
            x += 20
        y += 20
                             

root = Tk()

#set size of main window
root.geometry("600x600")
root.title('Sudoku')

#add label for path
var = StringVar()
lbParam = Label(root, textvariable=var)
var.set("Choose a csv file:")
lbParam.pack(side=LEFT)
lbParam.place(x=10,y=30,width=120)

#add a text box for path 
tbPath = Entry(root, bd =5, state = DISABLED)
#tbPath.configure(state = 'disabled')
tbPath.pack(side = LEFT)
tbPath.place(x=130,y=30,width=300)


#add button for choosing path
btChoose = Button(root, text ='...', command = choosing_file, height=1, width=25);
btChoose.place(x=432,y=28,width=30)

#add button for download the data from the csv file
btDownload = Button(root, text ='Download', command = download_data, height=1, width=80);
btDownload.place(x=465,y=28, width = 80)

#add label for timer
dimer_data = StringVar()
lbTimer = Label(root, textvariable=dimer_data)
lbTimer.pack(side=LEFT)
lbTimer.place(x=190,y=300,width=200)

root.mainloop()

main.resolving()    