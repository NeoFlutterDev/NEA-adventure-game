import sqlite3

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

createDatabase()
