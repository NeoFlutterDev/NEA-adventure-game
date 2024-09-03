import sqlite3
import string

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

createDatabase()
