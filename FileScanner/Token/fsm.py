from enum import Enum

""" 
    Start state
    based on next char switch state


"""
class States(Enum): 
    start = 1
    ID_token = 2
    NumToken = 3
    initChar = 4
    midChar = 5
    CharToken = 6
    midString = 7
    StringToken = 8
    AssignToken = 9
    RelopToken = 10
    divisor = 11
    MulopToken = 12
    LeftParen = 13
    RightParen = 14
    LeftCurly = 15
    RightCurly = 16
    LeftBracket = 17
    RightBracket = 18
    CommaToken = 19
    SemiToken = 20
    ColonToken = 21
    midRelop = 22
    errorState = 23
    commentLine = 24
    commentBlockStart = 25
    AddOpToken = 26
    midAddOp = 27
    NotToken = 28
    commentBlockEnd = 29
    Multiply = 30
    illegalTokenState = 31
    noChar = 32
    illegalCharState = 33
    noString = 34
    illegalStringState = 35
    decimal = 36
    exponState = 37
    signState = 38
    endOfFileState = 39
   
tokenStates = [States.AddOpToken, States.AssignToken, States.CharToken, States.ColonToken,
               States.CommaToken, States.ID_token, States.LeftBracket, States.LeftCurly,
               States.LeftParen, States.MulopToken, States.NotToken, States.NumToken,
               States.RelopToken, States.RightBracket, States.RightCurly, States.RightParen,
               States.SemiToken, States.StringToken, States.midRelop, States.Multiply,
               States.divisor]

def newState(char, currentState): # Finite State Machine
    match currentState:
        case States.start:
            if char.isalpha():
                return States.ID_token
            elif char.isdigit():
                return States.NumToken
            elif char == "'":
                return States.initChar
            elif char == "\"":
                return States.midString
            elif char == "=":
                return States.AssignToken
            elif (char == "!"):
                return States.NotToken
            elif (char == "<" or char == ">"):
                return States.midRelop
            elif (char == "*"):
                return States.Multiply
            elif (char == "%" or char == "&"):
                return States.MulopToken
            elif char == "/":
                return States.divisor
            elif char == "(":
                return States.LeftParen
            elif char == ")":
                return States.RightParen
            elif char == "{":
                return States.LeftCurly
            elif char == "}":
                return States.RightCurly
            elif char == "[":
                return States.LeftBracket
            elif char == "]":
                return States.RightBracket
            elif char == ",":
                return States.CommaToken
            elif char == ":":
                return States.ColonToken
            elif char == ";":
                return States.SemiToken
            elif (char == "+" or char == "-"):
                return States.AddOpToken
            elif char == "|":
                return States.midAddOp
            else:
                return States.illegalTokenState
        case States.ID_token:
            if (char.isalpha() or char.isdigit()):
                return States.ID_token
            else:
                return States.errorState
        case States.NumToken:
            if char.isdigit():
                return States.NumToken
            elif (char == 'e' or char == 'E'):
                return States.exponState
            elif char == ".":
                return States.decimal
            else:
                return States.errorState
        case States.decimal:
            if char.isdigit():
                return States.NumToken
            else:
                return States.errorState
        case States.exponState:
            if char == "+" or char == "-":
                return States.signState
            else:
                return States.errorState
        case States.signState:
            if char.isdigit():
                return States.NumToken
            else:
                return States.errorState
        case States.initChar:
            if char == "'":
                return States.CharToken
            elif char == "\\":
                return States.noChar
            elif char != "\n":
                return States.midChar
            else:
                return States.errorState
        case States.midChar:
            if char == "'":
                return States.CharToken
            else:
                return States.errorState
        case States.midString:
            if char == "\\":
                return States.noString
            elif char != '\n' and char != "\"" or char == ' ':
                return States.midString
            elif char == "\"":
                return States.StringToken
            else:
                return States.errorState
        case States.noString:
            if char == "n":
                return States.illegalStringState
            elif char != '\n' and char != "\"" or char == ' ':
                return States.midString
            elif char == "\"":
                return States.StringToken
            else:
                return States.errorState
        case States.midRelop:
            if char == "=":
                return States.RelopToken
            else:
                return States.errorState
        case States.Multiply:
            if char == "/":
                return States.commentBlockEnd
            else:
                return States.errorState
        case States.MulopToken:
            if char == "&":
                return States.MulopToken
            else:
                return States.errorState
        case States.midAddOp:
            if char == "|":
                return States.AddOpToken
            else:
                return States.errorState
        case States.NotToken:
            if char == "=":
                return States.RelopToken
            else:
                return States.errorState
        case States.divisor:
            if char == "/":
                return States.commentLine
            elif char == "*":
                return States.commentBlockStart
            else:
                return States.errorState
        case States.noChar:
            if char == "n":
                return States.illegalCharState
            elif char =="'":
                return States.CharToken
            else:
                return States.errorState
        case States.AssignToken:
            if char == "=":
                return States.RelopToken
            else:
                return States.errorState

def isTokenState(tokenState):
    return True if tokenState in tokenStates else False  