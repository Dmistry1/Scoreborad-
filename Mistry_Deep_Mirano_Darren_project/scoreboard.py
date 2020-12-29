# Darren Mirano, Deep Misty
# CMSC 411 Project
# Due Date: Dec 6, 2020

#Initialize memory
memory = [45, 12, 0, 0, 10, 135, 254, 127, 18, 4, 55, 8, 2, 98, 13, 5, 233, 158, 167]

#initialize registers 
registers = {"F0" : 0, "F1" : 0, "F2" : 0, "F3" : 0, "F4" : 0, "F5" : 0, "F6" : 0, "F7" : 0, "F8" : 0, "F9" : 0, "F10" : 0, "F11" : 0,
             "F12" : 0, "F13" : 0, "F14" : 0, "F15" : 0, "F16" : 0, "F17" : 0, "F18" : 0, "F19" : 0, "F20" : 0, "F21" : 0, "F22" : 0, 
             "F23" : 0, "F24" : 0, "F25" : 0, "F26" : 0, "F27" : 0, "F28" : 0, "F29" : 0, "F30" : 0, "F31" : 0} 

#initialize interger register 
intergerRegister = {"$0" : 0,"$1" : 0, "$2" : 0, "$3" : 0, "$4" : 0, "$5" : 0, "$6" : 0, "$7" : 0, "$8" : 0, "$9" : 0, "$10" : 0, "$11" : 0, "$12" : 0, "$13" : 0,
                    "$14" : 0,"$15" : 0,"$16" : 0,"$17" : 0,"$18" : 0,"$19" : 0,"$20" : 0,"$21" : 0,"$22" : 0,"$23" : 0,"$24" : 0,"$25" : 0,"$26" : 0,"$27" : 0,
                    "$28" : 0,"$29" : 0,"$30" : 0,"$31" : 0}

#Function to determine if hardware is busy. returns 1 if not busy, return 0 if busy
def canIssueBusy(scoreboard, currInst, potentialCycle):
    currInstSplit = currInst.split(" ")
    currCommand = currInstSplit[0]

    size = len(scoreboard)
    index = 0  

    if(currCommand == "ADD.D" or currCommand == "ADDI" or currCommand == "SUB.D" or currCommand == "SUB"): #All these commands share the same hardware
         while (index < size):
            currSB = scoreboard[index]
            currSBInst = currSB[0]

            currSBinstSplit = currSBInst.split(" ")
            currSBcommand = currSBinstSplit[0]
            if(currSBcommand == "ADD.D" or currSBcommand == "ADDI" or currSBcommand == "SUB.D" or currSBcommand == "SUB"):
                prevWB = currSB[4]
                if(prevWB >= potentialCycle): #Hardware is busy
                    issueVal = prevWB + 1
                    return issueVal

            index = index + 1

    if(currCommand == "S.D" or currCommand == "L.D"): #These two commands share the same hardware
        while (index < size):
            currSB = scoreboard[index]
            currSBInst = currSB[0]

            currSBinstSplit = currSBInst.split(" ")
            currSBcommand = currSBinstSplit[0]
            if(currSBcommand == "L.D" or currSBcommand == "S.D"):
                prevWB = currSB[4]
                if(prevWB >= potentialCycle): #Hardware is busy
                    issueVal = prevWB + 1
                    return issueVal

            index = index + 1

    else:
        while (index < size):
            currSB = scoreboard[index]
            currSBInst = currSB[0]

            currSBinstSplit = currSBInst.split(" ")
            currSBcommand = currSBinstSplit[0]

            if(currSBcommand == currCommand):
                prevWB = currSB[4]
                if(prevWB >= potentialCycle): #Hardware is busy
                    issueVal = prevWB + 1
                    return issueVal

            index = index + 1

    issueVal = potentialCycle
    return issueVal

