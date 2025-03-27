#Project Name: WheelAware
#Ahmed Saeed Ahmed Mohamed - 202211615
#Kazi Mahir Al Wafi - 202211829

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math, random, time

#initialize OpenGL and Pygame
pygame.init()
display_width, display_height = 800, 600
pygame.display.set_mode((display_width, display_height), DOUBLEBUF | OPENGL)
gluOrtho2D(0, display_width, 0, display_height)  # Set the coordinate system

# Game states
TITLE_SCREEN = 0
GAMEPLAY = 1
game_state = TITLE_SCREEN

# Function to draw buildings with different colors
def draw_building(x, y, width, height, color):
    vertices = [
        (x, y),
        (x + width, y),
        (x + width, y + height),
        (x, y + height)
    ]
    glBegin(GL_QUADS)
    glColor3f(*color)  # Use the provided color
    for vertex in vertices:
        glVertex2f(*vertex)
    glEnd()

    # Shadow on the right side
    shadow_width = width * 0.2  # Adjust shadow width
    shadow_color = (color[0] * 0.5, color[1] * 0.5, color[2] * 0.5)  # Darken color

    glBegin(GL_QUADS)
    glColor3f(*shadow_color)
    glVertex2f(x + width, y)  # Bottom right
    glVertex2f(x + width + shadow_width, y)  # Extended shadow width
    glVertex2f(x + width + shadow_width, y + height)
    glVertex2f(x + width, y + height)
    glEnd()

# Function to draw windows
def draw_window(x, y, width, height):
    vertices = [
        (x, y),
        (x + width, y),
        (x + width, y + height),
        (x, y + height)
    ]
    glBegin(GL_QUADS)
    glColor3f(232/255.0, 175/255.0, 131/255.0)  # Grey window color
    for vertex in vertices:
        glVertex2f(*vertex)
    glEnd()

# Function to draw streetlights
def draw_streetlight(x, y):    
    # Draw the pole
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.5, 0.5)  # Pole color
    glVertex2f(x, y)
    glVertex2f(x + 5, y)
    glVertex2f(x + 5, y + 150)
    glVertex2f(x, y + 150)
    glEnd()

    glColor3f(1.0, 1.0, 0.0)  # Normal bright light

    glBegin(GL_QUADS)
    glVertex2f(x - 10, y + 150)
    glVertex2f(x + 15, y + 150)
    glVertex2f(x + 15, y + 160)
    glVertex2f(x - 10, y + 160)
    glEnd()

    # Enable transparency for the light cone
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0, 1.0, 0.0, 0.2)  # Soft yellow light with transparency

    # Draw the cone-shaped light
    glBegin(GL_TRIANGLES)
    glVertex2f(x + 2.5, y + 155)  # Light source (near the top of the streetlight)
    glVertex2f(x - 30, 50)  # Left side of light on pavement
    glVertex2f(x + 35, 50)  # Right side of light on pavement
    glEnd()

    glDisable(GL_BLEND)  # Disable transparency after drawing




# Function to draw pavement
def draw_pavement():
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)  # Pavement color
    glVertex2f(0, 0)
    glVertex2f(800, 0)
    glVertex2f(800, 50)
    glVertex2f(0, 50)
    glEnd()


# Function to draw pixelated clouds
def draw_cloud(x, y, size):
    glColor3f(1.0, 1.0, 1.0)  # White color for clouds
    for offset_x in [-size * 0.5, 0, size * 0.50]:  # Horizontal offsets
        for offset_y in [-size * 0.3, 0, size * 0.3]:  # Vertical offsets
            glBegin(GL_TRIANGLE_FAN)
            for angle in range(0, 360, 10):  # Draw a circle
                rad = math.radians(angle)
                glVertex2f(x + offset_x + size * 0.5 * math.cos(rad), y + offset_y + size * 0.5 * math.sin(rad))
            glEnd()


def draw_sky():
    for i in range(100):  #Create a gradient from a soft blue to a pale orange
        t = i / 100.0
        r = (1.0 - t) * 0.7 + t * 0.9  #orange
        g = (1.0 - t) * 0.7 + t * 0.6  #green
        b = (1.0 - t) * 0.9 + t * 0.5  #blue
        
        y_start = t * 600  #Scale to window height (0 to 600)
        y_end = (t + 0.01) * 600  #Next gradient step
        
        glBegin(GL_QUADS)
        glColor3f(r, g, b)
        glVertex2f(0, y_start)  #Bottom left
        glVertex2f(800, y_start)   #Bottom right
        glVertex2f(800, y_end)  #Top right
        glVertex2f(0, y_end)  #Top left
        glEnd()

