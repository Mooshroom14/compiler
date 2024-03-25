from enum import Enum

def printToken(tokens, state, value):
    string = "[SCANNER] token "
    match state:
        case tokens.ID_token:
            if keyWordLookup(value):
                token = value.upper()
                string += f"{token} "
            else:
                string += "ID "
        case tokens.NumToken:
            string += "NUMBER "
        case tokens.CharToken:
            string += "CHARLITERAL "
        case tokens.StringToken:
            string += "STRING "
        case tokens.SemiToken:
            string += "SEMICOLON "
        case tokens.AssignToken:
            string += "ASSIGNOP "
        case tokens.ColonToken:
            string += "COLON "
        case tokens.AddOpToken:
            string += "ADDOP "
        case tokens.CommaToken:
            string += "COMMA "
        case tokens.MulopToken:
            string += "MULOP "
        case tokens.RelopToken:
            string += "RELOP "
        case tokens.LeftParen:
            string += "LEFTPAREN "
        case tokens.RightParen:
            string += "RIGHTPAREN "
        case tokens.LeftBracket:
            string += "LEFTBRACKET "
        case tokens.RightBracket:
            string += "RIGHTBRACKET "
        case tokens.LeftCurly:
            string += "LEFTCURLY "
        case tokens.RightCurly:
            string += "RIGHTCURLY "
        case tokens.midRelop:
            string += "RELOP "
        case tokens.Multiply:
            string += "MULOP "
        case tokens.divisor:
            string += "MULOP, "
        case tokens.NotToken:
            string += "NOT "
        case tokens.endOfFileState:
            string += "EOF "
        
    string += f"{value}"
    if value == ' ':
        print("Space")
    if value != ' ':
        print(string)

keys = ["int","char","return","if","else","for","do","while","switch","case","default","write","read","continue","break","newline"]

def keyWordLookup(string):
    if string in keys:
        return True
    else:
        return False
    
class tokens(Enum):
    INT = 1
    CHAR = 2
    RETURN = 3
    IF = 4
    ELSE = 5
    FOR = 6
    DO = 7
    WHILE = 8
    SWITCH = 9
    CASE = 10
    DEFAULT = 11
    WRITE = 12
    READ = 13
    CONTINUE = 14
    BREAK = 15
    NEWLINE = 16
    ID = 17
    NUMBER = 18
    CHARLITERAL = 19
    STRING = 20
    SEMICOLON = 21
    ASSIGN = 22
    COLON = 23
    ADDOP = 24
    COMMA = 25
    MULOP = 26
    RELOP = 27
    LEFTPAREN = 28
    RIGHTPAREN = 29
    LEFTBRACKET = 30
    RIGHTBRACKET = 31
    LEFTCURLY = 32
    RIGHTCURLY = 33
    NOT = 34
    EOF = 35
    NULL = 36
        
def returnToken(intokens, state, value):
    match state:
        case intokens.ID_token:
            if keyWordLookup(value):
                match value:
                    case "int":
                        return tokens.INT
                    case "char":
                        return tokens.CHAR
                    case "return":
                        return tokens.RETURN
                    case "if":
                        return tokens.IF
                    case "else":
                        return tokens.ELSE
                    case "for":
                        return tokens.FOR
                    case "do":
                        return tokens.DO
                    case "while":
                        return tokens.WHILE
                    case "switch":
                        return tokens.SWITCH
                    case "case":
                        return tokens.CASE
                    case "default":
                        return tokens.DEFAULT
                    case "write":
                        return tokens.WRITE
                    case "read":
                        return tokens.READ
                    case "continue":
                        return tokens.CONTINUE
                    case "break":
                        return tokens.BREAK
                    case "newline":
                        return tokens.NEWLINE
            else:
                return tokens.ID
        case intokens.NumToken:
            return tokens.NUMBER
        case intokens.CharToken:
            return tokens.CHARLITERAL
        case intokens.StringToken:
            return tokens.STRING
        case intokens.SemiToken:
            return tokens.SEMICOLON
        case intokens.AssignToken:
            return tokens.ASSIGN
        case intokens.ColonToken:
            return tokens.COLON
        case intokens.AddOpToken:
            return tokens.ADDOP
        case intokens.CommaToken:
            return tokens.COMMA
        case intokens.MulopToken:
            return tokens.MULOP
        case intokens.RelopToken:
            return tokens.RELOP
        case intokens.LeftParen:
            return tokens.LEFTPAREN
        case intokens.RightParen:
            return tokens.RIGHTPAREN
        case intokens.LeftBracket:
            return tokens.LEFTBRACKET
        case intokens.RightBracket:
            return tokens.RIGHTBRACKET
        case intokens.LeftCurly:
            return tokens.LEFTCURLY
        case intokens.RightCurly:
            return tokens.RIGHTCURLY
        case intokens.midRelop:
            return tokens.RELOP
        case intokens.Multiply:
            return tokens.MULOP
        case intokens.divisor:
            return tokens.MULOP
        case intokens.NotToken:
            return tokens.NOT
        case intokens.endOfFileState:
            return tokens.EOF
