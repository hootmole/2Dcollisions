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

        for edge_index in range(len(self.static_mesh.vertex_table) - 1):
            # assign 2 working vertexes, assuming that 2 vertexes next to each other in vertex table are connected with edge that is linear function
            vertex1 = sum(vertex_table[edge_index], self.pos) # P1
            vertex2 = sum(vertex_table[edge_index + 1], self.pos) # P2

            d_vertex_x = vertex2[0] - vertex1[0]
            d_vertex_y = vertex2[1] - vertex1[1]

            vertex_distance = math.sqrt(d_vertex_x ** 2 + d_vertex_y ** 2)
            slope_angle = math.atan2(d_vertex_y, d_vertex_x) # alpha
            self.slope_angle = slope_angle

            distance = math.cos(slope_angle) * (vertex1[1] - ball.pos[1]) - math.sin(slope_angle) * (vertex1[0] - ball.pos[0])

            x_distance_to_collision_point = math.sin(-slope_angle) * distance
            y_distance_to_collision_point = math.cos(-slope_angle) * distance

            # set values
            self.ball_collision_point = sum(ball.pos, [x_distance_to_collision_point, y_distance_to_collision_point])
            self.distance_to_ball = abs(distance)

    def handle_collision(self, ball: Ball):
        self.calculate_ball_collision_point(ball)
        velocity = ball.vel
        
        # check if colliding
        if self.distance_to_ball <= ball.size:
            # rotate velocity vector by slope angle of function at collision point
            # mirror y axis by multiplying y value by -1
            bounce_velocity = [
                velocity[0] * math.cos(-self.slope_angle) - velocity[1] * math.sin(-self.slope_angle),
                -(velocity[0] * math.sin(-self.slope_angle) + velocity[1] * math.sin(-self.slope_angle)),
            ]
            ball.vel = bounce_velocity







line = Mesh([
    [-200, 200],
    [100, 0],
    ])

ball = Ball([300, 500], [0, -0.0], 50, [255, 0, 255], win)
brick = Brick([width / 2, height / 2], line, True, "yellow", win)

run = True
FPS = 60

acceleration = 0.1
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
            ball.vel = sum(ball.vel, [0, acceleration])

        if keys[pygame.K_a]:
            ball.vel = sum(ball.vel, [-acceleration, 0])

        if keys[pygame.K_s]:
            ball.vel = sum(ball.vel, [0, -acceleration])

        if keys[pygame.K_d]:
            ball.vel = sum(ball.vel, [acceleration, 0])

    ball.vel = sum(ball.vel, product(ball.vel, [-friction, -friction]))

        
            

    
    win.fill((0, 0, 0)) 
    
    ball.draw()
    brick.draw()
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
    pygame.draw.line(win, "green", reverseY(ball.pos), reverseY(brick.ball_collision_point))
    pygame.draw.circle(win, "red", reverseY(brick.ball_collision_point), 5)


    y += 1.5
    # brick.static_mesh.vertex_table[1] = [brick.static_mesh.vertex_table[1][0], y]

    if y > height:
        y = 0



    pygame.display.update() 
    
    
    


pygame.quit() 
