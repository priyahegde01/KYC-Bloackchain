from tkinter import *
import requests
import json
from tkinter import messagebox
import pandas as pd
from tkinter import ttk

root = Tk()
root.geometry("1200x480+700+420")
root.title("KYC -Blockchain") 

text = Text(root, width=50, height=4, wrap="word", font=("Helvetica",12), bg = "#E6E3FF")
Label(root, width=10, height=2, text="Bank:", font=("Helvetica",11), background = "#89a7d0",anchor=NE).grid(row=0, column=0,sticky="NW")
text.grid(row=0,column=1,sticky="W")
text.insert('1.0', 'ICICI')
text.focus_set()

text1 = Text(root, width=50, height=4, wrap="word", font=("Helvetica",12), bg = "#E6E6FA")
Label(root, width=10, height=2, text="Branch: ", font=("Helvetica",11), background = "#89a7d0",anchor=NE).grid(row=1, column=0,sticky="NW")
text1.grid(row=1,column=1,sticky="W")
text1.insert('1.0', 'ABC Nagar')
text1.focus_set()

text2 = Text(root, width=50, height=4, wrap="word", font=("Helvetica",12), bg = "#E6E6FA")
Label(root, width=10, height=2,text="Date: ",font=("Helvetica",11), background = "#89a7d0",anchor=NE).grid(row=2, column=0,sticky="NW")
text2.grid(row=2,column=1)
text2.insert('1.0', '15.01.2019')
text2.focus_set()

text3 = Text(root, width=50, height=4, wrap="word", font=("Helvetica",12), bg = "#E6E6FA")
Label(root, width=10, height=2, text="Account Number: ", font=("Helvetica",11), background = "#89a7d0",anchor=NE).grid(row=3, column=0,sticky="NW")
text3.grid(row=3,column=1)
text3.insert('1.0', '718237891327892')
text3.focus_set()


text4 = Text(root, width=50, height=4, wrap="word", font=("Helvetica",12), bg = "#E6E6FA")
Label(root, width=10, height=2,text="Account Holder Name:", font=("Helvetica",11), background = "#89a7d0",anchor=NE).grid(row=4, column=0,sticky="NW")
text4.grid(row=4,column=1)
text4.insert('1.0', 'Mr.Sherlock')
text4.focus_set()

text5 = Text(root, width=50, height=4, wrap="word", font=("Helvetica",12), bg = "#E6E6FA")
Label(root, width=15, height=2, text="Account Type:", font=("Helvetica",11), background = "#89a7d0",anchor=NE).grid(row=0, column=3,sticky="NE")
text5.grid(row=0,column=4)
text5.insert('1.0', 'Joint')
text5.focus_set()


text9 = Text(root, width=50, height=4, wrap="word", font=("Helvetica",12), bg = "#E6E6FA")
Label(root, width=15, height=2, text="File Path:", font=("Helvetica",11), background = "#89a7d0",anchor=NE).grid(row=2, column=3,sticky="NE")
text9.grid(row=2,column=4)
text9.insert('1.0', 'File Path')
text9.focus_set()


def add_record(node):
    bank = str(text.get("1.0", "end"))
    branch = str(text1.get("1.0", "end"))
    date = str(text2.get("1.0", "end"))
    account_number = str(text3.get("1.0", "end"))
    account_holder_name = str(text4.get("1.0", "end"))
    account_type = str(text5.get("1.0", "end"))
    file_name = str(text9.get("1.0", "end"))
    
    payload = {'bank':bank, 'file_name':file_name, 'branch': branch[:-1], 'date': date[:-1], ' account_number':  account_number[:-1], 'account_holder_name':account_holder_name[:-1],  'account_type':  account_type[:-1],  'file_name': file_name[:-1]}
    url = "http://127.0.0.1:{}/add_record".format(node)
    response = requests.post(url, json=payload)
    messagebox.showinfo("Information","Bank record has been broadcasted to the network and confirmed in block number {}.".format(getchain("http://127.0.0.1:5001/get_chain")[-1]['index']))
    mineblock("http://127.0.0.1:{}/mine_block".format(node))
    

def getchain(url):
    r = requests.get(url)
    data = r.json()
    return data['chain']

