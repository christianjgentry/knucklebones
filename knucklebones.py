import random
from collections import Counter

##################
### Player Info ###
##################


class Player:
    def __init__(self, name):
        self.name = name
        self.gameState = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.score = 0


player1 = Player('Player 1')
player2 = Player('Player 2')

##################
### Game Logic ###
##################

# Global variable tracking which player's turn it is
turnCount = 0

# Global variable tracking which player's turn it is
gameOver = False

# Simulates the rolling of a six sided die


def rollDice():
    return random.randint(1, 6)

# Prints the current game state for players to visualize


def currentGameState():
    print(f'{player1.name}: {player1.score} Points')
    print(
        f'|{player1.gameState[0][0]}|{player1.gameState[1][0]}|{player1.gameState[2][0]}|')
    print(
        f'|{player1.gameState[0][1]}|{player1.gameState[1][1]}|{player1.gameState[2][1]}|')
    print(
        f'|{player1.gameState[0][2]}|{player1.gameState[1][2]}|{player1.gameState[2][2]}|')
    print('|A|B|C|')
    print(
        f'|{player2.gameState[0][0]}|{player2.gameState[1][0]}|{player2.gameState[2][0]}|')
    print(
        f'|{player2.gameState[0][1]}|{player2.gameState[1][1]}|{player2.gameState[2][1]}|')
    print(
        f'|{player2.gameState[0][2]}|{player2.gameState[1][2]}|{player2.gameState[2][2]}|')
    print(f'{player2.name}: {player2.score} Points\n')

# Determines the current player


def currentPlayer():
    global turnCount
    if turnCount % 2 == 0:
        currentPlayer = player1

    else:
        currentPlayer = player2

    return currentPlayer

# Determines the current opponent


def currentOpponent():
    global turnCount
    if turnCount % 2 == 0:
        currentOpponent = player2

    else:
        currentOpponent = player1

    return currentOpponent

# Takes user input to associate a letter with a numeric column


def whichColumn():
    while True:
        whichColumn = input('Which column do you want to put your die? \n')

        if whichColumn == "A":
            column = 0
            break

        elif whichColumn == "B":
            column = 1
            break

        elif whichColumn == "C":
            column = 2
            break

        else:
            print('Please enter a valid column. [A, B, C]\n')

    return column

# Allows the current player to select which column their die roll should be place in


def selectColumn(turnRoll):
    while True:
        currentGameState()
        column = whichColumn()
        if len(list(i for i in currentPlayer().gameState[column] if isinstance(i, int))) < 3:
            break
        else:
            print('This column is already full. Please select a valid column.\n')

    currentPlayer().gameState[column].insert(0, turnRoll)

    # Determine if opponent's board is affected by selection.
    while turnRoll in currentOpponent().gameState[column]:
        currentOpponent().gameState[column].remove(turnRoll)

# Determines if the current player can make a move


def isGameOver():
    # TODO: I need to refactor this. I want to see if each of the columns is filled to indicate that a player has no moves left.
    if len(list(i for i in currentPlayer().gameState[0] if isinstance(i, int))) >= 3 and len(list(i for i in currentPlayer().gameState[1] if isinstance(i, int))) >= 3 and len(list(i for i in currentPlayer().gameState[2] if isinstance(i, int))) >= 3:
        global gameOver
        gameOver = True

# The main logic surrounding each player's turn


def playerTurn():

    # Announce current player
    print(f'It is {currentPlayer().name}\'s turn!\n')

    # Roll the die
    global turnRoll
    turnRoll = rollDice()
    print(f'{currentPlayer().name} rolled a {turnRoll}\n')

    # Determine which column the die should go in
    selectColumn(turnRoll)

    # Show the updated game state
    currentGameState()
    print(chr(27) + "[2J")

    # Calculate the each player's score
    calculateScore()

    # Check if player is out of turns.
    isGameOver()

    # Increment the turn count
    global turnCount
    turnCount += 1


# Logic to calculate the score


class MyCounter(Counter):
    def __ini__(*arg, **kwargs):
        super().__init__(*arg, **kwargs)

    def sum_entries(self):
        total = 0
        for key, val in self.items():
            if isinstance(key, int):
                total += key**val
        return total

# Calculates each player's score


def calculateScore():
    playerColumnAScore = MyCounter(
        currentPlayer().gameState[0]).sum_entries()
    playerColumnBScore = MyCounter(
        currentPlayer().gameState[1]).sum_entries()
    playerColumnCScore = MyCounter(
        currentPlayer().gameState[2]).sum_entries()

    opponentColumnAScore = MyCounter(
        currentOpponent().gameState[0]).sum_entries()
    opponentColumnBScore = MyCounter(
        currentOpponent().gameState[1]).sum_entries()
    opponentColumnCScore = MyCounter(
        currentOpponent().gameState[2]).sum_entries()

    # Sum all column scores together
    currentPlayer().score = playerColumnAScore + \
        playerColumnBScore + playerColumnCScore
    currentOpponent().score = opponentColumnAScore + \
        opponentColumnBScore + opponentColumnCScore

# The game loop for Knucklebones


def Knucklebones():
    # Game loop while players have turns
    while gameOver == False:

        playerTurn()

    # Announce that game has ended
    print(f'Game over. {currentPlayer().name} can\'t make another move.\n')

    # Announce results
    currentGameState()

    if player1.score > player2.score:
        print(f'{player1.name} Wins!!!\n')
    elif player2.score > player1.score:
        print(f'{player2.name} Wins!!!\n')
    elif player1.score == player2.score:
        print('It\'s a tie!')

    # TODO: Ask if players would like to play again

##################
### Start Game ###
##################


Knucklebones()
