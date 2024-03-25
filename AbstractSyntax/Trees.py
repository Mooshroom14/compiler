from enum import Enum
from FileParser import helper

class productions(Enum):
    prDef = 0
    prType = 1
    prFuncDef = 2
    prFuncHead = 3
    prFuncBody = 4
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
                print(f"{helper.spaces()}Type: {item[1]},")
                print(f"{helper.spaces()}ID: {item[2]},")
                helper.outdent()
                print(f"{helper.spaces()})")
            elif item[0] == "funcDef":
                print(f"{helper.spaces()}funcDef (")
                helper.indent()
                print(f"{helper.spaces()}Type: {item[1]},")
                print(f"{helper.spaces()}ID: {item[2]},")
                print(f"{helper.spaces()}Parameters: {item[3][0]},")
                print(f"{helper.spaces()}Body: {item[3][1]}")
                helper.outdent()
                print(f"{helper.spaces()})")

        helper.outdent()
        print(f"{helper.spaces()}]")
        pass

class StatementTree:
    def createStatementTree(prod):
        statement = ""
        match(prod):
            case productions.prBreak:
                statement = "breakState()"
            case productions.prNewline:
                statement = "newLineState()"
            case productions.prNull:
                statement = "nullState()"

        return statement

class ExpressionTree:
    def createExpressionTree(prod):
        statement = ""
        match(prod):
            case productions.prFuncCall:
                statement = "funcCall()"
            case productions.prExpression:
                statement = "expr()"
            case productions.prMinus:
                statement = "minus()"
            case productions.prNot:
                statement = "not()"

        return statement

class OperatorTree:
    def Operator(op):
        return ["Operator", op]

