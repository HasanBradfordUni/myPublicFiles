import pygame
from pygame.locals import *
from time import sleep
from random import randint

LIGHT = (53, 53, 53)
DARK = (220, 189, 194)
SCREEN = (0,255,0)
HIGHLIGHT = (255,255,0)
piecesDict = {"Pawn Black":"bP","Pawn White":"wP","Queen Black":"bQ","Queen White":"wQ"}

class Chest(pygame.sprite.Sprite):
    def __init__(self, pieceContains, location, whiteRank, blackRank, image_file):
        pygame.sprite.Sprite.__init__(self)
        self.__contains = pieceContains
        self.__location = location
        self.__whiteRank = whiteRank
        self.__blackRank = blackRank

        self.surf = pygame.Surface((75, 75))
        self.surf = pygame.image.load(image_file).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(location))

    def setWhiteRank(whiteRank):
        self.__whiteRank = whiteRank

    def setBlackRank(blackRank):
        self.__blackRank = blackRank

    def setPieceContains(piece):
        self.__contains = piece

    def getWhiteRank():
        return self.__whiteRank

    def getBlackRank():
        return self.__blackRank

    def getPieceContains():
        return self.__contains

    def getLocation():
        return self.__location

class Text(pygame.sprite.Sprite):
    def __init__(self, text, color, colour):
        # Call the parent class (Sprite) constructor  
        pygame.sprite.Sprite.__init__(self)
    
        self.font = pygame.font.SysFont("Arial", 100)
        self.textSurf = self.font.render(text, 1, color)
        self.surf = pygame.Surface((1000, 100))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect(center=(650,50,))
        
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.surf.blit(self.textSurf, [1000/2 - W/2, 100/2 - H/2])

class Board(object):
    def __init__(self):
        self.width = 8
        self.length = 8
        
class Square(pygame.sprite.Sprite):
    def __init__(self, colour, location):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface((100, 100))
        self.surf.fill(colour)
        self.location = location
        self.rect = self.surf.get_rect(center=(location))

    def getCoords(self):
        return self.location

class Piece(pygame.sprite.Sprite):
    def __init__(self, pieceType):
        pygame.sprite.Sprite.__init__(self)
        self._type = pieceType

    def get_type(self):
        return self._type

class Pawn(Piece):
    def __init__(self, pieceType, image_file, location, colour, rank):
        super().__init__(pieceType)
        self.surf = pygame.Surface((75, 75))
        self.surf = pygame.image.load(image_file).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.__location = location
        self.rect = self.surf.get_rect(center=(location))
        self.__colour = colour
        self.__rank = rank

    def get_possibleMoves(self, piecePos, possibleMoves, moveNum1, moveNum2, capturing):
        pieceX = round(((piecePos[0] - 200) / 100) - 1)
        pieceY = round(((piecePos[1] - 100) / 100) - 1)
        possibleMoves[pieceX][pieceY] = False
        if self.__colour == "Black":
            if capturing:
                possibleMoves[pieceX-1][pieceY-1] = True
            elif moveNum2 == 1:
                possibleMoves[pieceX][pieceY-1] = True
                possibleMoves[pieceX][pieceY-2] = True
            else:
                possibleMoves[pieceX][pieceY-1] = True
        elif self.__colour == "White":
            if capturing:
                possibleMoves[pieceX+1][pieceY+1] = True
            elif moveNum1 == 1:
                possibleMoves[pieceX][pieceY+1] = True
                possibleMoves[pieceX][pieceY+2] = True
            else:
                possibleMoves[pieceX][pieceY+1] = True
        return possibleMoves

    def checkMove(self, moveFrom, moveWhere, possibleMoves, capturing):
        X = moveWhere[0]
        Y = moveWhere[1]
        pieceX = round(((X - 200) / 100) - 1)
        pieceY = round(((Y - 100) / 100) - 1)
        if possibleMoves[pieceX][pieceY]:
            moveValid = True
        else:
            moveValid = False
        if capturing:
            captured = True
        else:
            captured = False
        if moveValid:
            self.__rank += 1
        return moveValid, captured

    def checkCapturing(self, piecePos, piecesArray):
        pieceX = round(((piecePos[0] - 200) / 100) - 1)
        pieceY = round(((piecePos[1] - 100) / 100) - 1)
        try:
            if self.__colour == "White":
                leftCapture = piecesArray[pieceX-1][pieceY+1]
                rightCapture = piecesArray[pieceX+1][pieceY+1]
            elif self.__colour == "Black":
                leftCapture = piecesArray[pieceX-1][pieceY-1]
                rightCapture = piecesArray[pieceX+1][pieceY-1]
            else:
                leftCapture = None
                rightCapture = None
        except:
            leftCapture = None
            rightCapture = None
        if leftCapture != None or rightCapture != None:
            capturing = True
        else:
            capturing = False
        return capturing
    
    def getCoords(self):
        return self.__location

    def getColour(self):
        return self.__colour

    def getRank(self):
        return self.__rank

