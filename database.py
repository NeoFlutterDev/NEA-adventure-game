import sqlite3
import string
import os
import random

def createDatabase():
    import sqlite3

questions = 10
con = sqlite3.connect('storage.db')
con.execute("PRAGMA foreign_keys = 1")
cur = con.cursor()

# Create the 'accounts' table
cur.execute('''
    CREATE TABLE IF NOT EXISTS accounts(
    accountKey INTEGER PRIMARY KEY AUTOINCREMENT, 
    characterName varchar(255),
    encryptedPassword varchar(255),
    level varchar(255), 
    money varchar(255), 
    weapon varchar(255), 
    armour varchar(255))
''')

# Create the 'questions' table
cur.execute('''
    CREATE TABLE IF NOT EXISTS questions(
    questionKey INTEGER PRIMARY KEY AUTOINCREMENT, 
    question varchar(255),
    answer varchar(255))
''')

# Create the 'weights' table
cur.execute('''
    CREATE TABLE IF NOT EXISTS weights(
    weightKey INTEGER PRIMARY KEY AUTOINCREMENT,
    correct varchar(255), 
    incorrect varchar(255), 
    weight varchar(255), 
    questionID INTEGER,
    FOREIGN KEY (questionID) REFERENCES questions(questionKey)
    )
''')

con.commit()
con.close()
#this creates three seperate tables for the database

def generate_salt():
    return os.urandom(16)

def loop_length(string):
    loopLength = 0
    for char in string:
        loopLength += ord(char)
    return (loopLength % 50) + random.randint(len(string) % 5, 50 * len(string))

def hash_encryption(string):
    hashValue = 0
    primes = [6221, 7433, 2203, 4817, 4241, 6449, 4549, 5717, 2861, 4507, 7607, 7549, 5209]
    for i in range(len(string)):
        hashValue = (hashValue << 3) ^ (hashValue >> 5)
        prime = primes[i % len(primes)]
        hashValue += ord(string[i]) * prime
        hashValue = hashValue % (2**256 - 1)
    return hashValue

def base64_encode(hashValue):
    characterSet = string.digits + string.ascii_letters + '+' + '/'
    base = 64
    encoded = []
    while hashValue > 0:
        hashValue, remainder = divmod(hashValue, base)
        encoded.append(characterSet[remainder])

    alphanumericString = ''.join(reversed(encoded))
    length = 16

    if len(alphanumericString) > length:
        alphanumericString = alphanumericString[:length]
    elif len(alphanumericString) < length:
        alphanumericString = alphanumericString.zfill(length)

    return alphanumericString

def hashing_algorithm(string):
    salt = generate_salt().hex()
    salted_input = string + salt
    hashValue = hash_encryption(salted_input)
    loopLength = loop_length(salted_input)
    for i in range(loopLength):
        hashValue = hash_encryption(str(hashValue)) + salt
    return base64_encode(hashValue)

createDatabase()
