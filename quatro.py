import copy
# An individual piece
class Piece:
	def __init__(self, light, tall, solid, square):
		self.light = light
		self.tall = tall
		self.solid = solid
		self.square = square

	def __str__(self):
		name = ""
		traitList = ('light', 'tall', 'solid', 'square')
		for trait in traitList:
			if int(getattr(self, trait)) == 0:
				name += "F"
			else:
				name += "T"
		return name

# Generate all pieces
def pieces_start():
	piecesList = []
	for i in range(2):
		for j in range(2):
			for k in range(2):
				for l in range(2):
					piecesList.append(Piece(bool(i),bool(j),bool(k),bool(l)))
	return piecesList

# A given game state
class GameState:
	def __init__(self, board, currentPiece, availablePieces):
		self.board = board
		self.currentPiece = currentPiece
		self.availablePieces = availablePieces

	# Starts a new game
	@classmethod
	def new_game(cls):
		board = [[None, None, None, None], 
				 [None, None, None, None], 
				 [None, None, None, None], 
				 [None, None, None, None]]
		availablePieces = pieces_start()
		return cls(board, None, availablePieces)

	def __str__(self):
		state = ""
		for i in range(4):
			for j in range(4):
				if self.board[i][j] == None:
					state += "XXXX "
				else:
					state += str(self.board[i][j]) + " "
			state += "\n"
		return state

	# Converts a name to a Piece object
	def findPiece(self, code):
		for piece in self.availablePieces:
			if str(piece) == code:
				return piece
		return None

	# Picks a pieces from available choices
	def choosePiece(self, piece):
		piece = self.findPiece(piece)
		self.currentPiece = piece
		self.availablePieces.remove(piece)

	# Places a piece on the board
	def placePiece(self, x, y):
		self.board[x][y] = self.currentPiece
		self.currentPiece = None

	# Returns the piece at a location
	def checkPiece(self, x, y):
		return self.board[x][y]

	def isQuarto(self, p1, p2, p3, p4):
		# any cells are empty
		if any(p is None for p in [p1, p2, p3, p4]):
			return False

		traitList = ('light', 'tall', 'solid', 'square')
		for trait in traitList:
			t1 = getattr(p1, trait)
			t2 = getattr(p2, trait)
			t3 = getattr(p3, trait)
			t4 = getattr(p4, trait)
			if t1 == t2 == t3 == t4:
				return True
		return False

	def checkQuarto(self):
		for i in range(4):
			if self.isQuarto(self.checkPiece(i, 0), self.checkPiece(i, 1), 
							self.checkPiece(i, 2), self.checkPiece(i, 3)):
				return True
			if self.isQuarto(self.checkPiece(0, i), self.checkPiece(1, i), 
							self.checkPiece(2, i), self.checkPiece(3, i)):
				return True
		if self.isQuarto(self.checkPiece(0, 0), self.checkPiece(1, 1), 
						self.checkPiece(2, 2), self.checkPiece(3, 3)):
			return True
		if self.isQuarto(self.checkPiece(3, 0), self.checkPiece(2, 1), 
						self.checkPiece(1, 2), self.checkPiece(0, 3)):
			return True 
		return False

count = 0 

def minimax(state, is_maximizer, is_placing):
	global count
	count += 1
	if count % 10000 == 0: print("Nodes visited:", count)

	# Termination conditions first
	if state.checkQuarto():  # someone just won
		return -1, None
	if len(state.availablePieces) == 0:  # board is full
		return 0, None
	
	# Then handle the recursive cases
	if is_placing:
		best = float('-inf')
		best_move = None
		for x in range(4):
			for y in range(4):
				if state.checkPiece(x, y) is None:
					new_state = copy.deepcopy(state)
					new_state.placePiece(x, y)
					score, _ = minimax(new_state, is_maximizer, not is_placing)
					if score > best:
						best = score
						best_move = (x, y)
		return best, best_move
	else:
		best = float('inf')
		best_move = None
		for piece in state.availablePieces:
			new_state = copy.deepcopy(state)
			new_state.choosePiece(str(piece))
			score, _ = minimax(new_state, not is_maximizer, is_placing)
			if score < best:
				best = score
				best_move = str(piece)
		return best, best_move
def main():
	game = GameState.new_game()
	# Manually place three tall pieces in row 0
	game.choosePiece("TTFF")
	game.placePiece(0, 0)
	game.choosePiece("TTFT")
	game.placePiece(0, 1)
	game.choosePiece("TFTF")
	game.placePiece(0, 2)
	# Set up the winning piece
	game.choosePiece("TFFF")
	print(game)
	# Ask minimax for the best move
	score, best_move = minimax(game, True, True)
	print("Best move:", best_move)
	print("Score:", score)

if __name__ == '__main__':
	main()