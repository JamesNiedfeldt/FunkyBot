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
        '^': 3,
        '*': 2,
        '/': 2,
        '+': 1,
        '-': 1 }

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
    tokens = re.split('([-]?[0-9]*[.]?[0-9]+)|(sqrt)|([+/\-*^()])', string)
    tokens = list(filter(None, tokens)) #Remove empty list entries
    return list(filter(lambda x: not x.isspace(), tokens)) #Remove whitespace

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
            if t == 'sqrt':
                operators.append(t)
            elif t in _prec.keys():
                while (len(operators) > 0
                       and operators[-1] not in ('(',')','sqrt')
                       and (_prec[operators[-1]] > _prec[t]
                            or (_prec[operators[-1]] == _prec[t] and t != '^'))
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
                if len(operators) > 0 and operators[-1] == 'sqrt':
                    output.append(operators.pop())
    while len(operators) > 0:
        output.append(operators.pop())

    return output

#==== Perform the calculation on postfix equation ====
def __doMath(rpn):
    i = 0
    tmp = 0

    while len(rpn) > 1:
        #Binary operator
        if rpn[i] in _prec.keys():
            if rpn[i] == '+':
                tmp = rpn[i-2] + rpn[i-1]
            if rpn[i] == '-':
                tmp = rpn[i-2] - rpn[i-1]
            if rpn[i] == '*':
                tmp = rpn[i-2] * rpn[i-1]
            if rpn[i] == '/':
                tmp = rpn[i-2] / rpn[i-1]
            if rpn[i] == '^':
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

        #Operand
        else:
            i += 1

    return rpn[0]

#==== Verify if tokens are workable ====
def __verifyTokens(tokens):
    numOperands = sum(re.fullmatch('[-]?[0-9]*[.]?[0-9]+',t) != None for t in tokens)
    numOperators = sum(re.fullmatch('[+/\-*^]',t) != None for t in tokens)
    numFuncs = sum(re.fullmatch('sqrt',t) != None for t in tokens)
    numLeftPeren = tokens.count('(')
    numRightPeren = tokens.count(')')

    if numOperands <= 0:
        raise errors.CustomCommandException("calc", "few_operands")
    elif numOperators + numFuncs <= 0:
        raise errors.CustomCommandException("calc", "few_operators")
    elif numLeftPeren != numRightPeren:
        raise errors.CustomCommandException("calc", "open_perens")
    elif numOperators > numOperands:
        raise errors.CustomCommandException("calc", "too_many_operators")

