from FileParser import helper
from FileScanner.Token.tokenOps import tokens as tokens
from AbstractSyntax import Trees
import sys

debug = 4
activeToken = ""
codeFile = ""
currTokenVal = ""

def setup(file, DEBUG):
   global debug 
   global codeFile
   debug = DEBUG
   codeFile = file
    
def loadToken():
    global activeToken
    global currTokenVal
    activeToken, currTokenVal = helper.getNextToken(codeFile, debug, False)

def Program():
    defList = []
    helper.entering("Program", debug)
    loadToken()
    while (activeToken != tokens.EOF):
        defList.append(definition())
        loadToken()
    helper.accept(activeToken, tokens.EOF)
    helper.exiting("Program", debug)
    if debug == 0 or debug == 2:
        print("[PARSER] Successful Parse!")
    return Trees.ProgramTree.createProgramTree(defList)

def definition():
    helper.entering("Definition", debug)
    ID, value = Type()
    loadToken()
    if (activeToken == tokens.LEFTPAREN):
        loadToken()
        prod = Trees.productions.prFuncDef
        funcDefTree = FunctionDefinition()
    elif (activeToken == tokens.SEMICOLON):
        prod = None
    helper.exiting("Definition", debug)
    return Trees.DefinitionTree.createDefinitionTree(ID, prod, value, funcDefTree)

def Type():
    helper.entering("Type", debug)
    if (activeToken == tokens.CHAR):
        prod = "char"
        loadToken()
        helper.accept(activeToken, tokens.ID)
    elif (activeToken == tokens.INT):
        prod = "int"
        loadToken()
        helper.accept(activeToken, tokens.ID)
    else:
        print("ERROR: Illegal Type!")
        sys.exit()
    val = currTokenVal
    helper.exiting("Type", debug)
    return prod,val

def FunctionDefinition():
    helper.entering("Function Definition", debug)
    header = FunctionHeader()
    body = FunctionBody()
    helper.exiting("Function Definition", debug)
    return [header,body]

def FunctionHeader():
    helper.entering("Function Header", debug)
    params = []
    if activeToken != tokens.RIGHTPAREN:
        params = FormalParamList()
        helper.accept(activeToken, tokens.RIGHTPAREN)
    else:
        helper.accept(activeToken, tokens.RIGHTPAREN)
    helper.exiting("Function Header", debug)
    return params

def FunctionBody():
    helper.entering("Function Body", debug)
    loadToken()
    helper.accept(activeToken, tokens.LEFTCURLY)
    body = CompoundStatement()
    helper.exiting("Function Body", debug)
    return body

def FormalParamList():
    helper.entering("Formal Parameter List", debug)
    params = []
    while(activeToken != tokens.RIGHTPAREN):
        ID, var = Type()
        loadToken()
        params.append([ID, var])
        if activeToken == tokens.COMMA:
           loadToken()
    helper.exiting("Formal Parameter List", debug)
    return params

def Statement():
    helper.entering("Statement", debug)
    tree = []
    match(activeToken):
        case tokens.IF:
            prod = Trees.productions.prIf
            tree = ifStatement()
        case tokens.RETURN:
            prod = Trees.productions.prReturn
            tree.append(ReturnStatement())
        case tokens.BREAK:
            prod = Trees.productions.prBreak
            tree.append(breakStatement())
        case tokens.LEFTCURLY:
            prod = Trees.productions.prCompound
            tree.append(CompoundStatement())
        case tokens.SEMICOLON:
            prod = Trees.productions.prNull
            tree.append(NullStatement())
        case tokens.WHILE:
            prod = Trees.productions.prWhile
            tree.append(WhileStatement())
        case tokens.READ:
            prod = Trees.productions.prRead
            tree.append(ReadStatement())
        case tokens.WRITE:
            prod = Trees.productions.prWrite
            tree.append(WriteStatement())
        case tokens.NEWLINE:
            prod = Trees.productions.prNewline
            tree.append(newLineStatement())
        case _:
            prod = Trees.productions.prExprStatement
            tree.append(ExpressionStatement())
    helper.exiting("Statement", debug)
    return Trees.StatementTree.createStatementTree(prod, tree)

def ExpressionStatement():
    helper.entering("Expression Statement", debug)
    tree = Expression()
    helper.accept(activeToken, tokens.SEMICOLON)
    helper.exiting("Expression Statement", debug)
    return Trees.ExpressionTree.createExpressionTree("expr()", tree)

def breakStatement():
    helper.entering("Break Statement", debug)
    loadToken()
    helper.accept(activeToken, tokens.SEMICOLON)
    helper.exiting("Break Statement", debug)
    return "break"

def CompoundStatement():
    helper.entering("Compound Statement", debug)
    statementList = []
    loadToken()
    while(activeToken != tokens.RIGHTCURLY):
        if(activeToken == tokens.INT or activeToken == tokens.CHAR):
            ID, value = Type()
            loadToken()
            helper.accept(activeToken, tokens.SEMICOLON)
            statementList.append(["varDef", ID, value])
            loadToken()
        else:
            statementList.append(Statement())
            loadToken()
    
    helper.accept(activeToken, tokens.RIGHTCURLY)
    helper.exiting("Compound Statement", debug)
    return statementList

