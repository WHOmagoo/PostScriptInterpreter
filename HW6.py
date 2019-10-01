#Hugh McGough
#This file was developed in Windows

#------------------------- 10% -------------------------------------
# The operand stack: define the operand stack and its operations

opstack = []

# now define functions to push and pop values on the opstack according to your
# decision about which end should be the hot end. Recall that `pass` in Python is
# a no-op: replace it with your code.


def opPop():
    if(len(opstack) > 0):
        return opstack.pop()
    return None


def opPush(value):
    if value is not None:
        opstack.append(value)

# Remember that there is a Postscript operator called "pop" so we choose
#different names for these functions.


#-------------------------- 20% -------------------------------------
# The dictionary stack: define the dictionary stack and its operations

dictstack = [({},0)]
currentDictIndex = 0

# now define functions to push and pop dictionaries on the dictstack, to define
# name, and to lookup a name


def dictPop():
    if len(dictstack) > 0:
        return dictstack.pop()
    return None
    pass
# dictPop pops the top dictionary from the dictionary stack.


def dictPush(dictionary):
    if isinstance(dictionary, dict) or isinstance(dictionary, tuple):
        dictstack.append(dictionary)
    else:
        print("Non dictionary was passed to push to the dictionary stack")


# dictPush pushes a new dictionary to the dictstack. Note that, your interpreter
# will call dictPush only when Postscript “begin” operator is called. “begin”
# should pop the empty dictionary from the opstack and push it onto the dictstack
# by calling dictPush. You may either pass this dictionary (which you popped from
# opstack) to dictPush as a parameter or just simply push a new empty dictionary
# in dictPush.


def define(name, value):
    curDict = dictPop()
    if curDict is not None:
        curDict[0][name] = value
        dictPush(curDict)
    else:
        dictPush({name: value})
    pass

# def defineDynamic(name, value):
#     if len(dictstack) > 0:
#         curDict = dictstack[latestDict]
#         dict = findFirstOccurenceOf(name, curDict, latestDict)
#         if dict is  None:
#             curDict[0][name] = value
#         else:
#             dict[name] = value
#
#     else:
#         dictPush(({name: value}, 0))
#     pass

def defineDynamic(name, value):
    dictstack[currentDictIndex][0][name] = value

def findFirstOccurenceOf(var, dict, curIndex):
    if dict[1] == curIndex:
        return None
    elif var in dict[0].keys():
        return curIndex
    else:
        return findFirstOccurenceOf(var, dictstack[dict[1]], dict[1])

# add name:value to the top dictionary in the dictionary stack. (Keep the ‘/’ in
# name when you add it to the top dictionary) Your psDef function should pop the
# name and value from operand stack and call the “define” function.


def psDef():
    value = opPop()
    name = opPop()

    if len(name) > 1 and name[:1] == '/' and value is not None:
        define(name, value)
    else:
        opPush(name)
        opPush(value)
        print("Operands missing for def")


    pass

#
# def psDefDynamic():
#     value = opPop()
#     name = opPop()
#     if len(name) > 1 and name[:1] == '/' and value is not None:
#         defineDynamic(name, value)
#     else:
#         opPush(name)
#         opPush(value)
#         print("Operands missing for def")
#
#
# pass


# def lookup(name):
#     name = '/' + name
#     for dictionary in reversed(dictstack):
#         if name in dictionary.keys():
#             return dictionary[name]
#
#     return None

def lookup(name):
    name = '/' + name
    localCurrentDictIndex = currentDictIndex
    while True:
        if name in dictstack[localCurrentDictIndex][0].keys():
            return (dictstack[localCurrentDictIndex][0][name], localCurrentDictIndex)
        else:
            if localCurrentDictIndex == 0:
                return None
            else:
                localCurrentDictIndex = dictstack[localCurrentDictIndex][1]
# return the value associated with name
# What is your design decision about what to do when there is no definition for
# name?

#--------------------------- 15% -------------------------------------
# Arithmetic and comparison operators: define all the arithmetic and
# comparison operators here -- add, sub, mul, div, eq, lt, gt
# Make sure to check the operand stack has the correct number of parameters and
# types of the parameters are correct.


def add():
    if can_do_arithmetic():
        opPush(opPop() + opPop())
    else:
        print("Missing operand for add")



def sub():
    if can_do_arithmetic():
        opPush(-1 * opPop() + opPop())
    else:
        print("Missing operand for sub")


