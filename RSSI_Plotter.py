#program to plot tag RSSI values
#may need to update to split read events out by antenna

import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

def time_to_float(timestamp):
    #take timestamp in format HH:MM:SS.MS, convert to integer value in seconds
    elements = timestamp.split(':')
    hours = float(elements[0])
    minutes = float(elements[1])
    seconds = float(elements[2])
    time = (hours * 3600) + (minutes * 60) + seconds
    
    return time

def parse_RFID_data(path):
    #extract epc, rssi, antenna, and timestamp for each read event in the tag trace export file 
    i=0
    epc_list=[] #list of unique EPCs in export  file
    read_events = {} #dict to store epc, rssi, antenna, and timestamp for each read event
    read_event_list = [] #list of read event dicts 
    with open(path,'r',newline='') as csvfile:

        for read_event in csvfile:     

            #add each dict to a list of dictionaries with line data
            if i > 1:
                #separate csv line into a list of values, strip extra characters from timestamp entry
                elements = read_event.split(';') 
                epc = elements[0]
                rssi = float(elements[1]) #convert string to floating point value for RSSI
                antenna = elements[2]

                timestamp = elements[5]                
                timestamp = timestamp[:-2] #remove carriage return and line feed characters
                timestamp = timestamp.split()[0]                
                timestamp = time_to_float(timestamp)

                #Grab first timestamp value, set as start time.
                if i == 2:
                    start_time = timestamp
                    timestamp = 0
                elif i>2:
                    timestamp = timestamp - start_time

                

                #create dict for each line in csv file 
                line_data = {
                    'epc' : epc,
                    'rssi' : rssi,
                    'antenna' : antenna,
                    'timestamp' : timestamp,
                }
                read_event_list.append(line_data)            
            
                #creat list of unique EPCs        
                if epc not in epc_list:
                    epc_list.append(epc)        
            i+=1
        
    return read_event_list,epc_list
def generate_RSSI_vs_Time_dataset (read_event_list,epc_list):
    #Create empty list to contain all sets of timestamp data
    x_values = []
    #create empty list to contain all sets of RSSI data
    y_values = []     
    
    #how many tags were read?
    num_epcs = len(epc_list)

    #iterate through EPC list and add placeholder for x/y values corresponding to each EPC
    for j in range(0,num_epcs):
        x_values.append([])
        y_values.append([])
    #iterate through each read event and move RSSI / Timestamp values into lists corresponding to unique EPCs
    for element in read_event_list:
        k=0
        #check the EPC of each read event and sort rssi/timestamp
        for epc in epc_list:
            if element['epc'] == epc:
                y_values[k].append(element['rssi'])
                x_values[k].append(element['timestamp'])
            k+=1
    return x_values,y_values

def count_tag_read_events(epc_list,read_event_list):
    #This function iterates through each read event and counts every occurance of each tag EPC in the EPC list
    tag_read_counts=[]
    for i in range(0,len(epc_list)):
        tag_read_counts.append([0])
    
    for event in read_events:
        j=0
        for epc in epc_list:            
            if event['epc']==epc:
               
                tag_read_counts[j][0]+=1
            j+=1    
    return tag_read_counts

#Prompt User to select csv file export
path = filedialog.askopenfilename(title = ("SELECT EXPORT FILE"),
                                  filetypes=(("UHF Tag Trace Export File", "*.csv"),("all files", "*.*")) )


#initialize arrays
read_events = []
epc_list = []
x_value_set =[]
y_value_set =[]

#extract read event data from export file
read_events,epc_list = parse_RFID_data((path))
tag_counts = count_tag_read_events(epc_list,read_events)

###    GUI Programming         ###
##################################
def plot_all():
    global selected_epc_list
    global plot_data
    plot_data = 1
    selected_epc_list = epc_list
    
    window.destroy()
    
def plot_selected():
    global selected_epc_list
    global plot_data
    plot_data = 1
    v=0
    
    for epc in epc_list:
        
        if vardict['tag '+str(v)].get() ==1:
            selected_epc_list.append(epc)
        v+=1
    window.destroy()

window = tk.Tk()
window.configure(bg="#ffcc00") 
window.title('RSSI Plotter')
window.geometry('')
 
Label = tk.Label(window, bg="#ffcc00", 
             width=20, 
             text='Select Tags to Plot')
Label.pack()
Label2 = tk.Label(window, bg="#ffcc00", 
             width=20, 
             text='"Tag EPC"  (Read Count)')
Label2.pack()
checkboxes = []
vardict ={}
selected_epc_list=[]
plot_data = 0

#create checkboxes for each tag in read event dict
for c in range(len(epc_list)): 
    #initialize a new IntVar for each tag in EPC List
    vardict['tag '+str(c)]=tk.IntVar()
    #Initialize checkbuttons for each IntVar created
    checkbox = tk.Checkbutton(window,
                              text = str(epc_list[c])+'('+str(tag_counts[c][0])+')',
                              variable=vardict['tag '+str(c)],
                              bg="#ffcc00",
                              anchor='w',
                              justify="left")
    checkbox.pack(anchor='w')
    checkboxes.append(checkbox)

Scatter_Select = tk.IntVar()

tk.Button(window,text="Plot Selected",
          command=plot_selected,
          background = "black",
          fg='white').pack()
tk.Button(window,text="Plot ALL",
          command=plot_all,
          background = "black",
          fg='White').pack()

#Force Window to Top
window.attributes("-topmost", True)
window.mainloop()
### END GUI PROGRAMMING ###
###########################

#START PLOTTING LOGIC / Configuration

#create x/y data sets (timestamp = x, rssi = y)
x_value_set, y_value_set = generate_RSSI_vs_Time_dataset(read_events, selected_epc_list)      
#get tag counts
selected_tag_counts = count_tag_read_events(selected_epc_list,read_events)
counts = []
j=0
for count in selected_tag_counts:
    counts.append(selected_tag_counts[j][0])
    j+=1


if plot_data ==1:
    ### CONFIGURE BAR GRAPH
    plt.figure(1)
    k=0
    for element in selected_epc_list:
        plt.bar(selected_epc_list[k],counts[k])        
        k+=1


    plt.xlabel('Tag EPC')
    plt.ylabel("Total Read Events")
    plt.title("Read Count by Tag EPC")
    plt.legend(selected_epc_list, counts,loc='best')
    plt.grid(axis='y')
    plt.xticks(rotation=0)
    plt.tick_params(axis = 'x',which = 'major',labelsize =7)


    plt.figure(2)
    #plot each data set
    i=0

    
    #Create line for each entry in x/y value sets, round marker, legend displays EPC and total read count for that EPC
    for i in range(0,len(x_value_set)):
        plt.plot(x_value_set[i],y_value_set[i],marker ='.',label = "EPC:"+selected_epc_list[i]+" " + str(selected_tag_counts[i][0])+" Reads",alpha = 1)


    #configure RSSI plot
    plt.xticks( rotation=45)
    plt.title("Received Signal Strength Indicator (RSSI) by Tag")
    plt.xlabel('Time (s) From Start of Test')
    plt.ylabel("RSSI (dBm)")
    plt.legend(loc='best')
    plt.grid(axis= 'y')
    plt.show()