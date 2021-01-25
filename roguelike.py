import pygame,random

#window constants
width,height = 800,800
tile_size = 80

#colours
BLUE,GREEN,RED = (50,50,200),(50,200,50),(200,50,50)
YELLOW,WHITE,BLACK = (200,200,50),(200,200,200),(0,0,0)
GREY,BROWN,LIGHTBROWN = (100,100,100),(75,50,20),(150,75,30)

#initialise
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((width,height))
pygame.display.set_caption('Roguelike')
random.seed()

#game constants
game_width,game_height = 15,15
tiles = [[a for a in range(game_height)] for b in range(game_width)]
game_surface = pygame.Surface((tile_size*game_width,tile_size*game_height))
current_vision = pygame.Surface((tile_size*game_width,tile_size*game_height))
discovered = pygame.Surface((tile_size*game_width,tile_size*game_height))
discovered.set_colorkey(WHITE)
current_vision.set_colorkey(BLACK)
square = pygame.Surface((15,15))
square.fill(BLUE)

#game variables
game_obj = []
up,down,left,right = [0] * 4
wall_tiles = []
walls = []

class Tile():
    def __init__(self,pos,tile_type):
        self.pos = pos
        self.type = tile_type
        self.create_image(GREY)
        game_obj.append(self)
    def create_image(self,colour):
        image = pygame.Surface((tile_size,tile_size))
        pygame.draw.rect(image,colour,(2,2,tile_size-4,tile_size-4))
        self.image = image
    def draw(self):
        draw_pos = int(self.pos[0]*tile_size),\
        int(self.pos[1]*tile_size)
        game_surface.blit(self.image,draw_pos)
class Mob():
    def __init__(self,pos,image):
        self.pos = pos
        self.image = image

    def move(self,dx,dy):
        self.pos[0] += dx
        self.pos[1] += dy

    def draw(self):
        w,h = self.image.get_width(),self.image.get_height()
        draw_pos = int(self.pos[0]*tile_size-w/2),int(self.pos[1]*tile_size-h/2)
        game_surface.blit(self.image,draw_pos)

#test functions
def mark(surface,pos):                          
    pygame.draw.circle(surface,RED,pos,5)
def line(surface,start,end):
    pygame.draw.line(surface,BLUE,start,end,4)

#wall functions
def make_random_walls(width,height,tiles):      #generates the walls
    for col in range(1,6):                      #designate floor tiles
        for row in range(1,6):
            tiles[col][row].type = "floor"
        for row in range(7,12):
            tiles[col][row].type = "floor"

    
    not_designated_floor = []                   #list of all tiles that haven't been assigned
    for col in range(width):                    
        for row in range(height):
            tile = tiles[col][row]
            if tile.type == "none":
                not_designated_floor.append(tile)
    
    random.shuffle(not_designated_floor)        #create walls randomly in places where they 
    for tile in not_designated_floor:           #do not block the path
        if check_for_block(tiles,tile.pos):
            make_wall_tile(tile.pos[0],tile.pos[1])
def make_wall_tile(col,row):                    #turns a tile into a wall
    tiles[col][row].create_image(BLACK)
    tiles[col][row].type = "wall"
    wall_tiles.append(tiles[col][row])
def create_wall_borders():                      #create the lines that bound the wall tiles
    for tile in wall_tiles:
        col,row = tile.pos
        corners = [[col,row],[col+1,row],[col+1,row+1],[col,row+1]] 
        #create a wall on each border that is not bordered by another wall
        if col != 0:
            if tiles[col-1][row].type != "wall":
                walls.append([corners[0],corners[3]])
        if col != game_width-1:
            if tiles[col+1][row].type != "wall":
                walls.append([corners[1],corners[2]])
        if row != 0:
            if tiles[col][row-1].type != "wall":
                walls.append([corners[0],corners[1]])
        if row != game_height-1:
            if tiles[col][row+1].type != "wall":
                walls.append([corners[2],corners[3]])
def combine_wall_borders(walls):
    #where two walls are found to share a start/end point, combine them
    length = len(walls)
    a = 0
    while a < length:
        wall_a = walls[a]
        start_a,end_a = wall
        shared_walls = []

        for b in range(a,length):
            start_b,end_b = wall_b
            #if start_b in 
def check_for_block(tiles,pos):                 #checks if making the tile a wall blocks the path
    '''grid = [[True for a in range(game_height)] for b in range(game_width)]
    for col in range(game_width):
        for row in range(game_height):
            tile = tiles[col][row]
            if tile.type == "wall":
                grid[col][row] = False'''
    neighbours = 0

    col,row = pos
    if col == 0:
        neighbours += 1
    else:
        if tiles[col-1][row].type == "wall":
            neighbours += 1
    if col == game_width-1:
        neighbours += 1
    else:
        if tiles[col+1][row].type == "wall":
            neighbours += 1
    if row == 0:
        neighbours += 1
    else:
        if tiles[col][row-1].type == "wall":
            neighbours += 1
    if row == game_height-1:
        neighbours += 1
    else:
        if tiles[col][row+1].type == "wall":
            neighbours += 1

    return neighbours in [0,1,4]

def draw_game(char,surface,walls):
    camera = int(width/2-char.pos[0]*tile_size),int(height/2-char.pos[1]*tile_size)

    window.fill(BLACK)                          #clear the window
    for c in range(game_width):                 #draw the tiles
        for r in range(game_height):
            tiles[c][r].draw()                  
    player.draw()                               #draw the player
    window.blit(surface,camera)                 #draw game board
    hide_undiscovered(camera)
    pygame.display.update()