def mul():
    if can_do_arithmetic():
        opPush(opPop() * opPop())
    else:
        print("Missing operand for mult")


def div():
    if can_do_arithmetic():
        opPush(1/opPop() * opPop())
    else:
        print("Missing operand for div")


def eq():
    top = opPop()
    next = opPop()

    if top is not None and next is not None:
        opPush(top == next)
    else:
        print("Missing operand for eq")


def lt():
    if can_do_arithmetic():
        opPush(opPop() > opPop())
    else:
        print("Missing operand for lt")


def gt():
    if can_do_arithmetic():
        opPush(opPop() < opPop())
    else:
        print("Missing operand for gt")


def can_do_arithmetic():
    top = opPop()
    next = opPop()

    opPush(next)
    opPush(top)

    return isinstance(top, int) and isinstance(next, int)

#--------------------------- 15% -------------------------------------
# String operators: define the string operators length, get, getinterval


def length():
    val = opPop()

    if isinstance(val, str):
        opPush(len(val))
    else :
        opPush(val)
        print("Top operand was not a string for length")


def get():
    index = opPop()

    if isinstance(index, int):
        string = opPop()
        if isinstance(string, str):
            if(len(string) > index and index > 0):
                opPush(string[index])
        else:
            opPush(index)
            print("Index was out of bounds for get")

    else:
        opPush(index)
        print("Missing operand for get")



def getinterval():
    count = opPop()
    start = opPop()
    string = opPop()
    fix = False
    if isinstance(start, int):
        if isinstance(count, int):
            if isinstance(string, str):
                if start + count <= len(string):
                    opPush(string[start:(start+count)])
                else:
                    fix = True
                    print("The specified index or interval was out of bounds")
            else:
                fix = True
                print("The operand expected for string was not a string")
        else:
            fix = True
            print("The operand expected for count was not an int")
    else:
        fix = True
        print("The operand expected for the starting index was not an int")

    if fix:
        opPush(string)
        opPush(count)
        opPush(start)


#--------------------------- 15% -------------------------------------
# Boolean operators: define the boolean operators and, or, not;
# Remember that these take boolean operands only. Anything else is an error

def psAnd():
    if can_do_boolean():
        opPush(opPop() and opPop())
    else:
        print("Missing operand for and")


def psOr():
    if can_do_boolean():
        opPush(opPop() or opPop())
    else:
        print("Missing operand for or")


def psNot():
    top = opPop()
    if isinstance(top, bool):
        opPush(not top)
    else:
        opPush(top)
        print("Missing operand for not")


def can_do_boolean():
    top = opPop()
    next = opPop()

    opPush(next)
    opPush(top)

    return isinstance(top, bool) and isinstance(next, bool)


#--------------------------- 25% -------------------------------------
# Define the stack manipulation and print operators: dup, exch, pop, roll,
# copy, clear, stack

def dup():
    top = opPop()
    if top is not None:
        opPush(top)
        opPush(top)
    else:
        print("Missing operand for dup")


def exch():
    top = opPop()
    next = opPop()

    if top is not None:
        if next is not None:
            opPush(top)
            opPush(next)
        else:
            opPush(top)
            print("Missing second operand for exch")
    else:
        print("Missing first operand for exch")


def pop():
    opPop()


def roll():
    shift = opPop()
    count = opPop()

    #The original
    shiftCopy = shift
    countCopy = count

    shift = shift % count
    first = []
    second = []

    if isinstance(shift, int):
        if isinstance(count, int):
            while count > 0:
                val = opPop()
                if val is not None:
                    if shift > 0:
                        first.append(val)
                    else:
                        second.append(val)
                else:
                    first.reverse()
                    second.reverse()

                    for el in second:
                        opPush(el)


                    for el in first:
                        opPush(el)

                    second = []
                    first = []

                    opPush(countCopy)
                    opPush(shiftCopy)

                    print("The given element count was too small for the given stack.")
                    break

                count -= 1
                shift -= 1

            first.reverse()
            second.reverse()
            for el in first:
                opPush(el)

            for el in second:
                opPush(el)
        else:
            opPush(shift)

            print("Missing the second operand for roll")
    else:
        print("Missing the first operand for roll")


