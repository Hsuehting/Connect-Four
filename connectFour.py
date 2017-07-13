import pygame
import random
import sys
from pygame.locals import *

def checkWin(board):
    winCount = 0

    # Check for wins horizontally
    for i in range(6):
        for j in range(4):
            if (board[i * 7 + j] == board[i * 7 + j + 1] and
                board[i * 7 + j + 1] == board[i * 7 + j + 2] and
                board[i * 7 + j + 2] == board[i * 7 + j + 3] and
                board[i * 7 + j] != ' '):
                return True

    # Check for wins vertically
    for i in range(7):
        for j in range(3):
            if (board[i + (7 * j)] == board[i + (7 * j) + 7] and
                board[i + (7 * j) + 7] == board[i + (7 * j) + 14] and
                board[i + (7 * j) + 14] == board[i + (7 * j) + 21] and
                board[i + (7 * j)] != ' '):
                return True


    # Have worked down the conditionals a fair bit, still inefficient tho
    # Check for wins diagonally \ way
    for i in range(3):
        for j in range(2):
            if (board[8 * i + j] == board[8 * i + 8 + j] and
                board[8 * i + 8 + j] == board[8 * i + 16 + j] and
                board[8 * i + 16 + j] == board[8 * i + 24 + j] and
                board[8 * i + j] != ' '):
                return True

    for i in range(2):
        for j in range(2):
            if (board[2 + (5 * j) + (i * 8)] == board[2 + (5 * j) + (i * 8) + 8] and
                board[2 + (5 * j) + (i * 8) + 8] == board[2 + (5 * j) + (i * 8) + 16] and
                board[2 + (5 * j) + (i * 8) + 16] == board[2 + (5 * j) + (i * 8) + 24] and
                board[2 + (5 * j) + (i * 8)] != ' '):
                return True

    for i in range(2):
        if (board[3 + (i * 11)] == board[11 + (i * 11)] and
            board[11 + (i * 11)] == board[19 + (i * 11)] and
            board[19 + (i * 11)] == board[27 + (i * 11)] and
            board[3 + (i * 11)] != ' '):
            return True

    # Check for wins diagonally / way

    for i in range(3):
        for j in range(2):
            if (board[6 * i + 6 - j] == board[6 * i + 12 - j] and
                board[6 * i + 12 - j] == board[6 * i + 18 - j] and
                board[6 * i + 18 - j] == board[6 * i + 24 - j] and
                board[6 * i + 6 - j] != ' '):
                return True

    for i in range(2):
        for j in range(2):
            if (board[6 * i + 4 + (j * 9)] == board[6 * i + 10 + (j * 9)] and
                board[6 * i + 10 + (j * 9)] == board[6 * i + 16 + (j * 9)] and
                board[6 * i + 16 + (j * 9)] == board[6 * i + 22 + (j * 9)] and
                board[6 * i + 4 + (j * 9)] != ' '):
                return True

    for i in range(2):
        if (board[3 + (17 * i)] == board[9 + (17 * i)] and
            board[9 + (17 * i)] == board[15 + (17 * i)] and
            board[15 + (17 * i)] == board[21 + (17 * i)] and
            board[3 + (17 * i)] != ' '):
            return True

    return False

