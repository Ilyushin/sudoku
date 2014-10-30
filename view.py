import main, tkFileDialog, tkMessageBox, time, sys, way_resolving
from Tkinter import *

sys.setrecursionlimit(900000000)

def choosing_file():
    file = tkFileDialog.askopenfile(parent=root, filetypes = [('','*.csv')], mode='rb',title='Choose a file')
    if file != None:        
        tbPath.configure(state='normal')
        tbPath.delete(0, END)
        tbPath.insert(0, file.name)
        tbPath.configure(state='disabled')

def download_data():
    csv_path = tbPath.get()
    
    clear_solution = Label(root, textvariable='')
    clear_solution.place(x=420,y=80,width=300, height = 300)
    
    clear_button = Label(root, textvariable='')
    clear_button.place(x=330,y=200, width = 80, height = 100)
        
    if len(csv_path) == 0: 
        tkMessageBox.showinfo('Error.','Path for a csv file is empty!')
        return
    
    result = main.get_data(csv_path)
    
    if result and len(main.data_csv) != 0:
        
        draw_board(50, 110, main.data_csv)
    
        #add button for starting resolving
        btResolve = Button(root, text ='Resolve', command = start_resolving, height=1, width=80)
        btResolve.place(x=330,y=200, width = 80) 
    else:
        tkMessageBox.showinfo('Error.','Could not load data.')       

def save_data():
    file = tkFileDialog.asksaveasfile(parent=root, filetypes = [('','*.csv')], mode='w',title='Choose a file')
    if file != None:
        main.save_data(file.name, main.solut)
        tkMessageBox.showinfo('Info.','Saving was success.') 

def start_resolving():
    start = time.time()         
    main.solut = list(main.resolving())
    end = time.time()
    msecs = (end - start) * 1000
    timer_data.set('time: '+ str(msecs) + ' ms')
    if len(main.solut) > 0:
        draw_board(420, 110, main.solut)
        #add button for save result
        btSave = Button(root, text ='Save', command = save_data, height=1, width=80);
        btSave.place(x=330,y=240, width = 80)       

def draw_board(x_start, y_start, data_csv):
    x = x_start
    y = y_start
    for i in range(9):
        x = x_start
        for j in range(9):
            n = data_csv[i][j]
            var = StringVar()
            if n.data == 0:
                cell = Label(root, textvariable = var, bd = 3, relief=SUNKEN)
            else:
                cell = Label(root, textvariable = var, bd = 3, relief=SUNKEN, background = 'white')
                var.set(str(n.data))           
            
            cell.pack(side=LEFT)
            cell.place(x = x,y = y, width = 30, height = 30)
            x += 30
        y += 30

def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789.':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False                             

root = Tk()

#set size of main window
root.geometry("730x600")
root.title('Sudoku')

#add label for path
var = StringVar()
lbParam = Label(root, textvariable=var)
var.set("Choose a csv file:")
lbParam.pack(side=LEFT)
lbParam.place(x=10,y=30,width=120)

#add a text box for path 
tbPath = Entry(root, bd =5, state = DISABLED)
tbPath.pack(side = LEFT)
tbPath.place(x=130,y=30,width=300)

#add label for operation time
operatTime = StringVar()
lbOperTime = Label(root, textvariable=operatTime)
operatTime.set("Operation time (minute):")
lbOperTime.pack(side=LEFT)
lbOperTime.place(x=10,y=70,width=170)

#add a text box for operation time 
tbOperTime = Entry(root, bd =5)
tbOperTime.pack(side = LEFT)
tbOperTime.place(x=183,y=70,width=100)

#add button for choosing path
btChoose = Button(root, text ='...', command = choosing_file, height=1, width=25);
btChoose.place(x=432,y=28,width=30)

#add button for download the data from the csv file
btDownload = Button(root, text ='Download', command = download_data, height=1, width=80);
btDownload.place(x=465,y=28, width = 80)

#add label for timer
timer_data = StringVar()
lbTimer = Label(root, textvariable=timer_data)
lbTimer.pack(side=LEFT)
lbTimer.place(x=260,y=390,width=200)

root.mainloop()

main.resolving() 