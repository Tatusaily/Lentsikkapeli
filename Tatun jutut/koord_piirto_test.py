import pygame
import random
import math
import mysql.connector

yhteys = mysql.connector.connect(
         host='localhost',
         port= 3306,
         database='flight_game',
         user='user1',
         password='sala1',
         autocommit=True
         )

def GetAirportEU():
    query = f"SELECT latitude_deg, longitude_deg FROM airport WHERE continent= 'EU' AND(NOT iso_country = 'RU');"
    kursori = yhteys.cursor()
    kursori.execute(query)
    tulos = kursori.fetchall()
    return tulos


# Initialize Pygame
pygame.init()

# Set the window size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
koordisurfa = pygame.Surface((screen_width, screen_height))
bg = pygame.image.load("eu_map.jpg")

screen.blit(bg, (0, 0))
koordisurfa.fill("Red")
#TODO Laita se koordinaatti surface näkymään kartan päälle oikein

# Set the circle radius and line radius
circle_radius = 5
line_radius = 100

# Generate a list of random coordinates
num_points = 50
#Ankkuri koordinaatit vedetty islannin länsipuolelta.
ankkurix = 66.069068
ankkuriy = -31.690649
#Otetaan SQL haulla tulevat kentät ja koitetaan saada ne osumaan kartalle oikeaan kohtaan
airfields = GetAirportEU()
filtered_airports = random.sample(airfields, num_points)
points = []
for airport in filtered_airports:   #Vähennä lentokentän koordinaateista ankkuri TODO: Tee tää loppuun
    points.append((abs(airport[0] - ankkurix), abs(airport[1] - ankkuriy)))

print(points)

# Define a function to draw the circles and lines
def draw_points(points):
    # Draw the circles
    for i, point in enumerate(points):
        color = (0, 255, 0)
        if selected[i]:
            color = (255, 0, 0)
        pygame.draw.circle(koordisurfa, color, point, circle_radius)

    # Draw the lines
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = math.sqrt((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)
            if distance <= line_radius:
                color = (150, 150, 150)
                if selected[i] and selected[j]:
                    color = (255, 0, 0)
                pygame.draw.line(koordisurfa, color, points[i], points[j], 1)


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
