from FileScanner.Token import fsm
from FileScanner.Token import tokenOps as to
import sys

commentBlock = False
commentBlockCt = 0
midString = False
midChar = False
currLine = 0
currPos = 0
lineBuffer = ""
charBuffer = ''
currLineText =""
currentState = fsm.States.start

def scanNextToken(codeFile, debug, verbose):
    # Set up globals
    global currPos
    global currentState
    global midString
    global midChar
    global commentBlock
    global commentBlockCt
    global charBuffer
    global lineBuffer
    global currLineText
    global currLine

    # Set current token to a blank string
    currToken = ""
    endToken = False
    char = ""
    # Set up line and block comment handling
    midString = False
    midChar = False
    commentBlock = False
    commentBlockCt = 0

    # Loop until it recieves a token
    while (not endToken):
        # File loading
        if (lineBuffer == ""):
            lineBuffer = codeFile.readline() 
            if not lineBuffer:
                currentState = fsm.States.endOfFileState
                currToken = "null"
                break
            currLineText = lineBuffer
            currPos = 0
            currLine += 1

        # Pop the next character
        if charBuffer != "":
            char = charBuffer
            charBuffer = ""
            currentState == fsm.newState(char, currentState)
        else:
            char = lineBuffer[0]
            lineBuffer = lineBuffer[1:]

        # Error Handling
        midString = True if (currentState == fsm.States.midString or currentState == fsm.States.noString) else False

        if (currentState == fsm.States.midChar or currentState == fsm.States.noChar):
            midChar = True  
        elif (currentState == fsm.States.CharToken or currentState == fsm.States.illegalCharState):
            midChar = False

        if currentState == fsm.States.commentLine:
            lineBuffer = ""
            currToken = ""
            currentState = fsm.States.start
            lineBuffer = codeFile.readline() 
            currLineText = lineBuffer
            currPos = 0
            currLine += 1

            continue

        if currentState == fsm.States.illegalTokenState:
            print("WARNING: Illegal Character/Token Detected")
            currentState = fsm.States.start
            currToken = ""
            continue

        if currentState == fsm.States.illegalCharState:
            print("ERROR: CHARLITERALs cannot contain newline characters!")
            sys.exit()
        elif midChar and fsm.newState(char,currentState) != fsm.States.CharToken and fsm.newState(char, currentState) != fsm.States.illegalCharState:
            print("ERROR: Unterminated Charliteral!")
            sys.exit()
        
        if currentState == fsm.States.illegalStringState:
            print("ERROR: STRINGs cannot contain newline characters!")
            sys.exit()       

        # Check if we have the end of a token 
        #   by checking if there is the start of a token in the next character
        if fsm.isTokenState(currentState):
            match currentState:
                case fsm.States.ID_token:
                    if char == '(':
                        endToken = True
                    elif char == ';':
                        endToken = True
                    elif char == ')':
                        endToken = True
                    elif char == ',':
                        endToken = True
                    else:
                        endToken = False
                case fsm.States.NumToken:
                    if char == ')':
                        endToken = True
                    elif char == ';':
                        endToken = True
                    else:
                        endToken = False
                case fsm.States.LeftParen:
                    if char == "\"":
                        endToken = True
                    elif char.isalpha():
                        endToken = True
                    elif char == "(":
                        endToken = True
                    elif char == ")":
                        endToken = True
                    else:
                        endToken = False
                case fsm.States.StringToken:
                    if char == ")":
                        endToken = True
                    else:
                        endToken = False
                case fsm.States.RightParen:
                    if char == "{":
                        endToken = True
                    elif char == ";":
                        endToken = True
                    elif char == "=":
                        endToken = True
                    else:
                        endToken = False
                case fsm.States.SemiToken:
                    if char == "}":
                        endToken = True
                    else:
                        endToken = False
                case _ :
                    pass
            if endToken:
                charBuffer = char
                break
        # Check if we have run into white space
        if (char == ' ' or char == '\n'):
            if midString:
                currentState = fsm.newState(char, currentState)
                currToken += char
                currPos += 1
            elif currentState == fsm.States.start:
                currPos += 1
                continue               
            else:
                currPos += 1
                if not commentBlock:
                    break
                currentState = fsm.States.start
                currToken = ""
        # Check if we are at the end of the line
        #   and automatically end the token
        elif currPos == len(currLineText):
            currToken += char
            lineBuffer == ""
            endToken = True
            currentState = fsm.States.start
            break
        else:
            # Add current character to the current token
            currToken += char
            # Advance the state machine
            currentState = fsm.newState(char, currentState)
            # Advance the cursor 
            currPos += 1

    # If debug is on, print the token
    if (debug == 0 or debug == 1 or verbose):
        to.printToken(fsm.States, currentState, currToken)
    # Convert to token format
    token = to.returnToken(fsm.States, currentState, currToken)
    # Restore state machine to initial state
    currentState = fsm.States.start
    return token, currPos, currLine, currLineText, currToken