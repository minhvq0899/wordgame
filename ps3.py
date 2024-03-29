# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Minh Vu
# Collaborators : Ishraq Chowdhury
# Time spent    : 10 hours                                          

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    '*': 0, 'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    # compute first sum 
    first_sum = 0
    lower_case_word = word.lower()
    for element in lower_case_word: 
        first_sum += SCRABBLE_LETTER_VALUES[element]
    
    # compute second sum
    second_sum = 1
    second_component = 7*len(word)-3*(n-len(word))
    if second_component > 1:
        second_sum = second_component
    
    return first_sum * second_sum

    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """


# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#

def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
   
    hand={}
    num_vowels = int(math.ceil(n / 3)) - 1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    hand.update({'*', 1})
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    new_hand = hand.copy()
    lower_case_word = word.lower()
    for element in lower_case_word:
        if element in new_hand:
            new_hand[element] -= 1
    
    return new_hand
    
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    # make all words lower case and make a copy of hand dictionary
    lower_case_word = word.lower()
    copy_hand = hand.copy()
    
    # check if the word is composed of all the letter in hand  
    for element in lower_case_word:
       copy_hand[element] = copy_hand.get(element,-1) - 1
  
    for k in copy_hand:
       if copy_hand[k] < 0:
           return False

    # check if our word has a wildcard character    
    if '*' in lower_case_word: 
        # if * is not in our word, just check if it's a legitimate word
        # replace * with each vowels and check if that word is legitimate 
        for i in range (0, 5):
            lower_case_word = word.replace("*", VOWELS[i])
            if lower_case_word in word_list:
                return True
    else:
        if lower_case_word in word_list:
            return True

    return False

   

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
    return sum(len(set(hand)))
    

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """

    # Keep track of the total score
    total_score = 0

    finished = False #game not finished state
    
    # As long as there are still letters left in the hand:
    while calculate_handlen > 0:
        # Display the hand
        print("Current hand: ", display_hand(hand))
        # Ask user for input
        word = str(input("Enter word or !! to indicate that you are finished: "))
        
        # If the input is two exclamation points:
        if word == "!!":
            # End the game (break out of the loop)
            finished = True
            print("Total score: " + str(total_score))
            
            break;
            
        # Otherwise (the input is not two exclamation points):

            # If the word is valid:
        elif is_valid_word(word, hand, word_list) == True:
            #hand = update_hand(hand, word)
            n = calculate_handlen(hand)
            total_score += get_word_score(word,n)
                # Tell the user how many points the word earned,
                # and the updated total score
            print(word, " earned ", get_word_score(word, n), "points. Total: ", total_score, "points.")

                
            # Otherwise (the word is not valid):
        else:
                # Reject invalid word (print a message)
            print("This is not a valid word. Please choose another word.")
            # update the user's hand by removing the letters of their inputted word 
        
        
        hand = update_hand(hand, word)
    
    if finished == True: 
        return total_score
        print("Ran out of letters. Total score", total_score, " points.")
    
    else: #no more letters left in hand
        print("Ran out of letters. Total score", total_score, " points.")
        return total_score
        
            

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function
    

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    
    copy_hand = hand.copy()
    
    # if the user provide a letter not in the hand
    if letter not in copy_hand.keys():
        return hand
    
    # delete the letter from the dictionary
    how_many = copy_hand[letter]
    del copy_hand[letter]
    
    # choose a new letter
    replacement1 = random.choice(VOWELS)
    replacement2 = random.choice(CONSONANTS)
    while (replacement1 == letter and replacement1 != "*") or replacement2 == letter:
        replacement1 = random.choice(VOWELS)
        replacement2 = random.choice(CONSONANTS)
    replacement = {replacement1, replacement2}
    chosen_one = random.choice(replacement)
    copy_hand.update({chosen_one, how_many})
    
    return copy_hand
       


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    
    total_score = 0
    
    number_of_hand = int(input("Enter total number of hands: "))
    for i in (number_of_hand):
        hand = deal_hand(HAND_SIZE)
        print("Current hand: " + hand)
        subtitute = input("Would you like to subtitute a letter? ")
        if subtitute == "yes":
            sub_char = input("Which letter would you like to replace? ")
            hand = subtitute(hand, sub_char)
        
        print("Current hand: " + hand)
        
        answer = input("Please enter a word or '!!' to indicate you are done: ")
        
        
        


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
