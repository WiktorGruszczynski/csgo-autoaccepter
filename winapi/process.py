import os
import re

def listProcesses():
    #Running the aforementioned command and saving its output
    output = os.popen('wmic process get description, processid').read()

    #Convert console output to list
    proc_list = output.split("\n")

    #Create tool for removing too many whitespaces in string
    CutSpaces = re.compile(r"(?a:\s+)")
    
    #reduce whitespace to only one for every element
    proc_list = [CutSpaces.sub(" ", i).split(" ")[:-1] for i in proc_list if i != '']

    #remove first element from list
    proc_list.pop(0)

    #create dictionary for processes
    processes_dict = {}

    #for every process assign a key and value(pid) in dictionary
    for process in proc_list:
        name = process[0]
        pid = process[1]
        processes_dict[name] = pid


    return processes_dict
    

def is_process_alive(process:str):
    #check if process is alive
    if process in listProcesses():
        return True
    else:
        return False



def getPid(process_name:str):
    #list all active processes
    processes = listProcesses()
    
    #get id of process
    pname = processes[process_name] 

    #convert process type to int and return it
    return int(pname)