class Queen(Piece):
    def __init__(self, pieceType, image_file, location, colour, rank):
        super().__init__(pieceType)
        self.surf = pygame.Surface((75, 75))
        self.surf = pygame.image.load(image_file).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.__location = location
        self.rect = self.surf.get_rect(center=(location))
        self.__colour = colour
        self.__rank = rank

    def get_possibleMoves(self, piecePos, possibleMoves, moveNum1, moveNum2, capturing):
        pieceX = round(((piecePos[0] - 200) / 100) - 1)
        pieceY = round(((piecePos[1] - 100) / 100) - 1)
        possibleMoves[pieceX][pieceY] = False
        for x in range(len(possibleMoves)):
            try:
                possibleMoves[pieceX+x][pieceY] = True
            except:
                "Out of range"
            try:
                possibleMoves[pieceX-x][pieceY] = True
            except:
                "Out of range"
        for y in range(len(possibleMoves)):
            try: 
                possibleMoves[pieceX][pieceY+y] = True
            except:
                "Out of range"
            try:
                possibleMoves[pieceX][pieceY-y] = True
            except:
                "Out of range"
        for x in range(len(possibleMoves)):
            for y in range(len(possibleMoves)):
                if x == y:
                    try:
                        possibleMoves[pieceX+x][pieceY-y] = True
                    except:
                        "Out of range"
                    try:
                        possibleMoves[pieceX+x][pieceY+y] = True
                    except:
                        "Out of range"
                    try:
                        possibleMoves[pieceX-x][pieceY-y] = True
                    except:
                        "Out of range"
                    try:
                        possibleMoves[pieceX-x][pieceY+y] = True
                    except:
                        "Out of range"
        return possibleMoves

    def checkMove(self, moveFrom, moveWhere, possibleMoves):
        X = moveWhere[0]
        Y = moveWhere[1]
        pieceX = round(((X - 200) / 100) - 1)
        pieceY = round(((Y - 100) / 100) - 1)
        if possibleMoves[pieceX][pieceY]:
            moveValid = True
        else:
            moveValid = False
        return moveValid
    
    def getCoords(self):
        return self.__location

    def getColour(self):
        return self.__colour

    def getRank(self):
        return self.__rank

    def setRank(self, rank):
        self.__rank = rank

class Rook(Piece):
    def __init__(self, pieceType, image_file, location, colour, rank):
        super().__init__(pieceType)
        self.surf = pygame.Surface((75, 75))
        self.surf = pygame.image.load(image_file).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.__location = location
        self.rect = self.surf.get_rect(center=(location))
        self.__colour = colour
        self.__rank = rank

    def get_possibleMoves(self, piecePos, possibleMoves, moveNum1, moveNum2, capturing):
        pieceX = round(((piecePos[0] - 200) / 100) - 1)
        pieceY = round(((piecePos[1] - 100) / 100) - 1)
        possibleMoves[pieceX][pieceY] = False
        for x in range(len(possibleMoves)):
            try:
                possibleMoves[pieceX+x][pieceY] = True
            except:
                "Out of range"
            try:
                possibleMoves[pieceX-x][pieceY] = True
            except:
                "Out of range"
        for y in range(len(possibleMoves)):
            try: 
                possibleMoves[pieceX][pieceY+y] = True
            except:
                "Out of range"
            try:
                possibleMoves[pieceX][pieceY-y] = True
            except:
                "Out of range"
        return possibleMoves

    def checkMove(self, moveFrom, moveWhere, possibleMoves):
        X = moveWhere[0]
        Y = moveWhere[1]
        pieceX = round(((X - 200) / 100) - 1)
        pieceY = round(((Y - 100) / 100) - 1)
        if possibleMoves[pieceX][pieceY]:
            moveValid = True
        else:
            moveValid = False
        return moveValid
    
    def getCoords(self):
        return self.__location

    def getColour(self):
        return self.__colour

    def getRank(self):
        return self.__rank

    def setRank(self, rank):
        self.__rank = rank

