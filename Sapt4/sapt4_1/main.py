import threading, queue, time, random
import pytest
from unittest.mock import patch
import concurrent.futures
# ===============================================
# EXERCISE 1: Basic Unit Testing
# ===============================================

class Calculator:
    def add(self, a, b):
        return a + b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def multiply(self, a, b):
        return a * b

@pytest.fixture
def calc():
    return Calculator()

def test_add_returns_expected_for_positive_number(calc):
    assert calc.add(2, 3) == 5

def test_multiply_returns_expected_for_positive_number(calc):
    assert calc.multiply(4, -2) == -8

def test_divide_returns_expected_for_positive_number(calc):
    assert calc.divide(10, 2) == 5

def test_divide_throws_error_for_zero_input(calc):
    with pytest.raises(ValueError):
        calc.divide(5, 0)

def test_add_returns_expected_for_negative_number(calc):
    assert calc.add(-1, -2) == -3

def test_multiply_returns_expected_for_negative_number(calc):
    assert calc.multiply(-3, 3) == -9

def test_divide_returns_expected_for_negative_number(calc):
    assert calc.divide(-6, 2) == -3

# ===============================================
# EXERCISE 2: Mock Testing
# ===============================================

def send_notification(email, message):
    """Function that 'sends' an email notification"""
    print(f"Sending email to {email}: {message}")
    # Simulate email sending
    if "@" not in email:
        raise ValueError("Invalid email address")
    return f"Email sent to {email}"

def test_send_notification_valid():
    result = send_notification("test@example.com", "Hello")
    assert result == "Email sent to test@example.com"

def test_send_notification_invalid():
    with pytest.raises(ValueError):
        send_notification("invalid_email", "Hi")

@patch("builtins.print")
def test_send_notification_print_called(mock_print):
    send_notification("a@b.com", "Msg")
    mock_print.assert_called_with("Sending email to a@b.com: Msg")


# ===============================================
# EXERCISE 3: Parametrized Testing
# ===============================================

def is_strong_password(password):
    """Check if password meets strength requirements"""
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True

@pytest.mark.parametrize("password,expected", [
    ("MyPass123", True),
    ("StrongP@ss1", True),
    ("weak", False),
    ("NOLOWER123", False),
    ("noupper123", False),
    ("NoDigits", False),
])
def test_is_strong_password(password, expected):
    assert is_strong_password(password) == expected


# ===============================================
# EXERCISE 4: Threading Race Condition
# ===============================================

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        current = self.balance
        time.sleep(0.001)  # Simulate processing time
        self.balance = current + amount

    def withdraw(self, amount):
        if self.balance >= amount:
            current = self.balance
            time.sleep(0.001)  # Simulate processing time
            self.balance = current - amount
            return True
        return False

def test_race_condition():
    account = BankAccount(100)
    threads = []
    for _ in range(100):
        t1 = threading.Thread(target=account.deposit, args=(5,))
        t2 = threading.Thread(target=account.withdraw, args=(5,))
        threads.extend([t1, t2])
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("Final balance (should be 100):", account.balance)

# Fix with Lock
class SafeBankAccount(BankAccount):
    def __init__(self, balance=0):
        super().__init__(balance)
        self.lock = threading.Lock()

    def deposit(self, amount):
        with self.lock:
            super().deposit(amount)

    def withdraw(self, amount):
        with self.lock:
            return super().withdraw(amount)


# ===============================================
# EXERCISE 5: Producer-Consumer with Queue
# ===============================================
q = queue.Queue()

def producer(q, id):
    for _ in range(5):
        num = random.randint(1, 100)
        q.put(num)
        print(f"Producer {id} produced {num}")
        time.sleep(random.uniform(0.1, 0.5))

def consumer(q, id):
    while True:
        try:
            num = q.get(timeout=2)
            print(f"Consumer {id} consumed {num}, squared: {num*num}")
            q.task_done()
        except queue.Empty:
            break