def copy():
    copy = []
    count = opPop()
    countCopy = count

    if isinstance(count, int):
        while count > 0:
            thisElement = opPop()
            if thisElement is not None:
                copy.append(thisElement)
            else:
                print("Not enough elements to copy")
                copy.reverse()
                for el in copy:
                    opPush(el)

                opPush(countCopy)
                break

            count -= 1

        copy.reverse()
        for el in copy:
            opPush(el)

        for el in  copy:
            opPush(el)
    else:
        print("Missing first operand for copy")
        opPush(count)


def clear():
    opstack.clear()
    global dictstack
    dictstack = [({},0)]
    global currentDictIndex
    currentDictIndex = 0


def stack():
    print("==============")
    for el in reversed(opstack):
        if isinstance(el, str):
            print('(' + el + ')')
        else:
            print(el)
    print("==============")

    index = len(dictstack) - 1
    for curDict in reversed(dictstack):
        if curDict is not None:
            print('----' +  str(index) + '----' + str(curDict[1]) + '----')
            for key, val in curDict[0].items():
                print(key + ' ' + str(val))

            index -= 1

    print("==============")

#--------------------------- 20% -------------------------------------
# Define the dictionary manipulation operators: psDict, begin, end, psDef
# name the function for the def operator psDef because def is reserved in
# Python.
# Note: The psDef operator will pop the value and name from the opstack and
# call your own "define" operator (pass those values as parameters). Note that
# psDef()won't have any parameters.

def psDict():
    top = opPop()

    if top is not None:
        opPush({})
    else:
        print("Error with operand for dict")
        opPush(top)



def begin():
    top = opPop()
    if isinstance(top, dict):
        dictPush(top)
    else:
        opPush(top)
        print("Operand for begin was not a dictionary")


def end():
    dictPop()


#Test functions


def testOpPop():
    opPush(1)
    return opPop() == 1


def testOpPush():
    clear()
    opPush(4)


    return opstack == [4]
    pass


def testDictPop():
    dictstack.clear()
    dictPush({4: 1, 6: 3})
    dictPush({})
    dictPop()
    return dictstack == [{4: 1, 6:3}]
    pass


def testDictPush():
    dictstack.clear()
    dictPush({3: 4, 5: 6})
    return dictstack == [{3: 4, 5: 6}]
    pass


def testPsDef():
    clear()
    dictstack.clear()
    opPush('/y')
    opPush(2)
    psDef()
    return opstack == [] and dictstack == [{'/y': 2}]
    pass

def testLookup():
    opPush('/x')
    opPush(5)
    opPush('/y')
    opPush("my testing")
    psDef()
    psDef()

    return lookup('x') == 5 and lookup('y') == "my testing"
    pass


def testAdd():
    opPush(-3)
    opPush(7)
    add()
    return opPop() == 4
    pass


def testSub():
    opPush(10)
    opPush(6)
    sub()
    return opPop() == 4
    pass


def testMult():
    opPush(4)
    opPush(5)
    mul()
    return opPop() == 20
    pass

def testDiv():
    opPush(15)
    opPush(3)
    div()
    return opPop() == 5.0

    pass

def testEq():
    opPush(12)
    opPush(12)
    opPush(16)
    opPush(-7)
    eq()

    if opPop() is True:
        return False

    eq()

    return opPop() is True
    pass


def testLt():
    opPush(4)
    opPush(5)
    opPush(7)
    opPush(6)
    lt()

    if opPop() is True:
        return False
    lt()

    return opPop() is True
    pass


def testGt():
    opPush(4)
    opPush(5)
    opPush(7)
    opPush(6)
    gt()
    if opPop() is False:
        return False

    gt()
    return opPop() is False
    pass


def testLength():
    opPush("This is long")
    length()
    return opPop() == 12
    pass


def testGet():
    opPush("Meow!!")
    opPush(2)
    get()
    return opPop() == 'o'
    pass


def testGetInterval():
    opPush("Meow!!")
    opPush(2)
    opPush(3)
    getinterval()
    return opPop() == 'ow!'
    pass


def testPsAnd():
    opPush(True)
    opPush(True)
    opPush(False)
    opPush(True)
    psAnd()

    if opPop() is True:
        return False

    psAnd()

    return opPop() is True
    pass


def testPsOr():
    opPush(False)
    opPush(True)
    opPush(False)
    opPush(False)
    psOr()

    if opPop() is True:
        return False

    psOr()
    return opPop() is True
    pass


def testPsNot():
    opPush(True)
    opPush(False)

    psNot()

    if opPop() is False:
        return False

    psNot()

    return opPop() is False

    pass