#Checks for WAW errors. Gets passes a list of instructions, returns 1 if no WAW issues, return 0 if there is a WAW issue
def canIssueWAW(scoreboard, currInst, potentialCycle):
    data = currInst.split(" ") 
    currCommand = data[0]
       
    if(currCommand == "S.D"): #No such this as a WAW hazard when store is the currInst
        issueVal = 0
        return issueVal 
    
    split = data[1] #Gets the current instruction destination register 
    split1 = split.split(',')
    currDest = split1[0]

    size = len(scoreboard)
    index = 0
    while (index < size): #Loop through previous instructions and check for WAW hazards
        currSB = scoreboard[index]
        currSBinst = currSB[0]

        currCommand = currSBinst[0]
        if (currCommand == "S"):
            index = index + 1
            
        else:
            currSBinstSplit = currSBinst.split(" ")
            currSBinstSplit2 = currSBinstSplit[1]
            currSBinstSplit3 = currSBinstSplit2.split(',')
            currSBdest = currSBinstSplit3[0]

            if(currDest == currSBdest):
                prevWB = currSB[4]
                if(prevWB >= potentialCycle): #cycle still busy 
                    issueVal = prevWB + 1
                    return issueVal  

            index = index + 1

    issueVal = potentialCycle #Escapes the while loop, no WAW issues
    return issueVal

def canReadOpsRAW(scoreboard, currInst, potentialCycle):
    data = currInst.split(" ")
    currCommand = data[0]

    size = len(scoreboard)
    index = 0

    if (currCommand == "L.D"): #No such thing as a RAW hazard when currInst is load
        issueVal = potentialCycle
        return issueVal

    elif (currCommand == "S.D"): #Get read op from store command
        split = data[1]
        split1 = split.split(',')
        currSBread = split1[0]

        while (index < size): #Loop throught previous instructions and check for RAW hazards
            currSB = scoreboard[index]
            currSBinst = currSB[0]
            
            currSBinstSplit = currSBinst.split(" ")
            command = currSBinstSplit[0]
        
            if(command == "S.D"): #Stores cannot create RAW hazards, skip iteration
                index = index + 1

            elif(command == "L.D"): #Gets read value of load command and compare
                currSBinstSplit2 = currSBinstSplit[1]
                currSBinstSplit3 = currSBinstSplit2.split(',')
                currSBdest = currSBinstSplit3[0]
                
                if(currSBread == currSBdest):
                    prevWB = currSB[4]
                    if(prevWB >= potentialCycle): #cycle still busy 
                        issueVal = prevWB + 1
                        return issueVal  

                index = index + 1
            
            else: #Gets read value of all other commands
                currSBinstSplit2 = currSBinstSplit[1]
                currSBinstSplit3 = currSBinstSplit2.split(',')
                currSBdest = currSBinstSplit3[0]

                if(currSBread == currSBdest):
                    prevWB = currSB[4]
                    if(prevWB >= potentialCycle): #cycle still busy 
                        issueVal = prevWB + 1
                        return issueVal  

                index = index + 1
        
        issueVal = potentialCycle
        return issueVal

    else: #Gets read ops from all other commands, needs to be in different conditional since store commands have 1 read value whereas everything else has 2 read values
        split = data[2]
        split1 = split.split(',')
        currSBread1 = split1[0]
        currSBread2 = data[3]

        while (index < size):
            currSB = scoreboard[index]
            currSBinst = currSB[0]
            
            currSBinstSplit = currSBinst.split(" ")
            command = currSBinstSplit[0]
        
            if(command == "S.D"):
                index = index + 1

            elif(command == "L.D"): 
                currSBinstSplit2 = currSBinstSplit[1]
                currSBinstSplit3 = currSBinstSplit2.split(',')
                currSBdest = currSBinstSplit3[0]
                
                if(currSBread1 == currSBdest or currSBread2 == currSBdest):
                    prevWB = currSB[4]
                    if(prevWB >= potentialCycle): #cycle still busy 
                        issueVal = prevWB + 1
                        return issueVal  

                index = index + 1
            
            else:                      
                currSBinstSplit2 = currSBinstSplit[1]
                currSBinstSplit3 = currSBinstSplit2.split(',')
                currSBdest = currSBinstSplit3[0]

                if(currSBread1 == currSBdest or currSBread2 == currSBdest):
                    prevWB = currSB[4]
                    if(prevWB >= potentialCycle): #cycle still busy 
                        issueVal = prevWB + 1
                        return issueVal  

                index = index + 1
        
        issueVal = potentialCycle
        return issueVal

