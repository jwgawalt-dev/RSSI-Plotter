#program to plot tag RSSI values

import tkinter 
from tkinter import filedialog
import matplotlib.pyplot as plt

def parse_RFID_data(path):
    i=0
    epc_list=[]
    read_events = {}
    read_event_list = []
    with open(path,'r',newline='') as csvfile:

        for read_event in csvfile:     

            #add each dict to a list of dictionaries with line data
            if i > 1:
                #separate csv line into a list of values, strip extra characters from timestamp entry
                elements = read_event.split(';')
                epc = elements[0]
                rssi = float(elements[1])
                antenna = elements[2]
                timestamp = elements[5]
                #clear carriage return and line feed characters
                timestamp = timestamp[:-2]
                timestamp = timestamp.split()[0]
                #timestamp = timestamp.split('.')[0]

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
def create_XY_table (read_event_list,epc_list):

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

def count_tag_reads(epc_list,read_event_list):
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
path = filedialog.askopenfilename(title = ("SELECT EXPORT FILE"),filetypes=(("UHF Tag Trace Export File", "*.csv"),("all files", "*.*")) )

#Debug Path
#path =r'C:/Users/JGawal/Downloads/EPC_data_20230308 (4).csv'

#initialize arrays
read_events = []
epc_list = []
x_value_set =[]
y_value_set =[]

#extract read event from export file
read_events,epc_list = parse_RFID_data((path))
#create x/y data sets (timestamp = x, rssi = y)
x_value_set, y_value_set = create_XY_table(read_events, epc_list)
tag_counts = count_tag_reads(epc_list,read_events)


#plot each data set
i=0
for i in range(0,len(x_value_set)):
    plt.plot(x_value_set[i],y_value_set[i],marker ='.',label = "EPC:"+epc_list[i]+" " + str(tag_counts[i][0])+" Reads",alpha = 1)

#configure plot
plt.xticks( rotation=45)
plt.xlabel('Time of Read Event')
plt.ylabel("RSSI (dBm)")
plt.legend(loc='best')
plt.grid(axis= 'y')
plt.show()

