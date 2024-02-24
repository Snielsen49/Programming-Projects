import socket
import pygame
import pickle
import queue
import threading

#making a class to handle the server comunication using threads 
class NetworkThread(threading.Thread):
    def __init__(self, host, port, dataQueue):
        super().__init__()
        self.host = host
        self.port = port
        self.dataQueue = dataQueue
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

    #looking for data to recive i.e. gamestate and color
    def run(self):
        self.client_socket.connect((self.host, self.port))
        while self.running:
            try:
                data = self.client_socket.recv(4096)
                if data:
                    message = pickle.loads(data)
                    self.dataQueue.put(message)
            except:
                self.running = False

    #sending data out 
    def send(self, data):
        try:
            self.client_socket.sendall(pickle.dumps(data))
        except:
            self.running = False

    #stopping the thread and socket 
    def stop(self):
        self.running = False
        self.client_socket.close()



#starting thread 
dataQueue = queue.Queue()
networkThread = NetworkThread('localhost', 5555, dataQueue)
networkThread.start()

pygame.init()

#setting up screen 
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('Two Player Chess')
selected_piece = 100
valid_moves = []

#setting up fonts 
font = pygame.font.Font('freesansbold.ttf',20)
big_font = pygame.font.Font('freesansbold.ttf',50)

timer = pygame.time.Clock()
fps = 60


#varable for the clients color 
print('tring to get color')
my_color = dataQueue.get_nowait()
print(my_color)


#loading images and rescaling 
#black peices
blk_queen = pygame.image.load('LAN Chess/images/black queen.png')
blk_queen = pygame.transform.scale(blk_queen,(90,90))
blk_queen_small = pygame.transform.scale(blk_queen,(45,45))
blk_king = pygame.image.load('LAN Chess/images/black king.png')
blk_king = pygame.transform.scale(blk_king,(90,90))
blk_king_small = pygame.transform.scale(blk_king,(45,45))
blk_bishop = pygame.image.load('LAN Chess/images/black bishop.png')
blk_bishop = pygame.transform.scale(blk_bishop,(90,90))
blk_bishop_small = pygame.transform.scale(blk_bishop,(45,45))
blk_rook = pygame.image.load('LAN Chess/images/black rook.png')
blk_rook = pygame.transform.scale(blk_rook,(90,90))
blk_rook_small = pygame.transform.scale(blk_rook,(45,45))
blk_knight = pygame.image.load('LAN Chess/images/black knight.png')
blk_knight = pygame.transform.scale(blk_knight,(90,90))
blk_knight_small = pygame.transform.scale(blk_knight,(45,45))
blk_pawn = pygame.image.load('LAN Chess/images/black pawn.png')
blk_pawn = pygame.transform.scale(blk_pawn,(60,60))
blk_pawn_small = pygame.transform.scale(blk_pawn,(45,45))
#white peices 
wht_rook = pygame.image.load('LAN Chess/images/white rook.png')
wht_rook = pygame.transform.scale(wht_rook,(90,90))
wht_rook_small = pygame.transform.scale(wht_rook,(45,45))
wht_bishop = pygame.image.load('LAN Chess/images/white bishop.png')
wht_bishop = pygame.transform.scale(wht_bishop,(90,90))
wht_bishop_small = pygame.transform.scale(wht_bishop,(45,45))
wht_king = pygame.image.load('LAN Chess/images/white king.png')
wht_king = pygame.transform.scale(wht_king,(90,90))
wht_king_small = pygame.transform.scale(wht_king,(45,45))
wht_knight = pygame.image.load('LAN Chess/images/white knight.png')
wht_knight = pygame.transform.scale(wht_knight,(90,90))
wht_knight_small = pygame.transform.scale(wht_knight,(45,45))
wht_queen = pygame.image.load('LAN Chess/images/white queen.png')
wht_queen = pygame.transform.scale(wht_queen,(90,90))
wht_queen_small = pygame.transform.scale(wht_queen,(45,45))
wht_pawn = pygame.image.load('LAN Chess/images/white pawn.png')
wht_pawn = pygame.transform.scale(wht_pawn,(60,60))
wht_pawn_small = pygame.transform.scale(wht_pawn,(45,45))