producers = [threading.Thread(target=producer, args=(q, i)) for i in range(2)]
consumers = [threading.Thread(target=consumer, args=(q, i)) for i in range(3)]

for t in producers + consumers:
    t.start()
for t in producers:
    t.join()
q.join()

# ===============================================
# EXERCISE 6: Thread Synchronization with Events
# ===============================================

green_light = threading.Event()

def car(car_id):
    print(f"Car {car_id} waiting for green light")
    green_light.wait()
    print(f"Car {car_id} passes")

def traffic_light():
    print("Red light ON")
    time.sleep(2)
    print("Green light ON")
    green_light.set()

cars = [threading.Thread(target=car, args=(i,)) for i in range(5)]
for c in cars:
    c.start()
threading.Thread(target=traffic_light).start()

# ===============================================
# EXERCISE 7: Barrier Synchronization
# ===============================================

import threading, time, random

barrier = threading.Barrier(5)

def team_member(member_id):
    time.sleep(random.uniform(0.5, 2.0))
    print(f"Member {member_id} joined")
    barrier.wait()
    print(f"Member {member_id} starts meeting")

threads = [threading.Thread(target=team_member, args=(i,)) for i in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# ===============================================
# EXERCISE 8: Thread Pool Executor
# ===============================================

import threading

numbers = list(range(10))
filename = 'output.txt'
lock = threading.Lock()
barrier = threading.Barrier(len(numbers))
current = {'index': 0}

def write_number(i):
    while True:
        with lock:
            if current['index'] == i:
                with open(filename, 'a') as f:
                    f.write(f"{i}, ")
                current['index'] += 1
                break
        # Let other threads run
        barrier.wait()

# Clear file before writing
open(filename, 'w').close()

threads = [threading.Thread(target=write_number, args=(i,)) for i in numbers]
for t in threads:
    t.start()
for t in threads:
    t.join()


# ===============================================
# EXERCISE 10: Integration Testing with Fixtures
# ===============================================
class UserManager:
    def __init__(self):
        self.users = {}
        self.lock = threading.Lock()

    def add_user(self, username, email):
        with self.lock:
            if username in self.users:
                raise ValueError("User already exists")
            self.users[username] = {"email": email, "active": True}

    def get_user(self, username):
        return self.users.get(username)

    def deactivate_user(self, username):
        with self.lock:
            if username in self.users:
                self.users[username]["active"] = False

@pytest.fixture
def empty_manager():
    return UserManager()

@pytest.fixture
def manager_with_users():
    um = UserManager()
    um.add_user("alice", "alice@example.com")
    um.add_user("bob", "bob@example.com")
    return um

def test_add_and_get_user(empty_manager):
    empty_manager.add_user("charlie", "c@example.com")
    user = empty_manager.get_user("charlie")
    assert user["email"] == "c@example.com"
    assert user["active"]

def test_duplicate_user(manager_with_users):
    with pytest.raises(ValueError):
        manager_with_users.add_user("alice", "alice2@example.com")

def test_deactivate_user(manager_with_users):
    manager_with_users.deactivate_user("bob")
    assert not manager_with_users.get_user("bob")["active"]

def test_concurrent_adds(empty_manager):
    def add():
        try:
            empty_manager.add_user("dave", "d@example.com")
        except ValueError:
            pass
    threads = [threading.Thread(target=add) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert empty_manager.get_user("dave")["email"] == "d@example.com"

@pytest.mark.parametrize("username,email", [
    ("eve", "eve@example.com"),
    ("frank", "frank@example.com"),
])
def test_parametrized_add(empty_manager, username, email):
    empty_manager.add_user(username, email)
    assert empty_manager.get_user(username)["email"] == email


"""
import threading
import time
import random
import pytest
from unittest.mock import patch, MagicMock
# ===============================================
# EXERCISE 1: Basic Unit Testing
# ===============================================

class Calculator:
    def add(self, a, b):
        return a + b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def multiply(self, a, b):
        return a * b

# TODO: Write pytest tests for Calculator class
# Test cases should include:
# - Normal addition, multiplication and division
# - Division by zero error
# - Test for negative numbers

# ===============================================
# EXERCISE 2: Mock Testing
# ===============================================
# Test a function that sends emails. Mock the print function to verify email sending behavior.

def send_notification(email, message):
    """Function that 'sends' an email notification"""
    print(f"Sending email to {email}: {message}")
    # Simulate email sending
    if "@" not in email:
        raise ValueError("Invalid email address")
    return f"Email sent to {email}"

# TODO: Write a test using @patch to mock the email sending
# Verify that:
# - Function is called with correct arguments
# - Invalid emails raise ValueError
# - Function returns expected message

# ===============================================
# EXERCISE 3: Parametrized Testing
# ===============================================
# Test a password validation function with multiple test cases

def is_strong_password(password):
    """Check if password meets strength requirements"""
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True

# TODO: Create parametrized tests with different password examples:
# Valid: "MyPass123", "StrongP@ss1"
# Invalid: "weak", "NOLOWER123", "noupper123", "NoDigits"

# ===============================================
# EXERCISE 4: Threading Race Condition
# ===============================================
# Create a bank account class and demonstrate race conditions

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        current = self.balance
        time.sleep(0.001)  # Simulate processing time
        self.balance = current + amount

    def withdraw(self, amount):
        if self.balance >= amount:
            current = self.balance
            time.sleep(0.001)  # Simulate processing time
            self.balance = current - amount
            return True
        return False

# TODO: 
# 1. Create multiple threads that deposit/withdraw simultaneously
# 2. Show the race condition (final balance will be incorrect)
# 3. Fix it using threading.Lock

# ===============================================
# EXERCISE 5: Producer-Consumer with Queue
# ===============================================
# Implement a producer-consumer pattern using Queue

# TODO: Create a producer-consumer system where:
# - Producer threads generate random numbers and put them in a queue
# - Consumer threads take numbers from queue and process them (e.g., square them)
# - Use queue.Queue() for thread-safe communication
# - Create 2 producers and 3 consumers

# ===============================================
# EXERCISE 6: Thread Synchronization with Events
# ===============================================
# Create a traffic light system using Events

# TODO: Implement a traffic light controller where:
# - Red light event stops all cars
# - Green light event allows cars to pass
# - Use threading.Event() to coordinate
# - Create multiple car threads that wait for green light


# ===============================================
# EXERCISE 7: Barrier Synchronization
# ===============================================
# Implement a team meeting scenario using Barrier

# TODO: Create a virtual team meeting where:
# - 5 team members need to join before meeting starts
# - Use threading.Barrier(5) to wait for everyone
# - Each member takes different time to "connect"
# - Meeting only starts when all members are ready

# ===============================================
# EXERCISE 8: Thread Pool Executor
# ===============================================
# Use ThreadPoolExecutor for concurrent file processing

# TODO: 
# - Create a list of 10 numbers that will be written in a file "output.txt"
# - Use ThreadPoolExecutor to process them concurrently
# - Print results as they complete
# - Compare with sequential processing time

# ===============================================
# EXERCISE 10: Integration Testing with Fixtures
# ===============================================
# Create a comprehensive test suite using pytest fixtures

class UserManager:
    def __init__(self):
        self.users = {}
        self.lock = threading.Lock()
    
    def add_user(self, username, email):
        with self.lock:
            if username in self.users:
                raise ValueError("User already exists")
            self.users[username] = {"email": email, "active": True}
    
    def get_user(self, username):
        return self.users.get(username)
    
    def deactivate_user(self, username):
        with self.lock:
            if username in self.users:
                self.users[username]["active"] = False

# TODO: Create pytest fixtures and tests for UserManager:
# - Fixture for empty UserManager
# - Fixture for UserManager with test users
# - Test concurrent user additions (threading)
# - Test user operations with mocks
# - Parametrized tests for various user data

"""