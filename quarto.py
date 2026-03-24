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
def piecesStart():
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

	LINES = [
    # rows
    [(0,0),(0,1),(0,2),(0,3)],
    [(1,0),(1,1),(1,2),(1,3)],
    [(2,0),(2,1),(2,2),(2,3)],
    [(3,0),(3,1),(3,2),(3,3)],
    # columns
    [(0,0),(1,0),(2,0),(3,0)],
    [(0,1),(1,1),(2,1),(3,1)],
    [(0,2),(1,2),(2,2),(3,2)],
    [(0,3),(1,3),(2,3),(3,3)],
    # diagonals
    [(0,0),(1,1),(2,2),(3,3)],
    [(3,0),(2,1),(1,2),(0,3)],
	]

	# Starts a new game
	@classmethod
	def newGame(cls):
		board = [[None,None,None,None], 
				 [None,None,None,None], 
				 [None,None,None,None], 
				 [None,None,None,None]]
		availablePieces = piecesStart()
		return cls(board, None, availablePieces)

	def __str__(self):
		state = ""
		for i in range(4):
			for j in range(4):
				if self.board[i][j] == None:
					state += "OOOO "
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

	# Picks a piece from available choices
	def choosePiece(self, piece):
		piece = self.findPiece(piece)
		self.currentPiece = piece
		self.availablePieces.remove(piece)

	# Places a piece on the board
	def placePiece(self, x, y):
		self.board[x][y] = self.currentPiece
		self.currentPiece = None

	# Returns the piece at a location
	def getPiece(self, x, y):
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

	def quartoProx(self, line):
		allPieces = [self.getPiece(x, y) for x, y in line]
		proximityDict = {}
		placedPieces = [p for p in [p1, p2, p3, p4] if p is not None]

		traitList = ('light', 'tall', 'solid', 'square')
		for trait in traitList:
			trueCount = sum(1 for p in placedPieces if getattr(p, trait))
			falseCount = len(placedPieces) - trueCount
			if trueCount > 0 and falseCount > 0:
				proximityDict[trait] = False  # Quarto impossible for this trait
			else:
				proximityDict[trait] = max(trueCount, falseCount)
		return max(proximityDict.values())

	def checkQuarto(self):
		for line in self.LINES:
			if self.isQuarto(*(self.getPiece(x, y) for x, y in line)):
				return True
		return False

nodeCount = 0

def minimax(state, isMaximizer, isPlacing, alpha=float('-inf'), beta=float('inf')):
	global nodeCount

	nodeCount += 1
	if nodeCount % 10000 == 0: print("Nodes visited:", nodeCount)

	# End conditions
	if state.checkQuarto():  # someone just won
		return -1, None
	if len(state.availablePieces) == 0:  # board is full
		return 0, None

	# Recursive call with alpha-beta pruning
	if isPlacing:
		best = float('-inf')
		bestMove = None
		for x in range(4):
			for y in range(4):
				if state.getPiece(x, y) is None:
					newState = copy.deepcopy(state)
					newState.placePiece(x, y)
					score, _ = minimax(newState, isMaximizer, not isPlacing, alpha, beta)
					if score > best:
						best = score
						bestMove = (x, y)
					alpha = max(alpha, score)
					if alpha >= beta: return best, bestMove
		return best, bestMove
	else:
		best = float('inf')
		bestMove = None
		for piece in state.availablePieces:
			newState = copy.deepcopy(state)
			newState.choosePiece(str(piece))
			score, _ = minimax(newState, not isMaximizer, isPlacing, alpha, beta)
			if score < best:
				best = score
				bestMove = str(piece)
			beta = min(beta, score)
			if alpha >= beta: return best, bestMove
		return best, bestMove

def main():
	game = GameState.newGame()
	# Test scenario that's one move away from victory
	game.choosePiece("TTFF")
	game.placePiece(0, 0)
	game.choosePiece("TTFT")
	game.placePiece(0, 1)
	game.choosePiece("TFTF")
	game.placePiece(0, 2)
	game.choosePiece("TFFF")
	print(game)

	# test quartoProx
	print(game.checkQuarto())

if __name__ == '__main__':
	main()
