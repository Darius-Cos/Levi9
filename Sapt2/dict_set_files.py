import os
import random

"""
Ex 1:
Given a text, count how many times each letter appears.
Given large enoughs text, is there a difference between english and romanian texts?
"""
def count_letters(text):
    dict={}
    for i in text:
        if i not in dict:
            dict[i]=1
        else:
            dict[i]+=1
    print(dict)

"""
Ex 2:
Generate 1000 unique latitude and longitude coordinates of type (x,y), should be integers, x between -90 and 90, y between -180 and 180.
Find and print the closest two points and the farthest two points.
"""
def distance(cord1, cord2):
    x1, y1 = cord1
    x2, y2 = cord2
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5
def unique():
    coordonate=set()
    while len(coordonate)<10:
        x=random.randint(-90,90)
        y=random.randint(-180,180)
        coordonate.add((x,y))

        farthest=0
        closest=float('inf')
        closest_pair=None
        farthest_pair=None
        coordonatele=list(coordonate)
        for i in range(len(coordonatele)):
            for j in range(i+1,len(coordonatele)):
                dist=distance(coordonatele[i],coordonatele[j])
                if dist < closest:
                    closest = dist
                    closest_pair = (coordonatele[i], coordonatele[j])
                if dist > farthest:
                    farthest = dist
                    farthest_pair = (coordonatele[i], coordonatele[j])
        print("Coordonate generate:")
        for coord in coordonatele:
            print(coord)
        print("\nCel mai apropiat cuplu:", closest_pair, "cu distanța:", closest)
        print("Cel mai îndepărtat cuplu:", farthest_pair, "cu distanța:", farthest)


"""
Ex 3:
For a parking lot, you have the following information.
- a list of cars that is in the parking lot (existing_cars.txt)
- a list of cars that have parked in today (cars_in.txt)
- a list of cars that have left the parking lot today (cars_out.txt)

Print the number of cars and the car plates for the following:
- cars that have parked and also left today
- cars that were already parked (before today) and left today
- cars that are still in the parking lot
"""
def get_car_plates(file_name):
    with open(file_name, 'r')as fp:
        return set(line.strip() for line in fp.readlines())


def parking():
    existing_cars = get_car_plates('existing_cars.txt')
    cars_in = get_car_plates('cars_in.txt')
    cars_out =  get_car_plates('cars_out.txt')

    cars_that_left_immediately = cars_in.intersection(cars_out)
    existing_cars_that_left = existing_cars.intersection(cars_out)
    cars_still_in_parking = existing_cars.union(cars_in).difference(cars_out)

    print(f'{len(cars_that_left_immediately)} cars that have left immediately: {cars_that_left_immediately}')
    print(f'{len(existing_cars_that_left)} existing cars that have left: {existing_cars_that_left}')
    print(f'{len(cars_still_in_parking)} cars still in parking: {cars_still_in_parking}')



"""
Ex 4:
You are given a list of fictional transactions, where each transaction is represented as a tuple: (user_id, item, amount).
Count how many times each user made a transaction.
Count how many times each item was bought.
Find the user who made the most transactions.
Find the most frequently bought item.
"""
def transactions():
    person=[]
    with open('input_tranzactii.txt','r') as f:
        for line in f.readlines():
            user_id,item,amount=line.strip().split(',')
            person.append((user_id,item,int(amount)))
    user_transactions={}
    for user,_,_ in person:
        user_transactions[user]=user_transactions.get(user,0)+1
    item_transactions={}
    for _,items,_ in person:
        item_transactions[items]=item_transactions.get(items,0)+1

    most_active_user=max(user_transactions,key=user_transactions.get)
    most_bought_item=max(item_transactions,key=item_transactions.get)

    print("User with most transactions:", most_active_user)

    print("Most frequently bought item:", most_bought_item)


"""
Ex 5:
You're given a file input_studenti.txt that contains student grade data.
Each student has multiple grades per subject, and the structure is stored as a nested dictionary in the following format:
student_grades = {
    "Alice": {"Math": [8, 9, 7], "English": [6, 7], "Science": [9, 10, 10]},
    "Bob": {"Math": [10, 9], "English": [8, 9, 9], "Science": [6, 7]},
    ...-
}

Read the data from input.txt and parse it into the student_grades nested dictionary.
Print each student’s average grade across all subjects.
Find the student with the highest overall average grade. (Try using the max function and a lambda function as it's key for this)
"""
def average_grade(catalog):
    new_catalog={}
    for name,grades in catalog.items():
        total=0
        count=0
        for grade in grades.values():
            total+=sum(grade)
            count+=len(grade)
        new_catalog[name]=total/count if count!=0 else 0
    return new_catalog
def highest_grade(new_catalog):
    return max(new_catalog.items(), key=lambda x:x[1] ) #tuplu (cheie, valoare)
    #max(new_catalog, key=new_catalog.get) doar cheia cu valoarea max "Ana"

def read_files(file):
    catalog={}
    with open(file,'r') as f:
        for line in f:
            parts=line.strip().split(';')
            name=parts[0]
            subjects={}
            for part in parts[1:]:
                subject,grades=part.split(':')
                grades=list(map(int,grades.split(',')))
                subjects[subject]=grades
            catalog[name]=subjects

        return catalog


def studenti():
    catalog=read_files('input_studenti.txt')
    new_catalog=average_grade(catalog)
    print(new_catalog)
    student=highest_grade(new_catalog)
    print(student)


if __name__ == '__main__':
    print('--------------------------Count letters--------------------------')
    count_letters('Ana are mere ')
    print('--------------------------Distance two points--------------------------')
    unique()
    print('--------------------------Parking Slot--------------------------')
    parking()
    print('--------------------------Transactions:--------------------------')
    transactions()
    print('--------------------------CAtalog:--------------------------')
    studenti()

