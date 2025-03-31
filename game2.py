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
INSTRUCTIONS = 2
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
    text_surface = font.render(text, True, (255, 255, 255), (0, 0, 0))  # Text color is white
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    
    glRasterPos2f(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
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

    pygame.display.flip()  # Swap buffers once per frame



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
                    game_state = INSTRUCTIONS

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
        self.jump_power = -10
        self.velocity_y = 0
        self.gravity = 0.5
        self.on_ground = False
        self.window_width = window_width
        self.window_height = window_height
        self.ground_level = 50  # Height of the pavement

    def move(self, keys, obstacles):
        # Store original position for collision resolution
        original_x = self.x
        original_y = self.y
        
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
        
        # Check vertical collision after movement
        self.on_ground = False
        for obstacle in obstacles:
            if obstacle.collides_with(self):
                # If the character is on the ground, allow horizontal movement
                if self.on_ground:
                    break  # Exit the loop if on ground

        # Handle ground collision
        ground_y = self.ground_level  # Pavement is at y=50 in OpenGL coordinates
        if self.y + self.height > self.window_height - ground_y:
            self.y = self.window_height - ground_y - self.height
            self.velocity_y = 0
            self.on_ground = True

    def draw(self):
        glColor3f(1, 0, 0)  # Red character
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.window_height - self.y)
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

        # Render dialogue text for the first scene
        if GameScenes().current_scene_index == 0:  # Check if it's the first scene
            render_text("Welcome to WheelAware! Use arrow keys to move.", 400, 550, 24)  # Adjust position as needed

    def check_collision(self, player):
        """Check if the player collides with an obstacle."""
        for obstacle in self.obstacles:
            if obstacle.collides_with(player):
                return True
        return False


class Stair:
    def __init__(self, x, y, width, height, steps=10, direction="up"): 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.steps = steps  # Number of steps in the staircase
        self.direction = direction  # Direction of the stair (up or down)
        
        # Calculate dimensions for each step
        self.step_width = width / steps
        self.step_height = height / steps
    
    def draw(self):
        """Draw a staircase with the specified number of steps."""
        # Base color for the stairs
        base_color = (0.6, 0.3, 0.1)  # Brown base color
        
        # Draw the filled area under each step
        for i in range(self.steps):
            step_x = self.x + i * self.step_width
            if self.direction == "up":
                step_y = self.y + (i * self.step_height)  # Move up for each step
                # Draw the filled area under the step
                glBegin(GL_QUADS)
                glColor3f(*base_color)
                glVertex2f(step_x, self.y)  # Bottom left of the filled area
                glVertex2f(step_x + self.step_width, self.y)  # Bottom right of the filled area
                glVertex2f(step_x + self.step_width, step_y)  # Top right of the filled area
                glVertex2f(step_x, step_y)  # Top left of the filled area
                glEnd()
            elif self.direction == "down":
                step_y = self.y + self.height - (i + 1) * self.step_height  # Move down for each step
                # Draw the filled area under the step
                glBegin(GL_QUADS)
                glColor3f(*base_color)
                glVertex2f(step_x, step_y + self.step_height)  # Bottom left of the filled area
                glVertex2f(step_x + self.step_width, step_y + self.step_height)  # Bottom right of the filled area
                glVertex2f(step_x + self.step_width, self.y + self.height)  # Top right of the filled area
                glVertex2f(step_x, self.y + self.height)  # Top left of the filled area
                glEnd()

            # Draw the step as a filled rectangle
            glBegin(GL_QUADS)
            glColor3f(*base_color)
            glVertex2f(step_x, step_y)  # Bottom left
            glVertex2f(step_x + self.step_width, step_y)  # Bottom right
            glVertex2f(step_x + self.step_width, step_y + self.step_height)  # Top right
            glVertex2f(step_x, step_y + self.step_height)  # Top left
            glEnd()

    def collides_with(self, player):
        # Convert character coordinates to OpenGL coordinates
        char_x = player.x
        char_bottom = player.window_height - (player.y + player.height)  # Bottom of character in OpenGL coords
        
        # Check if character is horizontally within the staircase bounds
        if char_x + player.width > self.x and char_x < self.x + self.width:
            # Determine which step the character is over
            relative_x = char_x - self.x
            step_index = min(self.steps - 1, int(relative_x / self.step_width))
            
            # Calculate the height of the step at this position
            if self.direction == "up":
                step_height = self.y + (step_index + 1) * self.step_height
            elif self.direction == "down":
                step_height = self.y + self.height - (step_index) * self.step_height
            
            # Calculate the horizontal position of the step
            step_x = self.x + step_index * self.step_width
            
            # Check for vertical collision (landing on top of step)
            if char_bottom <= step_height and char_bottom + player.height >= step_height:
                # Position the character on top of the step
                player.y = player.window_height - step_height - player.height
                player.velocity_y = 0
                player.on_ground = True
                return True
            
            # Allow horizontal movement if the character is on the ground
            if player.on_ground:
                return False
                
        return False

