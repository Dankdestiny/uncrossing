import pygame,random,math

#window size constants
row_num = 11
pin_size = 50
margin = 4*pin_size
width = 4*pin_size + margin
height = row_num*pin_size

#colours
BLUE,GREEN,RED = (50,50,200),(50,200,50),(200,50,50)
YELLOW,WHITE,BLACK = (200,200,50),(200,200,200),(0,0,0)
GREY,BROWN,LIGHTBROWN = (100,100,100),(75,50,20),(150,75,30)

#initialise
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((width,height))
pygame.display.set_caption('Mastermind')
font = pygame.font.SysFont('arial', 18)
random.seed()

class GamePin():
    def __init__(self,col,row):
        self.col,self.row = col,row
        self.x,self.y = col*pin_size,row*pin_size   #x,y are the draw position in window
        self.colour = GREY
        self.update_image()
        game_grid[row][col] = self
    def update_image(self):
        image = pygame.Surface((pin_size,pin_size))
        image.fill(BROWN)
        image.set_colorkey(BROWN)
        c = int(pin_size/2),int(pin_size/2)         #center
        r = int(pin_size/3)                         #radius
        pygame.draw.circle(image,WHITE,c,r)
        pygame.draw.circle(image,self.colour,c,r-2)
        self.image = image
    def draw(self):                                 #blits image to window
        window.blit(self.image, (self.x,self.y))
class Button():
    def __init__(self,pos,size,text,function):
        self.pos,self.size,self.text,self.function = pos,size,text,function
        self.image = self.create_image()
        buttons.append(self)

    def create_image(self):
        size = self.size
        image = pygame.Surface(size)
        pygame.draw.rect(image, LIGHTBROWN, (2,2,size[0]-4,size[1]-4))
        text = font.render(self.text, True, BLACK)
        image.blit(text,(10,10))
        return image

    def draw(self):
        window.blit(self.image, self.pos)

def make_grid():
    for col in range(4):
        for row in range(row_num):
            GamePin(col,row)
def draw_grid():
    for col in range(4):
        for row in range(row_num):
            game_grid[row][col].draw()
def set_puzzle():
    for col in range(4):
        pin = game_grid[row_num-1][col]
        pin.colour = random.choice(game_colours)
        pin.update_image()
def change_colour(selected,colour):
    selected.colour = colour
    selected.update_image()
def next_turn(turn):
    for a in range(4):
        if game_grid[turn][a].colour == GREY:
            return False
    return True
def compare(turn):
    solution,guess = [],[]
    for i in range(4):
        solution.append(game_grid[row_num-1][i].colour)
        guess.append(game_grid[turn][i].colour)
    blacks = 0
    for i in [3,2,1,0]:
        if solution[i] == guess[i]:
            blacks += 1
            solution.pop(i)
            guess.pop(i)
    whites = 0
    for i in range(4-blacks):
        if solution[0] in guess:
            whites += 1
            guess.remove(solution[0])
        solution.pop(0)
    feedback(turn,blacks,whites)
    return blacks == 4
def feedback(turn,blacks,whites):
    p,q = (int(4.2*pin_size),int((turn+0.25)*pin_size))
    answer = []
    for i in range(blacks):
        answer.append("black")
    for i in range(whites):
        answer.append("white")
    for i in range(4-blacks-whites):
        answer.append(False)
    for i in range(4):
        s = int(pin_size/10)
        d = int(pin_size/4)
        x = d*(i%2)
        y = d*math.floor(i/2)
        if answer[i] == "black":
            pygame.draw.circle(background,BLACK,(p+x,q+y),s)
        elif answer[i] == "white":
            pygame.draw.circle(background,WHITE,(p+x,q+y),s)
def new_game():
    make_grid()
    set_puzzle()
    global turn
    turn = 0
    global solved
    solved = False
    global background
    background = pygame.Surface((width,height))
    background.fill(BROWN)
    for i in range(len(game_colours)):
        x_offset = pin_size*int(i%3)
        y_offset = pin_size*math.floor(i/3)
        x,y = 5*pin_size,3*pin_size
        s = int(pin_size/3)
        pygame.draw.circle(background,WHITE,(x+x_offset,y+y_offset),s)
        pygame.draw.circle(background,game_colours[i],(x+x_offset,y+y_offset),s-2)

        text = font.render(str(i+1), True, GREY)
        background.blit(text,(x+x_offset-5,y+y_offset-10))



#game variables
game_grid = [[False for a in range(4)] for b in range(row_num)]
buttons = []
game_colours = BLUE,GREEN,RED,YELLOW,WHITE,BLACK
selected_pin = False
cover = pygame.Surface((4*pin_size,pin_size))

#buttons
Button((5*pin_size,10),(3*pin_size-10,40),"New Game",new_game)

new_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            selected_pin = False
            x,y = pygame.mouse.get_pos()
            col,row = math.floor(x/50),math.floor(y/50)
            if 0 <= col < 4 and row == turn:
                selected_pin = game_grid[row][col]
            for button in buttons:
                if button.pos[0] < x < button.pos[0] + button.size[0] and \
                button.pos[1] < y < button.pos[1] + button.size[1]:
                    button.function()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                change_colour(selected_pin,GREY)
            if 49 <= event.key <= 54 and selected_pin:
                change_colour(selected_pin,game_colours[event.key-49])
            if event.key == pygame.K_SPACE:
                if next_turn(turn):
                    if compare(turn) or turn == 9:
                        solved = True
                    turn += 1
                    if selected_pin:
                        selected_pin = False

    window.blit(background,(0,0))
    for button in buttons:
        button.draw()
    draw_grid()
    if selected_pin: 
        c = int(pin_size/2+selected_pin.x),int(pin_size/2+selected_pin.y)         
        r = int(pin_size/3)                         
        pygame.draw.circle(window,RED,c,r)
        pygame.draw.circle(window,selected_pin.colour,c,r-2)
        
    if not solved:
        window.blit(cover,(0,pin_size*(row_num-1)))
    pygame.display.update()
    clock.tick(60)
