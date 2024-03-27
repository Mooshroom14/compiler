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

class ProgramTree:
    def createProgramTree(defList):
        return defList
    
    def printAST(ast, codeFile):
        print("\n<<< Abstract Syntax Tree >>>")
        print("Program (")
        helper.indent()
        print(f"{helper.spaces()}Source Code File: {codeFile}")
        for item in ast:
            DefinitionTree.printDefAST(item)
        helper.outdent()
        print(")")
        pass

class DefinitionTree:
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
        #print(f"{len(defAST)}")
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
                print(f"{helper.spaces()}Parameters: ({DefinitionTree.printParams(item[3][0])}),")
                print(f"{helper.spaces()}Body [")
                helper.indent()
                StatementTree.printStateAST(item[3][1])
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

class StatementTree:
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

        return statement
    
    def printStateAST(tree):
        for item in tree:
            print(item)
            print(f"{helper.spaces()}{item[0]} ", end = "")
            if item[0] == "blockState()":
                print("[")
                helper.indent()
                StatementTree.printStateAST(item[1])
                helper.outdent()
                print(f"\n{helper.spaces()}]")
            if item[0] == "ifState()":
                print("[")
                helper.indent()
                print(f"{helper.spaces()}Condition: {ExpressionTree.printExprAST(item[1][0])}")
                print(f"{helper.spaces()}Do: ")
                StatementTree.printStateAST(item[1][1])
                if item[1][2] != None:
                    print(f"{helper.spaces()}Else: ")
                    StatementTree.printStateAST(item[1][2])
            if item[0] == "varDef":
                helper.indent()
                print("(")
                print(f"{helper.spaces()}Type: {item[1]}, ID: {item[2]}")
                helper.outdent()
                print(f"{helper.spaces()})")
            if item[0] == "returnState()":
                if item[1] != None:
                    ExpressionTree.printExprAST(item[1])

class ExpressionTree:
    def createExpressionTree(prod, tree):
        statement = []
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
            return f"({tree[1]})"

class OperatorTree:
    def Operator(op):
        return ["Operator", op]

