""""

>>Strings

name = "Veda"
age = 24
salary = 50000.0
is_employed = True

intro = f"My name is {name}, I am {age} years old, I earn ${salary} per year, and it is {is_employed} that I am employed and have SRE Experience."
print(intro)

#string  methods
print(name.upper())
print(name.lower())
print(name.capitalize())
print(intro.replace("SRE", "AI"))

#list methods
skills = ["Python", "Java", "SRE"]

>>Dictionaries
       
engineer={

    "name": "VedaVidyadaran S",
    "age": 24,
    "skills": ("Python", "Windows", "SRE", "VMWare", "Linux", "AWS"),
    "experience": {"SRE": 2, "Python": 3, "AWS": 1},
    "roles": ("SRE Engineer")
}

name="Veda"
age=24

#print(f"my name is {name} and I am {age} old")

>>Functions

def greet_engineer(name):
    print(f"Good morning, {name}, you are oncall today")

greet_engineer("Veda")
greet_engineer("Raj")


>>Lists 

servers = ["Web-01", "web-02", "db-01", "cache-01"]

print(servers[0])  # Output: Web-01
print(servers[2])  # Output: db-01
servers.append("web-03")
print(servers)  # Output: ['Web-01', 'web-02', 'db-01', 'cache-01', 'web-03']
servers.remove("cache-01")
print(servers)  # Output: ['Web-01', 'web-02', 'db-01', 'web-03']

#Dictionaries

server = {
    'name': 'Web-01',
    'cpu': 67,
    'memory': 32,
    "status": 'active'
}

print(server['cpu'])  # Output: 67
print(server['status'])  # Output: active

#If Else Statements

cpu = 87

if cpu > 90:
    print("Critical - Call the SRE team immediately!")
elif cpu > 75:
    print("Warning - CPU usage is high, monitor closely.")
else:
    print("CPU usage is normal.")

#Loops

servers = ["web-01", "web-02", "db-01"]

for server in servers:
    print(f"checking status of {server}")

"""

#Everything together 

"""

from groq import Groq
from datetime import datetime
import json

servers = [
    {"name": "web-01", "cpu":97, "memory":80},
    {"name": "web-02", "cpu":60, "memory":60},
    {"name": "db-01", "cpu":60, "memory":50}
    ]

def check_server(server):
    name = server["name"]
    cpu = server["cpu"]
    memory = server["memory"]
    time = datetime.now().strftime("%H:%M:%S")

    if cpu > 95 or memory > 80:
        print(f"[{time}] Critical - {name} is under heavy load! CPU: {cpu}%, Memory: {memory}%")
    elif cpu > 70 or memory >= 60:
        print(f"[{time}] Warning - {name} is currently at Borderline Threshold! CPU: {cpu}%, Memory: {memory}%")
    else:
        print(f"[{time}] Systems {name} are under optimal performance. Get a coffee bruh")

for server in servers:
    check_server(server)
    

"""

def is_leap(leap):
    if (leap % 4 == 0 and leap % 100 != 0) or leap % 400 ==0:
            return True
    else:
        return False

print(is_leap(2000))
print(is_leap(1900))
print(is_leap(2024))
print(is_leap(2023))