def computerTurn(board):
    playerCanWin = False

    # FOREWARNING: A LOT OF SPAGHETTI
    # This is one of my very early projects
    # Just follows a set of rules to determine which move to make next
    # ======================================================
    #    AI RULES
    # ======================================================
    # 1. Win.
    # 2. Stop opponent's win
    # 3. Fork (Guaranteed Win)
    # 4. Stop Opponent's Fork
    # 5. Fork next turn
    # 6. Stop Opponent's Fork next turn
    # 7. More Fork Rules
    # 8. Play three in a row
    # 9. Stop player from getting three in a row
    # 10. Take Middle Column
    # 11. Take random spot that doesn't cause player to win
    # 12. Take random spot
    # ======================================================

    # If there's a move that will win the match, take it
    for i in range(7):
        tempBoard = list(board)
        tempBoard = placePiece(tempBoard, i, 'Y')
        if checkWin(tempBoard) == True:
            if board[i] == ' ':
                board = placePiece(board, i, 'Y')
                return board

    # If there's a move that will win the match for the opponent, take it
    for i in range(7):
        tempBoard = list(board)
        tempBoard = placePiece(tempBoard, i, 'R')
        if checkWin(tempBoard) == True:
            if board[i] == ' ':
                board = placePiece(board, i, 'Y')
                return board

    # If a move will create a fork (for computer) with multiple wins next
    # turn, take it
    for i in range(7):
        tempBoard = list(board)
        tempBoard = placePiece(tempBoard, i, 'Y')
        winCount = 0
        for j in range(7):
            tempBoard2 = list(tempBoard)
            tempBoard2 = placePiece(tempBoard2, j, 'Y')
            if checkWin(tempBoard2) == True:
                winCount += 1

            if winCount > 1:
                playerCanWin = False
                for k in range(7):
                    tempBoard3 = list(board)
                    tempBoard3 = placePiece(tempBoard3, i, 'Y')
                    tempBoard3 = placePiece(tempBoard3, k, 'R')
                    if checkWin(tempBoard3) == True:
                        playerCanWin = True

                if board[i] == ' ' and playerCanWin == False:
                    board = placePiece(board, i, 'Y')
                    return board

    # If a move will create a fork (for the player) with multiple wins
    # next turn, take it
    for i in range(7):
        tempBoard = list(board)
        tempBoard = placePiece(tempBoard, i, 'R')
        winCount = 0
        for j in range(7):
            tempBoard2 = list(tempBoard)
            tempBoard2 = placePiece(tempBoard2, j, 'R')
            if checkWin(tempBoard2) == True:
                winCount += 1

            if winCount > 1:
                playerCanWin = False
                for k in range(7):
                    tempBoard3 = list(board)
                    tempBoard3 = placePiece(tempBoard3, i, 'Y')
                    tempBoard3 = placePiece(tempBoard3, k, 'R')
                    if checkWin(tempBoard3) == True:
                        playerCanWin = True

                if board[i] == ' ' and playerCanWin == False:
                    board = placePiece(board, i, 'Y')
                    return board

    # If a move will create a fork with a win in two turns,
    # take it
    for i in range(7):
        tempBoard = list(board)
        tempBoard = placePiece(tempBoard, i, 'Y')
        for j in range(7):
            tempBoard2 = list(tempBoard)
            tempBoard2 = placePiece(tempBoard2, j, 'Y')
            winCount = 0
            if checkWin(tempBoard2) == False:
                for k in range(7):
                    tempBoard3 = list(tempBoard2)
                    tempBoard3 = placePiece(tempBoard3, k, 'Y')
                    if checkWin(tempBoard3) == True:
                        winCount += 1

                    if winCount > 1:
                        playerCanWin = False
                        for l in range(7):
                            tempBoard4 = list(board)
                            tempBoard4 = placePiece(tempBoard4, i, 'Y')
                            tempBoard4 = placePiece(tempBoard4, l, 'R')
                            if checkWin(tempBoard4) == True:
                                playerCanWin = True

                        if board[i] == ' ' and playerCanWin == False:
                            board = placePiece(board, i, 'Y')
                            return board
    # Fork in three turns
    for i in range(7):
        tempBoard = list(board)
        tempBoard = placePiece(tempBoard, i, 'Y')
        for j in range(7):
            tempBoard2 = list(board)
            tempBoard2 = placePiece(tempBoard2, j, 'Y')
            for k in range(7):
                tempBoard3 = list(tempBoard2)
                tempBoard3 = placePiece(tempBoard3, k, 'Y')
                winCount = 0
                if checkWin(tempBoard3) == False:
                    for l in range(7):
                        tempBoard4 = list(tempBoard3)
                        tempBoard4 = placePiece(tempBoard4, l, 'Y')
                        if checkWin(tempBoard4) == True:
                            winCount += 1

                        if winCount > 1:
                            playerCanWin = False
                            for m in range(7):
                                tempBoard5 = list(board)
                                tempBoard5 = placePiece(tempBoard5, i, 'Y')
                                tempBoard5 = placePiece(tempBoard5, l, 'R')
                                if checkWin(tempBoard5) == True:
                                    playerCanWin = True

                            if board[i] == ' ' and playerCanWin == False:
                                board = placePiece(board, i, 'Y')
                                return board

    # If a move will create opportunity for a win next turn, take it
    # (Play three in a row)
    for i in range(7):
        tempBoard = list(board)
        tempBoard = placePiece(tempBoard, i, 'Y')
        for j in range(7):
            tempBoard2 = list(tempBoard)
            tempBoard2 = placePiece(tempBoard2, j, 'Y')
            if checkWin(tempBoard2) == True:
                playerCanWin = False
                for k in range(7):
                    tempBoard3 = list(board)
                    tempBoard3 = placePiece(tempBoard3, i, 'Y')
                    tempBoard3 = placePiece(tempBoard3, k, 'R')
                    if checkWin(tempBoard3) == True:
                        playerCanWin = True

                if board[i] == ' ' and playerCanWin == False:
                    board = placePiece(board, i, 'Y')
                    return board

    # If a move will create opportunity for a win next turn (for player), take it
    # (Stop three in a row)
    for i in range(7):
        tempBoard = list(board)
        tempBoard = placePiece(tempBoard, i, 'R')
        for j in range(7):
            tempBoard2 = list(tempBoard)
            tempBoard2 = placePiece(tempBoard2, j, 'R')
            if checkWin(tempBoard2) == True:
                playerCanWin = False
                for k in range(7):
                    tempBoard3 = list(board)
                    tempBoard3 = placePiece(tempBoard3, i, 'Y')
                    tempBoard3 = placePiece(tempBoard3, k, 'R')
                    if checkWin(tempBoard3) == True:
                        playerCanWin = True

                if board[i] == ' ' and playerCanWin == False:
                    board = placePiece(board, i, 'Y')
                    return board

    # If middle isn't taken, take it
    if board[38] == ' ':
        board = placePiece(board, 3, 'Y')
        return board

    # Choose a random spot that won't lead to a win for the player next turn,
    # chooses it randomly to avoid the computer playing to the first open
    # column every time
    columnsChecked = 0
    while True:
        randomChoice = random.randint(0, 6)
        tempBoard = list(board)
        tempBoard = placePiece(tempBoard, randomChoice, 'Y')
        playerCanWin = False
        for j in range(7):
            tempBoard2 = list(tempBoard)
            tempBoard2 = placePiece(tempBoard2, j, 'R')
            if checkWin(tempBoard2) == True:
                playerCanWin = True

        if board[randomChoice] == ' ' and playerCanWin == False:
            board = placePiece(board, randomChoice, 'Y')
            return board

        columnsChecked += 1

        # If impossible to avoid a win for the player, play anywhere valid
        if columnsChecked > 20:
            while True:
                randomChoice = random.randint(0, 6)
                if board[randomChoice] == ' ':
                    board = placePiece(board, randomChoice, 'Y')
                    return board

