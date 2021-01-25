import pygame
from math import floor
from itertools import combinations

#initialise pygame
pygame.init()
window = pygame.display.set_mode((560,560))
pygame.display.set_caption('Sudoku Solver')
large_font = pygame.font.SysFont('arial', 30)
small_font = pygame.font.SysFont('arial', 12)
clock = pygame.time.Clock()
WHITE,BLUE,RED,GREY,BLACK = (255,255,255),(50,50,255),(255,50,50),(155,155,155),(0,0,0)

class Cell():

    def __init__(self,position): #initialises pos,value,candidates
        self.position = position
        self.value = False
        self.candidates = [1,2,3,4,5,6,7,8,9]
        
    def draw(self):
        x,y = self.position
        if self.value:
            draw_position = [112+40*x,104+40*y]
            text = large_font.render(str(self.value), True, BLACK)
            window.blit(text,draw_position)
        else:
            for cand in self.candidates:
                
                cand_x = 12*((cand - 1) % 3)
                cand_y = 12*floor((cand-1)/3)
                
                draw_position = [105+40*x+cand_x,102+40*y+cand_y]
                text = small_font.render(str(cand), True, BLACK)
                window.blit(text,draw_position)
                
    def remove_candidate(self,value): #removes value from candidates if it exists
        if value in self.candidates:
            self.candidates.remove(value)
            return True
        return False
        
    def set_value(self,value):
        self.value = value
        self.candidates = []
        return True
        
class Button():

    def __init__(self,position,size,text,function,parameter):
        self.position,self.size,self.text = position,size,text
        self.function,self.parameter = function,parameter
        self.image = self.draw_button()
        buttons.append(self)
        
    def draw_button(self):
        button = pygame.Surface(self.size)
        pygame.draw.rect(button,WHITE,(0,0,self.size[0],self.size[1]))
        text = large_font.render(str(self.text), True, BLACK)
        button.blit(text,(4,4))
        return button     
        
    def call_function(self):
        self.function(self.parameter)

#returns the cells of the region specified
def get_row(y,grid):
    row = []
    for a in range(0,9):
        row.append(grid[a][y])
    return row
def get_col(x,grid):
    col = []
    for a in range(0,9):
        col.append(grid[x][a])
    return col
def get_box(pos,grid):
    x,y = pos    
    x,y = [3*floor(x/3),3*floor(y/3)]
    box = []
    for a in range(x,x+3):
        for b in range(y,y+3):
            box.append(grid[a][b])
    return box

#creates grid squares and selected box
def draw_sudoku_grid():
    grid = pygame.Surface((401,401))
    grid.fill(GREY)
    for a in range(0,361,40):
        if a % 120:
            width = 1
        else:
            width = 2
        pygame.draw.line(grid,BLACK,(a,0),(a,360),width)
        pygame.draw.line(grid,BLACK,(0,a),(360,a),width)
    return grid
def draw_selected_box():
    selected_box = pygame.Surface((41,41))
    pygame.draw.rect(selected_box,RED,(0,0,41,41),1)
    selected_box.set_colorkey(BLACK)
    return selected_box

def reset_grid(grid): 
    for a in range(0,9):
        for b in range(0,9):
            grid[a][b].value = False
            grid[a][b].candidates = [1,2,3,4,5,6,7,8,9] 
def make_empty_grid(): 
    grid = []
    for a in range(0,9):
        grid.append([])
        for b in range(0,9):
            grid[a].append(Cell([a,b]))
    return grid
def are_there_duplicates(region):
    found = []
    for cell in region:
        if cell.value in found:
            return True
        else:
            found.append(cell.value)
    return False  
def is_it_solved(grid): 
    grid_filled = True
    for a in range(0,9):
        for b in range(0,9):
            if not grid[a][b].value:
                grid_filled = False
              
    if grid_filled:
        grid_valid = True
        for a in range(0,9):
            region = get_row(a,grid)
            if are_there_duplicates(region):
                grid_valid = False
            region = get_col(a,grid)
            if are_there_duplicates(region):
                grid_valid = False
            box = (a%3,floor(a/3))
            region = get_box(box,grid)
            if are_there_duplicates(region):
                grid_valid = False
        if grid_valid:
            answer = "valid"
        else:
            answer = "not valid"
    else:
        answer = "not filled"
    print(answer)
    return answer
def user_input_value(position,value,grid): #enter value to cell and update all regions
    x,y = position
    cell = grid[x][y]
    if value in cell.candidates:
        cell.set_value(value)
    update_all_regions(grid)
def get_mouse_cell(mouse): #returns coords of the cell mouse is in
    x,y = mouse
    cell_x = floor((x-100)/40)
    cell_y = floor((y-100)/40)
    if 0 <= cell_x <= 8 and 0 <= cell_y <= 8:
        return cell_x,cell_y
def update_visuals():
    window.fill(GREY)
    window.blit(grid,(100,100)) #draws the grid squares
    for a in range(0,9): #draws contents of every cell
        for b in range(0,9):
            cells[a][b].draw()
    if selected: #draws an outline on the selected box
        window.blit(selected_box,(100+40*selected[0],100+40*selected[1]))
    for b in buttons: #draws all buttons
        window.blit(b.image,b.position)
    pygame.display.update()

