"""
1. Model the following
a) A PhoneBook class that has a list of contacts
The PhoneBook should support the following
- ability to add contacts (check for phone number uniqueness)
- ability to remove contacts
- ability to check if a phone number is already in the contacts list
- a display method that shows all contacts in a pretty way
- implements the singleton design pattern

b) 3 different types of contacts, Friend, Colleague, Relative, having the following attributes

Friend:
- name
- phone number
- favorite activity
Colleague:
- name
- phone number
- place of work
Relative
- name
- phone number
- type of relative (ex: mother, brother, etc.)

The contacts should support the following:
- equality comparison
- string representation


2. Model the following:
a) a Point class that has two values, x and y, representing coordinates
Add suport for the following
- addition and substraction of two points
- equality
- string representation
Make examples showcasing these capabilities

b) a PointCollection class that has a list of points
Add support for the following
- check that a point is in the collection
- len support
- comparison between two point collections (based on length)
- addition and substraction (for both Point and PointCollection)
- string representation
Make examples showcasing these capabilities

c) a Triangle class that has 3 Point objects representing the corners of the triangle
Add support for the following
- validate that the points form a valid triangle (not a line)
- equality
- string representation
- len support (based on triangle area)
- comparison between other triangles (based on triangle area)
- in support (a triangle is within another triangle, a point is in the triangle, a point collection is in a triangle)

d) a Rectangle class that has 4 Point obejcts representing the corners of the rectangle
Add support for the following
- validate that the points form a valid rectangle
- equality
- string representation
- len support (based on rectangle area)
- comparison between other rectangles (based on rectangle area)
- in support  (a rectangle is within another rectangle, a point is in the rectangle, a point collection is in a rectangle)

"""

class Contact:
    def __init__(self, name: str, phone_number: str):
        self.name: str = name
        self.phone_number: str = phone_number

    def __str__(self) -> str:
        return f"------\nName: {self.name}\nPhone number: {self.phone_number}"

    def __eq__(self, other: 'Contact') -> bool:
        return self.phone_number == other.phone_number


class Friend(Contact):
    def __init__(self, name: str, phone_number: str, favorite_activity: str):
        super().__init__(name=name, phone_number=phone_number)
        self.favorite_activity: str = favorite_activity

    def __str__(self) -> str:
        return f"{super().__str__()}\nFavorite activity: {self.favorite_activity}"


class Colleague(Contact):
    def __init__(self, name: str, phone_number: str, place_of_work: str):
        super().__init__(name=name, phone_number=phone_number)
        self.place_of_work: str = place_of_work

    def __str__(self) -> str:
        return f"{super().__str__()}\nPlace of work: {self.place_of_work}"


class Relative(Contact):
    def __init__(self, name: str, phone_number: str, type_of_relative: str):
        super().__init__(name=name, phone_number=phone_number)
        self.type_of_relative: str = type_of_relative

    def __str__(self) -> str:
        return f"{super().__str__()}\nType of relative: {self.type_of_relative}"


class PhoneBook:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.contacts: list = []
            PhoneBook._initialized = True

    def __str__(self) -> str:
        return f"{"\n".join([contact.__str__() for contact in self.contacts])}"

    def __contains__(self, other: 'Contact') -> bool:
        return other in self.contacts

    def add_contact(self, contact: Contact) -> bool:
        if contact not in self.contacts:
            self.contacts.append(contact)
            return True
        return False

    def remove_contact(self, contact: Contact) -> bool:
        if contact in self.contacts:
            self.contacts.remove(contact)
            return True
        return False




friend_1 = Friend(name="John", phone_number="10000", favorite_activity="tennis")
relative_1 = Relative(name="Alex", phone_number="10000", type_of_relative="brother")
relative_2 = Relative(name="Alex", phone_number="123456", type_of_relative="brother")
relative_3 = Relative(name="Daniel", phone_number="123321", type_of_relative="brother")
# print(friend_1)
# print(relative_1)
# print(f"Is friend and relative the same? {friend_1 == relative_1}")

phone_book = PhoneBook()
phone_book.add_contact(friend_1)
phone_book.add_contact(relative_1)
phone_book.add_contact(relative_2)

print(phone_book)

# print(f"Is contact in phone book? {relative_3 in phone_book}")

phone_book.remove_contact(relative_2)

print(phone_book)




