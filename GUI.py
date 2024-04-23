mport tkinter as tk
from tkinter import ttk
import math
from matplotlib import pyplot
import numpy as np
import data_access_and_class_instantiation as daci
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import datetime
        
params = "Default"

def sort(param, minMax, sort):
    names = ["Luminosity","Apparent Size","Temperature", "Color Index","Distance","X","Y","Z"]
    modes = ['lum','app_size','temperature','ci','distance','x','y','z']
    changeParams(param,minMax,sort)
    lambda:updateFlag(False)
    if(sort == "HeapSort"):
        start_time = datetime.datetime.now()
        #heap.re_heapify(modes[names.index(param)],minMax)
        heap.heap_sort(modes[names.index(param)],minMax)
        end_time = datetime.datetime.now()
        changeTime(end_time - start_time)


        
        
    else:
        start_time = datetime.datetime.now()
        heap._quick_sort(modes[names.index(param)],minMax)
        end_time = datetime.datetime.now()
        changeTime(end_time - start_time)
        

    

    
class app(tk.Tk):

    def __init__(self,*args,**kwargs):

        
        


        tk.Tk.__init__(self,*args,**kwargs)
        self.tk.call('source','Forest-ttk-theme-master/forest-dark.tcl')
        ttk.Style().theme_use('forest-dark')
        main = tk.Frame(self,width = 1000, height = 650)
        main.pack_propagate(0)
        main.pack(fill="both", expand="true")
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=1)
        

        self.frames = {}
        pages = (startWindow,starWindow)
        for F in pages:
            frame = F(main, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            

        self.show_frame(startWindow)
        

    def show_frame(self,name):
        frame = self.frames[name]
            
        
        frame.tkraise()


class GUI(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.mainFrame = tk.Frame(self,width = 1000, height = 650)
        self.mainFrame.pack_propagate(0)
        self.mainFrame.pack(fill="both", expand="true")
        self.mainFrame.rowconfigure( 0, weight=1)
        self.mainFrame.columnconfigure(0,weight=0)
        self.mainFrame.columnconfigure(1, weight = 1)

class startWindow(GUI):
    def __init__(self,parent,controller):
        GUI.__init__(self,parent)
        
        selectFrame = tk.Frame(self.mainFrame,width = 300, height=600)
        selectFrame.pack_propagate(0)
        selectFrame.grid(column=0,row=0,sticky=("sewn"), padx=5, pady=5)


        data_frame = tk.Frame(self.mainFrame,width = 600, height=600,padx = 0)
        data_frame.pack_propagate(0)
        data_frame.grid(column=1,row=0,sticky= "sewn", padx = (0,5), pady=5)

        # Table declaration
        datasheet = ttk.Treeview(data_frame)
        star_features = ["id", "id type","Proper name","Luminosity","X","Y","Z","Distance","Apparent Size","Color Index","Temperature"]
        datasheet['columns'] = star_features
        datasheet["show"] = "headings"  # removes empty column
        for column in star_features:
            datasheet.heading(column, text=column)
            datasheet.column(column, width=150,minwidth=150)

        datasheet.place(relheight=0.98,relwidth=0.98)

        # Scrollers
        treescrollX = tk.Scrollbar(data_frame)
        treescrollX.configure(command=datasheet.yview)
        datasheet.configure(yscrollcommand=treescrollX.set)
        treescrollX.place(relx=0.98,relheight=0.979,relwidth=0.02)
        treescrollY = tk.Scrollbar(data_frame, orient= "horizontal")
        treescrollY.configure(command=datasheet.xview)
        datasheet.configure(xscrollcommand=treescrollY.set)
        treescrollY.place(rely=0.98, relheight=0.02,relwidth=0.979)
        timeString = tk.StringVar()
        def loadData():
            for i in datasheet.get_children():
                datasheet.delete(i)
            for i in range(1,len(heap.heap)):
                datasheet.insert("","end",values=[heap.heap[i].id,heap.heap[i].id_type,heap.heap[i].proper_name,heap.heap[i].luminosity,heap.heap[i].x0,heap.heap[i].y0,heap.heap[i].z0,heap.heap[i].distance,heap.heap[i].app_size,heap.heap[i].ci,heap.heap[i].temperature])
                timeString.set("Last sort time: " + lastTime)

        # Data insertion
        loadData()
        # Left side controls

        controlPanel = ttk.Frame(selectFrame,style='Card',height=500, width=250)
        controlPanel.grid(column=0,row=0,sticky="news")
        

        text1 = tk.Label(controlPanel, text="Sort by:")
        text1.grid(column=0,row=0,sticky='w',pady=[20,0],padx=[20,5])
        text2 = tk.Label(controlPanel,text="Extrema:")
        text2.grid(column=0,row=1,sticky='w',pady=[20,0],padx=[20,5])
        text3 = tk.Label(controlPanel, text="Sorting algorithm:")
        text3.grid(column=0,row=2, rowspan=2 ,sticky='nw',pady=[20,0],padx=[10,5])


        sortingParameter= tk.StringVar()
        sortingParameter.set("Sorting parameter")
        sortSelection = ttk.OptionMenu(controlPanel,sortingParameter,"Sorting parameter","Luminosity","Distance","Apparent Size","Temperature", "Color Index","X","Y","Z")
        sortSelection.grid(column=1,row=0,sticky = 'w',pady=[20,0],padx=[0,20])

        sortingComparison = tk.StringVar()
        sortingComparison .set("~")
        sortSelection2 = ttk.OptionMenu(controlPanel,sortingComparison ,"~","min","max")
        sortSelection2.place(y=55, relx= 0.29)
        sortSelection2.grid(column=1,row=1,sticky = 'w',pady=[20,0],padx=[0,20])

        sortSelection3 = tk.StringVar(controlPanel)
        sortSelection3.set("QuickSort")
        ttk.Radiobutton(controlPanel,text="QuickSort", variable=sortSelection3, value="QuickSort", command="printResults",style='Switch').grid(column=1,row=2,sticky="ws",pady=[20,0],padx=[0,20])
        ttk.Radiobutton(controlPanel,text="HeapSort", variable=sortSelection3, value="HeapSort", command="printResults",style='Switch').grid(column=1,row=3,sticky="wn",pady=[10,20],padx=[0,20])


        
        
        visualizeButton = ttk.Button(selectFrame, text= "Visualize", style = "Accent.TButton", command=lambda:parent.master.show_frame(starWindow))
        visualizeButton.grid(column=0,row=5,pady=[10,0])
        sortButton = ttk.Button(selectFrame, text= "Sort", style="Accent.TButton", command= lambda:[sort(sortingParameter.get(),sortingComparison.get(),sortSelection3.get()),loadData()])
        sortButton.grid(column=0,row=4,pady=[200,0])
        exitButton = ttk.Button(selectFrame, command=self.quit, text = "Exit")
        exitButton.place(relwidth=0.3,relx=0.7,rely=0.95)


        timeDisplay = tk.Label(selectFrame, textvariable=timeString)
        timeDisplay.grid(column = 0, row = 6, pady=[10,0])

    
            

        

class starWindow(GUI):
    
    def __init__(self,parent,controller):
        GUI.__init__(self,parent)
        selectFrame = ttk.Frame(self.mainFrame,width = 250, height=650)
        selectFrame.grid(column=0,row=0,sticky=("sewn"), padx=(0,5), pady=5)
        selectFrame.pack_propagate(0)

        graphFrame = ttk.Frame(self.mainFrame,width = 1000, height = 650)
        graphFrame.grid(column=1,row=0,sticky= "sewn", padx = (0,5), pady=5)

        infoPanel = ttk.Frame(selectFrame,width=222,height=325,style="Card")
        infoPanel.pack_propagate(0)
        infoPanel.grid(column=0,row=0,sticky="swen",padx=5,pady=(0,5))

        infoVar = tk.StringVar(value=params)
        infoText = tk.Label(infoPanel,textvariable=infoVar)
        infoText.place(rely= 0.1, relx= 0.2, relwidth=0.6)

        def updateParams():
            infoVar.set(params)
            lambda:updateFlag(True)

        controlPanel = ttk.Frame(selectFrame,width = 222,height=325,style='Card')
        controlPanel.pack_propagate(0)
        controlPanel.grid(column=0,row=1,sticky="sewn", padx=5,pady=0)

        figure = Figure(figsize=(10,5),facecolor="black")
        canvas = FigureCanvasTkAgg(figure, master=graphFrame)
        self.plot(figure,canvas)
        

        updateVar = tk.StringVar(value="Click to update!")
        def refreshUpdate():
            
            if (updateFlag == True):
                updateVar.set("Up to date!")
            else:
                updateVar.set("Click to update!")
            lambda:updateFlag(True)

        saveButton = ttk.Button(controlPanel, text = "Save Image", style = "Accent.TButton", command= saveFig(figure))
        saveButton.place(relx=0.275, rely = 0.2,relwidth=0.45)
        updateButton = ttk.Button(controlPanel, textvariable=updateVar, style = "Accent.TButton", command=lambda:[self.plot(figure,canvas),updateParams(),refreshUpdate])
        updateButton.place(relx=0.275, rely = 0.4,relwidth=0.45)
        visualizeButton = ttk.Button(controlPanel, text= "Go back", style = "Accent.TButton", command=lambda:[parent.master.show_frame(startWindow)])
        visualizeButton.place(relx=0.275, rely = 0.6,relwidth=0.45)

        

        exitButton = ttk.Button(controlPanel, command=self.quit, text = "Exit")
        exitButton.place(relx=0.60, rely = 0.85,relwidth=0.3)
        
        
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, graphFrame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def getParams(self):
        return params

    def makePlotX(self):
        rVal = []
        for i in range(1,500):
            rVal.append(heap.heap[i].phi * 180/math.pi)
        return rVal

    def makePlotY(self):
        rVal = []
        for i in range(1,500):
            rVal.append(heap.heap[i].theta * 180/math.pi)
        return rVal
        
    def makePlotS(self):
        rVal = []
        for i in range(1,500):
            rVal.append(-heap.heap[i].app_size)
        rVal =(rVal -np.min(rVal))**2
        return rVal 
        
    def makePlotC(self):
        rVal = []
        for i in range(1,500):
            if(heap.heap[i].ci >= 1.4):
              rVal.append("red")     
            elif(heap.heap[i].ci >= 0.8 and heap.heap[i].ci < 1.4):
                rVal.append("orange")
                    
            elif(heap.heap[i].ci >= 0.4 and heap.heap[i].ci < 0.8):
               rVal.append("yellow")

            elif(heap.heap[i].ci >= 0 and heap.heap[i].ci < 0.4):
                rVal.append("white")

            elif(heap.heap[i].ci < 0 and heap.heap[i].ci>=-0.4):
                rVal.append("cyan")
            else:
                rVal.append("pink")
                
        return rVal
            
    def plot(self,figure,canvas):
            
            
            X = self.makePlotX()
            Y = self.makePlotY()
            S = self.makePlotS()
            C = self.makePlotC()
            plot1 = figure.add_subplot().scatter(X,Y,S,c=C)
            ax = plot1.axes
            ax.set_xlabel("φ (longitude)")
            ax.set_ylabel("θ (latitude)")
            ax.set_facecolor("black")
            ax.xaxis.set_units("degrees")
            ax.xaxis.label.set_color("white")
            ax.tick_params(color = "white", labelcolor="white")
            ax.spines["bottom"].set_color("white")
            ax.spines["top"].set_color("white")
            ax.spines["right"].set_color("white")
            ax.spines["left"].set_color("white")
            ax.yaxis.set_units("degrees")
            ax.yaxis.label.set_color("white")
            ax.set_xlim(-180,180)
            ax.set_ylim(-90,90)
            ax.grid(True)
            canvas.draw()

        
    
        

lastTime = ""
updateFlag = True
heap = daci.create_star_data_heap("lum") 

def updateFlag(bool):
    global updateFlag
    updateFlag = bool

def changeTime(time):
    global lastTime
    lastTime = str(time)
def saveFig(figure):
    figure.savefig("figure.png", dpi = 1000)
def changeParams(param,minMax,sort):
    global params
    params = "Parameter: " + param + "\nType of sort: " + sort + "\nExtrema: " + minMax

root = app()
root.title('Star Gator')




root.mainloop()


        





root = app()

root.mainloop()
