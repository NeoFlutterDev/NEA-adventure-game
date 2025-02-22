import sqlite3
import string
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
            encryptedPassword TEXT NOT NULL,
            characterName TEXT NOT NULL,
            exp INTEGER NOT NULL, 
            money INTEGER NOT NULL, 
            armour TEXT,
            armourModifier REAL NOT NULL,
            weapon TEXT,
            weaponModifier REAL NOT NULL,
            kills INTEGER NOT NULL,
            deaths INTEGER NOT NULL)
        ''')
        
        # Create the 'questions' table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS questions(
            questionKey INTEGER PRIMARY KEY AUTOINCREMENT, 
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            incorrect1 TEXT NOT NULL,
            incorrect2 TEXT NOT NULL,
            incorrect3 TEXT NOT NULL)
        ''')
        
        # Create the 'weights' table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS weights(
            weightKey INTEGER PRIMARY KEY AUTOINCREMENT,
            correct INTEGER NOT NULL, 
            incorrect INTEGER NOT NULL, 
            weight REAL NOT NULL, 
            questionKey INTEGER NOT NULL,
            accountKey INTEGER NOT NULL,
            FOREIGN KEY (questionKey) REFERENCES questions(questionKey) ON DELETE CASCADE,
            FOREIGN KEY (accountKey) REFERENCES accounts(accountKey) ON DELETE CASCADE
            )
        ''')

        con.commit()

        cur.execute('SELECT COUNT(*) FROM questions WHERE questionKey = 3')
        result = cur.fetchone()[0]

        if result == 0:  # If no such question exists, insert the data
            questions = [
                'Name of the flow of charged particles',
                'Unit of charge measurement',
                'Current flow if 10C flows past in 2 minutes',
                'Another name for potential difference',
                '25C of charge shifts 50J of energy between 2 points, what is the voltage',
                'Current flow of a 100 ohm resistor with 5V across it',
                'Type of conductor is a fixed resistor',
                'Total resistance of a 2 and 3 ohm resistor in series',
                'Power transmitted by 2A flowing across 5V',
                'Power transmitted by 2A flowing through a 6 ohm resistor'
            ]

            answers = [
                ['Current', 'Potential difference', 'Resistance', 'Power'],
                ['Coulomb', 'Volt', 'Amp', 'Watt'], 
                ['0.083 A', '5 A', '20 A', '1200 A'], 
                ['Voltage', 'Current', 'Resistance', 'Power'], 
                ['2 V', '0.5 V', '5 V', '1250 V'], 
                ['0.05 A', '20 A', '500 A', '105 A'], 
                ['Ohmic conductor', 'Non-ohmic conductor', 'Poor conductor', 'Good conductor'], 
                ['5 ohms', '6 ohms', '1 ohm', '1.2 ohms'],
                ['10 W', '2.5 W', '0.4 W', '20 W'], 
                ['24 W', '12 W', '3 W', '1.5 W']
            ]
            
            for i in range(10):
                query = '''INSERT INTO questions (question, answer, incorrect1, incorrect2, incorrect3)
                VALUES (?, ?, ?, ?, ?)'''

                data = (questions[i], answers[i][0], answers[i][1], answers[i][2], answers[i][3])
                cur.execute(query, data)
                con.commit()

    except sqlite3.Error as e:
        print('Error:', e)
        #if any errors occur, print them

    finally:
        con.close()
        #close the connection

def table_accounts_insertion(name, password, exp, money, armour, armourModifier, weapon, weaponModifier, kills, deaths):
    accountKey = None
    
    try:
        con = sqlite3.connect('storage.db')
        cur = con.cursor()
        #connect to the database

        # Enable foreign key constraints
        con.execute("PRAGMA foreign_keys = ON")

        query = '''
        INSERT INTO accounts (characterName, encryptedPassword, exp, money, armour, armourModifier, weapon, weaponModifier, kills, deaths)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        #define the query, with placeholders

        data = (name, password, exp, money, armour, armourModifier, weapon, weaponModifier, kills, deaths)
        #enter the data that is to be inserted
        cur.execute(query, data)
     #execute the parameterised query
    
        con.commit()
        #commit the query

        accountKey = cur.lastrowid

    except sqlite3.Error as e:
        print('Error:', e)
        #if any errors occur, print them

    finally:
        con.close()
        #close the connection

        return accountKey

def load_all_accounts():
    try:
        con = sqlite3.connect('storage.db')
        cur = con.cursor()
        #connect to the database

        # Enable foreign key constraints
        con.execute("PRAGMA foreign_keys = ON")

        query = '''
        SELECT *
        FROM accounts
        '''
        #define the query

        cur.execute(query)
        #execute the query

        accounts = cur.fetchall()

        con.commit()
        #commit the query

        return accounts
    
    except sqlite3.Error as e:
        print('Error:', e)
        #if any errors occur, print them

    finally:
        con.close()
        #close the connection