class Bishop(Piece):
    def __init__(self, pieceType, image_file, location, colour, rank):
        super().__init__(pieceType)
        self.surf = pygame.Surface((75, 75))
        self.surf = pygame.image.load(image_file).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.__location = location
        self.rect = self.surf.get_rect(center=(location))
        self.__colour = colour
        self.__rank = rank

    def get_possibleMoves(self, piecePos, possibleMoves, moveNum1, moveNum2, capturing):
        pieceX = round(((piecePos[0] - 200) / 100) - 1)
        pieceY = round(((piecePos[1] - 100) / 100) - 1)
        possibleMoves[pieceX][pieceY] = False
        for x in range(len(possibleMoves)):
            for y in range(len(possibleMoves)):
                if x == y:
                    try:
                        possibleMoves[pieceX+x][pieceY-y] = True
                    except:
                        "Out of range"
                    try:
                        possibleMoves[pieceX+x][pieceY+y] = True
                    except:
                        "Out of range"
                    try:
                        possibleMoves[pieceX-x][pieceY-y] = True
                    except:
                        "Out of range"
                    try:
                        possibleMoves[pieceX-x][pieceY+y] = True
                    except:
                        "Out of range"
        return possibleMoves

    def checkMove(self, moveFrom, moveWhere, possibleMoves):
        X = moveWhere[0]
        Y = moveWhere[1]
        pieceX = round(((X - 200) / 100) - 1)
        pieceY = round(((Y - 100) / 100) - 1)
        if possibleMoves[pieceX][pieceY]:
            moveValid = True
        else:
            moveValid = False
        return moveValid
    
    def getCoords(self):
        return self.__location

    def getColour(self):
        return self.__colour

    def getRank(self):
        return self.__rank

    def setRank(self, rank):
        self.__rank = rank

class Knight(Piece):
    def __init__(self, pieceType, image_file, location, colour, rank):
        super().__init__(pieceType)
        self.surf = pygame.Surface((75, 75))
        self.surf = pygame.image.load(image_file).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.__location = location
        self.rect = self.surf.get_rect(center=(location))
        self.__colour = colour
        self.__rank = rank

    def get_possibleMoves(self, piecePos, possibleMoves, moveNum1, moveNum2, capturing):
        pieceX = round(((piecePos[0] - 200) / 100) - 1)
        pieceY = round(((piecePos[1] - 100) / 100) - 1)
        possibleMoves[pieceX][pieceY] = False
        try:
            possibleMoves[pieceX+2][pieceY+1] = True
        except:
            "Out of range"
        try:
            possibleMoves[pieceX-2][pieceY+1] = True
        except:
            "Out of range"
        try: 
            possibleMoves[pieceX+1][pieceY+2] = True
        except:
            "Out of range"
        try:
            possibleMoves[pieceX+1][pieceY-2] = True
        except:
            "Out of range"
        try:
            possibleMoves[pieceX+2][pieceY-1] = True
        except:
            "Out of range"
        try:
            possibleMoves[pieceX-1][pieceY+2] = True
        except:
            "Out of range"
        try:
            possibleMoves[pieceX-2][pieceY-1] = True
        except:
            "Out of range"
        try:
            possibleMoves[pieceX-1][pieceY-2] = True
        except:
            "Out of range"
        return possibleMoves

    def checkMove(self, moveFrom, moveWhere, possibleMoves):
        X = moveWhere[0]
        Y = moveWhere[1]
        pieceX = round(((X - 200) / 100) - 1)
        pieceY = round(((Y - 100) / 100) - 1)
        if possibleMoves[pieceX][pieceY]:
            moveValid = True
        else:
            moveValid = False
        return moveValid
    
    def getCoords(self):
        return self.__location

    def getColour(self):
        return self.__colour

    def getRank(self):
        return self.__rank

    def setRank(self, rank):
        self.__rank = rank

