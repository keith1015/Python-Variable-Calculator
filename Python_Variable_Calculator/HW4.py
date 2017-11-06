
import re #regular expressions to be used in isVariable

class Calculator:

    ## copy the stack class from HW3
    class stack:

        class node:
            def __init__(self, val, nextNode):
                self.value = val
                self.nextNode = nextNode

        def __init__(self):
            self.top = None
            self.size = 0

        def __len__(self):
            return self.size

        def push(self, val):
        #It adds a new node including val at the top pointer
            self.size = self.size + 1
            self.top = self.node(val, self.top)

        def pop(self):
            if self.size < 1:
                return "error. stack is empty."

            self.size = self.size - 1
            a = self.top.value
            self.top = self.top.nextNode

            return a

    ## Copy the functions but add "self"
    ## Also any use of function is in the form of self.function_name
    def exeOpr(self, num1, opr, num2):
        if opr=="+":
            return num1+num2
        elif opr=="-":
            return num1-num2
        elif opr=="*":
            return num1*num2
        elif opr=="/":
            if num2==0:
                print("zero division error: exeOpr")
                return "zero division error: exeOpr"
            else:
                return num1/num2
        elif opr=="^":
            return num1 ** num2
        else:
            print("fatal internal error in exeOpr")
            return "fatal internal error in exeOpr"
     
    def findNextOpr(self, s):
        if len(s)<=0 or not isinstance(s,str):
            print("type mimatch error: findNextOpr")
            return "type mimatch error: findNextOpr"

        s2 = list(s) #converts s to a list
        operator = ["+", "-", "/", "*", "^"]

        p1 = None
        p2 = None

        for i in s2: #find location of open and close brackets
            if i == '[':
                p1 = s2.index(i)
            if i == ']':
                p2 = s2.index(i)

        if (p1 != None) and (p2 != None):
            while p1 != (p2-1): #replace stuff inside bracket with space
                #print(p1)
                p1 = p1 + 1
                s2[p1] = " "
                #print(s2)

        for i in s2:
            if i in operator:
                return i
        else:
            return -1
     
    def isNumber(self, s):
        if len(s)==0 or not isinstance(s, str):
        #print("type mismatch error: isNumber")
            return "type mismatch error: isNumber"

        s = s.strip(" ")
        s = s[0:] #removes minus signs but only from the front of string

        try: #checks to make sure s2 is a number and doesn't have more than 1 period
            s=float(s)
            return True
        except:
            return False 

    ## new functions
    def isVariable(self, s):
        ## It returns True if s is a string
        #   that can be a variable, 
        #   i.e. after striping it consists of only
        #    alphabet letters and 0-9, 
        #    and the first char must be a letter

        s1 = str(s) #convert to string just in case it isn't
        str1 = s1.strip()
        str2 = str1[0]

        if re.match("^[A-Za-z0-9]+$", str1) and re.match("^[A-Za-z]+$", str2): #checks for #s and letters
            return True
        else:
            return False
 

    ### modify getNextNumber into this
    def getNextItem(self, expr, pos):
        #expr is a given arithmetic formula in string
        #pos = start position in expr
        #1st returned value = the next number or a variable(None if N/A)
        #   -- So the change is to recognize a variable
        #2nd returned value = the next operator (None if N/A)
        #3rd retruned value = the next operator position (None if N/A)

        if len(expr)==0 or not isinstance(expr, str) or pos<0 or pos>=len(expr) or not isinstance(pos, int):
        #print("type mismatch error: getNextItem")
            return None, None, "type mismatch error: getNextItem"

        string1 = expr[pos:] #sets string1 equal to position that was passed
        op=['-','+','*','/', '^']

        newOpr = self.findNextOpr(string1)

        if newOpr in op: 
            if expr.find(newOpr,pos)>=pos:
                oprPos=expr.find(newOpr,pos)
        else:
            newOpr=None

        if newOpr==None:
            oprPos = None

        aa = expr.count('[')
        bb = expr.count(']')

        expr = expr.replace('[', ' ', aa)
        expr = expr.replace(']', ' ', bb)

        if self.isNumber(expr[pos:oprPos]) == True: #checks to make sure if string is actually a #
            newNumber = float(expr[pos:oprPos])
        elif self.isVariable(expr[pos:oprPos]) == True:
            newNumber = str(expr[pos:oprPos]) #made it into a string
        else:
            newNumber = None #if it is a #, assigns value to newNumber

        return newNumber, newOpr, oprPos
        
    ### Other new / modified functions
    def __init__(self):
        self.lines = []  
        #e.g. if expr = " a = 2+3*(1+3 / 2) ; b = 4*(a+3)  ", 
        #   self.lines = [["a", "2+3*(1+3 / 2)"], ["b", "4*(a+3)"]]
        self.varDic = {}
        # The variable dictionary
        #   whose keys are all the currently detected variables
        #   whose values (as a dictionary) are
        #               the values of the variables
        # You can add other class instance variables here too

        
    def getLines(self, expr):
        #expr : input to calc
        #the function sets self.lines
        a = expr.strip()

        b = a.split(';') #splits the string at the semicolon and converts to list

        a1 = b[len(b)-1]

        a1 = a1.strip().lower()

        if 'return' in a1:
            a2 = a1[:6] + '=' + a1[6:]

        b[len(b)-1] = a2

        for i in b:
            i = i.split('=') #splits the string again at = sign
            self.lines.append(i)

        b2 = self.lines[len(self.lines)-1][0] 

        b2 = '__'+b2+'__'

        self.lines[len(self.lines)-1][0] = b2

    ### This is almost the same as _calc in HW3
    #       but with minor modification
    #       -- If there is a variable x instead of a number
    #           get its value from varDic["x"]
    def _calc(self, expr):
        expr = expr.strip()

        #if expr[0] == '-' and 

        #the below line checks if expr is a string
        if not isinstance(expr, str) or len(expr) <= 0:
            #print("argument error: line A in eval_expr")
            return "argument error: line A in eval_expr"

        #below line  creates three variables
        #sets them equal to whatever is returned by the getNextNumber function
        #the getNextNumber function is called. It passes the expr and integer 0

        if expr[0] == "-":
            newNumber, newOpr, oprPos = self.getNextItem(expr, 1)
            if newNumber is None:
                print("input formula error: line B in eval_expr")
                return "input formula error: line B in eval_expr"
            else:
                newNumber = newNumber * (-1)
        else:
            newNumber, newOpr, oprPos = self.getNextItem(expr, 0)


        if isinstance(newNumber, str):
            newNumber = newNumber.strip()
            newNumber = self.varDic[newNumber] #finds the key in varDic and assigns its value to newNumber
            newNumber = float(newNumber) #converts it to float


        if newNumber is None:
            #print("input formula error: line B in eval_expr")
            return "input formula error: line B in eval_expr"
        elif newOpr is None:
            return newNumber
        elif newOpr=="+" or newOpr=="-":
            mode="add" 
            addResult=newNumber #saves # at first index to addResult if 1st operator is + or -    
            mulResult=None          
        elif newOpr=="*" or newOpr=="/":
            mode="mul"
            addResult=0
            #lastOpr = "+"
            mulResult=newNumber #saves # at first index to mulResult if 1st operator is + or -
        elif newOpr == "^":
            mode = "expo"
            addResult = 0
            mulResult = None
            #lastMulOpr = "*"
            expoResult = newNumber

        #pos and opr are created
        pos=oprPos+1 #current positon
        opr=newOpr #current operator
        oldOpr = None

        while True:
        #--- code while loop ---#
            newNumber, newOpr, oprPos = self.getNextItem(expr, pos)

            if isinstance(newNumber, str):
                newNumber = newNumber.strip()
                newNumber = self.varDic[newNumber] #finds the key in varDic and assigns its value to newNumber
                newNumber = float(newNumber) #converts it to float

            if newNumber is None:
                return 'input formula error: line B in eval_expr'
            elif newOpr is None:
                if mode == 'mul':
                    mulResult = self.exeOpr(mulResult, opr, newNumber)
                    expoResult = 0
                if mode == 'add':
                    addResult = self.exeOpr(addResult, opr, newNumber)
                    expoResult = 0
                    mulResult = 0
                if mode == "expo":
                    if expoResult < 0:
                        expoResult = self.exeOpr(expoResult, opr, newNumber)
                        if expoResult < 0:
                                expoResult = expoResult
                        else:
                                expoResult = -expoResult
                    else:
                        expoResult = self.exeOpr(expoResult, opr, newNumber)
                    if oldOpr != None:
                        mulResult = self.exeOpr(mulResult,oldOpr,expoResult)
                        expoResult = 0
                    

            elif mode == 'add':
                if newOpr == '*' or newOpr =='/':
                    mode = 'mul'
                    if mulResult == None:
                         mulResult = newNumber #this is where 6 is
                    if opr=='-':
                        mulResult=-newNumber #it's also here
                    else:
                        mulResult=newNumber
                elif newOpr == '-' or newOpr =='+':
                    mode = 'add'
                    addResult = self.exeOpr(addResult,opr,newNumber)
                    mulResult = None
                elif newOpr == "^":
                    mode = "expo"
                    if opr == "-":
                        expoResult = -(newNumber)
                    else:
                        expoResult = newNumber
                                   
            elif mode == 'mul':
                if newOpr == '*' or newOpr =='/':
                    mode = 'mul'
                    mulResult = self.exeOpr(mulResult, opr, newNumber)
                elif newOpr == '-' or newOpr =='+':
                    mode = 'add'
                    if opr == "/" and newNumber == 0:
                        print("divide by zero error")
                    else:
                        mulResult=self.exeOpr(mulResult,opr,newNumber)
                        addResult +=mulResult
                        mulResult=0
                elif newOpr == "^":
                    mode = "expo"
                    oldOpr = opr
                    expoResult = newNumber

            elif mode == "expo":
                if newOpr == "*" or newOpr == "/":
                    mode = "mul"
                    if expoResult < 0:
                        expoResult = self.exeOpr(expoResult,opr,newNumber)*(-1)
                    else:
                        expoResult = self.exeOpr(expoResult,opr,newNumber)
                    if oldOpr!=None:
                        mulResult = self.exeOpr(mulResult, oldOpr, expoResult)
                        oldOpr=None
                    else:                    
                        mulResult = expoResult
                elif newOpr == "+" or newOpr == "-":
                    mode = "add"
                    if expoResult < 0:
                        expoResult = self.exeOpr(expoResult,opr,newNumber)*(-1)
                    else:
                        expoResult = self.exeOpr(expoResult,opr,newNumber)
                    if oldOpr != None:
                        mulResult = self.exeOpr(mulResult,oldOpr,expoResult)
                        expoResult = 0
                        addResult = addResult + mulResult
                        mulResult=0
                        oldOpr=None
                    else:
                        addResult = addResult + expoResult
                        expoResult=0
                    expoResult = 0
                elif newOpr == "^":
                    mode = "expo"
                    if expoResult < 0:
                        expoResult = self.exeOpr(expoResult,opr,newNumber)*(-1)
                    else:
                        expoResult = self.exeOpr(expoResult,opr,newNumber)
            if isinstance(mulResult,str):
                return 'divide by zero error'
                   
            if oprPos == None:
                if mulResult==None:
                    mulResult = 0
                break
            
            pos = oprPos+1
            opr= newOpr
        return addResult+mulResult+expoResult

    ### Again almost the same as calc(expr) of HW3
    def _calcHW3(self,expr):
        # This is calc(expr) of HW3
        stack1 = self.stack()

        expr = expr.strip()

        c1 = expr.count('(')
        c2 = expr.count(')')

        while c1>0:
            c1 = expr.count('(')
            for i in expr:
                if i == '(':
                    pos1 = expr.index(i)
                    expr = expr.replace('(', ' ', 1)
                    stack1.push(pos1)
                if i == ')':
                    pos2 = expr.index(i)
                    #print(pos2)
                    stack1.push(pos2)
                    close1= stack1.pop()
                    open1= stack1.pop()
                    #print(open1)
                    if isinstance(open1,str):
                        print("error")
                        return "error"
                    expr2 = expr[(open1)+1:close1]
                    #print(expr2)
                    if len(expr2) == 2 and expr2[0] == '-':
                        expr2 = ('0'+expr2)
                    expr2 = self._calc(expr2)
                    rp = expr[open1:close1+1]
                    if not isinstance(expr2, float) or len(expr) <= 0:
                        return "argument error: line A in eval_expr heree"
                    expr2 = str(expr2)
                    expr2 = ('['+expr2+']')
                    expr = expr.replace(rp, expr2)
                    #print(expr)
                    
        if len(stack1) > 0:
            print("error")
            return "error"
                    
        c3 = expr.count('(')
        if c3 == 0:
            expr = self._calc(expr)
            
        return expr

    ### THe main function

    def calc(self, expr):

        expr = expr.strip()

        if ';' not in expr:
            return self._calcHW3(expr)
        ## First split expr into the lines.
        try:
            self.getLines(expr)
        except:
            return 'error'
        ## Further modify so that self.lines is correctly set.
        ## Then execute self.lines from the top one by one
        ##       calling _calcHW3
        try:
            for a in range(len(self.lines)):
                var1 = self.lines[a][0]
                var2 = self.lines[a][1]

                var3 = self._calcHW3(var2)

                try:
                    var3=float(var3)
                except:
                    return "error"

                var1 = var1.strip()

                self.varDic[var1] = var3

                #print(self.varDic)

            return self.varDic['__return__']
        except:
            return 'error'
 

c = Calculator()
s = 'a = 2+2 ;b = 0+1; return a+b'

print(c.calc(s))
