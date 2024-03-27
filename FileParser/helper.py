import sys
import FileScanner.Lexeme as Lex
from FileScanner.Token.tokenOps import tokens as tokens

currLine = 0
currLineText = ""
currPos = 0
value = ""
astPos = 0
indentSize = 2

def entering(production, DEBUG):
    if DEBUG == 2 or DEBUG == 0:
        print(f"[PARSER] Entering {production}")

def exiting(production, DEBUG):
    if DEBUG == 2 or DEBUG == 0:
        print(f"[PARSER] Exiting {production}")

def getNextToken(file, debug, verbose):
    global currLine
    global currLineText
    global currPos
    global value
    nextToken, currPos, currLine, currLineText, value = Lex.scanNextToken(file, debug, verbose)

    return nextToken, value

def accept(loaded, token):
    global currLine
    global currLineText
    global currPos

    if loaded != token:
        spaces = errorSpaces(value)
        if currLineText[len(currLineText)-1] == "\n":
            currLineText = currLineText[:len(currLineText)-2]
        print(f"{currLine}: {currLineText}")
        print(f"{spaces}^ '{getTokenVal(token)}' expected")
        sys.exit()
    else:
        return True
    
def printTypeError():
    spaces = errorSpaces(value)
    if currLineText[len(currLineText)-1] == "\n":
        currLineText = currLineText[:len(currLineText)-2]
    print(f"{currLine}: {currLineText}")
    print(f"{spaces}^ int or char expected")
    sys.exit()
        
def errorSpaces(val):
    final = ""
    numSpaces = ((currPos) - 1) + 3
    for i in range(0,numSpaces):
        final += " "
    return final

def getTokenVal(tok):
    match(tok):
        case tokens.ID:
            return "an ID"
        case tokens.INT:
            return "keyword int"
        case tokens.CHAR:
            return "keyword char"
        case tokens.RETURN:
            return "keyword return"
        case tokens.IF:
            return "keyword if"
        case tokens.ELSE:
            return "keyword else"
        case tokens.FOR:
            pass
        case tokens.DO:
            pass
        case tokens.WHILE:
            return "keyword while"
        case tokens.SWITCH:
            pass
        case tokens.DEFAULT:
            pass
        case tokens.CASE:
            pass
        case tokens.WRITE:
            return "keyword write"
        case tokens.READ:
            return "keyword read"
        case tokens.CONTINUE:
            pass
        case tokens.BREAK:
            pass
        case tokens.NEWLINE:
            return "keyword newline"
        case tokens.NUMBER:
            pass
        case tokens.CHARLITERAL:
            pass
        case tokens.STRING:
            pass
        case tokens.SEMICOLON:
            return ";"
        case tokens.ASSIGN:
            pass
        case tokens.COLON:
            return ":"
        case tokens.ADDOP:
            pass
        case tokens.COMMA:
            return ","
        case tokens.MULOP:
            pass
        case tokens.RELOP:
            pass
        case tokens.LEFTBRACKET:
            return "["
        case tokens.RIGHTBRACKET:
            return "]"
        case tokens.LEFTCURLY:
            return "{"
        case tokens.RIGHTCURLY:
            return "}"
        case tokens.LEFTPAREN:
            return "("
        case tokens.RIGHTPAREN:
            return ")"
        case tokens.NOT:
            return "not"
        case tokens.EOF:
            return "eof"
        case tokens.NULL:
            pass

def indent():
    global astPos
    global indentSize
    astPos += indentSize

def outdent():
    global astPos
    global indentSize
    astPos -= indentSize

    if indentSize < 0:
        print("[Internal Error] illegal position in outdent")
        sys.exit()

def spaces():
    string = ""
    for i in range(0, astPos):
        string += " "

    return string