class Ramp:
    def __init__(self, x, y, width, height): 
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        """Draw a simple triangle for the ramp."""
        glColor3f(0.2, 0.6, 0.2)  # Green ramp
        glBegin(GL_TRIANGLES)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

    def collides_with(self, player):
        # Convert character position to OpenGL coordinates
        char_x = player.x
        char_bottom = player.window_height - (player.y + player.height)  # Bottom of character in OpenGL coords
        
        # Check if character is horizontally within the ramp
        if char_x + player.width > self.x and char_x < self.x + self.width:
            # Calculate the height of the ramp at the character's position
            # For a triangular ramp, the height increases linearly from right to left
            # (since the triangle goes from bottom-left to top-left to bottom-right)
            progress = 1.0 - min(1.0, max(0, (char_x - self.x) / self.width))
            ramp_height_at_position = self.y + progress * self.height
            
            # If character's bottom is at or below the ramp height
            if char_bottom <= ramp_height_at_position:
                # Position the character on top of the ramp
                player.y = player.window_height - ramp_height_at_position - player.height
                player.velocity_y = 0
                player.on_ground = True
                return True
        return False


class BumpyRoad:
    def __init__(self, x, y, width, height):  
        self.x = x
        self.y = y
        self.width = width
        self.height = height  

    def draw(self):
        """Draw a simple wavy road."""
        glColor3f(0.5, 0.5, 0.5)  # Gray road
        glBegin(GL_LINE_STRIP)
        for i in range(6):
            glVertex2f(self.x + i * 20, self.y + (i % 2) * 10)
        glEnd()

    def collides_with(self, player):
        # Convert character position to OpenGL coordinates
        char_x = player.x
        char_bottom = player.window_height - (player.y + player.height)  # Bottom of character in OpenGL coords
        
        # Check if character is horizontally within the bumpy road
        if char_x + player.width > self.x and char_x < self.x + self.width:
            # Calculate which segment of the bumpy road the character is over
            segment_width = 20  # Each bump segment is 20 wide
            segment_index = int((char_x - self.x) / segment_width)
            
            # Calculate the height at this segment (alternating up/down by 10 pixels)
            bump_height = self.y + (segment_index % 2) * 10
            
            # Character is colliding if its bottom is at or below the bump height
            if char_bottom <= bump_height + self.height:
                # Position the character on top of the bump
                player.y = player.window_height - (bump_height + self.height) - player.height
                player.velocity_y = 0
                player.on_ground = True
                return True
        return False


class GameScenes:
    def __init__(self):
        self.player = Character(50, 100, 800, 600)  # Start at (50, 100)
        self.current_scene_index = 0  # Start with the first scene
        self.scenes = [
            Scene([Stair(250, 50, 550, 350)]),  # Scene 1
            Scene([Ramp(0, 50, 550, 350), BumpyRoad(600, 50, 550, 7)]),  # Scene 2
        ]

    def update(self, keys):
        current_scene = self.scenes[self.current_scene_index]
        self.player.move(keys, current_scene.obstacles)  # Pass obstacles, not the entire scene

        # Scene transition logic
        if self.player.x > 750:
            self.current_scene_index += 1
            if self.current_scene_index >= len(self.scenes):
                self.current_scene_index = 0  # Loop back to the first scene
            self.player.x = 50  # Reset position to the left side


    def draw(self):
        """Draw the current scene and player."""
        self.scenes[self.current_scene_index].draw()  # Draw scene
        self.player.draw()  # Draw character
        pygame.display.flip()

def draw_dialogue_box(text, x, y, width=400, height=100):
    print("Drawing dialogue box")  # Debugging output
    # Draw the box background
    glColor4f(0.0, 0.0, 0.0, 0.7)  # Semi-transparent black (RGBA)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

    # Render the text inside the box
    render_text(text, x + 10, y + height - 30, size=24)  # Adjust position for padding

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
        
        # In the main game loop
        elif game_state == GAMEPLAY:
            game_scene.update(keys)  # Update the game state
            game_scene.draw()        # Draw the current scene (buildings, player, etc.)
            
            # Render the dialogue text at the top right
            render_text("Welcome to WheelAware! Use arrow keys to move.", 600, 570, 24)  # Adjust position as needed

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False


        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()