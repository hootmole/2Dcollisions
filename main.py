import pygame 
import math

pygame.init() 



width, height = (600, 600)
win = pygame.display.set_mode((width, height)) 

pygame.display.set_caption("BRUH") 
clock = pygame.time.Clock() 


def reverseY(val):
    if type(val) == type(1) or type(val) == type(1.0): # int or float
        return height - val
    else:
        return [val[0], height - val[1]]


def sum(v1, v2):
    v = []
    for i in range(len(v1)):
        v.append(v1[i] + v2[i])
    return v

def product(v1, v2):
    v = []
    for i in range(len(v1)):
        v.append(v1[i] * v2[i])
    return v

def vector_lenght(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2)


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
        pygame.draw.circle(self.win, self.color, reverseY(self.pos), self.size)



class Brick:
    def __init__(self, pos, static_mesh: Mesh, isAlive: bool, color, win) -> None:
        self.pos = pos
        self.isAlive = isAlive
        self.color = color
        self.win = win
        self.static_mesh = static_mesh
        self.distance_to_ball = None
        self.ball_collision_point = None
        self.slope_angles = []

    def draw(self):
        if self.isAlive:
            vertex_table = self.static_mesh.vertex_table
            for edge_index in range(len(vertex_table)):
                pygame.draw.line(self.win, self.color, reverseY(sum(vertex_table[edge_index - 1], self.pos)), reverseY(sum(vertex_table[edge_index], self.pos)))


    def handle_collision(self, ball: Ball):
        vertex_table = self.static_mesh.vertex_table

        ball_collisions_points_list = []
        distances_to_ball = []
        self.slope_angles = []

        for edge_index in range(len(vertex_table)):
            # assign 2 working vertexes, assuming that 2 vertexes next to each other in vertex table are connected with edge that is linear function
            vertex1 = sum(vertex_table[edge_index - 1], self.pos) # P1
            vertex2 = sum(vertex_table[edge_index], self.pos) # P2

            d_vertex_x = vertex2[0] - vertex1[0]
            d_vertex_y = vertex2[1] - vertex1[1]

            vertex_distance = math.sqrt(d_vertex_x ** 2 + d_vertex_y ** 2)

            # if d_vertex_x is zero (vertexes are above each other) set the slope angle to pi/2 (90deg)
            # if d_vertex_x == 0:
            #     slope_angle = math.pi / 2
            # else:
            #     slope_angle = math.atan2(d_vertex_y, d_vertex_x)

            slope_angle = math.atan2(d_vertex_y, d_vertex_x)

            self.slope_angles.append(slope_angle)

            distance = math.cos(slope_angle) * (vertex1[1] - ball.pos[1]) - math.sin(slope_angle) * (vertex1[0] - ball.pos[0])

            x_distance_to_collision_point = math.sin(-slope_angle) * distance
            y_distance_to_collision_point = math.cos(-slope_angle) * distance

            # set values for every edge
            ball_collisions_points_list.append(sum(ball.pos, [x_distance_to_collision_point, y_distance_to_collision_point]))
            distances_to_ball.append(abs(distance))
        
        # find the smallest edge distance and use the values
        distance_to_ball = min(distances_to_ball)
        working_edge = distances_to_ball.index(distance_to_ball) # edge that is colliding with ball
        
        working_slope_angle = self.slope_angles[working_edge]
        self.ball_collision_point = ball_collisions_points_list[working_edge] 


        # collision handeling part
        velocity = ball.vel
        
        if distance_to_ball <= ball.size: 
            # check if colliding
            normal_vector_angle = working_slope_angle + math.pi / 2
            normal_vector = [math.cos(normal_vector_angle), math.sin(normal_vector_angle)]

            dot = velocity[0] * normal_vector[0] + velocity[1] * normal_vector[1]

            #R=V−2N(V⋅N)
            bounce_vector = sum(
                velocity, [-dot * normal_vector[0] * 2, -dot * normal_vector[1] * 2])

            ball.vel = bounce_vector


    def draw_normal_vector(self, lenght, win):
        vertex_table = self.static_mesh.vertex_table

        for edge_index in range(len(self.static_mesh.vertex_table)):

            vertex1 = sum(vertex_table[edge_index - 1], self.pos) # P1
            vertex2 = sum(vertex_table[edge_index], self.pos) # P2

            normal_angle = self.slope_angles[edge_index] + (math.pi / 2)

            normal_vector = [math.cos(normal_angle) * lenght, math.sin(normal_angle) * lenght]
            origin = [
                (vertex1[0] + vertex2[0]) / 2,
                (vertex1[1] + vertex2[1]) / 2,
            ]

            normal_vector_left = sum(normal_vector, origin)
            normal_vector_right = sum([-normal_vector[0], -normal_vector[1]], origin)

            pygame.draw.line(win, "orange", reverseY(normal_vector_left), reverseY(normal_vector_right), 1)