def testDup():
    opPush(4)
    dup()

    return opPop() == 4 and opPop() == 4
    pass


def testExch():
    opPush(4)
    opPush("Test")
    exch()

    return opPop() == 4 and opPop() == "Test"
    pass


def testPop():
    opPush("Start")
    opPush(3)
    pop()
    return opPop() == "Start"

    pass


def testRoll():
    pass


def testCopy():
    opPush(False)
    opPush(4)
    opPush(2)
    copy()
    return opPop() == 4 and opPop() is False and opPop() == 4 and opPop() is False
    pass


def testClear():
    opPush(3)
    opPush("Clearing")
    opPush(False)
    clear()
    return opstack == []
    pass


def testBegin():
    dictstack.clear()
    opPush({})
    begin()
    return dictstack == [{}]
    pass

import re
import HW5_part1_solo


def ifelse():
    top = opPop()
    middle = opPop()
    bottom = opPop()

    if isinstance(top, list) and isinstance(middle, list) and isinstance(bottom, bool):
        if bottom:
            interpreterSPS(middle)
        else:
            interpreterSPS(top)
    else:
        opPush(bottom)
        opPush(middle)
        opPush(top)

def psIf():
    top =  opPop()
    next = opPop()
    if isinstance(top, list) and isinstance(next, bool):
        if next:
            interpreterSPS(top)
    else:
        opPush(next)
        opPush(top)