#Check for WAR errors, gets passed list of instructions
def canWriteBackWAR(scoreboard, currInst, potentialCycle):
    data = currInst.split(" ") 
    currCommand = data[0]
    split = data[1]
    split1 = split.split(',')
    currDest = split1[0]
    
    if (currCommand == "S.D"): #Cannot have a WAR hazard when currInst is store
        issueVal = potentialCycle
        return issueVal

    size = len(scoreboard)
    index = 0  
    while (index < size):
        currSB = scoreboard[index]
        currSBinst = currSB[0]

        currSBinstSplit = currSBinst.split(" ")
        currCommandSB = currSBinstSplit[0]

        if (currCommandSB == "L.D"): #Loads cannot create a WAR hazard
            index = index + 1

        elif(currCommandSB == "S.D"): #Gets read values of store command
            currSBinstSplit2 = currSBinstSplit[1]
            currSBinstSplit3 = currSBinstSplit2.split(',')
                
            currSBread = currSBinstSplit3[0]
            
            if(currDest == currSBread):
                prevWB = currSB[4]  
                if(prevWB >= potentialCycle): #Hardware is busy
                    issueVal = prevWB + 1
                    return issueVal
           
            index = index + 1

        else: #Gets read values of all other commands
            currSBinstSplit2 = currSBinstSplit[2]
            currSBinstSplit3 = currSBinstSplit2.split(',')
                
            currSBread1 = currSBinstSplit3[0]
            currSBread2 = currSBinstSplit[3]

            if(currDest == currSBread1 or currDest == currSBread2):
                prevWB = currSB[2]
                if(prevWB >= potentialCycle): #Hardware is busy
                    issueVal = prevWB + 1
                    return issueVal

            index = index + 1

    issueVal = potentialCycle #No WAR hazards detected
    return issueVal

