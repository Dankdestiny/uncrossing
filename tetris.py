import pygame,random

#set up
pygame.init()
window = pygame.display.set_mode((460,390))
pygame.display.set_caption('Tetris')
font = pygame.font.SysFont('arial', 40)
clock = pygame.time.Clock()
random.seed()

#constants
BLUE,RED,GREY,BLACK,ORANGE = (50,50,255),(200,50,50),(155,155,155),(0,0,0),(255,165,0)
YELLOW,CYAN,PURPLE,GREEN = (255,255,50),(50,255,255),(200,0,200),(0,200,0)

#variables
timer,score = 0,0
game_squares = [] #list of every square to be displayed
landed_squares = [] #list of every square that has landed

class GameSquare(): #each square in tetris is a GameSquare object

    def __init__(self,x,y,colour): #creates image and position, adds self to list
        self.x,self.y = x,y
        self.colour = colour
        self.image = self.draw_square(colour)
        game_squares.append(self) 
        
    def draw_square(self,colour): #returns a pygame surface of a coloured square
        image = pygame.Surface((30,30))
        pygame.draw.rect(image,colour,(0,0,30,30))
        pygame.draw.rect(image,BLACK,(0,0,30,30),1)
        return image
        
    def draw(self): #updates the pygame window with the game square image
        draw_pos = (30*self.x,30*self.y)
        window.blit(self.image,draw_pos)
        
    def move(self,x,y):
        self.x += x
        self.y += y

class Shape(): #the current falling object, and next object 
    
    def __init__(self,type,x,y):
        self.new_shape(type,x,y)
        
    def new_shape(self,type,x,y): #creates falling object from the top
        self.type = type
        self.colour = get_colour(type)
        self.max_rotations = get_rotations(type) #the number of distinct rotations
        self.rotation = 1 #relevant only to Shapes with 2 max_rotations
        
        squares = get_shape(type)
        self.squares = [] #self.squares is a set of game_squares that Shape is made of
        for square in squares:
            self.squares.append(GameSquare(x+square[0],y+square[1],self.colour))
      
    def hitting_floor(self): #returns True iff self about to hit a square/floor
        for square in self.squares:
            if square.y == 12:
                return True
            for landed in landed_squares:
                if square.x == landed.x and square.y + 1 == landed.y:
                    return True
        return False
      
    def down(self): #moves down if there's space
        add_score = 0
        '''the program didn't want to deal with the score variable when I used it 
        within the delete lines function, so instead I made a trail of returns to 
        pass the change in value of score, hence add_score variable'''
        
        if not self.hitting_floor(): #then there is space to fall
            for square in self.squares:
                square.move(0,1)
        else: #then self has landed
            for square in self.squares:
                landed_squares.append(square)
                
                if square.y <= 0: #ends game if self has landed at top: game is over
                    pygame.quit()
                    quit()
            
            add_score = delete_lines()
            
            #sets self's Shape equal to next's Shape
            self.new_shape(next.type,4,0)
            
            #create new Shape for next
            for square in next.squares:
                game_squares.remove(square)
            next.new_shape(random.randint(0,6),12,1)
            
        return add_score
        
    def move(self,change): #left-right movement
        
        for square in self.squares: #checks that self isn't moving out game area
            if not 0 <= square.x + change <= 9: 
                return
                
            for landed in landed_squares: #checks self isn't moving through another square
                if square.x + change == landed.x and square.y == landed.y:
                    return
           
        for square in self.squares:
            square.move(change,0)
                
    def rotate(self): #rotates self if that move is valid
        self.find_rotation(1) #performs the rotation
        if not self.check_rotation_valid():
            self.find_rotation(-1) #reverses rotation if it is invalid
        self.rotation *= -1
        
    def find_rotation(self,turn): #performs a rotation
        '''rotates self by finding each squares position relative to pivot,
        rotating, then moving square back to correct position'''
        [a,b,c,d] = self.squares
        pivot = [b.x,b.y] #the pivot of rotation
        
        for square in self.squares:
            if square != b:
                square.x -= b.x
                square.y -= b.y
                
                if self.max_rotations == 4:
                    square.x,square.y = -turn*square.y,turn*square.x
                
                elif self.max_rotations == 2:
                    '''rotation direction alternates for Shapes with rotational
                    symmetry'''
                    if self.rotation == 1:
                        square.x,square.y = -turn*square.y,turn*square.x
                    else:
                        square.x,square.y = turn*square.y,-turn*square.x
                        
                square.x += b.x
                square.y += b.y
        
    def check_rotation_valid(self): #returns True iff rotation is valid
        for square in self.squares:
            if square.x > 9 or square.x < 0 or square.y >= 12:
                return False
            for landed in landed_squares:
                if square.x == landed.x and square.y == landed.y:
                    return False
        return True