def load_account_attribute(attribute, accountKey):
    try:
        con = sqlite3.connect('storage.db')
        cur = con.cursor()
        #connect to the database

        # Enable foreign key constraints
        con.execute("PRAGMA foreign_keys = ON")

        query = f'''
        SELECT {attribute}
        FROM accounts
        WHERE accountKey = ?'''
        #define the query, with placeholders

        data = (accountKey,)
        #enter data that is to replace the old data
        cur.execute(query, data)
        #execute the parameterised query

        attributeValue = cur.fetchone()

        con.commit()
        #commit the query

        return attributeValue
    
    except sqlite3.Error as e:
        print('Error:', e)
        #if any errors occur, print them

    finally:
        con.close()
        #close the connection

def update_account_info(exp, money, weapon, weaponModifier, armour, armourModifier, accountKey):
    try:
        con = sqlite3.connect('storage.db')
        cur = con.cursor()
        #connect to the database

        # Enable foreign key constraints
        con.execute("PRAGMA foreign_keys = ON")

        query = '''
        UPDATE accounts
        SET exp = ?, money = ?, weapon = ?, weaponModifier = ?, armour = ?, armourModifier = ?
        WHERE accountKey = ?
        '''
        #define the query, with placeholders

        data = (exp, money, weapon, weaponModifier, armour, armourModifier, accountKey)
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