def placePiece(board, column, piece):
    if board[column] == ' ':
        lowestOpenRow = column

        for i in range(6):
            if board[column + (7 * i)] == ' ':
                lowestOpenRow = i

        board[lowestOpenRow * 7 + column] = piece
        return board

    else:
        return board

def printBoard(board):
    for i in range(len(board)):
        if board[i] == 'R':
            screen.blit(redPiece, ((i % 7) * COLUMNWIDTH, (i // 7) * ROWHEIGHT))

        elif board[i] == 'Y':
            screen.blit(yellowPiece, ((i % 7) * COLUMNWIDTH, (i // 7) * ROWHEIGHT))

def getOpenSpaces(board):
    openSpaces = 0
    for space in board:
        if space == ' ':
            openSpaces += 1

    return openSpaces

# Initalise sizes of windows and rows / columns
WINDOWWIDTH = 640
WINDOWHEIGHT = 600
COLUMNWIDTH = 90
ROWHEIGHT = 80

pygame.init()

# Initalise the gameBoard
gameBoard = [' ', ' ', ' ', ' ', ' ', ' ', ' ',
             ' ', ' ', ' ', ' ', ' ', ' ', ' ',
             ' ', ' ', ' ', ' ', ' ', ' ', ' ',
             ' ', ' ', ' ', ' ', ' ', ' ', ' ',
             ' ', ' ', ' ', ' ', ' ', ' ', ' ',
             ' ', ' ', ' ', ' ', ' ', ' ', ' ']


# Initalise window settings
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Connect 4')
largeFont = pygame.font.SysFont("arial", 80)
smallFont = pygame.font.SysFont("arial", 40)

# Initialise win/draw/loss text boxes
playerWins = largeFont.render('Player Wins!', 1, (0,0,0))
computerWins = largeFont.render('Computer Wins!', 1, (0,0,0))
gameDraw = largeFont.render('Draw!', 1, (0,0,0))
clickAnywhere = smallFont.render('Click Anywhere', 1, (0,0,0))
playAgain = smallFont.render('to Play Again', 1, (0,0,0))

# Initialise images
background = pygame.image.load('connect4Board.png').convert_alpha()
highlightRow = pygame.image.load('highlightRow.png').convert_alpha()
redPiece = pygame.image.load('redPiece.png').convert_alpha()
yellowPiece = pygame.image.load('yellowPiece.png').convert_alpha()

# Initalise booleans
running = True
computerWon = False
gameOver = False
turn = 0

while running == True:
    # Set up background
    screen.fill((255, 255, 255))
    screen.blit(background, (0,0))

    # Highlight the row on the board that the mouse is hovered over
    screen.blit(highlightRow, (pygame.mouse.get_pos()[0] // COLUMNWIDTH * COLUMNWIDTH, 0))

    printBoard(gameBoard)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[K_ESCAPE]:
            running = False

        elif event.type == MOUSEBUTTONDOWN and turn % 2 == 0 and gameOver == False:
            mouseX = pygame.mouse.get_pos()[0]
            if mouseX < 630:
                gameBoard = placePiece(gameBoard, (mouseX // 90), 'R')

                if checkWin(gameBoard) == True:
                    gameOver = True

                turn += 1

        # Reset the game settings on a click anywhere when the game is over
        elif event.type == MOUSEBUTTONDOWN and gameOver == True:
            gameBoard = [' ', ' ', ' ', ' ', ' ', ' ', ' ',
                         ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                         ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                         ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                         ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                         ' ', ' ', ' ', ' ', ' ', ' ', ' ']
            turn = 0
            computerWon = False
            gameOver = False


    # Perform computer's turn
    if turn % 2 != 0 and gameOver == False:
        gameBoard = computerTurn(gameBoard)
        if checkWin(gameBoard) == True:
            gameOver = True
            computerWon = True

        else:
            turn += 1

    # Print that game was a draw if turn exceeds 40
    elif turn >= 41 and gameOver == False:
        gameOver = True

    # Print if player or computer won
    if gameOver == True:
        if computerWon == True:
            screen.blit(computerWins, (60, 50))

        elif computerWon == False and turn < 41:
            screen.blit(playerWins, (120, 50))

        else:
            screen.blit(gameDraw, (220, 50))

        # Prompt that you can click anywhere to play again
        screen.blit(clickAnywhere, (200, 250))
        screen.blit(playAgain, (220, 300))

    pygame.display.flip()

pygame.quit()
