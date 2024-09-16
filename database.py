import sqlite3
import string
import os
import random

def createDatabase():
    try:
        con = sqlite3.connect('storage.db')
        
        # Enable foreign key constraints
        con.execute("PRAGMA foreign_keys = ON")
        
        # Create a cursor object to execute SQL commands
        cur = con.cursor()
        
        # Create the 'accounts' table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS accounts(
            accountKey INTEGER PRIMARY KEY AUTOINCREMENT, 
            characterName TEXT NOT NULL,
            encryptedPassword TEXT NOT NULL,
            level INTEGER NOT NULL, 
            money INTEGER NOT NULL, 
            weapon TEXT,
            armour TEXT)
        ''')
        
        # Create the 'questions' table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS questions(
            questionKey INTEGER PRIMARY KEY AUTOINCREMENT, 
            question TEXT NOT NULL,
            answer TEXT NOT NULL)
        ''')
        
        # Create the 'weights' table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS weights(
            weightKey INTEGER PRIMARY KEY AUTOINCREMENT,
            correct INTEGER NOT NULL, 
            incorrect INTEGER NOT NULL, 
            weight REAL NOT NULL, 
            questionKey INTEGER NOT NULL,
            FOREIGN KEY (questionKey) REFERENCES questions(questionKey)
            )
        ''')
        
        # Commit changes and close the connection
        con.commit()

    except sqlite3.Error as e:
        print('Error:', e)
        #if any errors occur, print them

    finally:
        con.close()
        #close the connection

def table_accounts_insertion(name, password, lvl, money, weapon, armour):

    try:
        con = sqlite3.connect('storage.db')
        cur = con.cursor()
        #connect to the database

        query = '''
        INSERT INTO accounts (characterName, encryptedPassword, level, money, weapon, armour)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        #define the query, with placeholders

        data = (name, password, lvl, money, weapon, armour)
        #enter the data that is to be inserted
        cur.execute(query, data)
     #execute the parameterised query
    
        con.commit()
        #commit the query

    except sqlite3.Error as e:
        print('Error:', e)
        #if any errors occur, print them

    finally:
        con.close()
        #close the connection

def update_account_info(lvl, money, weapon, armour, accountKey):

    try:
        con = sqlite3.connect('storage.db')
        cur = con.cursor()
        #connect to the database

        query = '''
        UPDATE accounts
        SET level = ?, money = ?, weapon = ?, armour = ?
        WHERE accountKey = ?
        '''
        #define the query, with placeholders

        data = (lvl, money, weapon, armour, accountKey)
        #enter data that is to replace the old data
        cur.execute(query, data)
        #execute the parameterised query

        con.commit()
        #commit the query

    except sqlite3.Error as e:
        print('Error:', e)
        #if any errors occur, print them

    finally:
        con.close()
        #close the connection

def delete_account(accountKey):
    
    try:
        con = sqlite3.connect('storage.db')
        cur = con.cursor()
        #connect to the database

        cur.execute('''
            DELETE FROM accounts where accountKey = ?
        ''', (accountKey,))
        #delete the account with the entered key

        con.commit()
        #commit changes

        if cur.rowcount == 0:
            print('No account deleted')
        else:
            pass
        #checks if any rows where affected, if any where, nothing happens. If not it prints that no accounts where deleted

    except sqlite3.Error as e:
        print('Error:', e)
        #if any errors occur, print them

    finally:
        con.close()
        #close the connection


def calculate_weight(correct, incorrect):
    
    weight_scale = 100
    min_weight = 1
    max_weight = 100
    #the starting weight, the minimum and maximum weights (all constants)

    total_answers = correct + incorrect
    #times the question has been answered

    if total_answers == 0:

        return 50
    #if the question hasn't been asked, the weight is 50 by default

    return min(max_weight, max(min_weight, weight_scale * (incorrect / total_answers)))
    #calculates weight based upon the ratio of incorrect answers to the total answers, and ensures that it is is within the bounds of 1-100


def loop_length(string):
    loopLength = 0
    for char in string:
        loopLength += ord(char)
    return ((loopLength % 50) + 1) * 37

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
    hashValue = hash_encryption(string)
    loopLength = loop_length(string)
    for i in range(loopLength):
        hashValue = hash_encryption(str(hashValue))
    return base64_encode(hashValue)
