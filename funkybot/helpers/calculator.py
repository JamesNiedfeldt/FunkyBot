#==== Description ====
"""
Contains all necessary functions for calculating math equations
"""

#==== Imports ====
import re
import math

from helpers import helper_functions as h
from errors import errors

#==== Globals ====
_prec = {
        '|': 4, #Represents unary '-'
        '^': 3,
        '*': 2,
        '/': 2,
        '+': 1,
        '-': 1 }
_funcs = ['sqrt', 'abs', 'log']

_numRe = '[0-9]*[.]?[0-9]+'
_opsRe = '[+/\-*^()]' #Does not account for '|'
_funcsRe = '(sqrt)|(abs)|(log)'
_parseRe = '({})|({})|{}'.format(_numRe, _opsRe, _funcsRe)

#==== Calculate given equation ====
def calculate(eq):
    try:
        tokens = __parse(eq)
        __verifyTokens(tokens)
        rpn = __postfix(tokens)
        return __doMath(rpn)
    except:
        raise

#==== Parse tokens from equation string ====
def __parse(string):
    tokens = re.split(_parseRe, string)
    tokens = list(filter(None, tokens)) #Remove empty list entries
    tokens = list(filter(lambda x: not x.isspace(), tokens)) #Remove whitespace

    i = 1
    if tokens[0] == '-': #Convert unary '-' to '|'
        tokens[0] = '|'
    while i < len(tokens):
        if tokens[i] == '-' and not __isNumber(tokens[i-1]): #Unary '-'
            tokens[i] = '|'
        elif tokens[i] == '(' and __isNumber(tokens[i-1]): #Implicit multiplication
            tokens.insert(i, '*')
        i += 1

    return tokens

#==== Apply Shunting-yard algorithm to make tokens postfix ====
#https://en.wikipedia.org/wiki/Shunting-yard_algorithm
def __postfix(tokens):
    output = []
    operators = []

    for t in tokens:
        try:
            num = float(t)
            output.append(num)
        except ValueError:
            if t in _funcs:
                operators.append(t)
            elif t in _prec:
                while (len(operators) > 0
                       and operators[-1] not in ('(',')',_funcs)
                       and (_prec[operators[-1]] > _prec[t]
                            or (_prec[operators[-1]] == _prec[t] and t not in ['^','|']))
                       and operators[-1] != '('):
                    output.append(operators.pop())
                operators.append(t)
            elif t == '(':
                operators.append(t)
            elif t == ')':
                while len(operators) > 0 and operators[-1] != '(':
                    output.append(operators.pop())
                if len(operators) > 0 and operators[-1] == '(':
                    operators.pop()
                if len(operators) > 0 and operators[-1] in _funcs:
                    output.append(operators.pop())
    while len(operators) > 0:
        output.append(operators.pop())

    return output

#==== Perform the calculation on postfix equation ====
def __doMath(rpn):
    i = 0
    tmp = 0

    while len(rpn) > 1:
        #Unary operator
        if rpn[i] == '|':
            rpn[i-1] = -rpn[i-1]
            del rpn[i]
            
        #Binary operator
        elif rpn[i] in _prec and rpn[i] != '|':
            if rpn[i] == '+':
                tmp = rpn[i-2] + rpn[i-1]
            if rpn[i] == '-':
                tmp = rpn[i-2] - rpn[i-1]
            elif rpn[i] == '*':
                tmp = rpn[i-2] * rpn[i-1]
            elif rpn[i] == '/':
                tmp = rpn[i-2] / rpn[i-1]
            elif rpn[i] == '^':
                tmp = rpn[i-2] ** rpn[i-1]

            rpn[i-2] = tmp
            del rpn[i-1:i+1]
            i -= 2

        #Function
        elif rpn[i] == 'sqrt':
            tmp = math.sqrt(rpn[i-1])
            rpn[i-1] = tmp
            del rpn[i]
            i -= 1
        elif rpn[i] == 'abs':
            tmp = math.fabs(rpn[i-1])
            rpn[i-1] = tmp
            del rpn[i]
            i -= 1
        elif rpn[i] == 'log':
            tmp = math.log10(rpn[i-1])
            rpn[i-1] = tmp
            del rpn[i]
            i -= 1

        #Operand
        else:
            i += 1

    if rpn[0].is_integer():
        return int(rpn[0])
    else:
        return round(rpn[0], 10)

#==== Verify if tokens are workable ====
def __verifyTokens(tokens):
    numLeftPeren = tokens.count('(')
    numRightPeren = tokens.count(')')
    numOperands = sum(__isNumber(t) for t in tokens)
    numFuncs = sum(re.fullmatch(_funcsRe, t) != None for t in tokens)
    numOperators = (sum(re.fullmatch(_opsRe, t) != None for t in tokens) +
                    - numLeftPeren - numRightPeren)

    if (tokens[-1] in _prec
        or (tokens[0] in _prec and tokens[0] != '|')):
        raise errors.CustomCommandException("calc", "missing_operand")

    for i in range(len(tokens)-1):
        if re.match('^(?!{}|\|)'.format(_parseRe), tokens[i]) != None:
            raise errors.CustomCommandException("calc", "bad_tokens")
        elif (tokens[i] in _prec
              and tokens[i-1] in _prec
              and tokens[i-1] != '|'):
            raise errors.CustomCommandException("calc", "missing_operand")

    if numOperators + numFuncs <= 0:
        raise errors.CustomCommandException("calc", "few_operators")
    elif numLeftPeren != numRightPeren:
        raise errors.CustomCommandException("calc", "open_perens")
    elif numOperators > numOperands:
        raise errors.CustomCommandException("calc", "too_many_operators")

#==== Verify if a token is a number ====
def __isNumber(tok):
    return re.fullmatch(_numRe, tok) != None

