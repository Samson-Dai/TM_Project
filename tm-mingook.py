#!/usr/bin/python
import sys
from copy import deepcopy

#this function reads rules and rule number to state what each rule does.
def read_rules(line, rule_num):
    global tm_machine#we have to save each rule in tm machine therefore take in global tm_machine variable
    line_list = line.split(',')
    init_state = line_list[0]#first is the initial state
    input_symbol = line_list[1]#input symbol to determine which state to go to
    new_state = line_list[2]#new state after take in the symbol
    new_symbol = line_list[3]
    direction = line_list[4]
    tm_machine["rules"][init_state][input_symbol]= {"state": new_state, "rule_num": rule_num, "output":new_symbol, "move":direction }#finally, save this rule to a tm_machine with a new_state and rule_num

def do_test(line):
    current_state = start_state  # set current state to the start state which means start from the initial state.
    for i in range(0, len(line)):
        letter = line[i]
        init_state = current_state

        if (letter not in alphabet):#if input symbols are not in alphabet then prints invalid error
            print("Invalid Input")
            current_state = rejected_state[0]#this is done because this state should not be an accepting state and therefore we mark it as a rejected state so that it does not print out accepted despite if the state is the accepted state.
            break;


        if (letter not in tm_machine[current_state]):#if there is not input symbol, letter, then it prints out current state does not have the input symbol to proceed.
            print("No rule for state " + str(current_state) + " with input "+ str(letter))
            current_state = rejected_state[0]##this is done because this state should not be an accepting state and therefore we mark it as a rejected state so that it does not print out accepted despite if the state is the accepted state.
            break;
        
        #after checking each of different symbols with states, we finally proceed with our logic
        new_state = tm_machine[current_state][letter][0]#save the new state with current input argument: current_state and input symbol
        rule_num = tm_machine[current_state][letter][1]#save the rule number with current input argument: current state and input symbol
        print(str(i+1)+","+str(rule_num)+","+str(init_state)+","+str(letter)+","+str(new_state))
        current_state = new_state #update current state

    if current_state in accepting_state:#check if the current state is the accepting state
        print("Accepted\n")
    else:#if not, print rejected
        print("Rejected\n")
    

#different varibles(easily recognizable by their names, and nothing tricky)
tm_machine = {
    "machine_name" : "",
    "tape_num" :0,
    "max_tape_len": 0,
    "max_steps" : 0,
    "tape_alphabet": [],
    "alphabet" :[],
    "states" :[],
    "start_state" : "",
    "accepting_state" : "",
    "rejected_state" : "",
    "current_state" :"",
    "tape_position" : 0,
    "rules" : {}
}

original_tape=[]
working_tape=[]

#taking the file argument which is the rules for the machine.
tm_file = sys.argv[1]
#testing bunch of inputs for the machine
#tape_file = sys.argv[2]
tm = open(tm_file, "r")#opening the rule file
#test = open(tape_file, "r")#opening the test file

try:  #read from the tm definition and construct the machine, print the information at the same time
    for i, line in enumerate(tm):
        line = line.rstrip()
        if i == 0:
            items = line.split(',')
            tm_machine["machine_name"] = items[0]
            tm_machine["tape_num"] = int(items[1])
            tm_machine["max_tape_len"] = int(items[2])
            tm_machine["max_steps"] = int(items[3])
        elif i == 1:#take the input symbols and save it into alphabet
            tm_machine["alphabet"] = line.split(',')
        elif i ==2:#defines the states
            states = line.split(',')
            tm_machine["states"] = states
            for state in states:#here, we save different states into tm_machine[state]
                tm_machine["rules"][state] = {}
        elif i == 3:#define the start state
            tm_machine["start_state"] = line
            tm_machine["current_state"] = line
        elif i ==4:#define the accepting state and call other states as rejected states
            temp_states = line.split(',')
            tm_machine["accepting_state"] = temp_states[0]
            tm_machine["rejected_state"] = temp_states[1]
        elif (i>=5 and i<(5+(tm_machine["tape_num"]))): #read to the original tape and set up the working tape  
            tm_machine["tape_alphabet"].append(line.split(','))
        else:#these are different cases of rules and we read the rule in function called, "read_rules"
            #print("Rule "+ str(i-4-tm_machine["tape_num"]) +" : "+ line)
            read_rules(line, i-4-tm_machine["tape_num"])

    """
    for line in test: #read from the test file and do the test
        line = line.rstrip()
        print("String : " + line)
        do_test(line)
    """

except:
    print "Cannot read the file"
finally:
    print(str(tm_machine))
    tm.close()#finally close the tm which is opened the rule file
    #test.close()#close the test file