def print_chain(node):
    x = getchain("http://127.0.0.1:{}/get_chain".format(node))

    global df
    df = pd.DataFrame(data=x, columns= ["index", "previous_hash", "proof", "timestamp", "data"])
    
    df.to_csv("transaction_{}.csv".format(node), sep=',')

    toplevel = Tk()
    toplevel.geometry("1200x550+600+400")
    toplevel.title("http://127.0.0.1:{}/get_chain".format(node))
    
    
    h = Scrollbar(toplevel, orient=HORIZONTAL)
    v = Scrollbar(toplevel, orient=VERTICAL)
    w = Canvas(toplevel, scrollregion=(0, 0, 10000, 10000), bg='#FFFFFF')
    h['command'] = w.xview
    v['command'] = w.yview
    
    def on_configure(event):
    # update scrollregion after starting 'mainloop' - when all widgets are in canvas
        w.configure(scrollregion=w.bbox('all'))
    
    
    w.grid(column=0, row=0, sticky=(N,W,E,S))
    h.grid(column=0, row=1, sticky=(W,E))
    #v.grid(column=1, row=0, sticky=(N,S))
    toplevel.grid_columnconfigure(0, weight=2)
    toplevel.grid_rowconfigure(0, weight=2)
    
    f = Frame(w)
    f.grid(row=0, column=0, sticky=(N,W,E,S))
    w.create_window((0,0), window=f, anchor='nw')
    w.bind('<Configure>', on_configure)
    
    canvas_width = 500 #230
    canvas_height = 500 #100

    colours = ("pink", "yellow")
               
    box=[]
    for ratio in ( 0.95, 0.8 ):
        box.append( (canvas_width * ratio,
                canvas_height * ratio,
                canvas_width * (1 - ratio),
                canvas_height * (1 - ratio) ) )
    
    
    # The process for making block visualization
    count = 0
    canvases, rect_ID = [], []
    
    for i in range(0, 1):
    
        for j in range(0, (len(df["index"]))):
            
            # Make a new canvas
            w= Canvas(f, width=canvas_width, height=canvas_height,scrollregion=(0, 0, 1000, 1000))
            # Draw a line
            line = w.create_line(0, canvas_height/2, canvas_width, canvas_height/2, fill="#476042", width=5)
            # Draw a rectangle
            itemRect = w.create_rectangle(box[0][0], box[0][1],box[0][2],box[0][3], fill=colours[0], tags=("{}".format(count)))
            # Write block text
            text = w.create_text(canvas_width / 2, canvas_height / 2, text="Block {} \n \n TimeStamp \n {}".format((df["index"][j]-1), df["timestamp"][j]), fill="black",font=("Helvetica",14))
            
            # Draw and show all canvas objects and canvas
            w.grid(row=i, column=j,sticky="news")
            
            # Append values needed for click identification
            rect_ID.append(w.gettags(2)[0])
            canvases.append(w)
            
            # Count to keep track of the tag values
            count += 1
            
    

    def key(event):
        print ("pressed", repr(event.char))
        
    def callback(event):
        clicked_at = event.widget.gettags(2)[0]
        print ("Retrieve information from Block {}". format(clicked_at))
        #print (df.iloc[:int(clicked_at)+1])
        
        toplevel = Tk()
        toplevel.geometry("1200x550+600+400")
        toplevel.title("Data")
        
        
        h = Scrollbar(toplevel, orient=HORIZONTAL)
        v = Scrollbar(toplevel, orient=VERTICAL)
        w1 = Canvas(toplevel, scrollregion=(0, 0, 10000, 10000), bg='#FFFFFF')
        h['command'] = w1.xview
        v['command'] = w1.yview
        
        def on_configure(event):
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
            w1.configure(scrollregion=w.bbox('all'))

        w1.grid(column=0, row=0, sticky=(N,W,E,S))
        #h.grid(column=0, row=1, sticky=(W,E))
        v.grid(column=1, row=0, sticky=(N,S))
        toplevel.grid_columnconfigure(0, weight=2)
        toplevel.grid_rowconfigure(0, weight=2)
        
        f = Frame(w1)
        f.grid(row=0, column=0, sticky=(N,W,E,S))
        w1.create_window((0,0), window=f, anchor='nw')
        w1.bind('<Configure>', on_configure)
        
    
        w2= Canvas(f, width=canvas_width, height=canvas_height,scrollregion=(0, 0, 1000, 1000))
        w2.grid(row=0, column=0,sticky="news")
        
        txt = Text(w2, width=10, height=2, wrap="word", font=("Helvetica",8), bg = "#E6E6FA")
        txt.insert('1.0', "Block")
        txt.grid(row=0,column=0)
        
        txt = Text(w2, width=20, height=2, wrap="word", font=("Helvetica",8), bg = "#E6E6FA")
        txt.insert('1.0', df.columns.values[3])
        txt.grid(row=0,column=1)
        
        txt = Text(w2, width=150, height=2, wrap="word", font=("Helvetica",8), bg = "#E6E6FA")
        txt.insert('1.0', df.columns.values[4])
        txt.grid(row=0,column=2)
        
        txt = Text(w2, width=10, height=2, wrap="word", font=("Helvetica",8), bg = "#E6E6FA")
        txt.insert('1.0', df.columns.values[2])
        txt.grid(row=0,column=3)
    
        txt = Text(w2, width=70, height=2, wrap="word", font=("Helvetica",8), bg = "#E6E6FA")
        txt.insert('1.0', df.columns.values[1])
        txt.grid(row=0,column=4)
        


        for i in range(0, int(clicked_at)+1):
            x = df["previous_hash"][i]
            y = df["timestamp"][i]
            z = df["data"][i]
            proof = df["proof"][i]
            block = int(clicked_at)
            

            txt = Text(w2, width=10, height=2, wrap="word", font=("Helvetica",8), bg = "#E6E6FA")
            txt.insert('1.0', i)
            txt.grid(row=i+1,column=0)
            
            txt = Text(w2, width=20, height=2, wrap="word", font=("Helvetica",8), bg = "#E6E6FA")
            txt.insert('1.0', y)
            txt.grid(row=i+1,column=1)
            
            txt = Text(w2, width=150, height=2, wrap="word", font=("Helvetica",8), bg = "#E6E6FA")
            txt.insert('1.0', z)
            txt.grid(row=i+1,column=2)
            
            txt = Text(w2, width=10, height=2, wrap="word", font=("Helvetica",8), bg = "#E6E6FA")
            txt.insert('1.0', proof)
            txt.grid(row=i+1,column=3)
            
            txt = Text(w2, width=70, height=2, wrap="word", font=("Helvetica",8), bg = "#E6E6FA")
            txt.insert('1.0', x)
            txt.grid(row=i+1,column=4)
        
    data = []
    for index, row in df.iterrows():
        data.append(row['data'])
    print (df)    
    #print ((data[1][0]))
    
    # binding canvas tags 
    for i in canvases:
        # Binding tags to key events
        i.bind("<Key>", key)
        i.bind("<Button-1>", callback)

    toplevel.resizable(width=True, height=True)
    toplevel.mainloop()

   
