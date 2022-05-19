from py_expression_eval import Parser
from sympy import *
from sympy import Symbol
from flask import Flask, request

parser = Parser()


def function(value, equation):
    x = Symbol('x')
    expr = equation
    expr = sympify(expr)
    expr = expr.subs(x, value)
    return expr.evalf()


def derivative(value, equation):
    x = Symbol('x')
    expr = diff(sympify(equation))
    expr = sympify(expr)
    expr = expr.subs(x, value)
    return expr.evalf()


app = Flask(__name__)


@app.route('/bisection', methods=['GET'])
def bisectionMethod():
    d = {'a': [], 'b': [], 'c': [], 'f(a)': [], 'f(b)': []}
    flag = 0
    bisectionEquation = str(request.args['equation'])
    bisectionEquation = bisectionEquation.replace(' ', '+')
    firstRoot = (request.args['firstRoot'])
    firstRoot = float(firstRoot)
    x = firstRoot
    firstRootResult = function(x, bisectionEquation)
    secondRoot = (request.args['secondRoot'])
    secondRoot = float(secondRoot)
    x = secondRoot
    secondRootResult = function(x, bisectionEquation)
    if firstRootResult * secondRootResult > 0:
        return str('The root values are not valid')
    else:
        while flag == 0:
            newRoot = (firstRoot + secondRoot) / 2
            newRoot = float("{:.5f}".format(newRoot))
            firstRootResult = function(firstRoot, bisectionEquation)
            d['a'].append("{:.5f}".format(firstRoot))
            d['b'].append("{:.5f}".format(secondRoot))
            d['c'].append("{:.5f}".format(newRoot))
            d['f(a)'].append(str(firstRootResult))
            d['f(b)'].append(str(secondRootResult))
            if firstRootResult * function(newRoot, bisectionEquation) < 0:
                secondRoot = newRoot
            else:
                firstRoot = newRoot
            if abs(firstRoot - secondRoot) < 0.0001:
                print(d)
                return d

                flag = 1


@app.route('/secant', methods=['GET'])
def secantMethod():
    d = {'a': [], 'b': [], 'c': [], 'error': []}
    flag = 0
    secantEquation = str(request.args['equation'])
    firstRoot = str(request.args['firstRoot'])
    firstRoot = float(firstRoot)

    secondRoot = str(request.args['secondRoot'])
    secondRoot = float(secondRoot)
    while flag == 0:
        firstRootResult = function(firstRoot, secantEquation)
        secondRootResult = function(secondRoot, secantEquation)

        if firstRootResult == secondRootResult:
            d['error'] = 'Math Error'
            return d
        newRoot = secondRoot - (secondRoot - firstRoot) * function(secondRoot, secantEquation) / (
                function(secondRoot, secantEquation) - function(firstRoot, secantEquation))
        newRootResult = function(newRoot, secantEquation)
        d['a'].append("{:.5f}".format(firstRoot))
        d['b'].append("{:.5f}".format(secondRoot))
        d['c'].append("{:.5f}".format(newRoot))
        firstRoot = secondRoot
        secondRoot = newRoot
        print(newRootResult)

        if abs(newRootResult) < 0.0001:
            print(d)
            return d

            flag = 1


@app.route('/newtonRaphason', methods=['GET'])
def newtonRaphason():
    d = {'a': [], 'b': [], 'error': []}
    flag = 0
    newtonRaphasonEquation = str(request.args['equation'])
    firstRoot = str(request.args['firstRoot'])
    firstRoot = float(firstRoot)
    while flag == 0:
        g0 = derivative(firstRoot, newtonRaphasonEquation)
        f0 = function(firstRoot, newtonRaphasonEquation)
        if g0 == 0.0:
            d['error'] = 'Math Error'
            return d
            exit(0)

        secondRoot = firstRoot - f0 / g0
        firstRoot = secondRoot
        d['a'].append("{:.5f}".format(firstRoot))
        d['b'].append("{:.5f}".format(secondRoot))
        f1 = function(secondRoot, newtonRaphasonEquation)
        if abs(f1) < 0.0001:
            return d
            exit(0)


@app.route('/falsePosition', methods=['GET'])
def falsePostion():
    flag = 0
    d = {'a': [], 'b': [], 'c': [], 'error': []}

    methodofFalsePositionEquation = str(request.args['equation'])
    firstRoot = str(request.args['firstRoot'])
    firstRoot = float(firstRoot)
    x = firstRoot
    firstRootResult = function(x, methodofFalsePositionEquation)
    secondRoot = str(request.args['secondRoot'])
    secondRoot = float(secondRoot)
    x = secondRoot
    secondRootResult = function(x, methodofFalsePositionEquation)
    if firstRootResult * secondRootResult > 0:
        print(d)
        return d
    while flag == 0:
        newRoot = firstRoot - function(firstRoot, methodofFalsePositionEquation) * ((secondRoot - firstRoot) / (
                function(secondRoot, methodofFalsePositionEquation) - function(firstRoot,
                                                                               methodofFalsePositionEquation)))
        newRoot = float("{:.5f}".format(newRoot))
        d['a'].append(("{:.5f}".format(firstRoot)))
        d['b'].append(("{:.5f}".format(secondRoot)))
        d['c'].append(("{:.5f}".format(newRoot)))

        firstRootResult = function(firstRoot, methodofFalsePositionEquation)
        if firstRootResult * function(newRoot, methodofFalsePositionEquation) < 0:
            secondRoot = newRoot
        else:
            firstRoot = newRoot
        if abs(function(newRoot, methodofFalsePositionEquation)) < 0.0001:
            return d


if __name__ == "__main__":
    app.run()