def hide_undiscovered(camera):                  #draws all things that player has seen
    current_vision.fill(WHITE)
    line_of_sight(player,walls,current_vision)  #draw line of sight
    discovered.blit(current_vision,(0,0))
    window.blit(discovered,camera)
def line_of_sight(mob,walls,surface):           #draws light of sight to surface
    x,y = int(mob.pos[0]*tile_size),int(mob.pos[1]*tile_size)   #assign variables
    w,h = surface.get_width(),surface.get_height()
    corners = [[0,0],[w,0],[w,h],[0,h]]             
    boundaries = []                                 
    for a in range(4):                          
        boundaries.append([corners[a-1],corners[a]]) 
    top_left,top_right,bottom_right,bottom_left = corners
    left,top,right,bottom = boundaries
    

    for wall in walls:                          #draws a shadow for each wall segment
        a,b = wall
        start = a[0]*tile_size,a[1]*tile_size   #start of the wall
        end = b[0]*tile_size,b[1]*tile_size     #end of the wall
        pts = [start[0]-x,start[1]-y]           #pts: vector from player to start
        pte = [end[0]-x,end[1]-y]               #pte: vector from player to end
        
        polygon = [start,end]                   #the corners of the polygon
        for vector in [pte,pts]:                #finds boundary draw points
            vx,vy = vector                      #by taking the vector and finding the 
            if vx < 0:                          #point where the vector would hit collide
                bx = x                          #with the edge of the game space
            else:
                bx = w - x                      #[bx,by] is the x,y vector to the boundaries 
            if vy < 0:                          #that [vx,vy] is pointing towards 
                by = y                          
            else:                               
                by = h - y
            
            if vx == 0:                             #bound_x,bound_y is the point where 
                if vy > 0:                          #vector would collide with the edge
                    boundary = bottom
                else:                               #if vx == 0, vector will collide 
                    boundary = top                  #with bottom if vy is positive 
                bound_x = int(x)                    #and top if vy is negative
                bound_y = boundary[0][1]
            else:                                   
                if abs(vy/vx) > abs(by/bx):         #if the pte/pts vector is steeper than 
                    if vy > 0:                      #the mob to corner vector, the bound point
                        boundary = bottom           #is on top/bottom. The sign of vy determines
                    else:                           #if it's top or bottom
                        boundary = top
                    bound_x = int(x+by*vx/abs(vy))  
                    bound_y = boundary[0][1]
                else:                               #if the pte/pts vector is less steep, the 
                    if vx > 0:                      #bound point is on left/right. The sign of vx
                        boundary = right            #determines if it's left or right
                    else:
                        boundary = left
                    bound_x = boundary[0][0]
                    bound_y = int(y+bx*vy/abs(vx))
            polygon.append([bound_x,bound_y])
        
        first,second = polygon[2],polygon[3]    
        if first[0] != second[0] and \
        first[1] != second[1]:                  #if bound points are on different borders
            if first[1] > second[1]:            #order bpoints by asc height
                first,second = second,first     
            
            if first[1] == 0:                       #first top
                if second[0] == 0:                  #first top second left
                    polygon.insert(3,top_left)        #then corner is top left
                elif second[0] == w:                #first top second right
                    polygon.insert(3,top_right)       #then corner is top right
                else:                               #first top second bottom
                    if x < first[0]:                #first top second bottom wall right
                        polygon.insert(3,top_right)   #then corners are on right
                        polygon.insert(3,bottom_right)
                    else:                           #first top second bottom wall left
                        polygon.insert(3,top_left)    #then corners are on left
                        polygon.insert(3,bottom_left)

            elif first[0] == 0:                     #first left
                if second[0] == w:                  #first left second right
                    if y < first[1]:                #first left second right wall bottom
                        polygon.insert(3,bottom_left) #then corners are on bottom
                        polygon.insert(3,bottom_right)
                    else:                           #first left second right wall top
                        polygon.insert(3,top_right)   #then corners are on top
                        polygon.insert(3,top_left)

                elif second[1] == h:                #first left second bottom
                    polygon.insert(3,bottom_left)     #then corner is bottom left

            elif first[0] == w:                     #first right
                if second[0] == 0:                  #first right second left
                    if y < first[1]:                #first right second left wall bottom
                        polygon.insert(3,bottom_left) #then corners are on bottom
                        polygon.insert(3,bottom_right)
                    else:                           #first right second left wall top
                        polygon.insert(3,top_right)   #then corners are on top
                        polygon.insert(3,top_left)
                else:                               #first right second bottom
                    polygon.insert(3,bottom_right)    #then corner is bottom right

        pygame.draw.polygon(surface,BLACK,polygon)  #draws quadrilateral behind the shadow

player = Mob([3,1],square)
for c in range(game_width):                     #creates game tiles
    for r in range(game_height):
        tiles[c][r] = Tile((c,r),"none")
make_random_walls(game_width,game_height,tiles)
create_wall_borders()

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        #Character controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                up = 1
            if event.key == pygame.K_s:
                down = 1
            if event.key == pygame.K_a:
                left = 1
            if event.key == pygame.K_d:
                right = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                up = 0
            if event.key == pygame.K_s:
                down = 0
            if event.key == pygame.K_a:
                left = 0
            if event.key == pygame.K_d:
                right = 0

        dx,dy = 0.05*(right-left),0.05*(down-up)
    
    player.move(dx,dy)
    draw_game(player,game_surface,walls)
    clock.tick(60)