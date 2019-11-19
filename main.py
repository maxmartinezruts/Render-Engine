import numpy as np
import pygame
import math

render = 0
# Screen parameters
width = 800
height = 800
center = np.array([width/2+200, height/2-200])
screen = pygame.display.set_mode((width, height))

# Colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
yellow = (255,255, 0)
fpsClock = pygame.time.Clock()
fps = 400
k = 2

def smoothMin(circles, new_center, k):

    min_smooth = circles[0].get_min_dist(new_center)

    for i in range(1, len(circles)):
        h = max(k-abs(min_smooth-circles[i].get_min_dist(new_center)),0)/k
        min_smooth = min(min_smooth,circles[i].get_min_dist(new_center)) - h**3*k/6.0
    return  min_smooth

# Convert coordinates form cartesian to screen coordinates (used to draw in pygame screen)
def cartesian_to_screen(car_pos):
    factor = 0.04
    screen_pos = np.array([center[0] * factor + car_pos[0], center[1] * factor - car_pos[1]]) / factor
    screen_pos = screen_pos.astype(int)
    return screen_pos

# Convert coordinates form screen to cartesian  (used to draw in pygame screen)
def screen_to_cartesian(screen_pos):
    factor = 0.04
    car_pos = np.array([screen_pos[0] - center[0], center[1] - screen_pos[1]]) * factor
    car_pos = car_pos.astype(float)
    return car_pos

def draw(n):
    global k
    global render
    render +=1
    circles[1].pos += np.array([0,-0.05,0])
    pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                k+=0.1
            if event.key == pygame.K_RIGHT:
                k-=0.1
            print(k)
    screen.fill((0, 0, 0))

    for circle in circles:
        pygame.draw.circle(screen, white, cartesian_to_screen(circle.pos),  int(circle.rad*25))

    camera = np.array([0,0,5])

    xs = np.linspace(-8,8,400)
    ys = np.linspace(-8,8,400)

    for i in range(len(xs)):
        for j in range(len(ys)):
            target = np.array([xs[i],ys[j],0])
            direction = (target-camera)/np.linalg.norm(target-camera)
            min_distance = 1
            new_center = np.array(list(camera))
            while min_distance > 0.01:
                if min_distance > 10:
                    break
                min_distance = smoothMin(circles, new_center, k)
                new_center = new_center + direction * min_distance

            distance = np.linalg.norm(camera-new_center)
            intensity = int(min(max((1-distance/6)*255,0),255))
            # print(min_distance,intensity)
            screen.fill((intensity,intensity,intensity), ([i, 400-j], (1, 1)))

    camera = np.array([0, 0, 5])


    for i in range(len(xs)):
        for j in range(len(ys)):
            target = np.array([xs[i], ys[j], 0])
            direction = (target - camera) / np.linalg.norm(target - camera)
            min_distance = 1
            new_center = np.array(list(camera))
            while min_distance > 0.01:
                if min_distance > 10:
                    break
                min_distance = min(circles[0].get_min_dist(new_center), circles[1].get_min_dist(new_center))
                new_center = new_center + direction * min_distance

            distance = np.linalg.norm(camera - new_center)
            intensity = int(min(max((1 - distance / 6) * 255, 0), 255))
            # print(min_distance,intensity)
            screen.fill((intensity, intensity, intensity), ([i, 800 - j], (1, 1)))

    camera = np.array([0, 0, 5])


    for i in range(len(xs)):
        for j in range(len(ys)):
            target = np.array([xs[i], ys[j], 0])
            direction = (target - camera) / np.linalg.norm(target - camera)
            min_distance = 1
            new_center = np.array(list(camera))
            while min_distance > 0.01:
                if min_distance > 10:
                    break
                min_distance = max(circles[0].get_min_dist(new_center), circles[1].get_min_dist(new_center))
                new_center = new_center + direction * min_distance

            distance = np.linalg.norm(camera - new_center)
            intensity = int(min(max((1 - distance / 6) * 255, 0), 255))
            # print(min_distance,intensity)
            screen.fill((intensity, intensity, intensity), ([400+i, 800 - j], (1, 1)))
    pygame.image.save(screen, "movie/render_"+str(n)+".jpg")
    pygame.display.flip()


class Circle:
    def __init__(self,pos,rad):
        self.pos = np.array([pos[0],pos[1],0])
        self.rad = rad

    def get_min_dist(self,pos):
        return np.linalg.norm(pos-self.pos)-self.rad

circles = []

for i in range(0):

    circles.append(Circle(np.random.uniform(-4,4,(2))*0.6,np.random.uniform(0.2,2)))

circles.append(Circle(np.array([0.,-1.]),2.))
circles.append(Circle(np.array([0.,2.5]),1.))

for i in range(1000):
    draw(i)
