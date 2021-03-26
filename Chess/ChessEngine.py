"""
This is responsible for storing information. It is determine what are the valid moves, and it will be able to have
a move log.
"""


class GameState():
    def __init__(self):
        # board is an 8x8 2d list , each element has 2 characters
        # first character represents the color of the piece
        # second character represents the type of piece
        # "--" mean empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.blackToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.incheck = False
        self.pins = []
        self.checks = []


        # self.startRow = startSq[0]
        # self.startCol = startSq[1]
        # self.endRow = endSq[0]
        # self.endCol = endSq[1]
        # self.pieceMoved = board[self.startRow][self.startCol]
        # self.pieceCaptured = board[self.endRow][self.endCol]
        # self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # logs the moves so we can undo later
        self.whiteToMove = not self.whiteToMove  # swap players
        # updates King's Location
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)



    '''
    Undo the last move made 
    '''

    def undoMove(self):
        if len(self.moveLog) != 0:  # makes sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turn back
            #updates the kings position
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    '''
    This will generate what moves aer correct besides check  
    '''

    def getValidMoves(self):
        moves = []
        self.incheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow= self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.incheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow),(checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()

        return  moves




    '''

    def in_check(self):
        if self.whiteToMove:
            return self.SquareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.SquareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def SquareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch to opponents move
        oppmov = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppmov:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    '''


    def getAllPossibleMoves(self):
        moves = []
        # moves = [Move((6, 4), (4, 4), self.board)]
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of columns in a given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # called the appropriate move function based on piece type
        return moves

    '''
    Gets the moves of the pawn 
    white move up while black moves down
    
    '''

    def getPawnMoves(self, r, c, moves):
        # making sure the square is empty
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned  = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:  # white pawn moves
            if self.board[r - 1][c] == "--":  # [r-1] we moving up the board # 1 square pawn advance
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r - 2][c] == "--":  # 2 square pawn advance
                        moves.append(Move((r, c), (r - 2, c), self.board))

            if c - 1 >= 0:  # captures to left  -----------------------------------captures - left and right diagonals
                if self.board[r - 1][c - 1][0] == 'b':  # enemy piece that we can capture
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # captures to right
                if self.board[r - 1][c + 1][0] == 'b':  # enemy piece that we can capture
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:  # black pawn moves
            if self.board[r + 1][c] == "--":  # [r-1] we moving up the board # 1 square pawn advance
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--":  # 2 square pawn advance
                        moves.append(Move((r, c), (r + 2, c), self.board))

            if c - 1 >= 0:  # captures to left  -----------------------------------captures - left and right diagonals
                if self.board[r + 1][c - 1][0] == 'w':  # enemy piece that we can capture
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # captures to right
                if self.board[r + 1][c + 1][0] == 'w':  # enemy piece that we can capture
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))
            # add the pawn promotions later

    '''
    Gets the moves of the rook
    they move up down left right
    '''

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break

        direction = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up left down right
        # enemyColor = "b" if self.whiteToMove else "w"
        if self.whiteToMove:
            enemyColor = "b"
        else:
            enemyColor = "w"
        for d in direction:  # go thru direction
            for i in range(1, 8):  # go thru the 7 values
                endRow = r + d[0] * i  # potentially moving up to 7 rows
                endCol = c + d[1] * i  # '' 7 columns
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # make sure the rook is on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--':  # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))  # has the chance to move
                        elif endPiece[0] == enemyColor:  # enemy piece valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break  # can't jump over the enemy piece
                        else:  # friendly piece invalid
                            break
                else:  # off board
                    break

    '''
       Gets the moves of the bishop
       '''

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        direction = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # top left, top right, bottom left, bottom right
        # enemyColor = "b" if self.whiteToMove else "w"
        if self.whiteToMove:
            enemyColor = "b"
        else:
            enemyColor = "w"
        for d in direction:
            for i in range(1, 8):  # bishop moves max 7 sq
                endRow = r + d[0] * i  # potentially moving up to 7 rows
                endCol = c + d[1] * i  # '' 7 columns
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # make sure the rook is on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--':  # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))  # has the chance to move
                        elif endPiece[0] == enemyColor:  # enemy piece valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break  # can't jump over the enemy piece
                        else:  # friendly piece invalid
                            break
                else:  # off board
                    break



    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (2, 1), (2, -1), (2, 1))
        if self.whiteToMove:
            allyColor = "w"
        else:
            allyColor = "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:  # if it is empty or enemy piece
                        moves.append(Move((r, c), (endRow, endCol), self.board))


    def getQueenMoves(self, r, c, moves):
        queenMoves = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        if self.whiteToMove:
            enemyColor = "b"
        else:
            enemyColor = "w"
        for d in queenMoves:
            for i in range(1, 8):  #  moves max 7 sq
                endRow = r + d[0] * i  # potentially moving up to 7 rows
                endCol = c + d[1] * i  # '' 7 columns
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # make sure  is on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':  # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))  # has the chance to move
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break  # can't jump over the enemy piece
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break

    '''
    Gets the moves of the King
    '''
    def getKingMoves(self, r, c, moves): # similar to knight
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    if allyColor == 'w':
                        self.whiteKingLocation = (r,c)
                    else:
                        self.blackKingLocation = (r,c)

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        directions = ((-1, 0), (0, -1), (1,0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B' ) or \
                                (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <=5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append(endRow, endCol, m[0], m[1])
        return inCheck, pins, checks





class Move():
    # maps keys to values
    # key : values
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    Overiding the equals to method 
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endCol, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
