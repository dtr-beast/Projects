from random import randint
from sys import exit
import sqlite3


def main():
    welcomeLine = ('1. Create an account\n'
                   '2. Log into account\n'
                   '0. Exit\n')

    loginLine = ('1. Balance\n'
                 '2. Add income\n'
                 '3. Do transfer\n'
                 '4. Close account\n'
                 '5. Log out\n'
                 '0. Exit\n')

    while True:
        prompt = input(welcomeLine)

        if prompt == '1':

            newCard = Card()
            newCard.created()
            # print("Executing Add to DB")
            newCard.addToDB()
            db.commit()
        elif prompt == '2':
            # login() takes the card number and PIN and finds whether it is a valid account in the database
            # Returns the result of the database search -> Account Row OR None
            result = login()
            if result is not None:
                print("\nYou have successfully logged in!\n")

                while True:
                    result = login(details=True, card=result[1], pin=result[2])
                    answer = input(loginLine)

                    if answer == '1':
                        # Check Balance
                        print(f"\nBalance: {result[-1]}\n")

                    elif answer == '2':
                        # Add Income
                        amount = int(input('Enter income:\n'))
                        updateBalance(result[1], amount)
                        print("Income was added!\n")
                        db.commit()

                    elif answer == '3':
                        # Transfer Money
                        print("Transfer")
                        card = input('Enter card number:\n')
                        if card == result[1]:
                            print("You can't transfer money to the same account!")
                        elif isNotLuhn(card):
                            print("Probably you made mistake in the card number.\n"
                                  "Please try again!")
                        else:
                            transferCard = login(details=True, card=card)
                            if transferCard:
                                amount = int(input('Enter how much money you want to transfer:\n'))
                                if amount > result[-1]:
                                    print("Not enough money!")
                                else:
                                    updateBalance(result[1], -amount)
                                    updateBalance(transferCard[1], amount)
                                    db.commit()
                                    print("Success!\n")

                            else:
                                print("Such a card does not exist.")

                    elif answer == '4':
                        # Close Account
                        scursor.execute(f"DELETE FROM card "
                                        f"WHERE number = '{result[1]}'; ")
                        print("The account has been closed!")
                        db.commit()
                        break

                    elif answer == '5':
                        # Log Out
                        db.commit()
                        break

                    elif answer == '0':
                        exit()
            else:
                print("\nWrong card number or PIN!\n")

        elif prompt == '0':
            exit()


def isNotLuhn(card):
    cardList = [int(i) for i in card]
    cardList = [value * 2 if index % 2 == 0 else value for (index, value) in enumerate(cardList)]
    cardList = list(map(lambda x: x - 9 if x > 9 else x, cardList))

    return sum(cardList) % 10 != 0


def login(details=False, card=None, pin=None) -> list:
    """ Asks for essential details, and then searches it in the database """
    if not details:
        card = input(f"\nEnter your card number:\n")
        pin = input("Enter you PIN:\n")
        # print(card, pin)
        tick = '\''
    scursor.execute(f"SELECT * "
                    f"FROM card "
                    f"WHERE number =  '{card}' {f'AND pin = {tick + str(pin) + tick}' if details == False else ''}; ")
    # data =
    # print(data)
    return scursor.fetchone()


def updateBalance(acc: str, amount: int) -> None:
    print(acc)
    """ Update the balance of a given account """
    scursor.execute(f'UPDATE card '
                    f'SET balance = balance + {amount} '
                    f"WHERE number = '{acc}'; ")
    db.commit()


class Card:

    def __init__(self):
        # ---------------Bank Identification Number------------------------------
        # Assumes the last number as 0
        checksum = 0
        # Makes a list of random numbers
        tempNumList = [randint(0, 9) for _ in range(9)]
        numList = tempNumList[:]
        # Multiplies by 2
        tempNumList = [numList[i] * 2 if i % 2 == 0 else numList[i] for i in range(9)]
        # Decrements any number more than 9
        tempNumList = list(map(lambda x: x - 9 if x > 9 else x, tempNumList))

        # If the number is not validated by Luhn Algorithm, the checksum is incremented until
        # it gets validated
        if (sum(tempNumList) + 8) % 10 != 0:
            for checksum in range(1, 10):
                if (sum(tempNumList) + 8 + checksum) % 10 == 0:
                    break

        numList = list(map(str, numList))

        self.accNum = '400000' + ''.join(numList) + str(checksum)
        # ------------------------------------------------------------------------

        # Creates a random number and fills it with '0's to make it a 4 digit number
        temppin = str(randint(1000, 9999)).zfill(4)
        # temppin = ((4 - len(str(temppin))) * '0') + str(temppin)
        self.pin = temppin

        self.balance = 0

    def created(self):
        # Method to prompt user successful card creation
        print("\nYour card has been created")
        print("Your card number:")
        print(self.accNum)
        print("You card PIN:")
        print(f"{self.pin}\n")

    def addToDB(self):
        # print('Adding')
        scursor.execute(f'INSERT INTO card (number, pin)'
                        f'VALUES ({self.accNum}, {self.pin}); ')
        db.commit()
        # print('Committed')
        # scursor.execute(f'SELECT * FROM card '
        #                 f'WHERE number = "{self.accNum}" AND pin = "{self.pin}";')
        # print(scursor.fetchone())


if __name__ == '__main__':
    try:
        db = sqlite3.connect(r'BankingSystem\card.s3db')
        scursor = db.cursor()
        scursor.executescript("DROP TABLE IF EXISTS card; "
                              "CREATE TABLE card"
                              "(id         INTEGER PRIMARY KEY,"
                              "number      TEXT,"
                              "pin         TEXT,"
                              "balance     INTEGER DEFAULT 0);")

        main()
    except sqlite3.OperationalError:
        print('SQL ERROR')
    finally:
        # scursor.execute("SELECT * FROM card;")
        # print(scursor.fetchall())
        print("\nBye!")
        db.commit()
        db.close()
