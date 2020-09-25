import pygame

#initiate pygame window
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((720,620))
pygame.display.set_caption('Connect4')

#constants
BLACK,BLUE,RED,YELLOW = (0,0,0),(20,150,200),(200,0,0),(200,200,50)

def make_piece(colour):
    image = pygame.Surface((80,80)) #make a new surface 80x80 pixels in size
    image.fill(BLUE) #make the entire surface blue
    pygame.draw.circle(image, colour, (40,40), 40) #draws a circle on the surface
    return image #return the new surface

def new_game():
    global turn,game_pieces
    turn = 1
    game_pieces = [[0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0]]

def insert_piece(column):
    global turn
    for a in range(5,-1,-1): #starts at the bottom and works up
        if game_pieces[column][a] == 0: #check if the current space is empty
            game_pieces[column][a] = turn
            check_for_win(column,a)
            turn = 3 - turn #swaps turn between 1 and 2
            break #finally, if the space is empty, end the loop

def check_direction(column,row,x_change,y_change):
    add_length = 0
    x,y = column + x_change , row + y_change
    
    while 0 <= x <= 6 and 0 <= y <= 5:
        if game_pieces[x][y] == turn:
            add_length += 1
            x += x_change
            y += y_change
        else:
            break
            
    return add_length
    
def check_for_win(column,row):
    for dir in [[1,0],[0,1],[1,1],[1,-1]]:
        length = 1
        length += check_direction(column,row,dir[0],dir[1])
        length += check_direction(column,row,-dir[0],-dir[1])
        if length >= 4:
            print("player ", turn, " wins!")
            return

team_circles = make_piece(BLACK),make_piece(RED),make_piece(YELLOW)
new_game()

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.KEYDOWN: #all player inputs
            if event.key == pygame.K_1:
                insert_piece(0)
            if event.key == pygame.K_2:
                insert_piece(1)
            if event.key == pygame.K_3:
                insert_piece(2)
            if event.key == pygame.K_4:
                insert_piece(3)
            if event.key == pygame.K_5:
                insert_piece(4)
            if event.key == pygame.K_6:
                insert_piece(5)
            if event.key == pygame.K_7:
                insert_piece(6)
            if event.key == pygame.K_SPACE:
                new_game()
    
    window.fill(BLUE)
    for a in range(0,7):
        for b in range(0,6):
            team = game_pieces[a][b]
            window.blit(team_circles[team], (20+100*a,20+100*b))
    pygame.display.update()