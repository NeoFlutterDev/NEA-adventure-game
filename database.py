import sqlite3
import string

def createDatabase():
    questions = 10
    con = sqlite3.connect('databases/storage.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE accounts(
        accountKey varchar(255) PRIMARY KEY, 
        characterName varchar(255),
        encryptedPassword varchar(255),
        level varchar(255), 
        money varchar(255), 
        weapon varchar(255), 
        armour varchar(255))
    ''')
    
    cur.execute('''
        CREATE TABLE questions(
        questionKey varchar(255) PRIMARY KEY, 
        question varchar(255),
        answer varchar(255))
    ''')

    cur.execute('''
        CREATE TABLE weights(
        questionKey varchar(255),
        correct varchar(255), 
        incorrect varchar(255), 
        weight varchar(255))
    ''')

def hashing_algorithm(string):
    hashValue = hash_encryption(string)
    for loop in range(5):
        hashValue = hash_encryption(str(hashValue))
    return base62_encode(hashValue)

def hash_encryption(string):
    hashValue = 0
    primes = [37, 53, 61, 79, 97]
    for i in range(len(string)):
        hashValue = (hashValue << 3) ^ (hashValue >> 5)
        prime = primes[i % len(primes)]
        hashValue += ord(string[i]) * prime
        hashValue = hashValue % (2**256 - 1)
    return hashValue

def base62_encode(hashValue):
    characterSet = string.digits + string.ascii_letters
    base = 62
    encoded = []
    while hashValue > 0:
        hashValue, remainder = divmod(hashValue, base)
        encoded.append(characterSet[remainder])

    alphanumericString = ''.join(reversed(encoded))
    length = 10

    if len(alphanumericString) > length:
        alphanumericString = alphanumericString[:length]
    elif len(alphanumericString) < length:
        alphanumericString = alphanumericString.zfill(length)

    return alphanumericString
