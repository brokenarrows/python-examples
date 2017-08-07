# -*- coding: utf-8 -*-
import sys
"""
In mathematics, the Fibonacci numbers are the numbers in the following integer sequence, called the Fibonacci sequence,
and characterized by the fact that every number after the first two is the sum of the two preceding ones

https://en.wikipedia.org/wiki/Fibonacci_number
"""


def fib(n):
    if n <= 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def main():
    print('Enter a number : ')
    num = int(sys.stdin.readline())
    print(fib(num))


if __name__ == '__main__':
    main()
