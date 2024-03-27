from enum import Enum
from FileParser import helper

class productions(Enum):
    prDef = 0
    prType = 1
    prFuncDef = 2
    prFuncHead = 3
   # prFuncBody = 4
    prFormalParams = 5
    prStatement = 6
    prExprStatement = 7
    prBreak = 8
    prCompound = 9
    prIf = 10
    prNull = 11
    prReturn = 12
    prWhile = 13
    prRead = 14
    prWrite = 15
    prNewline = 16
    prExpression = 17
    prRelopExpr = 18
    prSimpleExpr = 19
    prTerm = 20
    prPrimary = 21
    prFuncCall = 22
    prActualParams = 23
    prMinus = 24
    prNot = 25
    terOperator = 26
    terNum = 27
    terID = 28
    terCharLit = 29
    terStringLit = 30


def createProgramTree(defList):
    return defList

def printAST(ast, codeFile):
    print("\n<<< Abstract Syntax Tree >>>")
    print("Program (")
    helper.indent()
    print(f"{helper.spaces()}Source Code File: {codeFile}")
    for item in ast:
        printDefAST(item)
    helper.outdent()
    print(")")
    pass


def createDefinitionTree(ID, prod, value, tree):
    definition = []
    match(prod):
        case productions.prFuncDef:
            definition.append(["funcDef", ID, value, tree])
        case None:
            definition.append(["varDef", ID, value])

    return definition

def printDefAST(defAST):
    print(f"{helper.spaces()}Definition [")
    helper.indent()
    for item in defAST:
        if item[0] == "varDef":
            print(f"{helper.spaces()}varDef (")
            helper.indent()
            print(f"{helper.spaces()}Type: {item[0][1]}, ID: {item[0][2]}")
            helper.outdent()
            print(f"{helper.spaces()})")
        elif item[0] == "funcDef":
            print(f"{helper.spaces()}funcDef (")
            helper.indent()
            print(f"{helper.spaces()}Type: {item[1]},")
            print(f"{helper.spaces()}ID: {item[2]},")
            print(f"{helper.spaces()}Parameters: ({printParams(item[3][0])}),")
            print(f"{helper.spaces()}Body [")
            helper.indent()
            for i in item[3][1]:
                printStateAST(i)
            helper.outdent()
            print(f"{helper.spaces()}]")
            helper.outdent()
            print(f"{helper.spaces()})")

    helper.outdent()
    print(f"{helper.spaces()}]")
    pass

def printParams(paramList):
    string = ""
    for count, item in enumerate(paramList):
        string += f"{item[0]}"
        string += " "
        string += f"{item[1]}"
        if count != len(paramList)-1:
            string += ", "
    return string


def createStatementTree(prod, tree):
    statement = []
    match(prod):
        case productions.prBreak:
            statement = ["breakState()"]
        case productions.prNewline:
            statement = ["newLineState()"]
        case productions.prNull:
            statement = ["nullState()"]
        case productions.prIf:
            statement = ["ifState()", tree]
        case productions.prCompound:
            statement = ["blockState()", tree]
        case productions.prReturn:
            statement = ["returnState()", tree]
        case productions.prWhile:
            statement = ["whileState()", tree]
        case productions.prWrite:
            statement = ["writeState()", tree] 
        case productions.prRead:
            statement = ["readState()", tree]
        case productions.prExprStatement:
            statement = ["exprState()", tree]

    return statement

def printStateAST(tree):
    print(f"{helper.spaces()}{tree[0]} ", end = "")
    if tree[0] == "blockState()":
        print("[")
        helper.indent()
        for item in tree[1]:
            printStateAST(item)
        helper.outdent()
        print(f"\n{helper.spaces()}]")
    if tree[0] == "ifState()":
        print("[")
        helper.indent()
        print(f"{helper.spaces()}Condition: ")
        helper.indent()
        printExprAST([tree[1][0]])
        helper.outdent()
        print(f"{helper.spaces()}Do: ")
        helper.indent()
        #print(item[1][1])
        printStateAST(tree[1][1])
        if tree[1][2] != None:
            helper.outdent()
            print(f"{helper.spaces()}Else: ")
            helper.indent()
            printStateAST(tree[1][2])
        helper.outdent()
    if tree[0] == "varDef":
        print("(")
        helper.indent()
        print(f"{helper.spaces()}Type: {tree[1]}, ID: {tree[2]}")
        helper.outdent()
        print(f"{helper.spaces()})")
    if tree[0] == "returnState()":
        print(" [")
        if tree[1] != None:
            helper.indent()
            printExprAST(tree[1])
            helper.outdent()
            print(f"{helper.spaces()}]")
    if tree[0] == "exprState()":
        helper.indent()
        print("[")
        printExprAST(tree[1])
        print(f"{helper.spaces()}]")
        helper.outdent()
    if tree[0] == "whileState()":
        print(" [")
        helper.indent()
        print(f"{helper.spaces()}Condition: ")
        printExprAST(tree[1][0])
        print(f"{helper.spaces()}Do: ")
        helper.indent()
        printStateAST(tree[1][1])
        helper.outdent()
        print(f"{helper.spaces()}]")
    if tree[0] == "writeState()":
        print(" [")
        helper.indent()
        printExprAST(tree[1])
        helper.outdent()
        print(f"{helper.spaces()}]")
    if tree[0] == "newLineState()":
        print("")
    if tree[0] == "breakState()":
        print("")
    if tree[0] == "readState()":
        print(" [")
        helper.indent()
        printExprAST(tree[1])
        helper.outdent()
        print(f"{helper.spaces()}]")

def createExpressionTree(prod, tree):
    statement = ""
    match(prod):
        case productions.prFuncCall:
            statement = ["funcCall()", tree]
        case productions.prExpression:
            statement = ["expr()", tree]
        case productions.prMinus:
            statement = ["minus()", tree]
        case productions.prNot:
            statement = ["not()", tree]
        case productions.terNum:
            statement = ["Number", tree]
        case productions.terCharLit:
            statement = ["CharLiteral", tree]
        case productions.terID:
            statement = ["ID", tree]
        case productions.terStringLit:
            statement = ["StringLiteral", tree]

    return statement

def printExprAST(tree):
    if tree[0] == "expr()":
        if len(tree[1]) == 3:
            helper.indent()
            for item in tree[1]:
                printExprAST(item)
            helper.outdent()
        else:
            printExprAST(tree[1])
    elif tree[0] == "ID":
        print(f"{helper.spaces()}ID: {tree[1]} ")
    elif tree[0] == "Number":
        print(f"{helper.spaces()}Number: {tree[1]} ")
    elif tree[0] == "Operator":
        print(f"{helper.spaces()}Operator: {tree[1]} ")
    elif tree[0] == "CharLiteral":
        print(f"{helper.spaces()}Char Literal: {tree[1]} ")
    elif tree[0] == "StringLiteral":
        print(f"{helper.spaces()}String: {tree[1]} ")  
    elif tree[0] == "funcCall()":
        print(f"{helper.spaces()}Function Call( ")
        helper.indent()
        print(f"{helper.spaces()}ID: {tree[1]}")
        print(f"{helper.spaces()}Parameters: ")
        helper.indent()
        printExprAST(tree[2])
        helper.outdent()
        helper.outdent()
        print(f"{helper.spaces()})")
    elif tree[0] == "minus()" or tree[0] == "not()":
        printExprAST(tree[1])
    else:
        printExprAST(tree[0])          

def Operator(op):
    return ["Operator", op]

