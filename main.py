import pygame 


pygame.init() 



width, height = (600, 600)
win = pygame.display.set_mode((width, height)) 

pygame.display.set_caption("BRUH") 

x = 200
y = 200


def sum(v1, v2):
    v = []
    for i in range(len(v1)):
        v.append(v1[i] + v2[i])
    return v


class Mesh:
    def __init__(self, vertex_table) -> None:
        self.vertex_table = vertex_table



class Ball:
    def __init__(self, pos, vel, size, color, win): 
        self.pos = pos
        self.vel = vel
        self.size = size
        self.color = color
        self.win = win
        
    def draw(self):
        self.pos = sum(self.pos, self.vel)
        pygame.draw.circle(self.win, self.color, self.pos, self.size)
    
                    

class Brick:
    def __init__(self, pos, static_mesh, isAlive, color, win) -> None:
        self.pos = pos
        self.isAlive = isAlive
        self.color = color
        self.win = win
        self.static_mesh = static_mesh

    def draw(self):
        if self.isAlive:

            pygame.draw.rect(self.win, self.color, pygame.Rect(
                self.static_mesh.vertex_table[0][0], 
                self.static_mesh.vertex_table[0][1],
                self.static_mesh.vertex_table[1][0] - self.static_mesh.vertex_table[0][0],
                self.static_mesh.vertex_table[1][1] - self.static_mesh.vertex_table[0][1] + 2,
            ))

    def calculate_edge_distances_to_ball(self, ball):
        vertex_table = self.static_mesh.vertex_table

        for edge_index in range(len(self.static_mesh.vertex_table) - 1):
            # assign 2 working vertexes, assuming that 2 vertexes next to each other in vertex table are connected with edge that is linear function
            vertex1 = sum(vertex_table[edge_index], self.pos) # P1
            vertex2 = sum(vertex_table[edge_index + 1], self.pos) # P2

            d_vertex_x = vertex2[0] - vertex1[0]
            d_vertex_y = vertex2[1] - vertex1[1]

            d_H_x = vertex2[0] - ball.pos[0]
            d_H_y = vertex1[1] - ball.pos[1]

            # calculate the slope (DOES NOT WORK WHEN d_vertex_x == 0)
            if (vertex2[0] - vertex1[0]) == 0:
                slope = 0
            else:
                slope = (vertex2[1] - vertex1[1]) / (vertex2[0] - vertex1[0])

            
            
            point_x_distance = d_vertex_x - d_H_x - (d_H_y / slope)  # a
            point_y_distance = d_vertex_y - d_H_y - (d_H_x * slope)  # b






line = Mesh([
    [100, 100],
    [400, 100],
    ])

ball = Ball([200, 500], [0, -0.1], 10, [255, 0, 255], win)
brick = Brick([200, 200], line, True, "yellow", win)

run = True

while run:
    win.fill((0, 0, 0)) 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            run = False
            break
    
    
    ball.draw()
    brick.draw()
    pygame.display.update() 
    


pygame.quit() 