#Provided from the homework assignment
def tokenize(s):
    return re.findall("/?[a-zA-Z()][a-zA-Z0-9_()]*|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)

# The sequence of characters returned by the iterator should represent a string of prop
#erly nested
# parentheses pairs, from which the leading '(' has already been removed. If the
# parenteses are not properly nested, returns False.

def groupMatching(it):
    res = ['(']
    for c in it:
        if c==')':
            res.append(')')
            return res
        else:
            # note how we use a recursive call to group the inner
            # matching parenthesis string and append it as a whole
            # to the list we are constructing.
            # Also note how we've already seen the leading '(' of this
            # inner group and consumed it from the iterator.
            res.append(groupMatching(it))

    return False

    # function to turn a string of properly nested parentheses
    # into a list of properly nested lists.

def group(s):
    if s[0]=='(':
        return groupMatching(iter(s[1:]))
    else:
        return False

def parse(s):
    return myGroupMatching(iter(s[0:]))


def myGroupMatching(pIterator):
    result = []

    for token in pIterator:
        if token=='}':
            return result
        elif token=='{':
            result.append(myGroupMatching(pIterator))
        elif token.isdigit():
            result.append(int(token))
        elif token[0] == '-' and token[1:-1].isdigit:
            result.append((-1 * int(token[1:])))
        elif token.lower() == 'true':
            result.append(True)
        else:
            result.append(token)
    return result

def interpreter(string, scope):
    interpreterSPS(parse(tokenize(string)), scope)


#scope is string of either 'static' or 'dynamic'
def interpreterSPS(code, scope):
    if scope.lower() != 'static' and scope.lower() != 'dynamic':
        print("Static or Dynamic DictStack not specified")
        return

    global currentDictIndex
    global dictstack

    for arg in code:
        if isinstance(arg, int):
            opPush(arg)
        elif isinstance(arg, list):
            opPush(arg)
        elif arg[0:1] == '(':
            opPush(arg[1:-1])
        elif arg[0:1] == '/':
            opPush(arg)
        elif arg == 'add':
            add()
        elif arg == 'sub':
            sub()
        elif arg == 'mul':
            mul()
        elif arg == 'div':
            div()
        elif arg == 'eq':
            eq()
        elif arg == 'lt':
            lt()
        elif arg == 'gt':
            gt()
        elif arg == 'length':
            length()
        elif arg == 'get':
            get()
        elif arg == 'getinterval':
            getinterval()
        elif arg == 'and':
            psAnd()
        elif arg == 'or':
            psOr()
        elif arg == 'not':
            psNot()
        elif arg == 'dup':
            dup()
        elif arg == 'exch':
            exch()
        elif arg == 'pop':
            pop()
        elif arg == 'roll':
            roll()
        elif arg == 'copy':
            copy()
        elif arg == 'clear':
            clear()
        elif arg == 'stack':
            stack()
        elif arg == 'dict':
             psDict()
        elif arg == 'begin':
             begin()
        elif arg == 'end':
             end()
        elif arg == 'def':
            psDef()
        elif arg == 'if':
            psIf()
        elif arg == 'ifelse':
            ifelse()
        else:
            value = lookup(arg)
            if value is not None:
                if isinstance(value[0], list):

                    if scope.lower() == 'static':
                        dictstack.append(({}, value[1]))
                        lastDictIndex = currentDictIndex
                        currentDictIndex = len(dictstack) - 1
                        interpreterSPS(value[0], scope)
                        currentDictIndex = lastDictIndex
                    else:
                        dictstack.append(({}, currentDictIndex))
                        currentDictIndex += 1
                        interpreterSPS(value[0], scope)
                        currentDictIndex -= 1
                else:
                    opPush(value[0])
            else:
                print("There was an error looking up " + arg)

    del dictstack[currentDictIndex]

    if len(dictstack) == 0:
        dictstack = [({}, 0)]


if __name__ == '__main__':
    #
    # testCases = [
    #     ('opPop', testOpPop()),
    #     ('opPush', testOpPush()),
    #     ('dictPop', testDictPop()),
    #     ('dictPush', testDictPush()),
    #     ('psDef', testPsDef()),
    #     ('lookup', testLookup()),
    #     ('add', testAdd()),
    #     ('sub', testSub()),
    #     ('mult', testMult()),
    #     ('div', testDiv()),
    #     ('eq', testEq()),
    #     ('lt', testLt()),
    #     ('gt', testGt()),
    #     ('length', testLength()),
    #     ('get', testGet()),
    #     ('getInterval', testGetInterval()),
    #     ('psAnd', testPsAnd()),
    #     ('psOr', testPsOr()),
    #     ('psNot', testPsNot()),
    #     ('dup', testDup()),
    #     ('exch', testExch()),
    #     ('pop', testPop()),
    #     ('roll', testRoll()),
    #     ('copy', testCopy()),
    #     ('clear', testClear()),
    #     ('begin', testBegin())
    # ]
    #
    # allSucceeded = True
    #
    # for (name, result) in testCases:
    #     if result is False:
    #         allSucceeded = False
    #         print(name + " has failed")
    # if allSucceeded:
    #     print("All tests succeeded\n")

    input1 = """
    /x 4 def
    /g { x stack } def
    /f { /x 7 def g } def
    f
    """

    interpreter(input1, 'static')
    interpreter('clear', 'static')
    interpreter(input1, 'dynamic')
    interpreter('clear', 'static')

    input2 = """
        /m 50 def
        /n 100 def
        /egg1 {/m 25 def n} def
        /chic {
         /n 1 def
         /egg2 { n } def
         m n
         egg1
         egg2
         stack } def
        n
        chic
    """

    interpreter(input2, 'static')
    interpreter('clear', 'dynamic')
    interpreter(input2, 'dynamic')
    interpreter('clear', 'dynamic')

    input3 = """
        /x 10 def
        /A { x } def
        /C { /x 40 def A stack } def
        /B { /x 30 def /A { x } def C } def
        B
    """

    interpreter(input3, 'static')
    interpreter('clear', 'static')
    interpreter(input3, 'dynamic')
    interpreter('clear', 'static')

    # input1 = """
    # /square {
    #      dup mul
    # } def
    # (square)
    # 4 square
    # dup 16 eq true and
    # {(pass)} {(fail)} ifelse stack"""
    #
    # print("RESULT for input1:")
    # interpreter(input1)
    #
    # interpreter('clear')
    #
    # input2 = """
    #     (facto) dup length /n exch def
    #     /fact {
    #         0 dict begin
    #         /n exch def
    #         n 2 lt
    #         { 1}
    #         {n 1 sub fact n mul }
    #         ifelse
    #     end
    # } def
    # n fact stack
    # """
    #
    # print("RESULT for input2:")
    # interpreter(input2)
    #
    # interpreter('clear')
    #
    # input3 = """
    #     /lt6 { 6 lt } def
    #     1 2 3 4 5 6 4 -3 roll
    #     dup dup lt6 exch 3 gt and {mul mul} if
    #     stack
    #     clear
    #     """
    #
    # print("RESULT for input3:")
    # interpreter(input3)
    # interpreter('clear')
    #
    # input4 = """
    #     (CptS355_HW5) 4 3 getinterval
    #     (355) eq
    #     {(You_are_in_CptS355)} if
    #     stack
    #     """
    # print("RESULT for input4")
    # interpreter(input4)