#list of imgs
blk_img = [blk_queen, blk_king, blk_bishop, blk_knight, blk_rook, blk_pawn]
blk_img_small = [blk_queen_small, blk_king_small, blk_bishop_small, blk_knight_small, blk_rook_small, blk_pawn_small]
wht_img = [wht_queen, wht_king, wht_bishop, wht_knight, wht_rook, wht_pawn]
wht_img_small = [wht_queen_small, wht_king_small, wht_bishop_small, wht_knight_small, wht_rook_small, wht_pawn_small]
peice_img_loc = ['queen', 'king', 'bishop', 'knight', 'rook', 'pawn']

#drawing board
def drawboard():
    #drawing squares 
    for i in range(32):
        column = i % 4 
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'dark blue', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'dark blue', [700 - (column * 200), row * 100, 100, 100])

        #drawing lossed pieces area and game text area 
        pygame.draw.rect(screen, 'black', [800, 0, 200, 100])
        pygame.draw.rect(screen, 'gray', [800, 100, 200, 900])
        pygame.draw.rect(screen, 'black', [800, 100, 200, 900],5)
        game_text = ['Whites turn!','Pick a destination', 'Blacks turn!', 'Pick a destination']
        screen.blit(font.render(game_text[turnstep],True,'White',None),(810,40))

        #outlining board 
        for i in range(9):
            pygame.draw.line(screen,'black',(0,i*100),(800,i*100),2)
            pygame.draw.line(screen,'black',(i*100,0),(i*100,800),2)

#drawing pieces
def drawpieces():
    #drawing black pieces 
    for i in range(len(black_pieces)):
        index = peice_img_loc.index(black_pieces[i])
        #the pawn is smaller so it needs a difrent draw to be center
        if black_pieces[i] == 'pawn':
            screen.blit(blk_img[index],(black_loc[i][0] * 100 + 20, black_loc[i][1] * 100 + 20))
        else:
            screen.blit(blk_img[index],(black_loc[i][0] * 100 + 10, black_loc[i][1] * 100 + 10))
        
        #Highlight a selected piece 
        if turnstep >= 2 and i == selected_piece:
            pygame.draw.rect(screen, 'green', [black_loc[i][0] * 100 + 1, black_loc[i][1] * 100 + 1, 100, 100],3)

    #drawing white pieces 
    for i in range(len(white_pieces)):
        index = peice_img_loc.index(white_pieces[i])
        #the pawn is smaller so it needs a difrent draw to be center
        if white_pieces[i] == 'pawn':
            screen.blit(wht_img[index],(white_loc[i][0] * 100 + 20, white_loc[i][1] * 100 + 20))
        else:
            screen.blit(wht_img[index],(white_loc[i][0] * 100 + 10, white_loc[i][1] * 100 + 10))

        #Highlight a selected piece 
        if turnstep < 2 and i == selected_piece:
            pygame.draw.rect(screen, 'green', [white_loc[i][0] * 100 + 1, white_loc[i][1] * 100 + 1, 100, 100],3)