def ifStatement():
    helper.entering("If Statement", debug)
    ifTree = []
    loadToken()
    helper.accept(activeToken, tokens.LEFTPAREN)
    loadToken()
    ifTree.append(["expr()", Expression()])
    helper.accept(activeToken, tokens.RIGHTPAREN)
    loadToken()
    ifTree.append(Statement())
    loadToken()
    if activeToken == tokens.ELSE:
        loadToken()
        ifTree.append(Statement())
    else:
        ifTree.append(None)
    helper.exiting("If Statement", debug)
    return ifTree

def NullStatement():
    helper.entering("Null Statement", debug)
    helper.exiting("Null Statement", debug)
    return "null"

def ReturnStatement():
    helper.entering("Return Statement", debug)
    loadToken()
    Expression()
    helper.accept(activeToken, tokens.SEMICOLON)
    #loadToken()
    helper.exiting("Return Statement", debug)
    return Trees.productions.prReturn

def WhileStatement():
    helper.entering("While Statement", debug)
    loadToken()
    helper.accept(activeToken, tokens.LEFTPAREN)
    loadToken()
    Expression()
    helper.accept(activeToken, tokens.RIGHTPAREN)
    loadToken()
    Statement()
    helper.exiting("While Statement", debug)

def ReadStatement():
    helper.entering("Read Statement", debug)
    loadToken()
    helper.accept(activeToken, tokens.SEMICOLON)
    helper.exiting("Read Statement", debug)
    return Trees.productions.prRead

def WriteStatement():
    helper.entering("Write Statement", debug)
    loadToken()
    helper.accept(activeToken, tokens.LEFTPAREN)
    loadToken()
    ActualParameters()
    helper.accept(activeToken, tokens.RIGHTPAREN)
    loadToken()
    helper.accept(activeToken, tokens.SEMICOLON)
    helper.exiting("Write Statement", debug)
    return Trees.productions.prWrite

def newLineStatement():
    helper.entering("Newline Statement", debug)
    loadToken()
    helper.accept(activeToken, tokens.SEMICOLON)
    helper.exiting("Newline Statement", debug)
    return "newline"

def Expression():
    helper.entering("Expression", debug)
    tree = []
    tree.append(RelopExpression())
    if activeToken == tokens.ASSIGN:
        tree.append(Trees.OperatorTree.Operator(currTokenVal))
        loadToken()
        tree.append(RelopExpression())
    helper.exiting("Expression", debug)
    return Trees.ExpressionTree.createExpressionTree(None, tree)

def RelopExpression():
    helper.entering("Relop Expression", debug)
    tree = []
    tree.append(SimpleExpression())
    if activeToken == tokens.RELOP:
        tree.append(Trees.OperatorTree.Operator(currTokenVal))
        loadToken()
        tree.append(SimpleExpression())
    helper.exiting("Relop Expression", debug)
    return Trees.ExpressionTree.createExpressionTree(None, tree)

def SimpleExpression():
    helper.entering("Simple Expression", debug)
    tree = []
    tree.append(Term())
    #loadToken()
    if activeToken == tokens.ADDOP:
        tree.append(Trees.OperatorTree.Operator(currTokenVal))
        loadToken()
        tree.append(Term())
    helper.exiting("Simple Expression", debug)
    return tree

def Term():
    helper.entering("Term", debug)
    tree = []
    tree.append(Primary())
    if activeToken == tokens.MULOP:
        tree.append(Trees.OperatorTree.Operator(currTokenVal))
        loadToken()
        tree.append(Primary())
    helper.exiting("Term", debug)
    return tree

def Primary():
    helper.entering("Primary", debug)
    #loadToken()
    tree = []
    ID = ""
    prod = ""
    match(activeToken):
        case tokens.LEFTPAREN:
            loadToken()
            tree.append(Expression())
            helper.accept(activeToken, tokens.RIGHTPAREN)
            loadToken()
        case tokens.ID:
            ID = currTokenVal
            loadToken()
            if activeToken == tokens.LEFTPAREN:
                tree.append(["funcCall()", ID, FunctionCall()])
                helper.accept(activeToken, tokens.RIGHTPAREN)
            else:
                prod = Trees.productions.terID
                tree.append(Trees.ExpressionTree.createExpressionTree(prod, currTokenVal))
        case tokens.NOT:
            loadToken()
            tree.append(["not()", Primary()])   
        case tokens.NUMBER:
            prod = Trees.productions.terNum
            tree.append(Trees.ExpressionTree.createExpressionTree(prod, currTokenVal))
            loadToken()
        case tokens.STRING:
            prod = Trees.productions.terStringLit
            tree.append(Trees.ExpressionTree.createExpressionTree(prod, currTokenVal))
            loadToken()
        case tokens.CHARLITERAL:
            prod = Trees.productions.terCharLit
            tree.append(Trees.ExpressionTree.createExpressionTree(prod, currTokenVal))
            loadToken()
        
    if currTokenVal == "-":
        loadToken()
        tree.append(["minus()", Primary()])

    helper.exiting("Primary", debug)
    return tree

def FunctionCall():
    helper.entering("Function Call", debug)
    loadToken()
    if activeToken != tokens.RIGHTPAREN:
        tree = ActualParameters()
    else:
        tree = None
    loadToken()
    helper.accept(activeToken, tokens.RIGHTPAREN)
    helper.exiting("Function Call", debug)
    return tree

def ActualParameters():
    helper.entering("Actual Parameters", debug)
    params = []
    params.append(Expression())
    while activeToken == tokens.COMMA:
        loadToken()
        params.append(Expression())
    helper.exiting("Actual Parameters", debug)
    return params