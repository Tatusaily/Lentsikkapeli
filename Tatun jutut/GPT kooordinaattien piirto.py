import pygame
import random
import math
#CHAT GPT:N tekemä esimerkki

# Initialize Pygame
pygame.init()

# Set the window size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the circle radius and line radius
circle_radius = 5
line_radius = 100

# Generate a list of random coordinates
num_points = 50
points = [(random.randint(0, screen_width), random.randint(0, screen_height)) for i in range(num_points)]


# Define a function to draw the circles and lines
def draw_points(points):
    # Draw the circles
    for i, point in enumerate(points):
        color = (255, 255, 255)
        if selected[i]:
            color = (255, 0, 0)
        pygame.draw.circle(screen, color, point, circle_radius)

    # Draw the lines
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = math.sqrt((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)
            if distance <= line_radius:
                color = (255, 255, 255)
                if selected[i] and selected[j]:
                    color = (255, 0, 0)
                pygame.draw.line(screen, color, points[i], points[j], 1)


# Draw the initial points
selected = [False] * num_points
draw_points(points)

# Update the display
pygame.display.update()

# Keep the window open until the user closes it
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i, point in enumerate(points):
                distance = math.sqrt((pos[0]-point[0])**2 + (pos[1]-point[1])**2)
                if distance <= circle_radius:
                    selected[i] = not selected[i]
            draw_points(points)
            pygame.display.update()