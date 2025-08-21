import pandas as pd
import numpy as np
import random as rn

data=[1,2,3,4]
label=['a','b','c','d']
series=pd.Series(data,index=label)

print(series)

# Numpy Exercises

def exercise_1():
    """
    Select all even numbers from the array [1, 2, 3, 4, 5, 6, 7, 8].
    Output: [2, 4, 6, 8]
    """
    data=[1,2,3,4,5,6,7,8,9]
    x=np.array(data)
    ls_sorted=x[x%2==0]
    print(ls_sorted)
exercise_1()
def exercise_2():
    """
    Compute the mean, sum, and standard deviation of a random array of 100 numbers.
    Generate the array using np random module.
    """
    x=np.array([rn.randint(0,100) for _ in range(10)])
    suma=np.sum(x)
    mean=np.mean(x)
    deviation=np.std(x)
    print(f'Suma numerelor este:{suma}')
    print(f'Media lor este:{mean}')
    print(f'Deviacion este:{deviation}')
exercise_2()
def exercise_3():
    """
    Generate an 1D array with 12 elements. Reshape it into a 3x4 2D array.
    Example: in - [0 ,1 ,2, 3, 4, 5, 6, 7, 8, 9 , 10 , 11]
            out - [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]]
    """
    x=np.array([i for i in range(12)])
    print(x.reshape(3,4))
exercise_3()
def exercise_4():
    """
    Find the index of the maximum element in a 2D array.
    Example: in - [[3, 5, 10], [9, 2, 8]]
            out - (0, 2)
    """
    print('Maximul din fiecare linie este:')
    x = np.array([[3, 5, 10],[9, 2, 8]])
    for i in x:
        print(i.max(),end=' ')
    print()
exercise_4()
def exercise_5():
    """
    Create two 2x2 matrices. Perform the element-wise multiplication and the matrix multiplication (dot product).
    Example: in - [[1, 2], [3, 4]]
                  [[5, 6], [7, 8]]
            out - [[5, 12], [21, 32]]
                  [[19, 22], [43, 50]]
    """
    matrix_1=np.array([[1, 2], [3, 4]])
    matrix_2=np.array([[5, 6], [7, 8]])
    print(np.multiply(matrix_1, matrix_2))
    print(np.dot(matrix_1, matrix_2))

exercise_5()


# Pandas Exercises
"""
 Import the dataset from the week8_dataset folder in different dataframes.
 (sales, targets, product, salesperson, region)
 Using this data respond to the next questions:


 1. Which is the most profitable month on average?
    # clean sales data (remove $ and covert 'Sales', 'Cost' to float)
    # compute 'Margin' column = 'Sales' - 'Cost'
    # convert 'OrderDate' to datetime and extract month to 'OrderMonth' (dt.month)
    # group by 'OrderMonth' compute mean for 'Margin' column
    # find the month with the highest value of mean 

 2. Show names of top 5 best performing employees by total order value in 2020.
    # convert 'OrderDate' to datetime and extract year to 'Year' (dt.year)
    # filter sales by 'Year'
    # merge with salesperson by 'EmployeeKey'
    # group by 'Salesperson' to find the highest value for the sum of 'Sales'

 3. How many products were sold in 2020 grouped by product category?
    # filter sales by 'Year'
    # merge product with sales on 'ProductKey'
    # count the 'ProductKey' values grouped by 'Category'

 4. Which country is the least profitable?
    # merge sales with region by 'SalesTerritoryKey'
    # group by 'Country' to find the min 'Margin' value

 5. Find revenue margin, and target for each year.
    # clean target data (remove $ and covert 'Target' to float) and use also sales data
    # convert 'TargetMonth' to datetime and extract year to 'Year' (dt.year)
    # convert 'OrderDate' to datetime and extract year to 'Year' (dt.year)
    # revenue margin = group sales by 'Year' and compute the sum for 'Sales' and 'Margin' columns (from Q1)
    # target = group targets by 'Year' and compute the sum of 'Target' column
    # merge revenue margin with target on 'Year'

 6. Which product category made the most profit by year?
    # merge product with sales on 'ProductKey'
    # profit it's the sum of margin column grouped by 'Year' and 'Category'
    # find the category with the highest value 'Margin'

"""