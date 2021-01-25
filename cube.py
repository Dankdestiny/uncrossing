import pygame
from math import sin,cos,tan,asin,acos,atan,pi

#set up our playing screen
pygame.init()
screen_size = 500
window = pygame.display.set_mode((screen_size,screen_size))
pygame.display.set_caption('3D Game')
clock = pygame.time.Clock()

#variables of colour
BLUE,RED,GREY,BLACK,ORANGE = (50,50,255),(200,50,50),(155,155,155),(0,0,0),(255,165,0)
YELLOW,CYAN,PURPLE,GREEN = (255,255,50),(50,255,255),(200,0,200),(0,200,0)

class Vertex():
    def __init__(self,x,y,z):
        self.x,self.y,self.z = x,y,z
        self.image = self.create_image()
        vertices.append(self)
        
    def create_image(self): #returns rectangle for vertex
        image = pygame.Surface((4,4))
        image.fill(BLACK)
        return image
    
    def draw(self):
        self.screen_pos = self.find_screen_position()
        window.blit(self.image,self.screen_pos)
        
    def find_screen_position(self):
        #vector from camera to self
        camera_to_self = [self.x-camera.x , self.y-camera.y , self.z-camera.z]
        
        #how far self is in the direction of camera
        z = scalar_product(camera_to_self,camera.get_direction_vector())
        
        #the relative position self has on screen
        x = scalar_product(camera_to_self,camera.get_x_vector())
        y = scalar_product(camera_to_self,camera.get_y_vector())
        if z > 0:
            x /= z
            y /= z
        elif z < 0:
            x *= z
            y *= z
        else:
            return screen_size,int(screen_size/2)
            
        #take relative position and fits it to the window
        screen_x = int((x + 1/2)*screen_size)
        screen_y = int((-y + 1/2)*screen_size)
        return screen_x,screen_y
    
    def move(self,x,y,z):
        self.x += x
        self.y += y
        self.z += z
    
class Orientable(Vertex): #a vertex with a direction
    
    def __init__(self,x,y,z,theta=0,phi=0):
        super().__init__(x,y,z)
        self.theta,self.phi = theta,phi
        #theta is the angle in the xy plane
        #phi is the angle from the xy plane
    
    def get_direction_vector(self): #returns direction as a unit vector
        x = cos(self.theta)*cos(self.phi)
        y = sin(self.theta)*cos(self.phi)
        z = sin(self.phi)
        return [x,y,z]
    '''the angle of the projection of the camera direction vector in the xy plane
    after being rotated 90 degrees clockwise'''    
    def get_x_vector(self): 
        x = cos(self.theta+(pi/2))
        y = sin(self.theta+(pi/2))
        z = 0
        return [x,y,z]
    '''the angle of the camera direction vector after being rotated 90 degrees 
    '''    
    def get_y_vector(self):
        x = cos(self.theta)*cos(self.phi+(pi/2))
        y = sin(self.theta)*cos(self.phi+(pi/2))
        z = sin(self.phi+(pi/2))
        return [x,y,z]
        
    def rotate(self,move):
        x,y = move
        x *= -0.002
        y *= -0.002
        self.theta += x
        self.phi += y
    
class Polygon():

    def __init__(self,corners,colour):
        self.corners = []
        for corner in corners:
            self.corners.append(corner)
        self.colour = colour
        polygons.append(self)
        
    def find_distance(self): #sets self.distance to the average distance from camera
        found = 0
        corner_number = 0
        for corner in self.corners:
            corner_pos = corner.x,corner.y,corner.z
            camera_pos = camera.x,camera.y,camera.z
            vect = []
            for a in [0,1,2]:
                vect.append(corner_pos[a]-camera_pos[a])
            distance = (vect[0]**2 + vect[1]**2 + vect[2]**2)**0.5
            found += distance
            corner_number += 1
        found /= corner_number
        self.distance = found
        
    def draw(self):
        draw_corners = []
        for corner in self.corners:
            draw_corners.append(corner.screen_pos)
            
        pygame.draw.polygon(window, self.colour, draw_corners)

def scalar_product(a,b): #shows how far a moves in the direction of b
    ans = 0
    for i in [0,1,2]:
        ans += a[i] * b[i]
    return ans

def sort(group): #sorts polygons into order by distance
    #item is the list of objects, value is the criteria we are sorting by
    for p in group:
        p.find_distance()
    #order elements of group by distance, descending order
    length = len(group)
    for a in range(0,length-2):
        for b in range(0,length-1-a):
            if group[b].distance < group[b+1].distance:
                group[b],group[b+1] = group[b+1],group[b]

def make_a_square(x,y,z):
    new_vertices = []
    for c in [-5,5]:
        for a in [-5,5]:
            for b in [-5,5]:
                new_vertices.append(Vertex(x+a,y+b,z+c))
       
    Polygon([new_vertices[0],new_vertices[1],new_vertices[3],new_vertices[2]],ORANGE)
    Polygon([new_vertices[4],new_vertices[5],new_vertices[7],new_vertices[6]],YELLOW)
    Polygon([new_vertices[0],new_vertices[1],new_vertices[5],new_vertices[4]],RED)
    Polygon([new_vertices[1],new_vertices[3],new_vertices[7],new_vertices[5]],BLUE)
    Polygon([new_vertices[2],new_vertices[3],new_vertices[7],new_vertices[6]],GREEN)
    Polygon([new_vertices[0],new_vertices[2],new_vertices[6],new_vertices[4]],BLACK)


vertices,polygons = [],[]
camera = Orientable(50,0,0)

'''for a in range(-1,2):
    for b in range(-1,2):
        make_a_square(100,30*a,30*b)'''

make_a_square(100,0,0)





run,strafe = 0,0 #variables used to calculate run direction
forward,back,left,right = 0,0,0,0
up = 0
mouse_down = False
while True:
    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mouse.get_rel()
            mouse_down = True
            
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
            
        if event.type == pygame.MOUSEMOTION:
            if mouse_down:
                x,y = pygame.mouse.get_rel()
                camera.rotate((x,-y))
            
        if event.type == pygame.KEYDOWN: #control camera movement
            if event.key == pygame.K_w:
                forward = 1
            if event.key == pygame.K_s:
                back = 1
            if event.key == pygame.K_a:
                left = 1
            if event.key == pygame.K_d:
                right = 1
            if event.key == pygame.K_SPACE:
                up = 1
        if event.type == pygame.KEYUP: #ditto
            if event.key == pygame.K_w:
                forward = 0
            if event.key == pygame.K_s:
                back = 0
            if event.key == pygame.K_a:
                left = 0
            if event.key == pygame.K_d:
                right = 0
            if event.key == pygame.K_SPACE:
                up = 0
    
    run = forward - back
    strafe = right - left
    if run:
        x,y,z = camera.get_direction_vector()
        x *= run
        y *= run
        z *= run
        camera.move(x,y,z)
    if strafe:
        x,y,z = camera.get_x_vector()
        x *= strafe
        y *= strafe
        z *= strafe
        camera.move(x,y,0)
    if up:
        camera.move(0,0,1)
    
    #update visuals
    window.fill(GREY)
    
    sort(polygons)
    for p in vertices + polygons:
        p.draw()
    pygame.display.update()
    
    clock.tick(60)
    