def mineblock(url):
    r = requests.get(url)
    connect_nodes()
    replace_chains()


def connect_nodes():
    
    def add_5001():
        payload = {"nodes": ["http://127.0.0.1:5001","http://127.0.0.1:5002", "http://127.0.0.1:5003"]}
        url = "http://127.0.0.1:5001/connect_node"
        node = "http://127.0.0.1:5001"
        for i in payload['nodes']:
            if i == node:
                payload["nodes"].remove(i)
                response = requests.post(url, json=payload)
                #print ("Nodes {} are added to current node {}".format(payload['nodes'], node))
    
    def add_5002():
        payload = {"nodes": ["http://127.0.0.1:5001","http://127.0.0.1:5002", "http://127.0.0.1:5003"]}
        url = "http://127.0.0.1:5002/connect_node"
        node = "http://127.0.0.1:5002"
        for i in payload['nodes']:
            if i == node:
                payload["nodes"].remove(i)
                response = requests.post(url, json=payload)
                #print ("Nodes {} are added to {}".format(payload['nodes'], node))
    
    def add_5003():
        payload = {"nodes": ["http://127.0.0.1:5001","http://127.0.0.1:5002", "http://127.0.0.1:5003"]}
        url = "http://127.0.0.1:5003/connect_node"
        node = "http://127.0.0.1:5003"
        for i in payload['nodes']:
            if i == node:
                payload["nodes"].remove(i)
                response = requests.post(url, json=payload)
                #print ("Nodes {} are added to {}".format(payload['nodes'], node))
    
    add_5001(), add_5002(), add_5003()
    #print ("All nodes have been connected to each other")
    messagebox.showinfo("Information","All nodes have been connected to each other.")


