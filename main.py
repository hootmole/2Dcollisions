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

def difference(v1, v2):
    v = []
    for i in range(len(v1)):
        v.append(v1[i] - v2[i])
    return v

def vector_lenght2D(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2)

def vector_distance2D(v1, v2):
    return vector_lenght2D(difference(v1, v2))

def rotate_vec2D(v, angle):
    return [
        v[0] * math.cos(angle) - v[1] * math.sin(angle),
        v[0] * math.sin(angle) + v[1] * math.cos(angle),
    ]


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
    def __init__(self, pos, static_mesh: Mesh, isAlive: bool, color, win, is_enabled_testing = False) -> None:
        self.pos = pos
        self.isAlive = isAlive
        self.color = color
        self.win = win
        self.static_mesh = static_mesh
        self.distance_to_ball = None
        self.collision_point_pos = None
        self.slope_angles = []
        self.is_enabled_testing = is_enabled_testing

    def draw(self):
        if self.isAlive:
            vertex_table = self.static_mesh.vertex_table
            for edge_index in range(len(vertex_table)):
                pygame.draw.line(self.win, self.color, reverseY(sum(vertex_table[edge_index - 1], self.pos)), reverseY(sum(vertex_table[edge_index], self.pos)))


    def handle_collision(self, ball: Ball):
        vertex_table = self.static_mesh.vertex_table

        collision_points_pos_list = []
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

            # determine if edge imact or vertex impact
            # assuming vertex1 is the origin of rotation
            rotated_vertex2 = sum(rotate_vec2D([d_vertex_x, d_vertex_y], -slope_angle), vertex1) # [d_vertex_x, d_vertex_y] is the same as vertex2 - vertex1 (vector - origin)
            rotated_ball_pos = sum(rotate_vec2D(difference(ball.pos, vertex1), -slope_angle), vertex1)

            

            is_edge_impact = rotated_ball_pos >= min(vertex1, rotated_vertex2) and rotated_ball_pos <= max(vertex1, rotated_vertex2)
            if is_edge_impact:
                self.color = (0, 255, 0)
            else:
                self.color = (255, 0, 0)


            # edge impact
            if is_edge_impact:
                distance = math.cos(slope_angle) * (vertex1[1] - ball.pos[1]) - math.sin(slope_angle) * (vertex1[0] - ball.pos[0])

                x_distance_to_collision_point = math.sin(-slope_angle) * distance
                y_distance_to_collision_point = math.cos(-slope_angle) * distance

                # set values for every edge
                collision_points_pos_list.append(sum(ball.pos, [x_distance_to_collision_point, y_distance_to_collision_point]))
                distances_to_ball.append(abs(distance))
            
            else:
                # vertex impact
                vertex1_dist = vector_distance2D(ball.pos, vertex1)
                vertex2_dist = vector_distance2D(ball.pos, vertex2)
                
                if vertex1_dist < vertex2_dist:
                    distance = vertex1_dist
                    collision_points_pos_list.append(vertex1)

                else:
                    distance = vertex2_dist
                    collision_points_pos_list.append(vertex2)

                
                distances_to_ball.append(distance)

        

        # find the smallest edge distance and use the values
        distance_to_ball = min(distances_to_ball)
        working_edge_index = distances_to_ball.index(distance_to_ball) # edge that is colliding with ball
        
        working_slope_angle = self.slope_angles[working_edge_index]
        self.collision_point_pos = collision_points_pos_list[working_edge_index] 


        # vertex impact

        # edge impact
        # collision handeling part
        velocity = ball.vel
        
        if distance_to_ball <= ball.size and is_edge_impact: 
            # edge imact
            normal_vector_angle = working_slope_angle + math.pi / 2
            normal_vector = [math.cos(normal_vector_angle), math.sin(normal_vector_angle)]

            dot = velocity[0] * normal_vector[0] + velocity[1] * normal_vector[1]

            #R=V−2N(V⋅N)
            bounce_vector = sum(
                velocity, [-dot * normal_vector[0] * 2, -dot * normal_vector[1] * 2])

            ball.vel = bounce_vector

        elif distance_to_ball <= ball.size and not is_edge_impact:
            # vertex imact
            d_ball_pos_vec_pos = difference(self.collision_point_pos, ball.pos)

            normal_vector_angle = math.atan2(d_ball_pos_vec_pos[1], d_ball_pos_vec_pos[0]) + math.pi
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
    [-100, 0],
    [100, 0],
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


ball = Ball([70, 300], [1, 0.3], 50, [0, 0, 255], win)
brick = Brick([width / 2, height / 2], line, True, "yellow", win, 1)
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
    pygame.draw.line(win, "green", reverseY(ball.pos), reverseY(walls.collision_point_pos))
    pygame.draw.circle(win, "white", reverseY(walls.collision_point_pos), 2)

    pygame.draw.line(win, "green", reverseY(ball.pos), reverseY(brick.collision_point_pos))
    pygame.draw.circle(win, "white", reverseY(brick.collision_point_pos), 2)


    y += 1.5
    #brick.static_mesh.vertex_table[1] = [y, brick.static_mesh.vertex_table[1][0]]

    if y > height:
        y = 0



    pygame.display.update() 
    
    
    


pygame.quit() 
