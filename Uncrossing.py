import pygame,random
from math import sin,cos,pi,ceil,floor

#initalise
pygame.init()
screen_size = 500
window = pygame.display.set_mode((screen_size,screen_size))
pygame.display.set_caption('Uncrossing')
clock = pygame.time.Clock()
random.seed()

#lists
all_nodes,all_edges = [],[]

#constants
GREY,YELLOW,BLACK,RED = (155,155,155),(255,255,50),(0,0,0),(255,50,50)

class Node():
    
    def __init__(self,x,y):
        self.x,self.y = x,y #coordinates of self
        self.adj = [] #set of nodes that self is connected to by an Edge
        
        self.image = self.create_image() #sets own image to a yellow dot
        
        all_nodes.append(self) 
        
    def create_image(self): #returns an image of a yellow dot
        image = pygame.Surface((20,20))
        #make the surface background transparent
        image.fill(GREY)
        image.set_colorkey(GREY) 
        #draw a yellow dot with a black outline
        pygame.draw.circle(image, BLACK, (10,10), 10)
        pygame.draw.circle(image, YELLOW, (10,10), 8) 
        
        return image
    def draw(self): #draws image centered at self position
        window.blit(self.image, (self.x-10,self.y-10))
        
    def move(self,x,y): #moves self position by x,y, but won't go outside game space
        self.x += x
        self.y += y
        
        if self.x < 25:
            self.go_to(25,self.y)
        if self.x > 475:
            self.go_to(475,self.y)
            
        if self.y < 25:
            self.go_to(self.x,25)
        if self.y > 475:
            self.go_to(self.x,475)
    def go_to(self,x,y):
        self.x,self.y = x,y
    
class Edge():
    
    def __init__(self,start,end):
        self.start,self.end = start,end #start, end are nodes 
        self.colour = BLACK
        
        #ammends the adjacent's list of start,end to include each other
        start.adj.append(end) 
        end.adj.append(start) 
        
        all_edges.append(self)
        
    def draw(self): #draws a line from start position to end position
        pygame.draw.line(window, self.colour, (self.start.x,self.start.y), \
        (self.end.x,self.end.y), 3)
        
    #returns True iff crossing another edge,
    #if True, set colour to RED, else set colour to BLACK
    def crossing(self): 
        for edge in all_edges:
            if edge != self:
                self_start = self.start.x,self.start.y
                self_end = self.end.x,self.end.y
                edge_start = edge.start.x,edge.start.y
                edge_end = edge.end.x,edge.end.y
                
                if are_lines_crossing(self_start,self_end,edge_start,edge_end):
                    self.colour = RED
                    return True
        self.colour = BLACK
        return False

def get_distance(a,b): #get distance between position a to b
    
    x = a[0] - b[0]
    y = a[1] - b[1]
    return (x**2 + y**2)**0.5