#Function to generate scoreboard
#Returns scoreboard, a 2d list
def getScoreboard(instructions):
    scoreboard = []
    size = len(instructions)
    
    if( size == 0): #Base case for empty instruction set
        msg = "EMpty instruction set!"
        print(msg)
        return 0

    currInst = instructions[0] #Hard code cycles for first instruction
    currInstSplit = currInst.split(" ")
    currCommand = currInstSplit[0]

    currInstCycles = [] #currInstCycles stores the cycles when each stage is finished 
    currInstCycles.append(currInst) #Format for currInstCycles is [instruction, issueVal, readVal, ExVal, writeBackVal]
    currInstCycles.append(1)
    currInstCycles.append(2)

    if (currCommand == "L.D"):
        currInstCycles.append(3)
        currInstCycles.append(4)

    elif (currCommand == "ADD.D"):
        currInstCycles.append(4)
        currInstCycles.append(5)

    elif (currCommand == "ADDI"):
        currInstCycles.append(4)
        currInstCycles.append(5)

    elif (currCommand == "SUB"):
        currInstCycles.append(4)
        currInstCycles.append(5)

    elif (currCommand == "SUB.D"):
        currInstCycles.append(4)
        currInstCycles.append(5)

    elif (currCommand == "MUL.D"):
        currInstCycles.append(12)
        currInstCycles.append(13)

    elif (currCommand == "DIV.D"):
        currInstCycles.append(42)
        currInstCycles.append(43)

    elif (currCommand == "S.D"):
        currInstCycles.append(3)
        currInstCycles.append(4)

    scoreboard.append(currInstCycles)
    
    prevInstructions = []

    index = 1
    while (index < size): #Loop through rest of instructions
        currInstCycles = []
        currInst = instructions[index]

        currInstCycles.append(currInst) #Store current instruction at 0 index

        currInstSplit = currInst.split(" ")
        currCommand = currInstSplit[0] #Get type of instruction

        prevSB = scoreboard[index - 1]
        prevIssue = prevSB[1]
        potentialCycle = prevIssue + 1

        potentialIssueVal = canIssueBusy(scoreboard, currInst, potentialCycle) #Get cycle issue stage completes
        potentialIssueVal2 = canIssueWAW(scoreboard, currInst, potentialCycle)

        if(potentialIssueVal > potentialIssueVal2):
            issueVal = potentialIssueVal
        
        elif(potentialIssueVal < potentialIssueVal2):
            issueVal = potentialIssueVal2

        elif(potentialIssueVal == potentialIssueVal2):
            issueVal = potentialIssueVal

        currInstCycles.append(issueVal)

        potentialReadVal = issueVal + 1

        readVal = canReadOpsRAW(scoreboard, currInst, potentialReadVal) #Get cycle read stage completes
        currInstCycles.append(readVal)

        if (currCommand == "L.D"): #Execute stage
            exVal = readVal + 1
            
        elif (currCommand == "ADD.D"):
            exVal = readVal + 2
            
        elif (currCommand == "ADDI"):
            exVal = readVal + 2
            
        elif (currCommand == "SUB"):
            exVal = readVal + 2
            
        elif (currCommand == "SUB.D"):
            exVal = readVal + 2
            
        elif (currCommand == "MUL.D"):
            exVal = readVal + 10
            
        elif (currCommand == "DIV.D"):
            exVal = readVal + 40
            
        elif (currCommand == "S.D"):
            exVal = readVal + 1

        else:
            print("IVAN IS THE GOAT") #EASTER EGG ;)

        currInstCycles.append(exVal)
        
        potentialWBval = exVal + 1 
        WBval = canWriteBackWAR(scoreboard, currInst, potentialWBval) #Get cycle write back finishes
        currInstCycles.append(WBval)

        scoreboard.append(currInstCycles)
        index = index + 1

    return scoreboard

#For table formatting
def printScoreboard(scoreboard):
    print("Instruction \t\t\t Issue \t Read \t Execute \t Write Back")
    index = 0
    size = len(scoreboard)

    while (index < size):
        currInst = scoreboard[index]
        currInstPrint = currInst[0]
        currInstIssue = currInst[1]
        currInstRead = currInst[2]
        currInstEx = currInst[3]
        currInstWB = currInst[4]

        print(" {:<20}\t\t {} \t {} \t {} \t\t {}".format(currInstPrint, currInstIssue, currInstRead, currInstEx, currInstWB ))

        index = index + 1

#Load Operation 
def load(instruction):
    load = "This is a load command"

    data = instruction[2]
             
    split1 = data.split("(") #splits at the '('
    offset = split1[0] #Stores offset
 
    split2 = split1[1].split(")") #Cut off ")"
    memLocation = split2[0] #Actual memory location

    dest = instruction[1] #Get name of register destination
    dest2 = dest.split(",")
    destination = dest2[0]

    intMemLocation = int(memLocation) #converting string to an int 
    
    registers[destination] = memory[intMemLocation]

#Store Operation 
def store(instruction):

    data = instruction[2]

    split1 = data.split("(") #splits at the '('
    offset = split1[0] #Stores offset
 
    split2 = split1[1].split(")") #Cut off ")"
    memLocation = split2[0] #Actual memory location

    dest = instruction[1] #Get name of register destination
    dest2 = dest.split(",")
    destination = dest2[0]
    
    memLocation = registers[destination]

def mul(instruction):
    data = instruction[2]
    split1 = data.split(",") #splits at the ','
    op1 = split1[0] #Stores offset
    op2 = instruction[3]
    
    destinationSplit = instruction[1]
    destinationSplit1 = destinationSplit.split(",")
    destination = destinationSplit1[0]
    
    op3 = registers[op1]
    op4 = registers[op2]
        
    mul = op3 * op4

    registers[destination] = mul