def draw_road():
    glBegin(GL_QUADS)
    glColor3f(0.1, 0.1, 0.1)  # Dark grey/black road color
    glVertex2f(0, 0)
    glVertex2f(800, 0)
    glVertex2f(800, 30)  # Shorter than pavement
    glVertex2f(0, 30)
    glEnd()

    # Lane markings (white dashes)
    glColor3f(1.0, 1.0, 1.0)  # White color
    for i in range(0, 800, 80):  # Spaced dashed lines
        glBegin(GL_QUADS)
        glVertex2f(i, 12)
        glVertex2f(i + 30, 12)
        glVertex2f(i + 30, 18)
        glVertex2f(i, 18)
        glEnd()

# Function to render text as an OpenGL texture
def render_text(text, x, y, size=36):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, (255, 255, 255), (0, 0, 0))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    
    glRasterPos2f(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

def draw_title_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear both color and depth buffers

    # Draw the background scene directly
    display() 

    # Draw the title text
    render_text("WheelAware: An MS Awareness Game", 100, 500, 48)

    # Draw buttons
    glColor3f(0.0, 0.0, 0.0)
    
    # PLAY button
    glBegin(GL_QUADS)
    glVertex2f(300, 250)
    glVertex2f(500, 250)
    glVertex2f(500, 300)
    glVertex2f(300, 300)
    glEnd()
    render_text("PLAY", 370, 270, 36)
    
    # INSTRUCTIONS button
    glBegin(GL_QUADS)
    glVertex2f(300, 180)
    glVertex2f(500, 180)
    glVertex2f(500, 230)
    glVertex2f(300, 230)
    glEnd()
    render_text("INSTRUCTIONS", 310, 200, 36)

    glFlush()  # Force OpenGL to execute all commands

    pygame.display.flip()  # Swap buffers (only once per frame)



def handle_title_screen_events():
    global game_state
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            y = display_height - y  # Convert Pygame's Y-coordinates to OpenGL's

            print(f"Mouse Clicked at: {x}, {y}")  # Debugging

            if 300 <= x <= 500:
                if 250 <= y <= 300:
                    print("PLAY button clicked!")  # Debugging
                    game_state = GAMEPLAY  # Switch to gameplay
                elif 180 <= y <= 230:
                    print("INSTRUCTIONS button clicked!")  # Debugging


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw the sky
    draw_sky()

    # Draw buildings
    #back
    draw_building(0, 50, 100, 100, (105/255.0, 105/255.0, 105/255.0))
    draw_building(150, 50, 120, 350, (105/255.0, 105/255.0, 105/255.0))
    draw_building(400, 50, 120, 330, (105/255.0, 105/255.0, 105/255.0))
    draw_building(600, 50, 120, 210, (105/255.0, 105/255.0, 105/255.0))
    draw_building(700, 50, 120, 270, (105/255.0, 105/255.0, 105/255.0))
    #front
    draw_building(100, 50, 100, 300, (50/255.0, 50/255.0, 50/255.0))
    draw_building(250, 50, 150, 250, (50/255.0, 50/255.0, 50/255.0))
    draw_building(450, 50, 200, 200, (50/255.0, 50/255.0, 50/255.0))
    draw_building(700, 50, 80, 300, (50/255.0, 50/255.0, 50/255.0))
    # Draw windows
    for i in range(3):
        #buidling 1 (R to L)

        height = 310
        while height > 50:
            draw_window(117 + i * 25, height, 15, 15)
            height = height - 30
        
        #buidling 2
        draw_window(270 + i * 45, 250, 20, 30)
        draw_window(270 + i * 45, 200, 20, 30)
        draw_window(270 + i * 45, 150, 20, 30)
        draw_window(270 + i * 45, 100, 20, 30)

        #buidling 3       
        draw_window(550 + i * 35, 180, 20, 50)
        draw_window(550 + i * 35, 100, 20, 50)

        #buidling 4
        height = 330
        while height > 50:
            draw_window(708 + i * 25, height, 15, 15)
            height = height - 30

     
   
    # Draw streetlights
    draw_streetlight(50, 50)
    draw_streetlight(150, 50)
    draw_streetlight(300, 50)
    draw_streetlight(500, 50)
    draw_streetlight(680, 50)

    # Draw road
    draw_road()

    # Draw pavement
    draw_pavement()

    # Draw clouds
    draw_cloud(200, 450, 30)
    draw_cloud(400, 480, 40)
    draw_cloud(600, 450, 35)
    draw_cloud(300, 500, 25)


class Character:
    def __init__(self, x, y, window_width, window_height, width=30, height=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.jump_power = -10  # Negative because Pygame y-axis is inverted
        self.velocity_y = 0
        self.gravity = 0.5
        self.on_ground = False
        self.window_width = window_width
        self.window_height = window_height
        self.ground_level = window_height - 100  # Adjust based on screen size

    def move(self, keys):
        # Left/Right Movement
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        # Prevent going off-screen
        self.x = max(0, min(self.x, self.window_width - self.width))

        # Jumping
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

        # Apply gravity
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        # Collision with ground
        if self.y >= self.ground_level:
            self.y = self.ground_level
            self.velocity_y = 0
            self.on_ground = True

    def draw(self):
        glColor3f(1, 0, 0)  # Red character
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.window_height - self.y)  # Adjust for OpenGL coords
        glVertex2f(self.x + self.width, self.window_height - self.y)
        glVertex2f(self.x + self.width, self.window_height - (self.y + self.height))
        glVertex2f(self.x, self.window_height - (self.y + self.height))
        glEnd()


class Scene:
    def __init__(self, obstacles):
        self.obstacles = obstacles  # Store obstacles in the scene

    def draw(self):
        """Draw the scene, including background and obstacles."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen
        
        draw_sky()
        draw_building(0, 50, 300, 600, (50/255.0, 50/255.0, 50/255.0))  
        draw_building(450, 50, 300, 400, (50/255.0, 50/255.0, 50/255.0)) 
        

        # Draw all obstacles in the scene
        for obstacle in self.obstacles:
            obstacle.draw()

    def check_collision(self, player):
        """Check if the player collides with an obstacle."""
        for obstacle in self.obstacles:
            if obstacle.collides_with(player):
                return True
        return False

class Stair:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50

    def draw(self):
        """Draw a simple rectangle for the stair."""
        glColor3f(0.6, 0.3, 0.1)  # Brown stairs
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

    def collides_with(self, player):
        """Check if player's feet are on the stair."""
        player_bottom = player.y - player.height / 2  # Feet position
        return (
            self.x < player.x < self.x + self.width and
            player_bottom >= self.y and player_bottom <= self.y + self.height
        )


class Ramp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 30

    def draw(self):
        """Draw a simple triangle for the ramp."""
        glColor3f(0.2, 0.6, 0.2)  # Green ramp
        glBegin(GL_TRIANGLES)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

    def collides_with(self, player):
        """Check if player is stepping on the ramp."""
        player_bottom = player.y - player.height / 2
        return (
            self.x < player.x < self.x + self.width and
            player_bottom >= self.y and player_bottom <= self.y + self.height
        )


class BumpyRoad:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 20

    def draw(self):
        """Draw a simple wavy road."""
        glColor3f(0.5, 0.5, 0.5)  # Gray road
        glBegin(GL_LINE_STRIP)
        for i in range(6):
            glVertex2f(self.x + i * 20, self.y + (i % 2) * 10)
        glEnd()

    def collides_with(self, player):
        """Check if player is stepping on the bumpy road."""
        player_bottom = player.y - player.height / 2
        return (
            self.x < player.x < self.x + self.width and
            player_bottom >= self.y and player_bottom <= self.y + self.height
        )


class GameScenes:
    def __init__(self):
        self.player = Character(50, 100, 800, 600)  # Start at (50, 100)
        self.current_scene_index = 0  # Start with the first scene
        self.scenes = [
            Scene([Stair(200, 50), Ramp(400, 50)]),  # Scene 1 with stairs & ramp
            Scene([BumpyRoad(250, 50)]),  # Scene 2 with bumpy road
        ]

    def update(self, keys):
        self.player.move(keys)
        
        # If the player reaches the right edge, switch scenes
        if self.player.x > 750:
            self.current_scene_index += 1
            if self.current_scene_index >= len(self.scenes):
                self.current_scene_index = 0  # Loop back to the first scene
            self.player.x = 50  # Reset position to the left side

    def draw(self):
        self.scenes[self.current_scene_index].draw()  # Draw the current scene
        self.player.draw()
        pygame.display.flip()



def main():
    global game_state
    running = True
    clock = pygame.time.Clock()
    game_scene = GameScenes()

    while running:
        keys = pygame.key.get_pressed()

        if game_state == TITLE_SCREEN:
            draw_title_screen()
            handle_title_screen_events()
        
        elif game_state == GAMEPLAY:
            game_scene.update(keys)
            game_scene.draw()

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False


        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()