#!/usr/bin/python
import sys
from copy import deepcopy

#this function reads rules and rule number to state what each rule does.
def read_rules(line, rule_num):
    global tm_machine#we have to save each rule in tm machine therefore take in global tm_machine variable
    print("Rule " + str(rule_num)+": "+line)
    line_list = line.split(',')
    init_state = line_list[0]#first is the initial state
    new_state = line_list[2]#new state after take in the symbol
    input_symbol_str = line_list[1]#input symbol to determine which state to go to
    new_symbol_str = line_list[3]
    direction_str = line_list[4]
    tm_machine["rules"][init_state][input_symbol_str]= {"new_state": new_state, "rule_num": rule_num, "output":new_symbol_str, "direction":direction_str }#finally, save this rule to a tm_machine with a new_state and rule_num

def do_test(working_tapes):
    global tm_machine
    halt = False  # set a bool for halt the machine

    if len(working_tapes) > tm_machine["max_tape_len"]: # first check tape length
        halt = True
        output_msg = "ERROR: Tape length exceeds the maximum."
    
    tape_position = [0]*tm_machine["tape_num"] #reset the tape position when a new test starts
    current_state = tm_machine["start_state"]  # set current state to the start state which means start from the initial state.
    step_counter = 1
    output_msg = "" 
    
    while not halt:
        if current_state == tm_machine["accepting_state"]:
            output_msg = "Accepted"
            halt = True
            break
        elif current_state== tm_machine["rejected_state"]:
            output_msg = "Rejected"
            halt = True
            break

        init_state = current_state
        input_symbol_str = ""
        for i in range(tm_machine["tape_num"]):  #get the imput string
            #print("Current postion " + str(i))
            if (tape_position[i] >= len(working_tapes[i])): #if go over the tape length, we get blank
                input_symbol_str = input_symbol_str + "_"
                #print("Overflow, input is " + input_symbol_str)
            else:
                if (not(working_tapes[i][tape_position[i]]=="_" or working_tapes[i][tape_position[i]] in tm_machine["tape_alphabet"][i])):#if input symbols are not in alphabet then prints invalid error
                    halt = True
                    print("Symbol " + working_tapes[i][tape_position[i]] + " is invalid")
                    output_msg = "ERROR: Steps exceed the maximum."
                    break
                else:
                    #print("Add symbol " + working_tapes[i][tape_position[i]])
                    input_symbol_str = input_symbol_str + working_tapes[i][tape_position[i]]

        #print("Input is " + input_symbol_str)
        if (input_symbol_str not in tm_machine["rules"][init_state]): # no rule, reject 
            halt = True
            output_msg = "Rejected"
            break
            
        result = tm_machine["rules"][current_state][input_symbol_str]
        init_tape_position = tape_position
        #print("Result is " + str(result))
        #print("Current working_tapes: " + str(working_tapes))
        index_str = ''.join(str(e) for e in tape_position)
        for i in range(tm_machine["tape_num"]): #update the tapes and the position
            if result["output"][i] == "*":
                pass
            elif (tape_position[i]>=len(working_tapes[i])):
                working_tapes[i].append(result["output"][i])
            else:
                working_tapes[i][tape_position[i]] = result["output"][i]
            current_state = result["new_state"]
            if result["direction"][i] == "R":
                tape_position[i] +=1
            elif result["direction"][i] == "L":
                tape_position[i] -=1
            if tape_position[i]<0:
                tape_position[i] =0

        if not halt:
            print(str(step_counter) + "," + str(result["rule_num"])+","+','.join(str(e) for e in init_tape_position)+","+init_state+","+','.join(list(input_symbol_str))+","+current_state+","+','.join(list(result["output"]))+","+','.join(list(result["direction"]))) 

        step_counter += 1
        if step_counter > tm_machine["max_steps"]:
            halt = True
            output_msg = "ERROR: Steps exceed the maximum."

    print(output_msg)
    for i in range(tm_machine["tape_num"]):
        print("Tape " +str(i)+": "+ ''.join(working_tapes[i]))

    

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
    "rules" : {}
}

original_tapes=[]
test_caese = []

#taking the file argument which is the rules for the machine.
tm_file = sys.argv[1]
#testing bunch of inputs for the machine
tape_file = sys.argv[2]
tm = open(tm_file, "r")#opening the rule file
test = open(tape_file, "r")#opening the test file

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
            #here, we save different states into tm_machine[state]
            for state in states:
                tm_machine["rules"][state] = {}
        elif i == 3:#define the start state
            tm_machine["start_state"] = line
        elif i ==4:#define the accepting state and call other states as rejected states
            temp_states = line.split(',')
            tm_machine["accepting_state"] = temp_states[0]
            tm_machine["rejected_state"] = temp_states[1]
        elif (i>=5 and i<(5+(tm_machine["tape_num"]))): #read to the original tape and set up the working tape  
            tm_machine["tape_alphabet"].append(line.split(','))
        else:#these are different cases of rules and we read the rule in function called, "read_rules"
            read_rules(line, i-4-tm_machine["tape_num"])

    test_num = 0
    print(tape_file) #print the tape file
    #print("Test Case " + str(test_num))
    for i, line in enumerate(test): #read from the test file k lines a time, k is the num of tapes, and do the test
        if (i)%tm_machine["tape_num"] == 0 and i!=0:  #A testcase end, renew the tapes and do test
            working_tapes = original_tapes
            test_caese.append(original_tapes)
            do_test(working_tapes)
            test_num += 1
            #print("Test Case " + str(test_num))
            original_tapes = []
        line = line.rstrip()
        print("Tape " + str(i%tm_machine["tape_num"]) +": " + line)
        original_tapes.append(list(line))
    working_tapes = original_tapes  # need to do the last one by ourselves
    do_test(working_tapes)
    

except:
    print "Cannot read the file"
finally:
    #print(tm_machine)
    tm.close()#finally close the tm which is opened the rule file
    test.close()#close the test file