line = Mesh([
    [-100, 200],
    [177, -200],
    ])

square = Mesh([
    [-100, 100],
    [100, 100],
    [100, -100],
    [-100, -100],
])

walls_mesh = Mesh([
    [1, height - 1],
    [width - 1, height - 1],
    [width - 1, 1],
    [1, 1],
])


ball = Ball([30, 300], [1, 2.0], 10, [0, 0, 255], win)
brick = Brick([width / 2, height / 2], line, True, "yellow", win)
walls = Brick([0, 0], walls_mesh, True, "white", win)

run = True
FPS = 60

acceleration = 1
friction = 0.01
font = pygame.font.Font(None, 25)


y = 0

while run:
    clock.tick(FPS)
    start_time = pygame.time.get_ticks()

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            run = False
            break
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            ball.vel[1] += acceleration

        if keys[pygame.K_a]:
            ball.vel[0] += -acceleration

        if keys[pygame.K_s]:
            ball.vel[1] += -acceleration

        if keys[pygame.K_d]:
            ball.vel[0] += acceleration

        # if not (keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]):
        #     ball.vel = sum(ball.vel, product(ball.vel, [-friction, -friction]))

        # if keys[pygame.K_w]:
        #     ball.vel = sum(ball.vel, [0, acceleration])

        # if keys[pygame.K_a]:
        #     ball.vel = sum(ball.vel, [-acceleration, 0])

        # if keys[pygame.K_s]:
        #     ball.vel = sum(ball.vel, [0, -acceleration])

        # if keys[pygame.K_d]:
        #     ball.vel = sum(ball.vel, [acceleration, 0])

    # ball.vel = sum(ball.vel, product(ball.vel, [-friction, -friction]))

        
            

    
    win.fill((0, 0, 0)) 
    
    ball.draw()

    brick.draw()
    brick.handle_collision(ball)
    brick.draw_normal_vector(30, win)

    walls.draw()
    walls.handle_collision(ball)
    walls.draw_normal_vector(30, win)


    # draw fps counter
    end_time = pygame.time.get_ticks()  # Get the end time of the frame
    delta_time = end_time - start_time

    fps_text = font.render("FPS: {:.2f}".format(clock.get_fps()), True, (255, 255, 255) if clock.get_fps() > FPS else (255, 0, 0))
    win.blit(fps_text, (10, 10)) 

    single_frame_delay_time_text = font.render("Δt: {:.0f} ms".format(delta_time), True, (255, 255, 255))
    win.blit(single_frame_delay_time_text, (10, 30)) 


    # testing
    pygame.draw.line(win, "green", reverseY(ball.pos), reverseY(walls.ball_collision_point))
    pygame.draw.circle(win, "white", reverseY(walls.ball_collision_point), 2)

    pygame.draw.line(win, "green", reverseY(ball.pos), reverseY(brick.ball_collision_point))
    pygame.draw.circle(win, "white", reverseY(brick.ball_collision_point), 2)


    y += 1.5
    #brick.static_mesh.vertex_table[1] = [y, brick.static_mesh.vertex_table[1][0]]

    if y > height:
        y = 0



    pygame.display.update() 
    
    
    


pygame.quit() 
