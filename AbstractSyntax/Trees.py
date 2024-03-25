from enum import Enum

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


class ProgramTree:
    def createProgramTree(defList):
        return defList

class DefinitionTree:
    def createDefinitionTree(ID, prod):
        match(prod):
            case productions.prFuncDef:
                pass
            case _:
                pass

class StatementTree:
    def createStatementTree(prod):
        statement = ""
        match(prod):
            case productions.prBreak:
                statement = "breakState()"

        return statement

class ExpressionTree:
    def createExpressionTree(prod):
        pass

class OperatorTree:
    def Operator(op):
        return ["Operator", op]