def div(instruction):
    data = instruction[2]
    split1 = data.split(",") #splits at the ','
    op1 = split1[0] #Stores offset
    op2 = instruction[3]
    
    destinationSplit = instruction[1]
    destinationSplit1 = destinationSplit.split(",")
    destination = destinationSplit1[0]
    
    op3 = registers[op1]
    op4 = registers[op2]

    if (op4 == 0): #Divide by 0 case
        return
    div = op3 / op4

    registers[destination] = div
    
def addD(instruction):
    data = instruction[2]
    split1 = data.split(",") #splits at the ','
    op1 = split1[0] #Stores offset
    op2 = instruction[3]
    
    destinationSplit = instruction[1]
    destinationSplit1 = destinationSplit.split(",")
    destination = destinationSplit1[0]
    
    op3 = registers[op1]
    op4 = registers[op2]

    add = op3 + op4

    registers[destination] = add
    
def subD(instruction):
    data = instruction[2]
    split1 = data.split(",") #splits at the ','
    op1 = split1[0] #Stores offset
    op2 = instruction[3]
    
    destinationSplit = instruction[1]
    destinationSplit1 = destinationSplit.split(",")
    destination = destinationSplit1[0]
    
    op3 = registers[op1]
    op4 = registers[op2]

    sub = op3 - op4

    registers[destination] = sub

def addI(instruction):
    data = instruction[2]
    split1 = data.split(",") #splits at the ','
    op1 = split1[0] #Stores offset
    op2 = instruction[3]
    
    destinationSplit = instruction[1]
    destinationSplit1 = destinationSplit.split(",")
    destination = destinationSplit1[0]
    
    op3 = intergerRegister[op1]
    op4 = int(op2)

    addI = op3 + op4

    intergerRegister[destination] = addI

def sub(instruction):
    data = instruction[2]
    split1 = data.split(",") #splits at the ','
    op1 = split1[0] 
    op2 = instruction[3]
    
    destinationSplit = instruction[1]
    destinationSplit1 = destinationSplit.split(",")
    destination = destinationSplit1[0]
    
    op3 = intergerRegister[op1]
    op4 = intergerRegister[op2]

    sub = op3 - op4

    intergerRegister[destination] = sub

def printFPRegs():
    index = 0
    size = 32

    string = "F"

    print("Floating Point Register Values")

    while(index < size):
        string2 = str(index)
        FP = string + string2

        print(FP, registers[FP])
        index = index + 1
    
def printIntRegs():
    index = 0
    size = 32

    string = "$"

    print("Integer Register Values")

    while(index < size):
        string2 = str(index)
        FP = string + string2

        print(FP, intergerRegister[FP])
        index = index + 1

def main():
    #Read in instructions from text file, split at \n
    user_input = input("Enter the file name that you would like to test: ")
    
    my_file = open(user_input, "r")
    
    content = my_file.read()
    split_newLine = content.split("\n")
    
    instructionCount = len(split_newLine)
    
    scoreboard = getScoreboard(split_newLine)
    printScoreboard(scoreboard)
    print("\n")

    #Loop through instructions 
    index = 0
    while(index < instructionCount):
        currentInst = split_newLine[index]
        command = currentInst.split(" ") #Split current instruction into an array

        if (command[0] == "L.D"):
            load(command)

        elif (command[0] == "ADD.D"):
            addD(command)

        elif (command[0] == "ADDI"):
            addI(command)

        elif (command[0] == "SUB"):
            sub(command)

        elif (command[0] == "SUB.D"):
            subD(command)

        elif (command[0] == "MUL.D"):
            mul(command)

        elif (command[0] == "DIV.D"):
            div(command)
        
        elif (command[0] == "S.D"):
            store(command)
        
        else:
            print("Command not recognized")
            return
        
        index = index + 1
    
    printFPRegs()
    print("\n")
    printIntRegs()
    
main()

