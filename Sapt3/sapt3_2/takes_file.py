import os
import sys
import re
if __name__ == '__main__':
    filename = sys.argv[1]
    print(filename)
    print(os.path.isfile(filename))
    print(os.path.getsize(filename)/1000)
    with open(filename, "r") as file:
        for line in file:
            match = re.search("INFO",line)
            print(match.group(0))
            if match == "INFO":
                print(f"Found: {match}")

"""
Write a Python script that:
    Takes a log file path as a command-line argument.
    Uses os to verify the file exists and display its size in KB.
    Uses regex to identify ERROR and INFO entries, extracting timestamp, IP, username, and action.
    Reformats timestamps from "YYYY-MM-DD HH:MM:SS" to "DD-MMM-YYYY hh:mm AM/PM".
    Stores entries in two dictionaries (error_logs and info_logs), with reformatted timestamps as keys and details as values.
    Pretty-prints these dictionaries as JSON using json.dumps.
    Time the script's execution and print the elapsed time at the end.

     Outputt example:

Monitoring 'log.txt' (45.32 KB)

========== ERROR LOGS ==========
{
    "22-Jul-2025 12:29 PM": "IP: 198.51.100.8 | User: testuser",
    "22-Jul-2025 01:15 PM": "IP: 10.0.0.5 | User: admin"
}

========== INFO LOGS ==========
{
    "22-Jul-2025 12:38 PM": "User: testuser | Action: logged in | IP: 172.16.0.1",
    "22-Jul-2025 01:20 PM": "User: mary | Action: logged out | IP: 192.168.0.22"
}

Process completed in 0.011 seconds.
"""


"""
0. Set up a Virtual Environment:
    Create a new directory for your project.
    Inside this directory, create and activate a virtual environment named venv.
1. Generate Dummy Log Data:
    Create a module generate_logs.py within your project.
    This module should contain a function generate_random_logs(entries_number, filename) that:
    - Generates entries_number (e.g., 100-200) log entries.
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

2. Write a Python script that:
    Takes a log file path as a command-line argument.
    Uses os to verify the file exists and display its size in KB.
    Uses regex to identify ERROR and INFO entries, extracting timestamp, IP, username.
    Reformats timestamps from "YYYY-MM-DD HH:MM:SS" to "DD-MMM-YYYY hh:mm AM/PM".
    Stores entries in two dictionaries (error_logs and info_logs), with reformatted timestamps as keys and details as values.
    Pretty-prints these dictionaries as JSON using json.dumps.
    Time the script's execution and print the elapsed time at the end.

     Output example:

Monitoring 'log.txt' (45.32 KB)

========== ERROR LOGS ==========
{
    "22-Jul-2025 12:29 PM": "IP: 198.51.100.8 | User: testuser",
    "22-Jul-2025 01:15 PM": "IP: 10.0.0.5 | User: admin"
}

========== INFO LOGS ==========
{
    "22-Jul-2025 12:38 PM": "User: testuser | Action: logged in | IP: 172.16.0.1",
    "22-Jul-2025 01:20 PM": "User: mary | Action: logged out | IP: 192.168.0.22"
}

Process completed in 0.011 seconds.

"""
import os
import sys
import re
import json
import time
from datetime import datetime

start_time = time.time()

error_pattern = re.compile(
    r"\[(.*?)] ERROR: Failed login attempt from IP (\d+\.\d+\.\d+\.\d+) - Username: (\w+)"
)
info_pattern = re.compile(
    r"\[(.*?)] INFO: User (\w+) (logged in|logged out) from (\d+\.\d+\.\d+\.\d+)"
)

if len(sys.argv) != 2:
    print("Usage: python curs6_regex.py <path_to_log_file>")
    sys.exit(1)

file_path = sys.argv[1]

if not os.path.isfile(file_path):
    print(f"Error: File '{file_path}' does not exist.")
    sys.exit(1)

file_size_kb = os.path.getsize(file_path) / 1024
print(f"\nMonitoring '{file_path}' ({file_size_kb:.2f} KB)...\n")

error_logs = {}
info_logs = {}

def reformat_timestamp(ts_str):
    try:
        dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d-%b-%Y %I:%M %p")  # e.g., "22-Jul-2025 12:00 PM"
    except ValueError:
        return ts_str

# Process log lines
with open(file_path, "r") as file:
    for line in file:
        line = line.strip()

        error_match = error_pattern.match(line)
        if error_match:
            timestamp, ip, username = error_match.groups()
            new_ts = reformat_timestamp(timestamp)
            error_logs[new_ts] = f"IP: {ip} | User: {username}"
            continue

        info_match = info_pattern.match(line)
        if info_match:
            timestamp, username, action, ip = info_match.groups()
            new_ts = reformat_timestamp(timestamp)
            info_logs[new_ts] = f"User: {username} | Action: {action} | IP: {ip}"

print("\n========== ERROR LOGS ==========")
print(json.dumps(error_logs, indent=3))

print("\n========== INFO LOGS ==========")
print(json.dumps(info_logs, indent=3))

end_time = time.time()
elapsed_time = end_time - start_time
print(f"\nProcess completed in {elapsed_time:.3f} seconds.")