def are_lines_crossing(a,b,c,d): #returns True iff ab crosses cd
    
    #if both lines share a start or end point, assume no crossing
    if a == c or a == d or b == c or b == d:
        return False
    '''
    We have two lines, a->b and c->d. We represent each line algebraically as
    a(1-t) + bt, and c(1-s) + ds, where 
    a,b,c,d are constant vectors, and
    0 <= t,s <= 1,
    
    the lines intersect if there exist values of t,s between 0,1 such that
    a(1-t) + bt = c(1-s) + ds
    
    rearranging gives us:
    a(1-t) + bt - c(1-s) - ds = 0
    (a - c) + t(b - a) + s(c - d)
    
    giving us simultaneous equations between the x and y components:
    (a[0] - c[0]) + t(b[0] - a[0]) + s(c[0] - d[0]) = 0
    (a[1] - c[1]) + t(b[1] - a[1]) + s(c[1] - d[1]) = 0
    '''
    x_1 = a[0] - c[0]
    y_1 = b[0] - a[0]
    z_1 = c[0] - d[0]
    
    x_2 = a[1] - c[1]
    y_2 = b[1] - a[1]
    z_2 = c[1] - d[1]
    '''
    which we have rewritten as:
    (x_1) + t(y_1) + s(z_1) = 0         (1)
    (x_2) + t(y_2) + s(z_2) = 0         (2)
    
    then we solve the simultaneous equation
    '''
    if z_1 != 0:
        '''
        If we can divide by z_1:
        let m = z_2 / z_1
        multiply both sides of (1) by m:   
        
            (x_1) + t(y_1) + s(z_1) = 0
            m*(x_1) + m*t(y_1) + m*s(z_1) = 0
            m*(x_1) + m*t(y_1) + s(z_2) = 0         (3)
        
        subtract both sides of (2) from (3):
            
            m*(x_1) + m*t(y_1) + s(z_2) - {(x_2) + t(y_2) + s(z_2)} = 0 - 0
            m*(x_1) + m*t(y_1) - {(x_2) + t(y_2)} = 0
            (m*(x_1) - (x_2)) + t(m*y_1 - (y_2)) = 0        (4)
        '''
        m = z_2 / z_1
        if m*y_1 - y_2 != 0:
            '''
            If we can divide by m*y_1 - (y_2)
            then we can rearrange (4):
            
                (m*(x_1) - (x_2)) + t(m*y_1 - (y_2)) = 0        (5)
            =>  t(m*y_1 - (y_2)) = -(m*(x_1) - (x_2))
            =>  t = -(m*(x_1) - (x_2))/(m*y_1 - (y_2))
            =>  t = ((x_2) - m*x_1))/(m*y_1 - (y_2))
            
            we can substitute t into (1) and rearrange:
            
                (x_1) + t(y_1) + s(z_1) = 0
            =>  s(z_1) = -((x_1) + t(y_1))
            =>  s = -((x_1) + t(y_1))/(z_1)   (because z_1 is non zero)
            '''
            t = (x_2 - m*x_1)/(m*y_1 - y_2)
            s = -(x_1 + y_1*t)/z_1
        else: 
            '''
            If m*y_1 - (y_2) == 0 then we substitute into (5):
                
                (m*(x_1) - (x_2)) + t(m*y_1 - (y_2)) = 0
                (m*(x_1) - (x_2)) + t*0 = 0
                (m*(x_1) - (x_2)) = 0
                
            if (m*(x_1) - (x_2)) is non zero then there is a contradiction
            and there can be no value of t,s that satisfies the required conditions
            
            if it is 0 then the equation can be satisfied
            '''
            return m*x_1 - x_2 == 0
            
    elif z_2 != 0:
        #Similar to above
        m = z_1 / z_2
        if m*y_2 - y_1 != 0:
            t = (x_1 - m*x_2)/(m*y_2 - y_1)
            s = -(x_2 + y_2*t)/z_2
        else:
            return m*x_2 - x_1 == 0
    
    else:
        '''
        If both z_1 and z_2 are 0, then substituting into (1) and (2) gives
        
            (x_1) + t(y_1) + s(z_1) = 0
            (x_2) + t(y_2) + s(z_2) = 0
        
            (x_1) + t(y_1) = 0          (6)
            (x_2) + t(y_2) = 0          (7)
            
            as we can see, s has no effect on this equation, so as long as there
            is a value of t that satisfies the condition, then the lines cross.
            We shall give s an arbitrary value to avoid any exceptions
        '''
        s = 0
        if y_1 != 0 and y_2 != 0:
            '''
            if both y_1 and y_2 are non zero, then t must satisfy both (6) and (7):
            
                (x_1) + t(y_1) = 0 
            =>  t = -(y_1)/(x_1)
            
                (x_2) + t(y_2) = 0 
            =>  t = -(y_2)/(x_2)
            
            =>  t = -(y_1)/(x_1) = -(y_2)/(x_2)     (8)
            
            if (8) is met and t is between 0 and 1 then the lines cross
            '''
            return (0 <= -x_1/y_1 == -x_2/y_2 <= 1)
            
        elif y_1 == 0 and y_2 == 0:
            '''
            if both y_1 and y_2 are zero, (6) and (7) imply:
                
                (x_1) = 0
                (x_2) = 0
                
            return True if this is the case                
            '''
            return (x_1 == 0 and x_2 == 0)
        else: 
            #this block covers the case where exactly one of y_1 or y_2 is 0
            if y_1 == 0:
                '''
                    If y_1 = 0 then by (6) and (7) we have
                    
                        (x_1) = 0       (9)
                        (x_2) + t(y_2) = 0          (10)
                        
                    return False if (9) is not met.
                    assign t a value if (10) can be satisfied
                '''
                if x_1 != 0:
                    return False
                t = -y_2/x_2
                
            else: 
                #similar to above
                if x_2 != 0:
                    return False
                t = -y_1/x_1
        
    #if t and s have values between 0,1 then the lines cross
    return (0 <= t <= 1 and 0 <= s <= 1)