def replace_chains():
    def replace_chain_5001():
        url = "http://127.0.0.1:5001/replace_chain"
        r = requests.get(url)
    
    def replace_chain_5002():
        url = "http://127.0.0.1:5002/replace_chain"
        r = requests.get(url)
            
    def replace_chain_5003():
        url = "http://127.0.0.1:5003/replace_chain"
        r = requests.get(url)
    
    replace_chain_5001(),replace_chain_5002(),replace_chain_5003()
    #print ("All nodes have been update to the latest Report")
    messagebox.showinfo("Information","All nodes have been update to the latest Report.")

def isValid():
    url = ["http://127.0.0.1:5001/is_valid", "http://127.0.0.1:5002/is_valid", "http://127.0.0.1:5003/is_valid"]
    company = ["Bank 1", "Bank 2", "Bank 3"]
    count = 0
    for i in url:
        r = requests.get(i)
        r = json.loads(r.text)
        if r['Message'] == "Valid Chain. All blocks are valid.":
            messagebox.showinfo("Information","Blockchain at {} is found to be a valid.".format(company[count]))
        else:
            messagebox.showerror("Information","Blockchain at {} is found to be NOT valid.".format(company[count]))
        count +=1
            
# Buttons functions for nodes           
def chain_print_5001():
    print_chain(5001)
def chain_print_5002():
    print_chain(5002)
def chain_print_5003():
    print_chain(5003)


# Post to server
def post_from_5001():
    add_record(5001)
    print ("Posted to network from Bank 1")
def post_from_5002():
    add_record(5002)
    print ("Posted to network from Bank 2")
def post_from_5003():
    add_record(5003)
    print ("Posted to network from Bank 3")

bg, bg1 = "#d08935", "#8995d0"
b1 = Button(root, text="Report from Bank 1", font=("Helvetica",11,"bold"),  command=post_from_5001,  bg=bg, fg="#000000")
b1.grid(row=7,column=1, sticky=W)    

b1 = Button(root, text="Report from Bank 2", font=("Helvetica",11,"bold"),  command=post_from_5002,  bg=bg, fg="#000000")
b1.grid(row=8,column=1, sticky=W)  

b1 = Button(root, text="Report from Bank 3", font=("Helvetica",11,"bold"),  command=post_from_5003,  bg=bg, fg="#000000")
b1.grid(row=9,column=1, sticky=W)  
    
b2 = Button(root, text="Check Network Sync", font=("Helvetica",11,"bold"),  command=isValid,  bg=bg1, fg="#000000")
b2.grid(row=7,column=1, sticky=E)    

b3 = Button(root, text="Reports@Bank 1", font=("Helvetica",11,"bold"), command=chain_print_5001,  bg=bg, fg="#000000")
b3.grid(row=7,column=4, sticky=W) 
b4 = Button(root, text="Reports@Bank 2", font=("Helvetica",11,"bold"),  command=chain_print_5002,  bg=bg1, fg="#000000")
b4.grid(row=8,column=4, sticky=W) 
b5 = Button(root, text="Reports@Bank 3", font=("Helvetica",11,"bold"),  command=chain_print_5003,  bg=bg1, fg="#000000")
b5.grid(row=9,column=4, sticky=W)     

            
#function for about menu
def about():
    output = "Decentralized Distributed Ledger for failure rate reporting. \nThis program is a Proof-of-Concept software developed for research proposes only. \nRead more about this implemenation in the paper-Development of a Blockchain for Operational Follow-up of Safety Instrumented Systems."
    messagebox.showinfo("About", output)
    
#function ot close window     
def exit():
    root.destroy()

        
# create a toplevel menu
menubar = Menu(root, background ="#E6EE9C")
menubar.add_command(label="About", command=about)
menubar.add_command(label="Quit", command=exit)

# display the menu
root.config(menu=menubar, background="#89a7d0")
root.resizable(width=True, height=True)
root.mainloop()  #shows and runs the tKinter window