def get_colour(type): #returns the colour associated with type
    if type == 0:
        return RED
    elif type == 1:
        return YELLOW
    elif type == 2:
        return PURPLE
    elif type == 3:
        return ORANGE
    elif type == 4:
        return GREEN
    elif type == 5:
        return CYAN
    elif type == 6:
        return BLUE
def get_shape(type): #returns the Shape associated with type
    if type == 0:
        return [(1,0),(0,0),(0,1),(1,1)]
        
    elif type == 1:
        return [(-1,0),(0,0),(1,0),(2,0)]
    elif type == 2:
        return [(1,0),(0,0),(0,1),(-1,1)]
    elif type == 3:
        return [(-1,0),(0,0),(0,1),(1,1)]
        
    elif type == 4:
        return [(-1,0),(0,0),(1,0),(0,1)]
    elif type == 5:
        return [(-1,0),(0,0),(1,0),(1,1)]
    elif type == 6:
        return [(-1,0),(0,0),(1,0),(-1,1)]

'''get rotations returns the number of unique rotations a shape has,
this is relevant because shapes that have two rotations do not have a 
consistent pivot/turn direction when rotating them'''
def get_rotations(type):  
    if type == 0:
        return 1
    elif 1 <= type <= 3:
        return 2
    else:
        return 4

def sort(item): #returns item in ascending order
    length = len(item)
    for a in range(0,length-1):
        for b in range(0,length-1-a):
            if item[b] > item[b+1]:
                item[b],item[b+1] = item[b+1],item[b]
    return item
def delete_lines(): #deletes lines that are filled, moves all above lines down
    lines = [0]*13 
    '''each element of this array represents the number of squares
    found on each line'''
    full_lines = []
    add_score = 0
    
    for square in landed_squares: 
        a = square.y
        lines[a] += 1 #for each landed, add 1 to the line in lines corresponding to y
        
    for a in range(0,13):    
        if lines[a] == 10: 
            full_lines.append(a) #if a line is filled, add it to full_lines
            add_score += 1 #and increase score
    
    full_lines = sort(full_lines) #we want to start with the top filled line
    #and work down
    for line in full_lines: #for every full line
        to_remove = []
        for square in game_squares:
            if square.y == line: #find squares in the full line
                to_remove.append(square) #and add to the delete pile
                
        for square in to_remove: #then delete them
            game_squares.remove(square)
            landed_squares.remove(square)
            del(square)
        for square in landed_squares: #and move all squares above down 1
            if square.y < line:
                square.y += 1
    return add_score #return number equal to number of lines deleted

background = pygame.Surface((460,390))
background.fill(GREY)
pygame.draw.rect(background,BLACK,(0,0,300,400))

current_falling = Shape(random.randint(0,6),4,0) #creates the first Shape that falls
next = Shape(random.randint(0,6),12,1) #creates the next one

fast_forward = False
while True:
    for event in pygame.event.get(): #controls for movement
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                current_falling.move(-1)
            if event.key == pygame.K_RIGHT:
                current_falling.move(1)
            if event.key == pygame.K_DOWN:
                fast_forward = True
            if event.key == pygame.K_UP:
                current_falling.rotate()
        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            fast_forward = False
            
        if event.type == pygame.QUIT: 
            pygame.quit()            
            
    
    speed = (1+score/40) #causes the game to speed up as score increases
    if fast_forward:
        speed *= 10
        
    timer += 1 #calls the current Shape to fall after a certain amount of time
    if timer >= 60/speed: 
        add_score = current_falling.down()
        timer = 0
        score += add_score
    
    #update visuals
    window.blit(background,(0,0))
    for square in game_squares:
        square.draw()
    text = font.render(str(score), True, BLACK) 
    window.blit(text,(320,330))
    pygame.display.update() 
    
    clock.tick(60)