def new_graph(difficulty): #creates new puzzle, number of nodes equal to difficulty
    
    #creates a node on each corner
    Node(0,0), Node(0,500), Node(500,500), Node(500,0)
    
    #connects the nodes with a loop around the edge of the window
    for a in range(len(all_nodes)):
        Edge(all_nodes[a-1],all_nodes[a])
        
    #add new nodes and link them to all existing and valid nodes    
    for a in range(difficulty):
        #make a new node, positioned randomly
        new_node = Node(random.randint(150,350),random.randint(150,350))
        
        a = new_node.x,new_node.y #pos of new node
        
        valid_nodes = [] #set of nodes with a clear path from node to new_node
        for node in all_nodes[:-1]: #for every node except the new one
            b = node.x,node.y #pos of node
            
            #if the line from node to new_node doesn't cross an edge, then valid
            valid = True
            for edge in all_edges: #check all edges
                c = edge.start.x,edge.start.y #pos of edge start
                d = edge.end.x,edge.end.y #pos of edge end
                if are_lines_crossing(a,b,c,d):
                    valid = False #if there is a crossing, valid = False
                    break
            if valid: #if no crossing, add to valid nodes
                valid_nodes.append(node)
                    
        for node in valid_nodes: #connect all valid nodes
            Edge(node,new_node)
            
    for node in all_nodes: #shuffles all the nodes
        x,y = random.randint(25,screen_size-25),random.randint(25,screen_size-25)
        node.go_to(x,y)
def delete_graph(): #deletes all nodes and edges
    
    while len(all_edges):
        edge = all_edges.pop(0)
        del(edge)
    while len(all_nodes):
        node = all_nodes.pop(0)
        del(node)

#variables
difficulty = 1 #controls the number of nodes that spawn
solved = False #True when the current graph has no crossings
dragged_node = False #reference of the node currently being dragged

new_graph(difficulty)

while True:
    for event in pygame.event.get():
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: #if graph is solved, make a harder one
                if solved:
                    delete_graph()
                    difficulty += 1
                    new_graph(difficulty)
        
        if event.type == pygame.MOUSEBUTTONDOWN: #select node if mouse is over one
            x,y = pygame.mouse.get_pos()
            for node in all_nodes: #check all node
                distance = get_distance((x,y),(node.x,node.y)) 
                if distance < 10: #if mouse is on a node
                    dragged_node = node #select node
                    pygame.mouse.get_rel()
                    '''get rel is the distance between current mouse pos, and 
                    the location at which this function was last called. We want
                    to reset the value of get rel to the current position of mouse'''
                    break
        
        if event.type == pygame.MOUSEBUTTONUP: #deselect node
            dragged_node = False
            
        if event.type == pygame.MOUSEMOTION and dragged_node: #moves current node
            x,y = pygame.mouse.get_rel() #x,y equals change in mouse position
            dragged_node.move(x,y) #moves node equal to movement from mouse
    
    solved = True
    for item in all_edges: #checks all edges for crossings
        if item.crossing(): #if there is a crossing, game is unsolved
            solved = False
    
    #update visuals
    window.fill(GREY)
    for item in all_edges + all_nodes:
        item.draw()
    pygame.display.update()
    
    clock.tick(60)




