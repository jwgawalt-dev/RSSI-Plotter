#program to plot tag RSSI values

import csv
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
                timestamp = timestamp[:-2]
                timestamp = timestamp.split()

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
    #temp array to store individual instances of timestamp daa
    temp_x_values=[]
    #temp array to store individual instances of RSSI data
    temp_y_values = []
    j=0
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
                x_values[k].append(element['timestamp'][0])
            k+=1
    return x_values,y_values

#Prompt User to select csv file export

path = filedialog.askopenfilename(title = ("SELECT EXPORT FILE"),filetypes=(("UHF Tag Trace Export File", "*.csv"),("all files", "*.*")) )

#initialize arrays
read_event_list = []
epc_list = []
x_value_set =[]
y_value_set =[]

#extract read event from export file
read_event_list,epc_list = parse_RFID_data((path))
#create x/y data sets (timestamp = x, rssi = y)
x_value_set, y_value_set = create_XY_table(read_event_list, epc_list)

#plot each data set
i=0
for i in range(0,len(x_value_set)):
    plt.plot(x_value_set[i],y_value_set[i])
plt.xticks( rotation='vertical')
plt.xlabel('Time')
plt.ylabel("RSSI")
plt.show()

