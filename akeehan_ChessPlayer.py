from chess_player import ChessPlayer
from copy import deepcopy

class akeehan_ChessPlayer(ChessPlayer):

	def __init__(self, board, color):
		super().__init__(board, color)
				
				
	def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
	# YOUR MIND-BOGGLING CODE GOES HERE
	
	#Stalemate = -100
		#For obvious reasons
	
	#Checkmate = 100
		#For obvious reasons
	
	#Checks = 2
		#Prioritize captures over checks, but checks are better than "normal" moves
	
	#Material
		#pawn = 1
		#knight, bishop, fool = 3
		#rook = 5
		#queen = 9
		#princess = 4
		#dis ray = 6
		#king = inf
	
	#Development = 3
		#Prioritize moving pieces over pawns

		# Just declare colors here, so I can use them everywhere
		if self.color == "white":
			opp_color = "black"
		else:
			opp_color = "white"
			
		#Overall heuristic function
		def get_heuristic(board):
			#Reintialize score every function call
			score = 0
			
			#Get stalemate score
			stalemate_score = get_stalemate(board)

			#Get material score
			material_score = get_material(board)

			#Get checkmate score
			checkmate_score = get_checkmate(board)

			#Get check score
			check_score = get_check(board)

			#Get dev score
			dev_score = get_dev(board)

			#Calculate total score
			score = (stalemate_score + checkmate_score + material_score + check_score + dev_score)
						
			return score
			
			
		#Check for stalemates
		def get_stalemate(board):
			#Color logic
			if self.color == "black":
				#Check if stalemate
				if board._is_stalemated("white"):
					#Very very low heuristic value for this because I want to avoid it
					return -100
			else:
				#Check if stalemate
				if board._is_stalemated("black"):
					return -100
			return 0
			
		#Check for material
		def get_material(board):
			#Black score
			b_score = 0
			#White score
			w_score = 0
			
			#Iterate through the board and check what pieces are there
			for square in board:
				#Black
				#Rook
				if board[square].get_notation() == "r":
					b_score += 5
				#Knight, Bishop, Fool
				elif board[square].get_notation() in ["n", "b", "f"]:
					b_score += 3
				#Princess
				elif board[square].get_notation() == "s":
					b_score += 4
				#Disentigration Ray
				elif board[square].get_notation() == "y":
					b_score += 6
				#Queen
				elif board[square].get_notation() == "q":
					b_score += 9
				#Pawn
				elif board[square].get_notation() == "p":
					b_score += 1
				#White
				#Rook
				elif board[square].get_notation() == "R":
					w_score += 5
				#Knight, Bishop, Fool
				elif board[square].get_notation() in ["N", "B", "F"]:
					w_score += 3
				#Princess
				elif board[square].get_notation() == "S":
					w_score += 4
				#Disentigration Ray
				elif board[square].get_notation() == "Y":
					w_score += 6
				#Queen
				elif board[square].get_notation() == "Q":
					w_score += 9
				#Pawn
				elif board[square].get_notation() == "P":
					w_score += 1
			#Color logic
			if self.color == "black":
				total = b_score - w_score
			else:
				total = w_score - b_score
			return total
			
			
		#Check for checkmate
		def get_checkmate(board):
			#Color logic
			if self.color == "black":
				#Check for checkmate
				if board.is_king_in_checkmate("white"):
					#Very very high heuristic value for this obviously
					return 100
			else:
				#Check for checkmate
				if board.is_king_in_checkmate("black"):
					return 100
			return 0
			
		#Check for checks
		def get_check(board):
			#Color logic
			if self.color == "black":
				#Check for checks
				if board.is_king_in_check("white"):
					#Weight this below a capture of a piece, but above capturing pawns
					return 1
			else:
				#Check for checks
				if board.is_king_in_check("black"):
					return 1
			return 0
				
				
		#Get development
		def get_dev(board):
			#Reinitialize score every function call
			score = 0
			#Get the last moves for the board
			moves = board.moves
			#Check if there are no moves made
			if len(moves) > 0:
				#Grab the latest move from moves
				string = moves[len(moves) - 1]
				#Get the destination square from the board
				square = board[string[1]]
				#Logic to check if the last moved piece was not a pawn
				if opp_color == "black" and square != "P":
					score += 2
				elif opp_color == "white" and square != "p":
					score += 2
			return score
			
		
		#Minimax function
		def minimax(board, alpha, beta, player, depth):
			#This stores the moves and their associated heuristics for legal_moves
			potential_moves = []
			#This stores the moves sorted by their heuristics
			good_moves = []
			#Recursive base case
			if depth == 0:
				#Check heuristic
				return get_heuristic(board), None
			
			#Initialize
			best_move = None
			
			#If maximizing/Me
			if player:
				#Initialize
				maxx = float('-inf')
				#Get the legal moves
				my_legal_moves = self.board.get_all_available_legal_moves(self.color)
				good_moves = []
				potential_moves = []
				#Iterate through legal moves and sort based on heuristics and append to good_moves
				for move in my_legal_moves:
					hypo_board = deepcopy(self.board)
					hypo_board.make_move(move[0], move[1])
					heuristic = get_heuristic(hypo_board)
					
					potential_moves.append((move, heuristic))
						
				potential_moves.sort(key=lambda x: x[1], reverse=True)

				for move, _ in potential_moves:
					good_moves.append(move)
				
				#Iterate through good_moves and recursively check for best moves
				for move in good_moves:
					hypo_board = deepcopy(self.board)
					hypo_board.make_move(move[0], move[1])
					eval, _ = minimax(hypo_board, alpha, beta, False, depth - 1)
					#Alpha beta pruning
					if eval > maxx:
						maxx = eval
						best_move = move
					alpha = max(alpha, eval)
					if beta <= alpha:
						break
				return maxx, best_move
			#If minimizing/Opponent
			else:
				#Initialize
				minn = float('inf')
				#Get legal moves
				opp_legal_moves = self.board.get_all_available_legal_moves(opp_color)
				good_moves = []
				potential_moves = []
				
				#Iterate through legal moves and sort based on heuristics and append to good_moves
				for move in opp_legal_moves:
					hypo_board = deepcopy(self.board)
					hypo_board.make_move(move[0], move[1])
					heuristic = get_heuristic(hypo_board)
					potential_moves.append((move, heuristic))
					
				potential_moves.sort(key=lambda x: x[1], reverse=True)
				
				for move, _ in potential_moves:
					good_moves.append(move)
					
				#Iterate through good_moves and recursively check for best moves
				for move in good_moves:
					hypo_board = deepcopy(self.board)
					hypo_board.make_move(move[0], move[1])
					eval, _ = minimax(hypo_board, alpha, beta, True, depth - 1)
					#Alpha beta pruning
					if eval < minn:
						minn = eval
						best_move = move
					beta = min(beta, eval)
					if beta <= alpha:
						break
				return minn, best_move

		#Some logic to change the depth depending on time advantage/disadvantage
		if your_remaining_time > opp_remaining_time:
			depth = 4
		else:
			depth = 3
		
		#Get best eval and best move
		#Only care about best move here
		best_eval, best_move = minimax(self.board, float('-inf'), float('inf'), True, depth)

		return(best_move)
    			
    			
    			
    	
