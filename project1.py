#!/usr/bin/python3

import sys,random
# define function check_options(), if there is a "op" in sys.argv, global variable sort = True,else,sort = False
sort = "True"
def check_options(op) :
   if op in sys.argv :
      sort = "True"
      return sort
   else :
      sort = "False"
      return sort
# define function check_ips(). This function is to check whether the ip is valid.
def check_ips(string) :
   bits = string.split(".")
   if len(bits) != 4 :
      print("Invalid IP address")
   else :
      while True :
         if (eval(bits[0]) <= 255 and eval(bits[1]) <= 255 and eval(bits[2]) <= 255 and eval(bits[3]) <= 255) and (eval(bits[0]) >=0 and eval(bits[1]) >=0 and eval(bits[2]) >=0 and eval(bits[3]) >= 0) :  
            break
         else :
            print("Valid IP should in range (0,255)")
            break
# define function parse_file()
def parse_file(string) :
   file_object = open(string,"r")
   d = dict()  # create an empty dictionary
   for line in file_object.readlines() :
      if line[16:18] == 'IP' and ('Flags' in line or 'UDP' in line) : # fine TCP and UDP connections
         log_list = line.split()
         sip_list = log_list[2].split(".")
         dip_list = log_list[4].split(".")
         packet_size = log_list[len(log_list)-1]   # split line into 3 sections
         sip = sip_list[0] + "." + sip_list[1] + "." + sip_list[2] + "." + sip_list[3]
         dip = dip_list[0] + "." + dip_list[1] + "." + dip_list[2] + "." + dip_list[3] # remove ports number
         sdip = sip + ',' +dip
         if sdip not in d :
            d[sdip] = eval(packet_size)
         else :
            d[sdip] = d[sdip] + eval(packet_size)   # add values to previous same key 
            
   return d
# define function sort_list()
def sort_list(string) :
   list1=[]  # create an empty list
   d=parse_file(sys.argv[1])  # call function parse_file()
   list2 = sorted(d.values(),reverse=True)   # descending sort d.values()
   for i in range(0,len(d)-1) :
      for sdip in d.keys() :
         if d[sdip] == list2[i] and d[sdip] != list2[i+1] :
            list1.append(sdip)
         else :
            if d[sdip] == list2[i] and d[sdip] == list2[i+1] :
               list1.append(sdip)
               d[sdip] = random.randint(-100,-1)  # insert d.keys() into list1. If two keys have same value, change a value by a random number
   return list1
# define function print_list() to print the whole file
def print_list() :   
   d = parse_file(sys.argv[1])   # call function parse_file()
   list2 = sorted(d.values(),reverse=True)  # create list2 to store descending d.values()   
   list1 = sort_list(sys.argv[1])  # call function sort_list() 
   sort1 = check_options("-s") # call function check_options()
   if sort1 == 'True' :  # print a descending list form list2
      for i in range(0,len(d)) :
         print("source:",list1[i].split(",")[0], "dest: ",list1[i].split(",")[1], "total: ",list2[i])
   else :   
      for key in d.keys() :  # print a non-descending list from dict 
         print("source:", key.split(",")[0], "dest:", key.split(",")[1], "total:", d[key])
# define function print_on_list() to check the call argument which have one ip input
def print_one_ip(string) :     
   d = parse_file(sys.argv[1])   # call function parse_file()
   list2 = sorted(d.values(),reverse=True)  # create list2 to store descending d.values()   # call function check_options()
   list1 = sort_list(sys.argv[1])  # call function sort_list()
   sort1 = check_options("-s")   # call function check_options()
   if len(string.split(".")) == 4 : # check string format
      check_ips(string)
      if sort1 == 'True' :  # print a descending list form list2
         for i in range(0,len(d)) :
            if list1[i].split(",")[0] == string :
               print("source:",list1[i].split(",")[0], "dest: ",list1[i].split(",")[1], "total: ",list2[i])
      else :   
         for key in d.keys() :  # print a non-descending list from dict  
            if key.split(",")[0] == string :
               print("source:", key.split(",")[0], "dest:", key.split(",")[1], "total:", d[key])
# define function print_on_list() to check the call argument which have two ip input
def print_two_ip(string1,string2) :     
   d = parse_file(sys.argv[1])   # call function parse_file()
   list2 = sorted(d.values(),reverse=True)  # create list2 to store descending d.values()   # call function check_options()
   list1 = sort_list(sys.argv[1])  # call function sort_list()
   sort1 = check_options("-s")  # call function check_options()
   if len(string1.split(".")) == 4 and len(string2.split(".")) == 4 :
      check_ips(string1)
      check_ips(string2)
      if sort1 == 'True' :
         for i in range(0,len(d)) :
            if list1[i].split(",")[0] == string1 and list1[i].split(",")[1] == string2 :
               print("source:",list1[i].split(",")[0], "dest: ",list1[i].split(",")[1], "total: ",list2[i])
      else :   
         for key in d.keys() :   
            if key.split(",")[0] == string1 and key.split(",")[i] == string2 :
               print("source:", key.split(",")[0], "dest:", key.split(",")[1], "total:", d[key])

 #print output in different conditions
if len(sys.argv) == 2 :
   print_list()   
elif len(sys.argv) == 3 :
   if check_options("-s") == False :
      print_one_ip(sys.argv[2])
   else :
      print_list()
elif len(sys.argv) == 4 :      
   if check_options("-s") == False :
      print_two_ip(sys.argv[2],sys.argv[3])         
   else :
      if sys.argv[3] == "-s" :        
         print_one_ip(sys.argv[2]) 
      else :  
         print_one_ip(sys.argv[3])      
else :
   if len(sys.argv) == 5 :
      if sys.argv[4] == "-s" :
         print_two_ip(sys.argv[2],sys.argv[3])
      elif sys.argv[3] == "-s" :   
         print_two_ip(sys.argv[2],sys.argv[4])
      else :
         print_two_ip(sys.argv[3],sys.argv[4])

#"THIS ASSIGNMENT REPRESENTS MY OWN WORK IN ACCORDANCE WITH SENECA ACADEMIC POLICY"
# By: Aotao Xu
