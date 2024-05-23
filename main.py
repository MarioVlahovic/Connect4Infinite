import numpy as np
import pygame
import sys
import math

CYAN = (16, 161, 157)
BLACK = (255, 255, 255)
PURPLE = (84, 3, 117)
ORANGE = (255, 112, 0)

ROW_COUNT = 8
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece, turn):
	board[row][col] = piece
	turn += 1
	turn = turn % 2
	return turn

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0)) #flip up-down

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, CYAN, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE)) #(left, top, width, heigth)
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, PURPLE, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, ORANGE, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

myfont = pygame.font.SysFont("monospace", 75)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE)) #crta gornji prvokutnik po kojem se krece krug u zraku
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, PURPLE, (posx, int(SQUARESIZE/2)), RADIUS)
			else: 
				pygame.draw.circle(screen, ORANGE, (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == 0:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					turn = drop_piece(board, row, col, 1, turn)

					if winning_move(board, 1):
						label = myfont.render("Player 1 wins!!", 1, PURPLE)
						screen.blit(label, (40,10))
						game_over = True
				#else:
					
			# # Ask for Player 2 Input
			else:				
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					turn = drop_piece(board, row, col, 2, turn)

					if winning_move(board, 2):
						label = myfont.render("Player 2 wins!!", 1, ORANGE)
						screen.blit(label, (40,10))
						game_over = True
			if game_over == False:
				flush = 1
				for c in range(COLUMN_COUNT):
					for r in range(int(ROW_COUNT/2)):
						if board[r][c] == 0:
							flush = 0
				if flush == 1:
					for c in range(COLUMN_COUNT):
						for r in range(ROW_COUNT-1):
							if r < (ROW_COUNT -1):
								board[r][c] = board[r+1][c]
							else:
								board[r][c] = 0

			print_board(board)
			draw_board(board)

			if game_over:
				pygame.time.wait(3000)