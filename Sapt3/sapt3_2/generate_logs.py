from datetime import datetime
import random
import time
import sys

"""
This module should contain a function generate_random_logs(entries_number, filename) that:
Generates entries_number (e.g., 100-200) log entries.
      Each log entry should be a dictionary with keys like:
        - timestamp (current time, formatted between []; ex: [2025-07-22 12:54:07])
        - level (randomly choose from "INFO", "WARNING", "ERROR")
        - ip (a random integer using random.randint)
        - username (a random user, e.g. "test_user", "admin", "guest")
        - message (a random message, e.g., "User {user_name} logged in from IP {insert ip}",
                                            "User {user_name} logged out from IP {insert ip}",
                                            "Failed login attempt from IP ")
            * when the error message is "ERROR", add "- Username: {username}" at the end of message
    Writes these log entries, one per line, to the specified filename (e.g., system.log).

    example: [2025-07-22 13:14:04] ERROR: Failed login attempt from IP 192.168.1.10 - Username: john
"""




def generate_random_logs(entries_number, filename):
    #user
    username = ["test_user", "admin", "guest"]

    #level
    level = ["INFO", "WARNING", "ERROR"]

    for i in range(entries_number):
        #name
        user_name = random.choice(username)
        # time
        current_timestamp = time.time()
        dt_object = datetime.fromtimestamp(current_timestamp)
        formatted_full = dt_object.strftime("%Y-%m-%d , %I:%M:%S ")
        #level
        choose_randomly_level = random.choice(level)
        #IP
        ip1 = str(random.randint(1, 256))
        ip2 = str(random.randint(1, 256))
        ip3 = str(random.randint(1, 64))
        ip4 = str(random.randint(1, 10))
        ip = ip1 + '.' + ip2 + '.' + ip3 + '.' + ip4
        #message
        messages = [f"User {user_name} logged in from IP {ip}", f"User {user_name} logged out from IP {ip}",
                    f"Failed login attempt from IP {ip} "]


        print(choose_randomly_level)
        if choose_randomly_level == "ERROR":
            new_message = messages[0] + f" - Username: {user_name}"
            with open('generate_random','a') as file:
                file.write(f'[{formatted_full}] {choose_randomly_level} {new_message} \n')
        else:
            with open('generate_random', 'a') as file:
                file.write(f'[{formatted_full}] {choose_randomly_level} {messages[random.randint(0,1) ]} \n')




if __name__ == '__main__':
    entries_number=random.randint(1,10)
    filename=sys.argv[0]
    generate_random_logs(entries_number,filename)
