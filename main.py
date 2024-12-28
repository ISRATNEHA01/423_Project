from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import cos, sin, radians, pi
import random

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
PI = pi
paused = False

# Planet properties
planets = [
    {"name": "Mercury", "distance": 100, "size": 8, "speed": 0.5, "angle": 0},
    {"name": "Venus", "distance": 150, "size": 12, "speed": 0.3, "angle": 0},
    {"name": "Earth", "distance": 200, "size": 15, "speed": 0.2, "angle": 0},
    {"name": "Mars", "distance": 250, "size": 10, "speed": 0.1, "angle": 0},
    {"name": "Jupiter", "distance": 300, "size": 25, "speed": 0.07, "angle": 0}
]

play_box = {
    'width': 20,
    'height': 20,
    'up': (390, 760),
    'down': (390, 740),
    'right': (410, 750),
    'color': (0, 1, 0),
}
pause_box = {
    'width': 20,
    'height': 20,
    'up1': (395, 760),
    'down1': (395, 740),
    'up2': (405, 760),
    'down2': (405, 740),
    'color': (1, 0.75, 0),
}


def draw_midpoint_circle(xc, yc, r):

    x = 0
    y = r
    p = 1 - r

    points = []
    while x <= y:
        points.extend([
            (xc + x, yc + y),
            (xc - x, yc + y),
            (xc + x, yc - y),
            (xc - x, yc - y),
            (xc + y, yc + x),
            (xc - y, yc + x),
            (xc + y, yc - x),
            (xc - y, yc - x),
        ])
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
    return points


def FindZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy > 0:
            zone = 3
        elif dx <= 0 and dy <= 0:
            zone = 4
        elif dx > 0 and dy < 0:
            zone = 7
    else:
        if dx > 0 and dy > 0:
            zone = 1
        elif dx <= 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy <= 0:
            zone = 6
    return zone


def ConverttoZoneZero(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y


def ConvertfromZoneZero(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y


def MLA(x1, y1, x2, y2, color):
    zone = FindZone(x1, y1, x2, y2)
    x1, y1 = ConverttoZoneZero(x1, y1, zone)
    x2, y2 = ConverttoZoneZero(x2, y2, zone)
    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    dNE = 2 * (dy - dx)
    dE = 2 * dy
    x = x1
    y = y1
    while x <= x2:
        draw_points(*ConvertfromZoneZero(x, y, zone), color)
        x += 1
        if d < 0:
            d += dE
        else:
            d += dNE
            y += 1


def draw_text(x, y, text, color=(1, 1, 1)):    #for labeling planets
    '''Iterates over each character in the string text
           Converts each character to its ASCII value using ord(char).
           Passes this value to glutBitmapCharacter, which draws the character
            on the screen using the GLUT_BITMAP_HELVETICA_18 font '''
    glColor3f(*color)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))



def draw_orbit(xc, yc, radius):
    glBegin(GL_POINTS)
    points = draw_midpoint_circle(xc, yc, radius)
    for x, y in points:
        glVertex2f(x, y)
    glEnd()


def draw_points(x, y, color):
    glColor3f(*color)
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_button():
    global paused
    if not paused:
        # PAUSE
        MLA(*pause_box['up1'], *pause_box['down1'], pause_box['color'])
        MLA(*pause_box['up2'], *pause_box['down2'], pause_box['color'])
    else:
        # PLAY
        MLA(*play_box['right'], *play_box['up'], play_box['color'])
        MLA(*play_box['right'], *play_box['down'], play_box['color'])
        MLA(*play_box['up'], *play_box['down'], play_box['color'])

