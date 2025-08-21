import random

def exercise_1(n):
    """
    Write a function that prints numbers from 1 to 10.
    """
    for i in range(1,n+1):
        print(i, end=' ')
    pass

def exercise_2(n):
    """
    Write a function that returns the sum of all numbers from 1 to n.
    Example: exercise_2(5) should return 15 (1+2+3+4+5)
    """
    suma=0
    for i in range(1,n+1):
        suma=suma+i
    print(suma)
    pass

def exercise_3(n):
    """
    Write a function that takes a list of numbers and returns only the even numbers.
    Example: exercise_3([1, 2, 3, 4, 5, 6]) should return [2, 4, 6]
    """
    even_numbers= [x for x in range(1,n+1) if x % 2 == 0]
    print(even_numbers)
    pass

def exercise_4(text):
    """
    Write a function that reverses a string adn returns a list with each letter.
    Example: exercise_4("hello") should return ["o", "l", "l", "e", "h"]
    """
    new_list=[x for x in text]
    print(new_list[::-1])

    pass

def exercise_5(text):
    """
    Write a function that counts the number of vowels in a string.
    Example: exercise_5("hello world") should return 3
    """
    new_list = [x for x in text if x in 'aeiou']
    print(len(new_list))
    pass

def exercise_6(numbers):
    """
    Write a function that finds the maximum number in a list.
    Example: exercise_6([3, 7, 2, 9, 1]) should return 9
    """
    maximum=max(numbers)
    print(maximum)
    pass

def exercise_7(sorted_list, target):
    """
    Implement a search to find the index of a target value in a sorted list.
    Return -1 if not found.
    Example: exercise_7([1, 3, 5, 7, 9, 11], 7) should return 3
    """
    if target in sorted_list:
        print( sorted_list.index(target))
    else:
        return -1


def exercise_8(n):
    """
    Write a function that prints the multiplication table for a given number n.
    Example: exercise_8(3) should print:
    3 x 1 = 3
    3 x 2 = 6
    3 x 3 = 9
    ... up to 3 x 10 = 30
    """
    for i in range(1,n+1):
        print(f'3 X {i}={3*i}')
    pass

def exercise_9(n):
    """
    Write a function that calculates the factorial of a number.
    Example: exercise_9(5) should return 120 (5*4*3*2*1)
    """
    p=1
    for x in range(1,n+1):
        p*=x
    print(f'Factorial = {p}')
    pass


def is_prime(n):

    for x in range(2 ,n ):
        if n%x==0:
            return False
        else:
            return True


def exercise_10(n):
    """
    Write a function that checks if a number is prime.
    Example: exercise_10(17) should return True, is_prime(15) should return False
    """

    if is_prime(n):
        print( True)
    else:
        print( False)
    pass

def exercise_11(list1, list2):
    """
    Write a function that finds common elements between two lists.
    Example: exercise_11([1, 2, 3, 4], [3, 4, 5, 6]) should return [3, 4]
    """
    print('Common elements')
    for x in list1:
        if x in list2:
            print(x, end=' ')
    pass

def exercise_12(lst):
    """
    Write a function that removes duplicates from a list while preserving order.
    Example: exercise_12([1, 2, 2, 3, 4, 4, 5]) should return [1, 2, 3, 4, 5]
    """
    print('\nDuplicates' ,end=' ')
    new_set_list=set(lst)
    print(new_set_list)
    pass

def exercise_13(text, shift):
    """
    Write a function that implements a Caesar cipher (shifts each letter by n positions).
    You can search for ord and chr functions to help with character shifting.
    ord - converts a Unicode character to its corresponding integer Unicode code point value.
    chr - converts an integer Unicode code point value back to its corresponding character.
    Example: exercise_13("abc", 2) should return "cde"
    """
    new_text=''
    for x in text:
        new_text += chr(ord(x)+shift)
    print(new_text)
    pass


def Fibonacci(n):
    if n<=0:
        print("Incorrect Output")
    lista=[0,1]

    if n>2:
        for i in range(2,n):
            lista.append(lista[i-1]+lista[i-2])

    return lista


def exercise_14(n):
    """
    Write a function that generates the first n numbers in the Fibonacci sequence.
    Example: exercise_14(7) should return [0, 1, 1, 2, 3, 5, 8]
    """

    lista=Fibonacci(n)
    print(lista)
    pass



def Spiral_matrix():
    n=5
    vector=[random.randint(0,100) for _ in range(n*n+5)]
    vector.sort()

    matrix=[[0 for _ in range (n)] for _ in range(n)]
    print(matrix)
    left,right=0,n-1
    top,bottom=0,n-1
    k=0
    while left<=right and top<=bottom:
        for i in range (left,right+1):
            matrix[top][i]=vector[k]
            k+=1
        top+=1
        for i in range (top,bottom+1):
            matrix[i][right]=vector[k]
            k+=1
        right-=1
        if top <= bottom:
            for i in range(right,left-1,-1):
                matrix[bottom][i]=vector[k]
                k+=1
            bottom-=1
        if left <= right:
            for i in range(bottom,top-1,-1):
                matrix[i][left]=vector[k]
                k+=1
            left+=1
    print('Spiral matrix:')
    for i in matrix:
        print(i)

"""
00 01 02 03 04 
10 11 12 13 14
20 21 22 23 24
30 31 32 33 34
40 41 42 43 44
"""

if __name__ == "__main__":
    print("Python Week 3 Exercises")
    print("Complete each function above to solve the exercises.")
    n=10
    #exercise_1(n)
    #exercise_2(n)
    #exercise_3(n)
    #exercise_4("hello")
    #exercise_5("hello world")
    #exercise_6([3, 7, 2, 9, 1])
    #exercise_7([1, 3, 5, 7, 9, 11], 7)
    #exercise_8(3)
    #exercise_9(5)
    #exercise_10(17)
    #exercise_11([1, 2, 3, 4], [3, 4, 5, 6])
    #exercise_12([1, 2, 2, 3, 4, 4, 5])
    #exercise_13("abc", 2)
    #exercise_14(7)
    #exercise_15("A man a plan a canal Panama")
    Spiral_matrix()