#all the functions that try to solve the puzzle
def list_candidates(region): #returns all candidates that appear in region
    cand_list = []
    for cell in region:
        for cand in cell.candidates:
            if not cand in cand_list:
                cand_list.append(cand)
    return cand_list
def immediate_candidates(region):
    '''removes candidates whose region contains a cell with a value equal to it'''
    changed = False
    for a in region:
        for b in region:
            if a.value in b.candidates:
                changed = b.remove_candidate(a.value)
    return changed       
def open_n_ple(region,n):
    '''if n cells share the same n candidates, and no others, remove the 
    candidates within n cells from all other cells in region'''
    changed = False
    unsolved_cells = []
    for cell in region:
        if not cell.value:
            unsolved_cells.append(cell)
    
    pairs = [] #the list of all cells that have n candidates
    if len(unsolved_cells) > n:
        for a in unsolved_cells:
            if len(a.candidates) == n:
                pairs.append(a)

    combination_list = list(combinations(pairs,n)) #all combinations of 3 pairs
    for combo in combination_list:
        cands = []
        for a in range(0,n):
            cands.append(combo[a].candidates)
        #if combo[0].cand == combo[1].cand ...
        
        matching = True
        for a in range(0,n-1):
            if combo[a].candidates != combo[a+1].candidates:
                matching = False
                
        if matching:
            remove = combo[0].candidates
            for cell in unsolved_cells:
                valid_cell = True
                for a in range(0,n):
                    if cell == combo[a]:
                        valid_cell = False
                if valid_cell:
                    for a in remove:
                        if cell.remove_candidate(a):
                            changed = True
    return changed    
def hidden_singles(region):
    #if a candidate appears once in a region, set that cell value to candidate
    changed = False
    for number in range(1,10):
        occurances = 0
        for cell in region:
            if number in cell.candidates:
                occurances += 1
                hidden_single = cell
        if occurances == 1:
            changed = hidden_single.set_value(number)
    return changed     
def hidden_n_ple(region,n):
    '''
    we have a hidden n_ple in a given region if 
        there is a set of n number of candidates all of which: 
        appear in no cells except for a select n cells.
    if this condition is met, then all other candidates in these chosen cells
    can be deleted
    
    if a candidate appeared more than n times, it cannot be hidden, as it would appear
    in more than n cells, thus: we can make a set of candidates that only show
    in region up to n times. From this set we can create a list of all n combinations
    
    if, from searching region, we can find n cells that contain all appearences of 
    any set in combs, then remove all other 
    '''
    changed = False
    
    times_x_appears = [0]*9
    for cell in region:
        for candidate in cell.candidates: #for every time a candidate is in region
            times_x_appears[candidate-1] += 1
            
    potential_candidates = [] #candidates that could be part of a hidden n_ple
    for a in range(0,9):
        if times_x_appears[a] == n:
            potential_candidates.append(a+1)
            
    candidate_combinations = combinations(potential_candidates,n)
    #each element of this set is an n set of candidates
    for set in candidate_combinations:
        cells_that_have_candidate_in_set = []
        for cell in region:
            set_in_current_cell = False
            for candidate in set:
                if candidate in cell.candidates:
                    set_in_current_cell = True
                    break
            if set_in_current_cell:
                cells_that_have_candidate_in_set.append(cell)
                
        if len(cells_that_have_candidate_in_set) == n:
            for cell in cells_that_have_candidate_in_set:
                for candidate in range(1,10):
                    if not candidate in set:
                        changed = cell.remove_candidate(candidate)
    return changed    
def update_all_regions(grid):
    '''loop repeats until no changes are made
    the contents of the loop attempt to eliminate wrong answers, or find
    correct ones'''
    changed = True
    while changed == True:
        changed = False
        for a in range(0,9):
            row = get_row(a,grid)
            col = get_col(a,grid)
            box = get_box((3*(a%3),3*floor(a/3)),grid)
            for region in [row,col,box]:
                if immediate_candidates(region):
                    changed = True
                if hidden_singles(region):
                    changed = True
                for n in [2,3,4]:
                    if open_n_ple(region,n):
                        changed = True
                    if hidden_n_ple(region,n):
                        changed = True

def brute_force(grid):
    pass

grid = draw_sudoku_grid()
selected_box = draw_selected_box()
cells = make_empty_grid()

#creates the buttons
buttons = []
Button((100,40),(100,40),"Reset",reset_grid,cells)
Button((210,40),(130,40),"Solved?",is_it_solved,cells)
Button((350,40),(130,40),"Brute",brute_force,cells)

selected = False #holds coordinates of the currently selected cell
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN: #select cell or click button
            mouse = pygame.mouse.get_pos()
            selected = get_mouse_cell(mouse)
            x,y = mouse
            for b in buttons:
                if b.position[0] < x < b.position[0] + b.size[0] and \
                b.position[1] < y < b.position[1] + b.size[1]:
                    b.function(b.parameter)
        if event.type == pygame.KEYDOWN: #inputs a value into a cell
            if selected: 
                if 49 <= event.key <= 57:
                    user_input_value(selected,event.key-48,cells)
                    
    update_visuals()
    clock.tick(60)