#checking move options 
def checkoptions(pieces,locations,turn):

    #list to store moves
    moves_list = []
    #list to store move lists 
    all_moves = []

    for i in range(len(pieces)):

        location = locations[i]
        piece = pieces[i]

        #checking for each piece 
        if piece == 'king':
            moves_list = check_king(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'pawn':
            moves_list = check_pawn(location, turn)
        #adding moves to all moves 
        all_moves.append(moves_list)
        


    return all_moves

#check pawn moves 
def check_pawn(location,turn):
    moves_list = []
    if turn == 'white':

        #one square in front 
        if (location[0], location[1] - 1) not in white_loc and (location[0], location[1] - 1) not in black_loc and location[1] > 0:
            moves_list.append((location[0],location[1] - 1))
        #two squares in front 
        if (location[0], location[1] - 2) not in white_loc and (location[0], location[1] - 2) not in black_loc and location[1] == 6:
            moves_list.append((location[0],location[1] - 2))
        #diagonal atack right
        if (location[0] + 1,location[1] - 1) in black_loc:
            moves_list.append((location[0]+1,location[1]-1))
        #diagonal atack left
        if (location[0] - 1,location[1] - 1) in black_loc:
            moves_list.append((location[0]-1,location[1]-1))

    else:

        #one square in front 
        if (location[0], location[1] + 1) not in white_loc and (location[0], location[1] + 1) not in black_loc and location[1] < 7:
            moves_list.append((location[0],location[1] + 1))
        #two squares in front 
        if (location[0], location[1] + 2) not in white_loc and (location[0], location[1] + 2) not in black_loc and location[1] == 1:
            moves_list.append((location[0],location[1] + 2))
        #diagonal atack right
        if (location[0] + 1,location[1] + 1) in white_loc:
            moves_list.append((location[0]+1,location[1]+1))
        #diagonal atack left
        if (location[0] - 1,location[1] + 1) in white_loc:
            moves_list.append((location[0]-1,location[1]+1))
    return moves_list

#check moves for rook 
def check_rook(location,turn):

    moves = []

    #sets the colors of friends and foes
    if turn == 'white':
        friedly = white_loc
        enemy = black_loc

    if turn == 'black':
        friedly = black_loc
        enemy = white_loc
    
    #loop to check down up right left 
    for i in range(4):
        path = True
        chain = 1
        #down
        if i == 0:
            x = 0
            y = 1
        #up
        elif i == 1:
            x = 0
            y = -1
        #right
        elif i == 2:
            x = 1
            y = 0
        #left
        else:
            x = -1 
            y = 0

        #checks valid move is taken by frendly of off board 
        while path:
            if (location[0] + (chain * x), location[1] + (chain * y)) not in friedly and \
                0 <= location[0] + (chain * x) <= 7 and 0 <= location[1] + (chain * y) <= 7:
                #adds move
                moves.append((location[0] + (chain * x), location[1] + (chain * y)))
                #checks if foe piece is there 
                if (location[0] + (chain * x), location[1] + (chain * y)) in enemy:
                    path = False
                chain += 1
            else:
                path = False

    return moves

#checks knight moves
def check_knight(location,turn):

    moves = []

    #sets the colors of friends and foes
    if turn == 'white':
        friedly = white_loc

    if turn == 'black':
        friedly = black_loc

    #setting movment 1 up 2 left.....
    knight_movment = [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]

    #checking for frendly and if off board 
    for i in range(8):
        target = (location[0] + knight_movment[i][0], location[1] + knight_movment[i][1])
        if target not in friedly and 0<=target[0]<=7 and 0<=target[1]<=7:
            moves.append((location[0] + knight_movment[i][0], location[1] + knight_movment[i][1]))
    
    return moves

#checks bishop moves 
def check_bishop(location,turn):
    
    moves = []

    #sets the colors of friends and foes
    if turn == 'white':
        friedly = white_loc
        enemy = black_loc

    if turn == 'black':
        friedly = black_loc
        enemy = white_loc
    
    #loop to check diagonal
    for i in range(4):
        path = True
        chain = 1
        #up right
        if i == 0:
            x = 1
            y = 1
        #up left
        elif i == 1:
            x = -1
            y = 1
        #down right
        elif i == 2:
            x = 1
            y = -1
        #down left
        else:
            x = -1 
            y = -1

        #checks valid move is taken by frendly of off board 
        while path:
            if (location[0] + (chain * x), location[1] + (chain * y)) not in friedly and \
                0 <= location[0] + (chain * x) <= 7 and 0 <= location[1] + (chain * y) <= 7:
                #adds move
                moves.append((location[0] + (chain * x), location[1] + (chain * y)))
                #checks if foe piece is there 
                if (location[0] + (chain * x), location[1] + (chain * y)) in enemy:
                    path = False
                chain += 1
            else:
                path = False
    return moves
        
#check moves for queen 
def check_queen(location,turn):

    #gets bishop moves 
    moves = check_bishop(location,turn)
    #gets rook moves 
    queen_moves = check_rook(location,turn)

    for i in range(len(queen_moves)):
        moves.append(queen_moves[i])
    
    return moves

#check moves for king 
def check_king(location,turn):

    moves = []

    #sets the colors of friends and foes
    if turn == 'white':
        friedly = white_loc

    if turn == 'black':
        friedly = black_loc
    
    #setting movment 1 up 1 right ....
    king_movment = [(1,1), (1,0), (1,-1), (-1,-1), (-1,1), (-1,0), (0,1), (0,-1)]

    #checking for frendly and if off board 
    for i in range(8):
        target = (location[0] + king_movment[i][0], location[1] + king_movment[i][1])
        if target not in friedly and 0<=target[0]<=7 and 0<=target[1]<=7:
            moves.append((location[0] + king_movment[i][0], location[1] + king_movment[i][1]))
    
    return moves

#check moves for selected piece 
def check_moves():

    #returns white options
    if turnstep < 2:
        move_options = wht_options

    #returns black options
    else:
        move_options = blk_options

    valid_moves = move_options[selected_piece]

    return valid_moves

#draw valid moves of selected piece
def draw_moves(valid_moves):
    #looping through all moves and drawing a circle
    for i in range(len(valid_moves)):
        pygame.draw.circle(screen, 'black', (valid_moves[i][0] * 100 + 50, valid_moves[i][1] * 100 + 50),10)

#draw all captured pieces 
def draw_captured_pieces():
    for i in range(len(captured_pieces_blk)):
        piece = captured_pieces_blk[i]
        index = peice_img_loc.index(captured_pieces_blk[i])
        screen.blit(blk_img_small[index],(825, 105 + 45 * i))
    for i in range(len(captured_pieces_wht)):
        piece = captured_pieces_wht[i]
        index = peice_img_loc.index(captured_pieces_wht[i])
        screen.blit(wht_img_small[index],(925, 105 + 45 * i))

#draws flashing box if in check
def draw_check():
    
    if 'king' in white_pieces:
        #checking king location
        wht_king_idx = white_pieces.index('king')
        wht_king_loc = white_loc[wht_king_idx]
        #going through black options to see if piece can atack 
        for i in range(len(blk_options)):
            if wht_king_loc in blk_options[i]:
                #starts flashing
                if count > 15:
                    pygame.draw.rect(screen, 'dark red', [wht_king_loc[0] * 100 + 1, wht_king_loc[1] * 100 + 1, 100, 100], 5)
    
    if 'king' in black_pieces:
        #checking king location
        blk_king_idx = black_pieces.index('king')
        blk_king_loc = black_loc[blk_king_idx]
        #going through white options to see if piece can atack 
        for i in range(len(wht_options)):
            if blk_king_loc in wht_options[i]:
                #starts flashing
                if count > 15:
                    pygame.draw.rect(screen, 'dark red', [blk_king_loc[0] * 100 + 1, blk_king_loc[1] * 100 + 1, 100, 100], 5)

#draws game over box and text
def game_over():
    pygame.draw.rect(screen,'black',[200,200,700,400])
    screen.blit(big_font.render(f'{winner} is the Winner!',True,'white'),(300,300))
    screen.blit(big_font.render(f'Press any key to quit.',True,'white'),(300,400))
   

running = True
run = True
count = 0


while run:
    timer.tick(fps)

    #ticker for flashing 
    if count < 30:
        count += 1
    else:
        count = 0

    
    while running:
        try:
            
            print('trying to load game state')
            game_state = dataQueue.get(timeout=1)
            white_pieces = game_state['white_pieces']
            white_loc = game_state['white_loc']
            black_pieces = game_state['black_pieces']
            black_loc = game_state['black_loc']
            captured_pieces_wht = game_state['captured_pieces_wht']
            captured_pieces_blk = game_state['captured_pieces_blk']
            turnstep = game_state['turnstep']
            winner = game_state['winner']
            turn_color = game_state['turn_color']
            print('loaded game set up')
            running = False

        except queue.Empty:
            pass

    blk_options = checkoptions(black_pieces, black_loc, 'black')
    wht_options = checkoptions(white_pieces, white_loc, 'white')
    screen.fill('dark gray')
    drawboard()
    drawpieces()
    draw_captured_pieces()
    draw_check()
    

   
    
    if winner != None:
        game_over()

    if selected_piece != 100:
        valid_moves = check_moves()
        draw_moves(valid_moves)


    
        #event handling 
    for event in pygame.event.get():
        
        #end of game
        if event.type == pygame.QUIT:
            run = False 


        #click 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and winner == None:
            x_cord = event.pos[0] // 100
            y_cord = event.pos[1] // 100
            selected_cord = (x_cord,y_cord)

            #whites move
            if turnstep < 2 and selected_cord in white_loc:
                selected_piece = white_loc.index(selected_cord)
                if turnstep == 0:
                    turnstep = 1

            #selected piece can move there
            if selected_cord in valid_moves and selected_piece != 100 and turnstep < 2 and my_color == turn_color:
                white_loc[selected_piece] = selected_cord
                print('moved piece')

                #white is taking a black piece  
                if selected_cord in black_loc:
                    blk_piece = black_loc.index(selected_cord)
                    captured_pieces_blk.append(black_pieces[blk_piece])
                    if black_pieces[blk_piece] == 'king':
                        winner = 'White'
                    black_pieces.pop(blk_piece)
                    black_loc.pop(blk_piece)

                #reseting turn 
                game_state['white_pieces']= white_pieces
                game_state['white_loc'] = white_loc
                game_state['black_pieces'] = black_pieces 
                game_state['black_loc'] = black_loc 
                game_state['captured_pieces_wht'] = captured_pieces_wht
                game_state['captured_pieces_blk'] = captured_pieces_blk
                turnstep = 2 
                game_state['turnstep'] = turnstep
                game_state['winner'] = winner
                game_state['turn_color'] = 'black'
                networkThread.send(game_state)
                blk_options = checkoptions(black_pieces, black_loc, 'black')
                wht_options = checkoptions(white_pieces, white_loc, 'white')
                selected_piece = 100
                valid_moves = []
                running = True
                
                

            #blacks move 
            if turnstep > 1 and selected_cord in black_loc and my_color == turn_color:
                selected_piece = black_loc.index(selected_cord)
                if turnstep == 2:
                    turnstep = 3

                #selected piece can move there
            if selected_cord in valid_moves and selected_piece != 100 and turnstep > 2 and my_color == turn_color:
                black_loc[selected_piece] = selected_cord

                #black is taking a white piece  
                if selected_cord in white_loc:
                    wht_piece = white_loc.index(selected_cord)
                    captured_pieces_wht.append(white_pieces[wht_piece])
                    if white_pieces[wht_piece] == 'king':
                        winner = 'Black'
                    white_pieces.pop(wht_piece)
                    white_loc.pop(wht_piece)

                #reseting turn 
                game_state['white_pieces']= white_pieces
                game_state['white_loc'] = white_loc
                game_state['black_pieces'] = black_pieces 
                game_state['black_loc'] = black_loc 
                game_state['captured_pieces_wht'] = captured_pieces_wht
                game_state['captured_pieces_blk'] = captured_pieces_blk
                turnstep = 0 
                game_state['turnstep'] = turnstep
                game_state['winner'] = winner
                game_state['turn_color'] = 'white'
                networkThread.send(game_state)
                blk_options = checkoptions(black_pieces, black_loc, 'black')
                wht_options = checkoptions(white_pieces, white_loc, 'white')
                selected_piece = 100
                valid_moves = []
                running = True

    #not the clients turn so it remains looking for updates from server
    if turn_color != my_color:
        running = True

    pygame.display.flip()

    #end of game handling 
    if event.type == pygame.KEYDOWN and winner != None:
        run = False
        networkThread.stop()
        pygame.quit()   

networkThread.stop()   
pygame.quit()    