import sys
import random
import datetime

record = []
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

try:
    with open("bannedVocab.txt","r") as s:
        bannedVocab = s.read().splitlines()
except FileNotFoundError:
    print("bannedVocab.txt file not found. \n run without it?\n")
    temp = input("T / F: ")
    if temp == "T":
        print(":)")
    else:
        sys.exit()



print("Caesar cipher encrypt and decrypt service\ntype '/help' for help")

def checkHist(arr):
    for i, rec in enumerate(arr):
        print(f"Record {i + 1}:\nTime: {rec[1]}\nOperation Type: {rec[0]}\nInput: {rec[2]}\nOutput: {rec[3]}")

def checkVocab(s):
    outputVocab = s.lower().split()
    cnt = 0
    for word in outputVocab:
        if word in vocab:
            cnt += 1
            if cnt > len(outputVocab) / 6:
                return True
    return False

def isSmall(k):
    return 97 <= k <= 122

def isLetter(k):
    return 65 <= k <= 90 or isSmall(k)

def outputProcess(s, type):
    if type == 1:
        try:
            with open("result.txt", "w", encoding="Latin-1") as g:
                g.write(s)
            print("Done!")
        except IOError:
            print("Error writing to result.txt")
    else:
        print("Output: " + s)

def encrypt(s):
    k = random.randint(1, 25)
    output = ""
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
        intChar = ord(char)
        if isLetter(intChar):
            if (intChar - k < 97 and isSmall(intChar)) or (intChar - k < 65 and not isSmall(intChar)):
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

while True:
    command = input("Command: ")
    commandList = command.split(" ")
    if commandList[0] == "/quit":
        sys.exit()
    elif command == "/help":
        print("/decrypt <operation type(1 / 2)> <file name> - decrypt the text")
        print("/encrypt <operation type(1 / 2)> <file name> - encrypt the text")
        print("/quit - exiting this application")
        print("/hist - check the operation history in this session")
        print("type 1 - input by the file that you provide and output the text to 'result.txt'")
        print("type 2 - input and output text through terminal")
    elif commandList[0] == "/hist":
        checkHist(record)
    elif len(commandList) > 1:
        contentBool = True
        if commandList[1] == "1":
            try:
                with open(commandList[2], "r", encoding="Latin-1") as f:
                    content = f.read()
            except FileNotFoundError:
                print("File not exist")
                contentBool = False
        if contentBool:
            if commandList[0] == "/decrypt":
                if commandList[1] == "2":
                    content = input("Input the text you want to decrypt: ")
                output = decrypt(content, findDiff(content))
            elif commandList[0] == "/encrypt":
                if commandList[1] == "2":
                    content = input("Input the text you want to encrypt: ")
                output = encrypt(content)
            outputProcess(output, int(commandList[1]))
    else:
        print("invaid command \ntype '/help' for help")