def draw(piecesArray):
    pieces = pygame.sprite.Group()
    for x in range(0, board.width):
        for y in range(0, board.length):
            X = ((x+1)*100) + 200
            Y = ((y+1)*100) + 100
            if piecesArray[x][y] == "bP":
                rank = board.length - y
                b_pawn = Pawn("Pawn", "b_pawn.png", [X, Y], "Black", rank)
                pieces.add(b_pawn)
            elif piecesArray[x][y] == "wP":
                rank = y + 1
                w_pawn = Pawn("Pawn", "w_pawn.png", [X, Y], "White", rank)
                pieces.add(w_pawn)
            elif piecesArray[x][y] == "wQ":
                rank = y + 1
                w_queen = Queen("Queen", "w_queen.png", [X, Y], "White", rank)
                pieces.add(w_queen)
            elif piecesArray[x][y] == "bQ":
                rank = board.length - y
                b_queen = Queen("Queen", "b_queen.png", [X, Y], "Black", rank)
                pieces.add(b_queen)
    return pieces

pygame.init()

win = pygame.display.set_mode((1300, 1000), pygame.RESIZABLE)
pygame.display.set_caption("Chest Chess")

colour1 = DARK
colour2 = LIGHT

board = Board()

piecesArray = []
for x in range(0, board.width):
    piecesRow = []
    for y in range(0, board.length):
        piecesRow.append(None)
    piecesArray.append(piecesRow)

piecesArray[3][0] = "wP"
piecesArray[3][7] = "bP"
piecesArray[4][0] = "wP"
piecesArray[4][7] = "bP"

def draw_squares(colour1, colour2, squares):
    for x in range(0, board.width):
        for y in range(0, board.length):
            if x % 2 == 0 and y % 2 == 0:
                colour = colour1
            elif x % 2 == 1 and y % 2 == 1:
                colour = colour1
            else:
                colour = colour2
            X = ((x+1)*100) + 200
            Y = ((y+1)*100) + 100
            square = Square(colour, (X, Y))
            squares.add(square)
    return squares

def getPiece(mouseX, mouseY, coordsX, coordsY):
    if (mouseX - 50) < coordsX < (mouseX + 50) or (mouseY - 50) < coordsY < (mouseY + 50):
        return True
    else:
        return False

pieces = draw(piecesArray)
squares = pygame.sprite.Group()
squares = draw_squares(colour1, colour2, squares)
chests = pygame.sprite.Group()

def countPieces(pieceColour, blackCount, whiteCount):
    if pieceColour == "Black":
        blackCount += 1
    elif pieceColour == "White":
        whiteCount += 1
    return blackCount, whiteCount

clicks = 0
moveNum1 = 1
moveNum2 = 1
blackCount = 2
whiteCount = 2
playerTurn = "White"
turnText = Text("White's turn!", "White", SCREEN)
textBoxes1 = pygame.sprite.Group()
textBoxes1.add(turnText)
turnValid = False
gameOver = False

def checkGameOver(blackCount, whiteCount):
    if blackCount <= 0:
        gameOver = True
        winner = "White"
    elif whiteCount <= 0:
        gameOver = True
        winner = "Black"
    else:
        gameOver = False
        winner = None
    return gameOver, winner

possibleMoves = []
origPossibleMoves = []
for x in range(0, board.width):
    possibleMovesRow = []
    origPossibleMovesRow = []
    for y in range(0, board.length):
        possibleMovesRow.append(False)
        origPossibleMovesRow.append(False)
    possibleMoves.append(possibleMovesRow)
    origPossibleMoves.append(origPossibleMovesRow)

def displayGameOver(winner):
    win = pygame.display.set_mode((1300, 1000), pygame.RESIZABLE)
    pygame.display.set_caption("Chest Chess")
    text = f"The winner is: {winner}"
    displayText = Text(text, "Blue", SCREEN)
    run = True

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

        win.fill(SCREEN)

        win.blit(displayText.surf, displayText.rect)
        pygame.display.update()

    if not run:
        sleep(3)
        pygame.quit()

