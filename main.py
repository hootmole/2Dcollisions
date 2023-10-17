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
        self.slope_angle = None

    def draw(self):
        if self.isAlive:
            vertex_table = self.static_mesh.vertex_table
            for edge_index in range(len(self.static_mesh.vertex_table) - 1):
                pygame.draw.line(self.win, self.color, reverseY(sum(vertex_table[edge_index], self.pos)), reverseY(sum(vertex_table[edge_index + 1], self.pos)))
            # finish by connecting the first and last vertex
            pygame.draw.line(self.win, self.color, reverseY(sum(vertex_table[0], self.pos)), reverseY(sum(vertex_table[-1], self.pos)))

    def calculate_ball_collision_point(self, ball: Ball):
        vertex_table = self.static_mesh.vertex_table

        ball_collisions_points_list = []
        distances_to_ball = []

        for edge_index in range(len(self.static_mesh.vertex_table)):
            # assign 2 working vertexes, assuming that 2 vertexes next to each other in vertex table are connected with edge that is linear function
            vertex1 = sum(vertex_table[edge_index - 1], self.pos) # P1
            vertex2 = sum(vertex_table[edge_index], self.pos) # P2

            d_vertex_x = vertex2[0] - vertex1[0]
            d_vertex_y = vertex2[1] - vertex1[1]

            vertex_distance = math.sqrt(d_vertex_x ** 2 + d_vertex_y ** 2)
            slope_angle = math.atan2(d_vertex_y, d_vertex_x) # alpha
            self.slope_angle = slope_angle

            distance = math.cos(slope_angle) * (vertex1[1] - ball.pos[1]) - math.sin(slope_angle) * (vertex1[0] - ball.pos[0])

            x_distance_to_collision_point = math.sin(-slope_angle) * distance
            y_distance_to_collision_point = math.cos(-slope_angle) * distance

            # set values for every edge
            ball_collisions_points_list.append(sum(ball.pos, [x_distance_to_collision_point, y_distance_to_collision_point]))
            distances_to_ball.append(abs(distance))
        
        # find the smallest edge distance and use the values
        smallest_distance = min(distances_to_ball)
        smallest_distance_index = distances_to_ball.index(smallest_distance)

        self.distance_to_ball = smallest_distance
        self.ball_collision_point = ball_collisions_points_list[smallest_distance_index] 


        

    def handle_collision(self, ball: Ball):
        self.calculate_ball_collision_point(ball)
        velocity = ball.vel

        # check if colliding
        if self.distance_to_ball <= ball.size:
            # rotate velocity vector by slope angle of function at collision point
            # mirror y axis by multiplying y value by -1
            #
            normal_vector_angle = self.slope_angle + math.pi / 2
            normal_vector = [math.cos(normal_vector_angle), math.sin(normal_vector_angle)]

            dot = velocity[0] * normal_vector[0] + velocity[1] * normal_vector[1]
            
            #R=V−2N(V⋅N)
            bounce_vector = sum(
                velocity, [-dot * normal_vector[0] * 2, -dot * normal_vector[1] * 2])

            ball.vel = bounce_vector







line = Mesh([
    [-200, 200],
    [200, -200],
    ])

walls_mesh = Mesh([
    [1, height - 1],
    [width - 1, height - 1],
    [width - 1, 1],
    [1, 1]
])

ball = Ball([30, 300], [2, 2.0], 10, [0, 0, 255], win)
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
    walls.draw()
    walls.handle_collision(ball)
    brick.calculate_ball_collision_point(ball)
    brick.handle_collision(ball)

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
    # brick.static_mesh.vertex_table[1] = [brick.static_mesh.vertex_table[1][0], y]

    if y > height:
        y = 0



    pygame.display.update() 
    
    
    


pygame.quit() 
