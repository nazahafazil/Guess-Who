# GUESS WHO: EXECUTIVE FILE

import random
import os

#================================== CONSTANTS =================================#

CHARACTER_OFFICIAL_FILE = 'official_guess_who_characters.txt'
CHARACTER_USER_FILE = 'guess_who_characters.txt'

QUESTIONS = 20
POINTS_PER_QUESTION = 1000
POINTS_PER_TRAIT = 50
POINTS_FOR_CORRECT_GUESS = 1500

YES = 'Y'
NO = 'N'
READY = 'READY'
QUIT = 'Q'
GUESS = 'G'
QUESTION = 'A'
RECORD = 'R'
CONTINUE = 'C'

GAME_QUIT = -1
CHAR = '='

#================================ FILE READING ================================#

def read_file(filename: str) -> dict[str, list[str]]:
    
    file = open(filename)
    file.readline()

    characters_to_traits = {}
    line = file.readline()

    while line != '':
        line = line.strip()
        if line.isupper():
            character = line
            characters_to_traits[character] = []
        elif line.islower():
            characters_to_traits[character].append(line)
        line = file.readline()
    
    file.close()
    return characters_to_traits



def create_user_file(filename: str) -> None:

    file = open(filename)
    file_copy = open(CHARACTER_USER_FILE, 'w')

    copy = file.read()
    file_copy.write(copy)

    file.close()
    file_copy.close()



#================================== PRE-GAME ==================================#

def show_rules() -> bool:

    s = f'''RULES:
 > Characters will be chosen from {CHARACTER_USER_FILE}. Refer to this file\
 as you play!
 > During each round, you can choose from four options:
   > Ask a question about the character.
   > Guess the character.
   > Show a record of all past guesses (showing correct ones).
   > Quit the game.
 > You must guess the character within {QUESTIONS} rounds!
 > You only have one chance to guess a character correctly!
 > Points will be shown at the end of the game.
     '''
    print(s)



def computer_choose_character(character_dict: dict[str, list[str]])\
    -> dict[str, list[str]]:

    characters = list(character_dict.keys())
    return random.choice(characters)



#================================== GAMEPLAY ==================================#

def play_game(character_profile: list[str]) -> int:

    count = 1
    endloop = False
    traits_guessed = []
    record = {}

    while count < QUESTIONS and not endloop:
        print(CHAR * 20, f'Round {count}', CHAR * 20)
        move = select_move()

        if move.upper() == QUESTION:

            trait_guess = guess_trait(traits_guessed).strip()
            add_to_record(trait_guess, count, record)

            trait_guessed = check_trait(trait_guess.strip(),
                                        character_profile,
                                        traits_guessed)
            if trait_guessed:
                print(f'Yes, this character has {a_needed(trait_guess)}' +
                      f'{trait_guess}!')
                record[count] += ' (✓)'
                if character_profile == []:
                    print('You have guessed all my character\'s traits!')
                    print_record(record)
                    endloop = True
                else:
                    continue_game()
            else:
                print('No, this character does not have ' +
                      f'{a_needed(trait_guess)}{trait_guess}!')
                continue_game()

            count += 1

        elif move.upper() == GUESS:
            endloop = True

        elif move.upper() == RECORD:
            print_record(record)
            continue_game()

        else:
            print('You ended the game! You chicken...')
            return GAME_QUIT

    if count == QUESTIONS:
        print('\n' + CHAR * 20, f'Round {count}:', CHAR * 20 +
              '\nThis is the final round - you must guess my character!')

    return count



def select_move() -> str:

    print('Select your move!')
    move = input(f'[{QUESTION}] -> Ask a question!\n' +
                 f'[{GUESS}] -> Guess a character!\n' +
                 f'[{RECORD}] -> Show your record of guesses!\n' +
                 f'[{QUIT}] -> Quit the game.\n')

    while move.upper() not in (QUESTION, GUESS, QUIT, RECORD):
        move = input('Please select a move!\n')

    return move



def guess_trait(traits_guessed: list[str]) -> str:

    trait_guess = input('Question - Does this character have: ')

    while not trait_guess.replace(' ', '').isalpha() :
        trait_guess = input('Please enter a valid guess.\n' +
                            'Does this character have: ')

    while trait_guess in traits_guessed:
        trait_guess = input('You have already guessed that! ' +
                            'Guess something else.\n' +
                            'Does this character have: ')        

    return trait_guess



def add_to_record(trait: str, count: int, record: dict[int, str]) -> None:

    record[count] = trait



def check_trait(trait: str, 
                traits: list[str], 
                traits_guessed: list[str]) -> bool:

    if trait in traits:
        traits.remove(trait)
        traits_guessed.append(trait)
        return True
    return False



def continue_game():
    cont = input(f'Type {CONTINUE} to continue: ')
    
    while cont.upper() != CONTINUE :
        cont = input(f'Please enter {CONTINUE} to proceed: ')



def print_record(record: dict[int, str]) -> None:

    print(CHAR * 10, 'GUESSES RECORD', CHAR * 10)

    for key in record:
        print (' > Round ' + str(key) + ': ' + record[key])

    print(CHAR * 10, 'END OF RECORD', CHAR * 10)



def a_needed(trait_guess: str) -> str:
    
    if trait_guess.endswith('shirt') or\
       (trait_guess in ('scarf', 'hat', 'necklace', 'bracelet', 
                        'watch', 'scar')):
        return 'a '

    return ''



#================================= POST-GAME ==================================#

def guess_character(character: str,
                    traits: list[str],
                    questions_count: int) -> int:

    points = 0
    
    character_guess = input('Guess my character: ')
    while not character_guess.strip().isalpha():
        character_guess = input('Please guess a valid character: ')

    if character_guess.strip().upper() == character:
        points = ((POINTS_PER_QUESTION * (QUESTIONS - questions_count)) +
                  (POINTS_PER_TRAIT * len(traits)) +
                  POINTS_FOR_CORRECT_GUESS)
        print(f'You guessed correctly! My character is {character}.')
    else:
        print(f'You guessed incorrectly! My character is {character}. ' +
              'Try again next time!')

    return points



#================================ THE PROGRAM =================================#

if __name__ == '__main__':

    welcome = 'Welcome to GUESS WHO! (Adapted as a Python print game)'
    print(CHAR * len(welcome), welcome, CHAR * len(welcome), sep='\n')

    create_user_file(CHARACTER_OFFICIAL_FILE)
    
    show_rules()
    
    character_dict = read_file(CHARACTER_OFFICIAL_FILE)
    
    character = computer_choose_character(character_dict)
    character_profile = character_dict[character]

    print('A character has been chosen! Are you ready to play?')
    
    ready = input(f'Type {READY} to begin! Type {QUIT} to close the game.\n')

    while ready.upper() not in (READY, QUIT):
        ready = input(f'Please type {READY} or {QUIT}: ')
    
    if ready.upper() == READY:
        count_questions = play_game(character_profile)
        if count_questions != GAME_QUIT:
            points = guess_character(character,
                                     character_profile,
                                     count_questions)
            print(f' > You scored {points} points in this game.\n')
    else:
        print('You ended the game before it began. You chicken...\n')

    print(f'Note: {CHARACTER_USER_FILE} has been deleted.\n')
    os.remove(CHARACTER_USER_FILE)
    print('Thank you for playing!\n' + CHAR * 100)
