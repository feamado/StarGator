import tkinter as tk
from tkinter import ttk


    
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
        

    def show_frame(self, name):
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
        star_features = ["Luminosity", "Size", "Temperature", "Distance", "test1", "test2","test3","test4","test5","test6","test7"]
        datasheet['columns'] = star_features
        datasheet["show"] = "headings"  # removes empty column
        for column in star_features:
            datasheet.heading(column, text=column)
            datasheet.column(column, width=100,minwidth=100)

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

        # Data insertion
        for i in range(1000):
            datasheet.insert("","end",values=["miau" + str(i),"mua","aefkn","f","test1","2","3","4","5","6","7"])

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
        sortSelection = ttk.OptionMenu(controlPanel,sortingParameter,"Luminosity","a","f","g")
        sortSelection.grid(column=1,row=0,sticky = 'w',pady=[20,0],padx=[0,20])

        sortingComparison = tk.StringVar()
        sortingComparison .set("~")
        sortSelection2 = ttk.OptionMenu(controlPanel,sortingComparison ,"min","max")
        sortSelection2.place(y=55, relx= 0.29)
        sortSelection2.grid(column=1,row=1,sticky = 'w',pady=[20,0],padx=[0,20])

        sortSelection3 = tk.StringVar(controlPanel)
        sortSelection3.set("QuickSort")
        ttk.Radiobutton(controlPanel,text="QuickSort", variable=sortSelection3, value="QuickSort", command="printResults",style='Switch').grid(column=1,row=2,sticky="ws",pady=[20,0],padx=[0,20])
        ttk.Radiobutton(controlPanel,text="HeapSort", variable=sortSelection3, value="HeapSort", command="printResults",style='Switch').grid(column=1,row=3,sticky="wn",pady=[10,20],padx=[0,20])


        
        
        visualizeButton = ttk.Button(selectFrame, text= "Visualize", style = "Accent.TButton", command=lambda:parent.master.show_frame(starWindow))
        visualizeButton.grid(column=0,row=5,pady=[200,0])

        exitButton = ttk.Button(selectFrame, command=self.quit, text = "Exit")
        exitButton.grid(column=0,row=8)
        

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

        controlPanel = ttk.Frame(selectFrame,width = 222,height=325,style='Card')
        controlPanel.pack_propagate(0)
        controlPanel.grid(column=0,row=1,sticky="sewn", padx=5,pady=0)

        printButton = ttk.Button(selectFrame, text= "Print Image", style= "Accent.TButton")

        visualizeButton = ttk.Button(controlPanel, text= "Go back", style = "Accent.TButton", command=lambda:parent.master.show_frame(startWindow))
        visualizeButton.place(relx=0.325, rely = 0.7,relwidth=0.35)

        exitButton = ttk.Button(controlPanel, command=self.quit, text = "Exit")
        exitButton.place(relx=0.325, rely = 0.8,relwidth=0.35)


        





root = app()

root.mainloop()
