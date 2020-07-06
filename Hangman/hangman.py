from random import choice
from sys import exit

print("H A N G M A N")

words = ['python', 'java', 'kotlin', 'javascript']
word = choice(words)
print(word)
wordLen = len(word)
while True:
    if input('Type "play" to play the game, "exit" to quit: ') == 'exit':
        break
    guessDct = {}
    foundWords = set(word)

    tries = 8
    while tries > 0:
        if len(foundWords) == 0:
            print("You guessed the word!\n"
                  "You survived!")
            exit()

        guessStr = ''
        for i in word:
            guessStr += i if i not in foundWords else '-'

        print('\n' + guessStr)
        guess = input('Input a letter: ')

        if len(guess) != 1:
            print("You should input a single letter")
            continue

        guessDct[guess] = guessDct.get(guess, 0) + 1

        if not guess.islower():
            print("It is not an ASCII lowercase letter")
        elif guessDct[guess] > 1:
            print("You already typed this letter")
        elif guess in foundWords:
            foundWords.remove(guess)
        else:
            tries -= 1
            print('No such letter in the word')

    print("You are hanged!\n")