def update_characterName(characterName, accountKey):
    try:
        con = sqlite3.connect('storage.db')
        cur = con.cursor()
        #connect to the database

        # Enable foreign key constraints
        con.execute("PRAGMA foreign_keys = ON")

        query = '''
        UPDATE accounts
        SET characterName = ?
        WHERE accountKey = ?
        '''
        #define the query, with placeholders

        data = (characterName, accountKey)
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

        # Enable foreign key constraints
        con.execute("PRAGMA foreign_keys = ON")
        
        cur.execute('''
            DELETE FROM accounts WHERE accountKey = ?
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

def delete_all_accounts():
    try:
        con = sqlite3.connect('storage.db')
        cur = con.cursor()
        #connect to the database

        # Enable foreign key constraints
        con.execute("PRAGMA foreign_keys = ON")
        
        cur.execute('''
            DELETE FROM accounts
        ''')
        #delete the account with the entered key

        con.commit()
        #commit changes

        if cur.rowcount == 0:
            print('No account deleted')
        else:
            print(f'{cur.rowcount} accounts deleted')
        #checks if any rows where affected, if any where, nothing happens. If not it prints that no accounts where deleted

    except sqlite3.Error as e:
        print('Error:', e)
        #if any errors occur, print them

    finally:
        con.close()
        #close the connection

def load_accounts():
    try:
        con = sqlite3.connect('storage.db')
        cur = con.cursor()
        #connect to the database

        # Enable foreign key constraints
        con.execute("PRAGMA foreign_keys = ON")
        
        cur.execute('''
            SELECT accountKey, characterName, exp
            FROM accounts
        ''')

        result = cur.fetchall()

        con.commit()

        return result

    except sqlite3.Error as e:
        print('Error:', e)
        #if any errors occur, print them

    finally:
        con.close()
        #close the connection

def load_account(accountKey):
    try:
        con = sqlite3.connect('storage.db')
        cur = con.cursor()
        #connect to the database

        # Enable foreign key constraints
        con.execute("PRAGMA foreign_keys = ON")
        
        query = '''
            SELECT characterName, exp, armour, armourModifier, weapon, weaponModifier
            FROM accounts
            WHERE accountKey = ?
        '''
        data = accountKey

        cur.execute(query, data)

        result = cur.fetchall()

        con.commit()

        return result

    except sqlite3.Error as e:
        print('Error:', e)
        #if any errors occur, print them

    finally:
        con.close()
        #close the connection


def calculate_weight(correct, incorrect):
    
    weightScale = 100
    minWeight = 25
    maxWeight = 100
    #the starting weight, the minimum and maximum weights (all constants)

    totalAnswers = correct + incorrect
    #times the question has been answered

    if totalAnswers == 0:

        return 50
    #if the question hasn't been asked, the weight is 50 by default

    return min(maxWeight, max(minWeight, weightScale * (incorrect / totalAnswers)))
    #calculates weight based upon the ratio of incorrect answers to the total answers, and ensures that it is is within the bounds of 1-100

def update_question(answer, questionKey, accountKey):
    try:
        # Connect to the database
        con = sqlite3.connect('storage.db')
        cur = con.cursor()
        con.execute("PRAGMA foreign_keys = ON")

        # Determine which column to update based on the answer
        if answer == 'correct':
            answerColumn = 'correct'
            option = 0
        elif answer == 'incorrect':
            answerColumn = 'incorrect'
            option = 1
        else:
            raise ValueError("Answer must be either 'correct' or 'incorrect'.")

        # Fetch the current correct and incorrect counts
        cur.execute('''
            SELECT correct, incorrect
            FROM weights
            WHERE questionKey = ? and accountKey = ?
        ''', (questionKey, accountKey))
        result = cur.fetchone()

        if result is None:
            raise ValueError(f"No data found for weightKey {questionKey}")

        # Get current values for correct and incorrect answers
        correct, incorrect = result

        # Increment either the correct or incorrect count based on the answer
        if option == 0:
            correct += 1
        else:
            incorrect += 1

        # Recalculate the weight
        newWeight = calculate_weight(correct, incorrect)

        # Update the database with the new values
        cur.execute(f'''
            UPDATE weights
            SET {answerColumn} = ?, weight = ?
            WHERE questionKey = ? and accountKey = ?
        ''', (correct if option == 0 else incorrect, newWeight, questionKey, accountKey))

        # Commit the changes
        con.commit()

    except sqlite3.Error as e:
        print('Database Error:', e)

    except ValueError as ve:
        print('Value Error:', ve)

    finally:
        # Close the connection and cursor
        if cur:
            cur.close()
        if con:
            con.close()

def weight_insertion(accountKey):
    print(f"Inserting weights for accountKey: {accountKey}")
    try:
        # Connect to the database
        con = sqlite3.connect('storage.db')
        cur = con.cursor()
        con.execute("PRAGMA foreign_keys = ON")

        questionIDs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for questionKey in questionIDs:
            query = '''
            INSERT INTO weights (correct, incorrect, weight, questionKey, accountKey)
            VALUES (?, ?, ?, ?, ?)
            '''

            cur.execute(query, (0, 0, 50, questionKey, int(accountKey)))
            con.commit()

    except sqlite3.Error as e:
        print('Database Error:', e)

    except ValueError as ve:
        print('Value Error:', ve)

    finally:
        # Close the connection and cursor
        if cur:
            cur.close()
        if con:
            con.close()

def pull_question(questionKey):
    try:
        # Connect to the database
        con = sqlite3.connect('storage.db')
        cur = con.cursor()
        con.execute("PRAGMA foreign_keys = ON")

        query = '''
        SELECT question, answer, incorrect1, incorrect2, incorrect3
        FROM questions
        WHERE questionKey = ?'''

        cur.execute(query, (questionKey, ))

        return cur.fetchone()
    
    except sqlite3.Error as e:
        print('Database Error:', e)

    except ValueError as ve:
        print('Value Error:', ve)
    
    finally:
        # Close the connection and cursor
        if cur:
            cur.close()
        if con:
            con.close()


def get_question(accountKey):
    try:
        # Connect to the database
        con = sqlite3.connect('storage.db')
        cur = con.cursor()
        con.execute("PRAGMA foreign_keys = ON")

        query = '''
        SELECT weight, questionKey
        FROM weights
        WHERE accountKey = ?'''

        cur.execute(query, (accountKey,))

        questions = cur.fetchall()
        
        sumWeights = 0
        for question in questions:
            sumWeights += question[0]
        
        chosenQuestion = random.uniform(1, sumWeights)

        for i in range(len(questions)):
            chosenQuestion -= questions[i][0]
            if chosenQuestion <= 0:
                return pull_question(questions[i][1]), questions[i][1]
            
    except sqlite3.Error as e:
        print('Database Error:', e)

    except ValueError as ve:
        print('Value Error:', ve)
    
    finally:
        # Close the connection and cursor
        if cur:
            cur.close()
        if con:
            con.close()

def loop_length(text):
    loopLength = 0
    for char in text:
        loopLength += ord(char)
    return ((loopLength % 50) + 1) * 37
    '''converts each character in the string to their ascii code
    sums the ascii codes, then mods them by 50, adds 1, then multiplies by 37'''

def hash_encryption(text):
    hashValue = 0
    primes = [6221, 7433, 2203, 4817, 4241, 6449, 4549, 5717, 2861, 4507, 7607, 7549, 5209]
    for i in range(len(text)):
        hashValue = (hashValue << 3) ^ (hashValue >> 5)
        prime = primes[i % len(primes)]
        hashValue += ord(text[i]) * prime
        hashValue = hashValue % (2**256 - 1)
    return hashValue
    '''loops this code by the length of the string
    it XORs the string which is shifted by 3, by the string shifted by 5
    it then adds on the ascii code of the selected character and multiplies it by a prime number
    then it mods the string to keep it within a certain range'''

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
    '''creates a base64 character set, and divides the hashValue by 64 every time, using the remainder as the next base64 character.
    it then reverses the hash and cuts off digits to ensure a 16 digit hash.
    in the case of a hash being less than 16 digits (no cases found yet) the remainging slots are filled with 0s'''

def hashing_algorithm(text):
    hashValue = hash_encryption(text)
    loopLength = loop_length(text)
    for i in range(loopLength):
        hashValue = hash_encryption(str(hashValue))
    return base64_encode(hashValue)
    '''hashes the intital text, then gets the loop length based on the new hashValue.
    then it loops an amount of times based upon loop length, hashing the hashValue that many times.
    then it encodes the hashValue and returns it'''


#print(load_account_attribute('characterName', 41)[0])
#print(load_account_attribute('encryptedPassword', 41)[0])
#weight_insertion(4)
createDatabase()