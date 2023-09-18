'''
import nltk
nltk.download()
'''
import string
import random
from bs4 import BeautifulSoup
import requests

word_file = "5_letter_words.txt"

def web_scrape_wordlist():

    r = requests.get('https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt')
    soup = BeautifulSoup(r.content, 'html.parser')
    words = list(str(soup).split('\n'))
    for i in range(len(words)):
        words[i] = words[i].strip('\r')
    return words

def generate_wordlist():

    try:
        with open (word_file, 'r') as file:
            wordlist = file.readlines()
            for word in range(len(wordlist)):
                wordlist[word] = wordlist[word].strip().lower()
            file.close()

    except:

        from nltk.corpus import words
        all_words = words.words()
        '''
        all_words = web_scrape_wordlist()'''
        wordlist = [word for word in all_words if len(word) == 5]
        with open('5_letter_words.txt', 'w') as file:
            for word in wordlist:
                file.write(word.lower() + "\n")


    if len(wordlist) != 0:
        print("Five letter word list generated")
    else:
        print("Something went wrong!")
    return wordlist

def first_guess(wordlist):
    repeat_letters = True
    while repeat_letters:
        guess = random.choice(wordlist)
        #print(f"Generating first guess - {guess}")
        if len(set(guess)) != len(guess):
            #print("Duplicate letters")
            continue
        else:
            #print("No duplicate letters")
            repeat_letters = False

    return guess

def guess_validity(guess, misplaced_letters, answer_letters):
    guess_check = list(misplaced_letters)
    #print(f"Checking new guess - {guess}", end="")
    for letter in misplaced_letters:
        if letter not in guess:
            #print(f"guess does not contain {letter}")
            return True
        else:
            guess_check.remove(letter)

    if len(guess_check) != 0:
        #print("not all misplaced letters in guess")
        return True

    for i in range(len(guess)):
        # print(f"Checking letter {i} - {guess[i]}")

        if guess[i] not in answer_letters[i]:
            #print(f"Guess invalid, {guess[i]} not in {answer_letters[i]}")
            #print("guess doesn't have known letters in place")
            return True

        else:
            if i == len(guess) - 1:
                #print("Guess valid")
                return False

            else:
                # print("Letter valid")
                continue

def make_guess(wordlist, answer_letters, misplaced_letters):

    bad_guess = True
    guess = ""

    while bad_guess:
        try:
            guess = random.choice(wordlist)
        except IndexError:
            print("Could not guess word")
        #print(f"\nNew guess = {guess}")
        bad_guess = guess_validity(guess, misplaced_letters, answer_letters)
        if bad_guess == True:
            wordlist.remove(guess)


    print(f"\nGuess = {guess}")
    #print(f"Word list length = {len(wordlist)}")
    return guess, wordlist

def list_alphabet():
  return list(string.ascii_lowercase)

def find_secret_word(wordlist):
    words_in_file = wordlist.copy()
    guesses = 0
    answer_letters = {
        0: list_alphabet(),
        1: list_alphabet(),
        2: list_alphabet(),
        3: list_alphabet(),
        4: list_alphabet()
        }
    misplaced_letters = []
    guess = first_guess(wordlist)
    print(f"First Guess = {guess}")
    #guess = input("Input guess\n")

    while guesses >= 0 :
        guess_accepted = input("Guess accepted? (y/n)\n")
        if guess_accepted == 'n':
            words_in_file.remove(guess)
            print(f"Removing {guess} from word file")
            with open(word_file, 'w') as file:
                for word in words_in_file:
                    file.write(word + "\n")
                file.close()

        else:

            guesses += 1
            letter_check = (input("What was the response? (Black = 0, Amber = 1, Green = 2)\n"))
            while len(letter_check) != 5:
                letter_check = (input("Invalid response, try again. (Black = 0, Amber = 1, Green = 2)\n"))
            if letter_check == '22222':
                break
            for i in range(len(letter_check)):
                if int(letter_check[i]) == 0:
                    if len(set(guess)) == len(guess):
                        for j in range(len(guess)):
                            try:
                                answer_letters[j].remove(guess[i])
                            except:
                                continue
                    else:
                        answer_letters[i].remove(guess[i])

                elif int(letter_check[i]) == 1:
                    misplaced_letters.append(guess[i])
                    answer_letters[i].remove(guess[i])
                elif int(letter_check[i]) == 2:
                    answer_letters[i] = guess[i]

        wordlist.remove(guess)
        guess, wordlist = make_guess(wordlist, answer_letters, misplaced_letters)
        #guess = input("Input guess\n")

    print(f"Number of guesses = {guesses}")
    #print(len(wordlist))
    return guess



if __name__ == '__main__':

    wordlist = generate_wordlist()

    #wordlist = generate_wordlist()

    answer = find_secret_word(wordlist)
    print(f"Answer = {answer}")