def spawnChests(piecesCount):
    chests = pygame.sprite.Group()
    for num in range(10-piecesCount):
        rank = randint(1, 8)
        row = randint(1, 8)
        X = ((row)*100) + 200
        Y = ((rank)*100) + 100 
        chest = Chest(None, (X, Y), rank, 8-rank, "Chest.png")
        chests.add(chest)
    return chests
    
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicks += 1
            if clicks % 2 == 0:
                if not gameOver:
                    possibleMoves = origPossibleMoves
                    squares = pygame.sprite.Group()
                    squares = draw_squares(colour1, colour2, squares)
                    blackCount = 0
                    whiteCount = 0
                    for piece in pieces:
                        coords = piece.getCoords()
                        mouseX = mouse[0]
                        mouseY = mouse[1]
                        coordsX = coords[0]
                        coordsY = coords[1]
                        thisPiece = getPiece(mouseX, mouseY, coordsX, coordsY)
                        pieceType = piece.get_type()
                        pieceColour = piece.getColour()
                        pieceRank = None         
                        blackCount, whiteCount = countPieces(pieceColour, blackCount, whiteCount)
                        piecesCount = blackCount + whiteCount
                        gameOver, winner = checkGameOver(blackCount, whiteCount)
                        if (moveNum1 + moveNum2) % 5 == 0:
                            chests = spawnChests(piecesCount)
                        if thisPiece:
                            if pieceType == "Pawn":
                                pieceRank = piece.getRank()
                                capturing = piece.checkCapturing(coords, piecesArray)
                                moveValid, captured = piece.checkMove(coords, mouse, possibleMoves, capturing)
                            else:
                                moveValid = piece.checkMove(coords, mouse, possibleMoves)
                            if moveValid and pieceColour == playerTurn:
                                turnValid = True
                                prevPieceX = round(((coordsX - 200) / 100) - 1)
                                prevPieceY = round(((coordsY - 100) / 100) - 1)
                                piece.kill()
                                piecesArray[prevPieceX][prevPieceY] = None
                                pieceX = round(((mouseX - 200) / 100) - 1)
                                pieceY = round(((mouseY - 100) / 100) - 1)
                                if pieceRank == 7:
                                    pieceType = "Queen"
                                newPiece = piecesDict[str(pieceType)+" "+str(pieceColour)]
                                piecesArray[pieceX][pieceY] = newPiece
                                if pieceColour == "White":
                                    moveNum1 += 1
                                elif pieceColour == "Black":
                                    moveNum2 += 1
                            else:
                                turnValid = False
                    if playerTurn == "White":
                        playerTurn = "Black"
                        turnText = Text("Black's turn!", "Black", SCREEN)
                        textBoxes1 = pygame.sprite.Group()
                        textBoxes1.add(turnText)
                    elif playerTurn == "Black":
                        playerTurn = "White"
                        turnText = Text("White's turn!", "White", SCREEN)
                        textBoxes1 = pygame.sprite.Group()
                        textBoxes1.add(turnText)
                    else:
                        playerTurn = "White"
                        turnText = Text("White's turn!", "White", SCREEN)
                        textBoxes1 = pygame.sprite.Group()
                        textBoxes1.add(turnText)
                    for piece in pieces:
                        piece.kill()
                    pieces = draw(piecesArray)
                else:
                    displayGameOver(winner)
                    run = False
            else:
                if not gameOver:
                    squares = pygame.sprite.Group()
                    squares = draw_squares(colour1, colour2, squares)
                    for piece in pieces:
                        coords = piece.getCoords()
                        mouseX = mouse[0]
                        mouseY = mouse[1]
                        coordsX = coords[0]
                        coordsY = coords[1]
                        if (mouseX - 50) < coordsX < (mouseX + 50) or (mouseY - 50) < coordsY < (mouseY + 50):
                            possibleMoves = origPossibleMoves
                            possibleMoves = piece.get_possibleMoves(coords, possibleMoves, moveNum1, moveNum2, False)
                    for x in range(0, len(possibleMoves)):
                        for y in range(0, len(possibleMoves)):
                            if possibleMoves[x][y]:                    
                                X = ((x+1)*100) + 200
                                Y = ((y+1)*100) + 100
                                square = Square(HIGHLIGHT, (X, Y))
                                squares.add(square)
                else:
                    displayGameOver(winner)
                    run = False

    win.fill(SCREEN)
    
    mouse = pygame.mouse.get_pos()
    
    for square in squares:
        win.blit(square.surf, square.rect)
    for piece in pieces:
        win.blit(piece.surf, piece.rect)
    for textBox in textBoxes1:
        win.blit(textBox.surf, textBox.rect)
    for chest in chests:
        win.blit(chest.surf, chest.rect)
    pygame.display.update()

if not run:
    pygame.quit()
