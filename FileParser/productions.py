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
    print("[PARSER] Successful Parse!")
    return Trees.ProgramTree.createProgramTree(defList)

def definition():
    helper.entering("Definition", debug)
    ID = Type()
    loadToken()
    if (activeToken == tokens.LEFTPAREN):
        loadToken()
        prod = FunctionDefinition()
    elif (activeToken == tokens.SEMICOLON):
        prod = None
    helper.exiting("Definition", debug)
    return Trees.DefinitionTree.createDefinitionTree(ID, prod)

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
    helper.exiting("Type", debug)
    return prod

def FunctionDefinition():
    helper.entering("Function Definition", debug)
    header = FunctionHeader()
    body = FunctionBody()
    helper.exiting("Function Definition", debug)
    return header,body

def FunctionHeader():
    helper.entering("Function Header", debug)
    if activeToken != tokens.RIGHTPAREN:
        FormalParamList()
        helper.accept(activeToken, tokens.RIGHTPAREN)
    else:
        helper.accept(activeToken, tokens.RIGHTPAREN)
    helper.exiting("Function Header", debug)

def FunctionBody():
    helper.entering("Function Body", debug)
    loadToken()
    helper.accept(activeToken, tokens.LEFTCURLY)
    CompoundStatement()
    helper.exiting("Function Body", debug)

def FormalParamList():
    helper.entering("Formal Parameter List", debug)
    while(activeToken != tokens.RIGHTPAREN):
       Type()
       loadToken()
       if activeToken == tokens.COMMA:
           loadToken()
    helper.exiting("Formal Parameter List", debug)

def Statement():
    helper.entering("Statement", debug)
    match(activeToken):
        case tokens.IF:
            prod = ifStatement()
        case tokens.RETURN:
            prod = ReturnStatement()
        case tokens.BREAK:
            prod = breakStatement()
        case tokens.LEFTCURLY:
            prod = CompoundStatement()
        case tokens.SEMICOLON:
            prod = NullStatement()
        case tokens.WHILE:
            prod = WhileStatement()
        case tokens.READ:
            prod = ReadStatement()
        case tokens.WRITE:
            prod = WriteStatement()
        case tokens.NEWLINE:
            prod = newLineStatement()
        case tokens.SEMICOLON:
            prod = NullStatement()
        case _:
            prod = ExpressionStatement()
    helper.exiting("Statement", debug)
    return Trees.StatementTree.createStatementTree(prod)

def ExpressionStatement():
    helper.entering("Expression Statement", debug)
    Expression()
    if activeToken == tokens.LEFTBRACKET:
        CompoundStatement()
    else:
        helper.accept(activeToken, tokens.SEMICOLON)
    helper.exiting("Expression Statement", debug)

def breakStatement():
    helper.entering("Break Statement", debug)
    loadToken()
    helper.accept(activeToken, tokens.SEMICOLON)
    helper.exiting("Break Statement", debug)
    return Trees.productions.prBreak

def CompoundStatement():
    helper.entering("Compound Statement", debug)
    loadToken()
    while(activeToken != tokens.RIGHTCURLY):
        print(f"Current Token (Statement): {activeToken}")
        if(activeToken == tokens.INT or activeToken == tokens.CHAR):
            loadToken()
            helper.accept(activeToken, tokens.ID)
            loadToken()
            helper.accept(activeToken, tokens.SEMICOLON)
            loadToken()
        else:
            Statement()
            loadToken()
    
    helper.accept(activeToken, tokens.RIGHTCURLY)
    helper.exiting("Compound Statement", debug)

def ifStatement():
    helper.entering("If Statement", debug)
    loadToken()
    helper.accept(activeToken, tokens.LEFTPAREN)
    loadToken()
    Expression()
    helper.accept(activeToken, tokens.RIGHTPAREN)
    loadToken()
    Statement()
    loadToken()
    if activeToken == tokens.ELSE:
        loadToken()
        Statement()
    helper.exiting("If Statement", debug)

def NullStatement():
    helper.entering("Null Statement", debug)
    helper.exiting("Null Statement", debug)
    return Trees.productions.prNull

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
    return Trees.productions.prNewline

def Expression():
    helper.entering("Expression", debug)
    prod = RelopExpression()
    if activeToken == tokens.ASSIGN:
        loadToken()
        RelopExpression()
    helper.exiting("Expression", debug)
    return Trees.ExpressionTree.createExpressionTree(prod)

def RelopExpression():
    helper.entering("Relop Expression", debug)
    SimpleExpression()
    if activeToken == tokens.RELOP:
        loadToken()
        SimpleExpression()
    helper.exiting("Relop Expression", debug)

def SimpleExpression():
    helper.entering("Simple Expression", debug)
    Term()
    #loadToken()
    if activeToken == tokens.ADDOP:
        loadToken()
        Term()
    helper.exiting("Simple Expression", debug)

def Term():
    helper.entering("Term", debug)
    Primary()
    if activeToken == tokens.MULOP:
        loadToken()
        Primary()
    helper.exiting("Term", debug)

def Primary():
    helper.entering("Primary", debug)
    #loadToken()
    match(activeToken):
        case tokens.LEFTPAREN:
            loadToken()
            Expression()
            helper.accept(activeToken, tokens.RIGHTPAREN)
            loadToken()
        case tokens.ID:
            loadToken()
            if activeToken == tokens.LEFTPAREN:
                FunctionCall()
                helper.accept(activeToken, tokens.RIGHTPAREN)
        case tokens.NOT:
            loadToken()
            Primary()    
        case tokens.NUMBER:
            loadToken()
        case tokens.STRING:
            loadToken()
        case tokens.CHARLITERAL:
            loadToken()
        
    if currTokenVal == "-":
        loadToken()
        Primary()

    helper.exiting("Primary", debug)

def FunctionCall():
    helper.entering("Function Call", debug)
    loadToken()
    if activeToken != tokens.RIGHTPAREN:
        ActualParameters()
    loadToken()
    helper.accept(activeToken, tokens.RIGHTPAREN)
    helper.exiting("Function Call", debug)

def ActualParameters():
    helper.entering("Actual Parameters", debug)
    Expression()
    if activeToken == tokens.COMMA:
        loadToken()
        Expression()
    helper.exiting("Actual Parameters", debug)