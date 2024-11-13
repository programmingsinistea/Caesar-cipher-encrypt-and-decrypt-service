import sys
import random
import datetime

record = []
#try to access the file
try:
    with open("vocab.txt", "r") as f:
        vocab = f.read().splitlines()
except FileNotFoundError:
    print("vocab.txt file not found. \n run without it?\n")
    temp = input("T / F: ")
    if temp == "T":
        print("Warning: some funtion may not work")
    else:
        sys.exit()

#provide guide
print("Caesar cipher encrypt and decrypt service\ntype '/help' for help")

def checkHist(arr):
    for i, rec in enumerate(arr):
        print(f"Record {i + 1}:\nTime: {rec[1]}\nOperation Type: {rec[0]}\nInput: {rec[2]}\nOutput: {rec[3]}")

def checkVocab(s):
    outputVocab = s.lower().split()# turn the vocab into small letter than
    cnt = 0
    for word in outputVocab:
        if word in vocab:
            cnt += 1
            if cnt > len(outputVocab) / 6:
                return True
    return False

def isSmall(k):# k is ARCLL of the string
    return 97 <= k <= 122

def isLetter(k): # k is ARCLL of the string
    return 65 <= k <= 90 or isSmall(k)

def outputProcess(s, type):#output the result
    if type == 1:
        try:
            with open("result.txt", "w", encoding="Latin-1") as g:#open the result file
                g.write(s) #write the result into the result.txt
            print("Done!")#the the user the output process has been complete
        except IOError:
            print("Error writing to result.txt")
    else:
        print("Output: " + s)

def encrypt(s):
    k = random.randint(1, 25)#generate the shift 
    output = "" # create a output string
    for char in s: 
        intChar = ord(char)
        if isLetter(intChar):
            if (intChar + k > 122 and isSmall(intChar)) or (intChar + k > 90 and not isSmall(intChar)):
                newAscii = intChar + k - 26
            else:
                newAscii = intChar + k
            output += chr(newAscii)
        else:
            output += char
    time = datetime.datetime.now()
    record.append(["Encryption", time.strftime("%d/%m/%Y - %H:%M:%S"), s, output])
    return output

def findDiff(s):
    cnt = [0] * 26
    for char in s:
        intChar = ord(char)
        if isLetter(intChar):
            letterIndex = intChar - (97 if isSmall(intChar) else 65)
            cnt[letterIndex] += 1
    maxIndex = cnt.index(max(cnt))
    diff = maxIndex - 4
    return diff if diff >= 0 else diff + 26

def decrypt(s, k):
    output = ""
    for char in s:
        intChar = ord(char) # return ARCLL of 'char'
        if isLetter(intChar):
            if (intChar - k < 97 and isSmall(intChar)) or (intChar - k < 65 and not isSmall(intChar)): # prevent runtime error (out of range)
                newAscii = intChar - k + 26
            else:
                newAscii = intChar - k
            output += chr(newAscii)
        else:
            output += char
    if len(output.split()) > 200 or checkVocab(output):
        time = datetime.datetime.now()
        record.append(["Decryption", time.strftime("%d/%m/%Y - %H:%M:%S"), s, output])
        return output
    return decrypt(output, 1)

while True: #main loop of the program
    command = input("Command: ") # ask for commands
    commandList = command.split(" ") #split the commands in half  (name + number)
    if commandList[0] == "/quit":#identify the name
        sys.exit() # use system command to quit the program
    elif command == "/help":#identify the name
        print("/decrypt <operation type(1 / 2)> <file name> - decrypt the text \n /encrypt <operation type(1 / 2)> <file name> - encrypt the text \n /quit - exiting this application \n /hist - check the operation history in this session \n type 1 - input by the file that you provide and output the text to 'result.txt \n type 2 - input and output text through terminal") # print the instruction

    elif commandList[0] == "/hist":#identify the name
        checkHist(record) #print h=user history
    elif len(commandList) > 1:# if number is include in the command 
        contentBool = True#define content bool (if the file exits or not) and default as True (will be change)
        if commandList[1] == "1": #identify the number
            try:#check if the file user mentioned exits or not
                with open(commandList[2], "r", encoding="Latin-1") as f:
                    content = f.read()
            except FileNotFoundError:#if not exits:
                print("File not exist")
                contentBool = False #set contentBool False
        if contentBool:
            if commandList[0] == "/decrypt":#identify the name
                if commandList[1] == "2":#identify the number
                    content = input("Input the text you want to decrypt: ") #receive the string user want to decrypt
                output = decrypt(content, findDiff(content))
            elif commandList[0] == "/encrypt":#identify the name 
                if commandList[1] == "2":#identify the number
                    content = input("Input the text you want to encrypt: ")#receive the string user want to encrypt
                output = encrypt(content)
            outputProcess(output, int(commandList[1]))
    else:
        print("invaid command \ntype '/help' for help")