def draw_filled_circle(x, y, radius, color):
    glColor3f(*color)  # Set the color of the circle
    glBegin(GL_POINTS)  # Begin drawing points

    def draw_circle_points(cx, cy, x, y):
        for dy in range(-y, y + 1):
            glVertex2f(cx + x, cy + dy)
            glVertex2f(cx - x, cy + dy)

        for dy in range(-x, x + 1):
            glVertex2f(cx + y, cy + dy)
            glVertex2f(cx - y, cy + dy)

    x_point = 0
    y_point = radius
    d = 1 - radius

    draw_circle_points(x, y, x_point, y_point)

    while x_point < y_point:
        x_point += 1
        if d < 0:
            d += 2 * x_point + 1
        else:
            y_point -= 1
            d += 2 * (x_point - y_point) + 1
        draw_circle_points(x, y, x_point, y_point)

    glEnd()  # End drawing points

NUM_STARS = 100  # Number of stars
stars = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for _ in range(NUM_STARS)]


def draw_stars():
    glColor3f(1.0, 1.0, 1.0)  # White color for stars
    glPointSize(2)  # Small points for stars
    glBegin(GL_POINTS)
    for x, y in stars:
        glVertex2f(x, y)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw stars in the background
    draw_stars()

    # Draw the Sun
    draw_filled_circle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 40, (1.0, 1.0, 0.0))

    # Draw planets and their orbits
    for planet in planets:
        # Draw the orbit
        glColor3f(0.5, 0.5, 0.5)  # Gray
        draw_orbit(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, planet["distance"])

        # Calculate planet position
        planet["angle"] += planet["speed"]
        if planet["angle"] >= 360:
            planet["angle"] -= 360

        rad_angle = radians(planet["angle"])
        planet_x = WINDOW_WIDTH // 2 + planet["distance"] * cos(rad_angle)
        planet_y = WINDOW_HEIGHT // 2 + planet["distance"] * sin(rad_angle)

        # Draw the planet
        if planet["distance"] == 100:
            draw_filled_circle(planet_x, planet_y, planet["size"], (0.75, 0.75, 0.75))  # Mercury
        elif planet["distance"] == 150:
            draw_filled_circle(planet_x, planet_y, planet["size"], (0.9, 0.85, 0.7))  # Venus
        elif planet["distance"] == 200:
            draw_filled_circle(planet_x, planet_y, planet["size"], (0.7, 0.8, 0.9))  # Earth
        elif planet["distance"] == 250:
            draw_filled_circle(planet_x, planet_y, planet["size"], (0.8, 0.4, 0.2))  # Mars
        else:
            draw_filled_circle(planet_x, planet_y, planet["size"], (0.8, 0.7, 0.5))  # Jupiter

        # Draw the planet's name near its position
        text_x = planet_x + planet["size"] + 10
        text_y = planet_y + planet["size"] + 10
        draw_text(text_x, text_y, planet["name"], color=(1, 1, 1))  # White color

    draw_button()

    glutSwapBuffers()

'''The cosine of the angle gives the horizontal projection of the planet's 
position relative to the Sun.'''
'''The sine of the angle gives the vertical projection of the planet's 
 position relative to the Sun.'''

def mouseListener(button, state, x, y):
    global paused, pause_box
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        if pause_box['up1'][0] <= x <= pause_box['up2'][0] + pause_box['width'] and pause_box['down1'][
            1] <= WINDOW_HEIGHT - y <= pause_box['up2'][1] + pause_box['height']:
            if paused:
                print("Play clicked")
            else:
                print("Pause clicked")
            paused = not paused

    glutPostRedisplay()


def keyboardListener(key, x, y):
    if not paused:
        if key == b'i':
            for planet in planets:
                if planet['speed'] < 3:
                    planet['speed'] += 0.1
                    print('Speed increasing')
        if key == b'd':
            for planet in planets:
                if planet['speed'] > 0.1:
                    planet['speed'] -= 0.1
                    print('Speed decreasing')

        glutPostRedisplay()


def update():
    if not paused:
        glutPostRedisplay()


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Solar System with Midpoint Algorithm")
    init()
    glutDisplayFunc(display)
    glutIdleFunc(update)
    glutMouseFunc(mouseListener)
    glutKeyboardFunc(keyboardListener)

    glutMainLoop()


if __name__ == "__main__":
    main()