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
    font = pygame.font.Font(None, size)  # Use default font
    text_surface = font.render(text, True, (255, 255, 255), (0, 0, 0))  # White text with black background
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
    def __init__(self, x, y, window_width, window_height, width=30, height=50, character_type="walking"):
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
        self.character_type = character_type  # "walking" or "wheelchair"
        self.facing_right = True  # Track which direction the character is facing
        self.animation_frame = 0  # For walking animation
        self.animation_time = 0  # Time tracker for animation

    def move(self, keys, obstacles):
        # Store original position for collision resolution
        original_x = self.x
        original_y = self.y
        
        # Update animation time
        self.animation_time += 1
        if self.animation_time > 10:  # Change animation frame every 10 game ticks
            self.animation_frame = (self.animation_frame + 1) % 4  # 4 animation frames
            self.animation_time = 0
        
        # Left/Right Movement
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.facing_right = True

        # Prevent going off-screen
        self.x = max(0, min(self.x, self.window_width - self.width))

        # Jumping - only allowed for walking character
        if self.character_type == "walking" and keys[pygame.K_SPACE] and self.on_ground:
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
        if self.character_type == "walking":
            self.draw_pixelated_character()
        elif self.character_type == "wheelchair":
            self.draw_wheelchair_character()
    
    def draw_pixelated_character(self):
        # Create a pixelated human character instead of a red block
        
        # Adjust OpenGL coordinates for drawing
        char_x = self.x
        char_y = self.window_height - self.y - self.height
        
        # Head (slightly darker skin tone)
        glColor3f(0.9, 0.75, 0.65)  # Skin color
        glBegin(GL_QUADS)
        glVertex2f(char_x + 10, char_y + self.height - 5)  # Bottom left
        glVertex2f(char_x + self.width - 10, char_y + self.height - 5)  # Bottom right
        glVertex2f(char_x + self.width - 10, char_y + self.height)  # Top right
        glVertex2f(char_x + 10, char_y + self.height)  # Top left
        glEnd()
        
        # Body (shirt)
        glColor3f(0.2, 0.4, 0.8)  # Blue shirt
        glBegin(GL_QUADS)
        glVertex2f(char_x + 7, char_y + self.height - 20)  # Bottom left
        glVertex2f(char_x + self.width - 7, char_y + self.height - 20)  # Bottom right
        glVertex2f(char_x + self.width - 7, char_y + self.height - 5)  # Top right
        glVertex2f(char_x + 7, char_y + self.height - 5)  # Top left
        glEnd()
        
        # Legs (pants)
        glColor3f(0.1, 0.1, 0.5)  # Dark blue pants
        
        # Left leg
        glBegin(GL_QUADS)
        leg_offset = 5 if (self.animation_frame % 2 == 0) else 3
        glVertex2f(char_x + 10, char_y)  # Bottom left
        glVertex2f(char_x + 15, char_y)  # Bottom right
        glVertex2f(char_x + 15, char_y + self.height - 20 - leg_offset)  # Top right
        glVertex2f(char_x + 10, char_y + self.height - 20)  # Top left
        glEnd()
        
        # Right leg
        glBegin(GL_QUADS)
        leg_offset = 3 if (self.animation_frame % 2 == 0) else 5
        glVertex2f(char_x + self.width - 15, char_y)  # Bottom left
        glVertex2f(char_x + self.width - 10, char_y)  # Bottom right
        glVertex2f(char_x + self.width - 10, char_y + self.height - 20 - leg_offset)  # Top right
        glVertex2f(char_x + self.width - 15, char_y + self.height - 20)  # Top left
        glEnd()
        
        # Arms
        glColor3f(0.2, 0.4, 0.8)  # Same as shirt
        
        # Left arm
        arm_swing = math.sin(self.animation_time * 0.2) * 3
        arm_y_offset = 0 if self.on_ground else -5  # Raise arms when jumping
        glBegin(GL_QUADS)
        if self.facing_right:
            glVertex2f(char_x + 5, char_y + self.height - 18 + arm_swing)
            glVertex2f(char_x + 8, char_y + self.height - 18 + arm_swing)
            glVertex2f(char_x + 8, char_y + self.height - 8 + arm_y_offset)
            glVertex2f(char_x + 5, char_y + self.height - 8 + arm_y_offset)
        else:
            glVertex2f(char_x + 5, char_y + self.height - 18 - arm_swing)
            glVertex2f(char_x + 8, char_y + self.height - 18 - arm_swing)
            glVertex2f(char_x + 8, char_y + self.height - 8 + arm_y_offset)
            glVertex2f(char_x + 5, char_y + self.height - 8 + arm_y_offset)
        glEnd()
        
        # Right arm
        glBegin(GL_QUADS)
        if self.facing_right:
            glVertex2f(char_x + self.width - 8, char_y + self.height - 18 - arm_swing)
            glVertex2f(char_x + self.width - 5, char_y + self.height - 18 - arm_swing)
            glVertex2f(char_x + self.width - 5, char_y + self.height - 8 + arm_y_offset)
            glVertex2f(char_x + self.width - 8, char_y + self.height - 8 + arm_y_offset)
        else:
            glVertex2f(char_x + self.width - 8, char_y + self.height - 18 + arm_swing)
            glVertex2f(char_x + self.width - 5, char_y + self.height - 18 + arm_swing)
            glVertex2f(char_x + self.width - 5, char_y + self.height - 8 + arm_y_offset)
            glVertex2f(char_x + self.width - 8, char_y + self.height - 8 + arm_y_offset)
        glEnd()
        
        # Eyes
        glColor3f(0.1, 0.1, 0.1)  # Black eyes
        eye_x = char_x + 18 if self.facing_right else char_x + 12
        glPointSize(2.0)
        glBegin(GL_POINTS)
        glVertex2f(eye_x, char_y + self.height - 3)
        glEnd()
    
    def draw_wheelchair_character(self):
        # Draw the same pixelated character but sitting in a wheelchair
        char_x = self.x
        char_y = self.window_height - self.y - self.height
        
        # First draw the wheelchair (under the character)
        self.draw_wheelchair(char_x, char_y)
        
        # Draw the seated character (adjusted position to sit in the wheelchair)
        # The character will be slightly smaller and positioned to look like they're sitting
        
        # Head (slightly darker skin tone)
        glColor3f(0.9, 0.75, 0.65)  # Skin color
        glBegin(GL_QUADS)
        glVertex2f(char_x + 10, char_y + self.height - 10)  # Bottom left
        glVertex2f(char_x + self.width - 10, char_y + self.height - 10)  # Bottom right
        glVertex2f(char_x + self.width - 10, char_y + self.height - 5)  # Top right
        glVertex2f(char_x + 10, char_y + self.height - 5)  # Top left
        glEnd()
        
        # Body (shirt) - shortened to look seated
        glColor3f(0.2, 0.4, 0.8)  # Blue shirt
        glBegin(GL_QUADS)
        glVertex2f(char_x + 7, char_y + self.height - 25)  # Bottom left
        glVertex2f(char_x + self.width - 7, char_y + self.height - 25)  # Bottom right
        glVertex2f(char_x + self.width - 7, char_y + self.height - 10)  # Top right
        glVertex2f(char_x + 7, char_y + self.height - 10)  # Top left
        glEnd()
        
        # Legs (pants) - bent to look seated
        glColor3f(0.1, 0.1, 0.5)  # Dark blue pants
        
        # Left leg - bent at knee
        glBegin(GL_QUADS)
        glVertex2f(char_x + 10, char_y + 5)  # Foot
        glVertex2f(char_x + 15, char_y + 5)  # Foot
        glVertex2f(char_x + 15, char_y + self.height - 25)  # Hip
        glVertex2f(char_x + 10, char_y + self.height - 25)  # Hip
        glEnd()
        
        # Right leg - bent at knee
        glBegin(GL_QUADS)
        glVertex2f(char_x + self.width - 15, char_y + 5)  # Foot
        glVertex2f(char_x + self.width - 10, char_y + 5)  # Foot
        glVertex2f(char_x + self.width - 10, char_y + self.height - 25)  # Hip
        glVertex2f(char_x + self.width - 15, char_y + self.height - 25)  # Hip
        glEnd()
        
        # Arms - on wheelchair
        glColor3f(0.2, 0.4, 0.8)  # Same as shirt
        
        # Left arm on wheelchair
        glBegin(GL_QUADS)
        glVertex2f(char_x + 5, char_y + self.height - 25)  # Shoulder
        glVertex2f(char_x + 8, char_y + self.height - 25)  # Shoulder
        glVertex2f(char_x + 8, char_y + self.height - 15)  # Hand on wheel
        glVertex2f(char_x + 5, char_y + self.height - 15)  # Hand on wheel
        glEnd()
        
        # Right arm on wheelchair
        glBegin(GL_QUADS)
        glVertex2f(char_x + self.width - 8, char_y + self.height - 25)  # Shoulder
        glVertex2f(char_x + self.width - 5, char_y + self.height - 25)  # Shoulder
        glVertex2f(char_x + self.width - 5, char_y + self.height - 15)  # Hand on wheel
        glVertex2f(char_x + self.width - 8, char_y + self.height - 15)  # Hand on wheel
        glEnd()
        
        # Eyes
        glColor3f(0.1, 0.1, 0.1)  # Black eyes
        eye_x = char_x + 18 if self.facing_right else char_x + 12
        glPointSize(2.0)
        glBegin(GL_POINTS)
        glVertex2f(eye_x, char_y + self.height - 7)
        glEnd()
    
    def draw_wheelchair(self, x, y):
        """Draw a more realistic wheelchair."""
        # Dimensions
        wheel_radius = self.width * 0.35
        chair_width = self.width * 0.9
        
        # Wheels (larger, more detailed)
        wheel_centers = [
            (x + wheel_radius * 0.8, y + wheel_radius * 1.2),  # Left wheel
            (x + chair_width - wheel_radius * 0.8, y + wheel_radius * 1.2)  # Right wheel
        ]
        
        # Draw the wheels
        for wheel_center in wheel_centers:
            # Main wheel (black tire)
            glColor3f(0.1, 0.1, 0.1)  # Black
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(*wheel_center)  # Center
            for angle in range(0, 360, 10):
                rad_angle = math.radians(angle)
                glVertex2f(wheel_center[0] + wheel_radius * math.cos(rad_angle), 
                          wheel_center[1] + wheel_radius * math.sin(rad_angle))
            glEnd()
            
            # Inner wheel (silver/metallic)
            glColor3f(0.7, 0.7, 0.7)  # Silver
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(*wheel_center)  # Center
            for angle in range(0, 360, 10):
                rad_angle = math.radians(angle)
                glVertex2f(wheel_center[0] + wheel_radius * 0.85 * math.cos(rad_angle), 
                          wheel_center[1] + wheel_radius * 0.85 * math.sin(rad_angle))
            glEnd()
            
            # Spokes
            glColor3f(0.8, 0.8, 0.8)  # Light silver
            glLineWidth(1.5)
            glBegin(GL_LINES)
            for angle in range(0, 360, 30):
                rad_angle = math.radians(angle)
                glVertex2f(wheel_center[0], wheel_center[1])  # Center
                glVertex2f(wheel_center[0] + wheel_radius * 0.85 * math.cos(rad_angle), 
                          wheel_center[1] + wheel_radius * 0.85 * math.sin(rad_angle))
            glEnd()
            
            # Wheel rim highlight
            glColor3f(0.9, 0.9, 0.9)  # Almost white
            glLineWidth(1.0)
            glBegin(GL_LINE_LOOP)
            for angle in range(0, 360, 10):
                rad_angle = math.radians(angle)
                glVertex2f(wheel_center[0] + wheel_radius * 0.85 * math.cos(rad_angle), 
                          wheel_center[1] + wheel_radius * 0.85 * math.sin(rad_angle))
            glEnd()
            
            # Hand rim
            glColor3f(0.5, 0.5, 0.5)  # Gray
            glLineWidth(2.0)
            glBegin(GL_LINE_LOOP)
            for angle in range(0, 360, 10):
                rad_angle = math.radians(angle)
                glVertex2f(wheel_center[0] + wheel_radius * 0.7 * math.cos(rad_angle), 
                          wheel_center[1] + wheel_radius * 0.7 * math.sin(rad_angle))
            glEnd()
        
        # Draw small front casters (small wheels)
        caster_radius = wheel_radius * 0.25
        caster_centers = [
            (x + wheel_radius * 0.8, y + self.height * 0.2),  # Left caster
            (x + chair_width - wheel_radius * 0.8, y + self.height * 0.2)  # Right caster
        ]
        
        for caster_center in caster_centers:
            # Caster wheel
            glColor3f(0.3, 0.3, 0.3)  # Dark gray
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(*caster_center)  # Center
            for angle in range(0, 360, 15):
                rad_angle = math.radians(angle)
                glVertex2f(caster_center[0] + caster_radius * math.cos(rad_angle), 
                          caster_center[1] + caster_radius * math.sin(rad_angle))
            glEnd()
            
            # Caster fork
            glColor3f(0.5, 0.5, 0.5)  # Gray
            glLineWidth(1.5)
            glBegin(GL_LINES)
            glVertex2f(caster_center[0], caster_center[1])  # Center
            glVertex2f(caster_center[0], caster_center[1] + caster_radius * 2)  # Up to frame
            glEnd()
        
        # Chair frame
        frame_color = (0.3, 0.3, 0.8)  # Blue frame
        
        # Seat
        glColor3f(*frame_color)
        glBegin(GL_QUADS)
        glVertex2f(x + wheel_radius * 0.4, y + wheel_radius * 1.8)  # Back left
        glVertex2f(x + chair_width - wheel_radius * 0.4, y + wheel_radius * 1.8)  # Back right
        glVertex2f(x + chair_width - wheel_radius * 0.4, y + wheel_radius * 1.0)  # Front right
        glVertex2f(x + wheel_radius * 0.4, y + wheel_radius * 1.0)  # Front left
        glEnd()
        
        # Backrest
        glBegin(GL_QUADS)
        glVertex2f(x + wheel_radius * 0.4, y + wheel_radius * 1.8)  # Bottom left
        glVertex2f(x + chair_width - wheel_radius * 0.4, y + wheel_radius * 1.8)  # Bottom right
        glVertex2f(x + chair_width - wheel_radius * 0.4, y + wheel_radius * 3.0)  # Top right
        glVertex2f(x + wheel_radius * 0.4, y + wheel_radius * 3.0)  # Top left
        glEnd()
        
        # Footrests
        glColor3f(0.4, 0.4, 0.4)  # Dark gray
        glBegin(GL_QUADS)
        # Left footrest
        glVertex2f(x + wheel_radius * 0.5, y + self.height * 0.3)  # Bottom left
        glVertex2f(x + wheel_radius * 1.0, y + self.height * 0.3)  # Bottom right
        glVertex2f(x + wheel_radius * 1.0, y + self.height * 0.4)  # Top right
        glVertex2f(x + wheel_radius * 0.5, y + self.height * 0.4)  # Top left
        glEnd()
        
        glBegin(GL_QUADS)
        # Right footrest
        glVertex2f(x + chair_width - wheel_radius * 1.0, y + self.height * 0.3)  # Bottom left
        glVertex2f(x + chair_width - wheel_radius * 0.5, y + self.height * 0.3)  # Bottom right
        glVertex2f(x + chair_width - wheel_radius * 0.5, y + self.height * 0.4)  # Top right
        glVertex2f(x + chair_width - wheel_radius * 1.0, y + self.height * 0.4)  # Top left
        glEnd()
        
        # Armrests
        glColor3f(*frame_color)
        # Left armrest
        glBegin(GL_QUADS)
        glVertex2f(x + wheel_radius * 0.4, y + wheel_radius * 2.2)  # Bottom left
        glVertex2f(x + wheel_radius * 0.9, y + wheel_radius * 2.2)  # Bottom right
        glVertex2f(x + wheel_radius * 0.9, y + wheel_radius * 2.4)  # Top right
        glVertex2f(x + wheel_radius * 0.4, y + wheel_radius * 2.4)  # Top left
        glEnd()
        
        # Right armrest
        glBegin(GL_QUADS)
        glVertex2f(x + chair_width - wheel_radius * 0.9, y + wheel_radius * 2.2)  # Bottom left
        glVertex2f(x + chair_width - wheel_radius * 0.4, y + wheel_radius * 2.2)  # Bottom right
        glVertex2f(x + chair_width - wheel_radius * 0.4, y + wheel_radius * 2.4)  # Top right
        glVertex2f(x + chair_width - wheel_radius * 0.9, y + wheel_radius * 2.4)  # Top left
        glEnd()
        
        # Push handles
        glColor3f(0.2, 0.2, 0.2)  # Dark gray
        # Left handle
        glBegin(GL_QUADS)
        glVertex2f(x + wheel_radius * 0.5, y + wheel_radius * 3.0)  # Bottom
        glVertex2f(x + wheel_radius * 0.6, y + wheel_radius * 3.0)  # Bottom
        glVertex2f(x + wheel_radius * 0.6, y + wheel_radius * 3.3)  # Top
        glVertex2f(x + wheel_radius * 0.5, y + wheel_radius * 3.3)  # Top
        glEnd()
        
        # Right handle
        glBegin(GL_QUADS)
        glVertex2f(x + chair_width - wheel_radius * 0.6, y + wheel_radius * 3.0)  # Bottom
        glVertex2f(x + chair_width - wheel_radius * 0.5, y + wheel_radius * 3.0)  # Bottom
        glVertex2f(x + chair_width - wheel_radius * 0.5, y + wheel_radius * 3.3)  # Top
        glVertex2f(x + chair_width - wheel_radius * 0.6, y + wheel_radius * 3.3)  # Top
        glEnd()

class Scene:
    def __init__(self, obstacles):
        self.obstacles = obstacles  # Store obstacles in the scene

    def draw(self):
        """Draw the scene's background"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen
        
        draw_sky()
        draw_building(0, 50, 300, 600, (50/255.0, 50/255.0, 50/255.0))  
        draw_building(450, 50, 300, 400, (50/255.0, 50/255.0, 50/255.0)) 
        draw_pavement()
        
        # Draw all obstacles in the scene
        for obstacle in self.obstacles:
            obstacle.draw()


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
                step_y = self.y + (self.steps - i - 1) * self.step_height  # Move down for each step
                # Draw the filled area under the step
                glBegin(GL_QUADS)
                glColor3f(*base_color)
                glVertex2f(step_x, self.y)  # Bottom left of the filled area
                glVertex2f(step_x + self.step_width, self.y)  # Bottom right of the filled area
                glVertex2f(step_x + self.step_width, step_y)  # Top right of the filled area
                glVertex2f(step_x, step_y)  # Top left of the filled area
                glEnd()

            # Draw the step as a filled rectangle
            glBegin(GL_QUADS)
            glColor3f(*base_color)
            
            if self.direction == "up":
                step_y = self.y + (i * self.step_height)
            else:  # direction == "down"
                step_y = self.y + (self.steps - i - 1) * self.step_height
                
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
    def __init__(self, x, y, width, height, incline=True):  
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.incline = incline  # True = Incline, False = Decline

    def draw(self):
        """Draw the ramp as a triangle with incline or decline."""
        glColor3f(0.6, 0.3, 0.1)  
        glBegin(GL_TRIANGLES)
        if self.incline:
            glVertex2f(self.x, self.y)  # Bottom-left
            glVertex2f(self.x + self.width, self.y + self.height)  # Top-right
            glVertex2f(self.x + self.width, self.y)  # Bottom-right
        else:
            glVertex2f(self.x, self.y + self.height)  # Top-left
            glVertex2f(self.x + self.width, self.y)  # Bottom-right
            glVertex2f(self.x, self.y)  # Bottom-left
        glEnd()

    def collides_with(self, player):
        """Handles player collision with the ramp."""
        char_x = player.x
        char_bottom = player.window_height - (player.y + player.height)  

        # Check if character is within the horizontal range of the ramp
        if self.x <= char_x <= self.x + self.width:
            # Calculate ramp height at player's position
            progress = (char_x - self.x) / self.width  
            if not self.incline:
                progress = 1 - progress  # Flip calculation for declining ramps

            ramp_height_at_position = self.y + progress * self.height

            # If the character's bottom is at or below the ramp height
            if char_bottom <= ramp_height_at_position:
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
        self.bumps = 12  # Number of bumps
        self.bump_width = width / self.bumps
        
    def draw(self):
        """Draw a realistic-looking bumpy road with 3D effect."""
        # Draw the base road
        glBegin(GL_QUADS)
        glColor3f(0.3, 0.3, 0.3)  # Dark gray for the road base
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height/3)  # Lower height for base
        glVertex2f(self.x, self.y + self.height/3)
        glEnd()
        
        # Draw individual bumps
        for i in range(self.bumps):
            bump_x = self.x + i * self.bump_width
            
            # Vary the bump heights slightly for more natural look
            bump_height = self.height * (0.5 + 0.3 * math.sin(i * 0.8))
            
            # Draw the bump with shading
            glBegin(GL_QUADS)
            
            # Top of the bump (lighter color)
            glColor3f(0.5, 0.5, 0.5)  # Medium gray for top
            glVertex2f(bump_x, self.y + self.height/3)
            glVertex2f(bump_x + self.bump_width, self.y + self.height/3)
            glVertex2f(bump_x + self.bump_width, self.y + bump_height)
            glVertex2f(bump_x, self.y + bump_height)
            
            glEnd()
            
            # Draw highlight on top of bump
            glBegin(GL_QUADS)
            glColor3f(0.6, 0.6, 0.6)  # Light gray for highlight
            
            highlight_width = self.bump_width * 0.7
            highlight_x = bump_x + (self.bump_width - highlight_width) / 2
            
            glVertex2f(highlight_x, self.y + bump_height * 0.9)
            glVertex2f(highlight_x + highlight_width, self.y + bump_height * 0.9)
            glVertex2f(highlight_x + highlight_width, self.y + bump_height)
            glVertex2f(highlight_x, self.y + bump_height)
            glEnd()
            
            # Add crack details for realism
            if i % 3 == 0:  # Add a crack every few bumps
                glBegin(GL_LINES)
                glColor3f(0.1, 0.1, 0.1)  # Dark color for cracks
                
                start_x = bump_x + self.bump_width * 0.3
                end_x = bump_x + self.bump_width * 0.7
                crack_y = self.y + bump_height * 0.7
                
                glVertex2f(start_x, crack_y)
                glVertex2f(end_x, crack_y + self.height * 0.1)
                glEnd()

    def collides_with(self, player):
        # Convert character position to OpenGL coordinates
        char_x = player.x
        char_bottom = player.window_height - (player.y + player.height)
        
        # Check if character is horizontally within the bumpy road
        if char_x + player.width > self.x and char_x < self.x + self.width:
            # Calculate which bump the character is over
            bump_index = int((char_x - self.x) / self.bump_width)
            bump_index = min(bump_index, self.bumps - 1)  # Ensure index is in range
            
            # Calculate bump height at this position (using same formula as in draw)
            bump_x = self.x + bump_index * self.bump_width
            bump_height = self.height * (0.5 + 0.3 * math.sin(bump_index * 0.8))
            bump_y = self.y + bump_height
            
            # Character is colliding if its bottom is at or below the bump height
            if char_bottom <= bump_y:
                # Position the character on top of the bump
                player.y = player.window_height - bump_y - player.height
                player.velocity_y = 0
                player.on_ground = True
                
                # Add a small bumping effect when walking
                if player.velocity_y == 0:
                    # Small random up/down movement when on bumpy road
                    player.y += math.sin(pygame.time.get_ticks() * 0.01) * 1.5
                
                return True
        return False
    
class Pillar:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        """Draws the pillar."""
        """Draws a rectangular pillar as an obstacle."""
        glColor3f(0.6, 0.3, 0.1)  # Brownish pillar color
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)                      # Bottom-left
        glVertex2f(self.x + self.width, self.y)               # Bottom-right
        glVertex2f(self.x + self.width, self.y + self.height)      # Top-right
        glVertex2f(self.x, self.y + self.height)              # Top-left
        glEnd()

    def collides_with(self, player):
        """Handles collision with the player character."""
        char_x = player.x
        char_y = player.y
        char_width = player.width
        char_height = player.height

        # Check if the character is overlapping the pillar
        horizontal_overlap = (char_x + char_width > self.x and char_x < self.x + self.width)
        vertical_overlap = (char_y + char_height > self.y and char_y < self.y + self.height)

        if horizontal_overlap and vertical_overlap:
            # **Vertical Collision**: Landing on top of the pillar
            if player.velocity_y < 0 and char_y + char_height >= self.y:
                player.y = self.y + self.height
                player.velocity_y = 0
                player.on_ground = True
                return True

            # **Horizontal Collision**: Block movement when walking into the pillar
            if char_x + char_width >= self.x and player.x < self.x:  # Moving right
                player.x = self.x - char_width  # Stop at the left side of the pillar
            elif char_x <= self.x + self.width and player.x > self.x:  # Moving left
                player.x = self.x + self.width  # Stop at the right side of the pillar

            return True

        return False

#Dialgogue Box System
class DialogueBox:
    def __init__(self, text, x, y, width=700, height=100):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True  # Track visibility of the dialogue box
        self.created_time = pygame.time.get_ticks()  # Record when the box was created
        self.last_key_time = 0  # Time when the last key was processed

    def draw(self):
        if self.visible:
            # Enable transparency for the dialogue box
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            
            # Draw the box background
            glColor4f(0.0, 0.0, 0.0, 0.7)  # Semi-transparent black (RGBA)
            glBegin(GL_QUADS)
            glVertex2f(self.x, self.y)
            glVertex2f(self.x + self.width, self.y)
            glVertex2f(self.x + self.width, self.y + self.height)
            glVertex2f(self.x, self.y + self.height)
            glEnd()
            
            glDisable(GL_BLEND)  # Disable transparency after drawing

            # Render the text inside the box
            render_text(self.text, self.x + 10, self.y + self.height - 30, size=24)  # Adjust position for padding
            
            # Add a "Press ENTER to continue" prompt
            render_text("Press ENTER to continue", self.x + 10, self.y + 20, size=18)

    def dismiss(self):
        self.visible = False  # Hide the dialogue box

class ManageDialogue:
    def __init__(self):
        self.dialogue_boxes = []  # List to hold dialogue boxes
        self.current_dialogue_index = 0  # Track the current dialogue box being displayed
        self.last_key_press_time = 0  # To prevent multiple key presses
        self.scene_dialogues = {}  # Dictionary to store dialogues for different scenes
        self.location_dialogues = {}  # Dictionary to store dialogues for specific locations
        self.shown_dialogues = set()  # Track already shown dialogues
        
        # Add initial dialogue boxes
        self.add_dialogue_box("welcome", "Welcome to WheelAware!", 10, 450)
        # Set up scene-specific dialogues
        self.setup_scene_dialogues()
        self.setup_location_dialogues()

    def setup_scene_dialogues(self):
        """Set up dialogues for each scene transition"""
        self.scene_dialogues[0] = [
            {"id": "scene0_controls", "text": "Use arrow keys to move your character.", "x": 10, "y": 450},
            {"id": "scene0_jump", "text": "and press SPACE to jump.", "x": 10, "y": 450},
            {"id": "scene0_intro", "text": "Scene 1: A Young Diagnosis", "x": 10, "y": 450},
            {"id": "scene0_1", "text": "This young patient was recently diagnosed with Multiple Sclerosis.", "x": 10, "y": 450},
            {"id": "scene0_2", "text": "Multiple Sclerosis (MS) is a chronic condition affecting the nervous system.", "x": 10, "y": 450},
            {"id": "scene0_3", "text": "At first, MS symptoms might seem mild.", "x": 10, "y": 450},
            {"id": "scene0_4", "text": "Many young people with MS can walk, run, and live actively.", "x": 10, "y": 450},
            {"id": "scene0_4", "text": "But movement can become more difficult over time.", "x": 10, "y": 450},
            {"id": "scene0_5", "text": "Mission 1: Climb the stairs", "x": 10, "y": 450}
        ]
        self.scene_dialogues[1] = [
            {"id": "scene1_intro", "text": "Keep going!", "x": 10, "y": 450},
        ]
        self.scene_dialogues[2] = [
            {"id": "scene2_intro", "text": "A few bumps won’t slow him down. Not yet.", "x": 10, "y": 450},
            {"id": "scene2_ms", "text": "MS can cause balance issues, making uneven surfaces challenging, even at this young age.", "x": 10, "y": 450},
            {"id": "scene0_5", "text": "Mission 2: Cross the uneven road", "x": 10, "y": 450}
        ]
    # part 2 (wheelchair transition)
        self.scene_dialogues[3] = [
            {"id": "scene3_transition", "text": "Years have passed. Your MS has progressed.", "x": 10, "y": 450},
            {"id": "scene3_wheelchair1", "text": "Due to arising symptoms like muscle weakness and balance problems...", "x": 10, "y": 450},
            {"id": "scene3_wheelchair2", "text": "...You now use a wheelchair to get around.", "x": 10, "y": 450},
            {"id": "scene3_controls", "text": "Use LEFT and RIGHT arrow keys to move. You can no longer jump.", "x": 10, "y": 450},
            {"id": "scene3_ramps", "text": "Ramps are now your best friend for navigating obstacles.", "x": 10, "y": 450}
        ]
        self.scene_dialogues[4] = [
            {"id": "scene4_transition", "text": "Uneven roads are harder to pass now.", "x": 10, "y": 450}
        ]
        self.scene_dialogues[5] = [
            {"id": "scene5_transition", "text": "Multiple Sclerosis affects mobility over time. Simple tasks can become difficult.", "x": 10, "y": 450},
            {"id": "scene5_transition1", "text": "Climbing these stairs was easy a long time ago...", "x": 10, "y": 450},
            {"id": "scene5_transition2", "text": "...but now, they're an imposible barrier.", "x": 10, "y": 450},
            {"id": "scene5_transition3", "text": "Sadly, many places forget about accessibility. ", "x": 10, "y": 450},
            {"id": "scene5_transition4", "text": "Options like ramps and elevators, should be available everywhere. ", "x": 10, "y": 450},
            {"id": "scene5_transition5", "text": "Caring about MS means caring about making spaces open to everyone.", "x": 10, "y": 450},
            {"id": "scene5_transition6", "text": "Accessibility isn't a privilege—it's a necessity. ", "x": 10, "y": 450},
            {"id": "scene5_transition7", "text": "Thank You For Playing.", "x": 10, "y": 450}
        ]

    def setup_location_dialogues(self):
        """Set up dialogues for specific locations within scenes"""
        # Scene 0 locations
        self.location_dialogues[0] = [ 
            {"id": "stairs_top", "x_range": (600, 800), "text": "Great! That was easy.", "x": 10, "y": 450},
            
        ]
    def add_dialogue_box(self, dialogue_id, text, x, y):
        """Add a new dialogue box to the list."""
        new_box = DialogueBox(text, x, y)
        self.dialogue_boxes.append({"id": dialogue_id, "box": new_box})

    def show_dialogue(self, dialogue_id):
        """Show a specific dialogue by ID"""
        # Hide any currently visible dialogue
        self.dismiss_current_dialogue()
        
        # Find and show the requested dialogue
        for i, dialogue in enumerate(self.dialogue_boxes):
            if dialogue["id"] == dialogue_id and dialogue_id not in self.shown_dialogues:
                dialogue["box"].visible = True
                self.current_dialogue_index = i
                self.shown_dialogues.add(dialogue_id)
                return True
        
        return False

    def dismiss_current_dialogue(self):
        """Dismiss the currently visible dialogue"""
        if 0 <= self.current_dialogue_index < len(self.dialogue_boxes):
            self.dialogue_boxes[self.current_dialogue_index]["box"].dismiss()

    def check_scene_dialogues(self, scene_index):
        """Check if there are dialogues to show for the current scene"""
        if scene_index in self.scene_dialogues:
            for dialogue_info in self.scene_dialogues[scene_index]:
                if dialogue_info["id"] not in self.shown_dialogues:
                    self.add_dialogue_box(dialogue_info["id"], dialogue_info["text"], dialogue_info["x"], dialogue_info["y"])
                    self.show_dialogue(dialogue_info["id"])
                    return True
        return False

    def check_location_dialogues(self, scene_index, player_x):
        """Check if there are dialogues to show for the current location"""
        if scene_index in self.location_dialogues:
            for dialogue_info in self.location_dialogues[scene_index]:
                x_min, x_max = dialogue_info["x_range"]
                if x_min <= player_x <= x_max and dialogue_info["id"] not in self.shown_dialogues:
                    self.add_dialogue_box(dialogue_info["id"], dialogue_info["text"], dialogue_info["x"], dialogue_info["y"])
                    self.show_dialogue(dialogue_info["id"])
                    return True
        return False

    def update(self, events, scene_index, player_x):
        """Update the game state, including dialogue box management."""
        current_time = pygame.time.get_ticks()
        
        # Always check for location-based dialogues first
        self.check_location_dialogues(scene_index, player_x)
        
        # Process key presses for dialogue boxes
        for event in events:
            if event.type == KEYDOWN and event.key == K_RETURN:
                # Only process if enough time has passed since the last key press (prevents multiple triggers)
                if current_time - self.last_key_press_time > 300:  # 300ms delay
                    if self.current_dialogue_index < len(self.dialogue_boxes):
                        # Dismiss current dialogue box
                        self.dismiss_current_dialogue()
                        self.last_key_press_time = current_time
                        
                        # Always check for scene dialogues after dismissing current dialogue
                        self.check_scene_dialogues(scene_index)

    def draw(self):
        """Draw the current dialogue box if it exists."""
        if 0 <= self.current_dialogue_index < len(self.dialogue_boxes):
            self.dialogue_boxes[self.current_dialogue_index]["box"].draw()

class GameScenes:
    def __init__(self):
        self.player = Character(50, 100, 800, 600, character_type="walking")  # Start with walking character
        self.current_scene_index = 0  # Start with the first scene
        self.previous_scene_index = 0  # Track the previous scene
        self.scenes = [
            # Part 1
            Scene([Stair(150, 50, 550, 350), Pillar(700,50,150,350)]),  
            Scene([Pillar(0, 50, 150, 350), Stair(150, 50, 550, 350, 10,"down")]), 
            Scene([BumpyRoad(100,50,100,20), BumpyRoad(250,50,100,20), BumpyRoad(400,50,100,20), BumpyRoad(550,50,100,20)]), 
            # Part 2
            Scene([Ramp(150, 50, 700, 50, True)]), 
            Scene([BumpyRoad(100,50,100,20), BumpyRoad(250,50,100,20), BumpyRoad(400,50,100,20), BumpyRoad(550,50,100,20)]),
            Scene([Stair(150, 50, 550, 350), Pillar(700,50,150,350)])

        ]
        self.scene_change = False  # Flag to track scene changes
        self.wheelchair_transition_triggered = False  # Flag to track if we've done the wheelchair transition
        
    def update(self, keys):
        self.previous_scene_index = self.current_scene_index
        current_scene = self.scenes[self.current_scene_index]
        self.player.move(keys, current_scene.obstacles)  # Pass obstacles, not the entire scene

        # Scene transition logic
        if self.player.x > 750:
            self.current_scene_index = (self.current_scene_index + 1) % len(self.scenes)
            self.player.x = 50  # Reset position to the left side
            self.scene_change = True
            
            # Check if we're transitioning from scene 3 to scene 4 (index 2 to 3)
            if self.previous_scene_index == 2 and self.current_scene_index == 3 and not self.wheelchair_transition_triggered:
                # Change to wheelchair character
                self.player.character_type = "wheelchair"
                self.wheelchair_transition_triggered = True
                # Could add special dialogue here
                
        else:
            self.scene_change = False

    def draw(self):
        """Draw the current scene and player."""
        self.scenes[self.current_scene_index].draw()  # Draw scene
        self.player.draw()  # Draw character

def main():
    global game_state
    running = True
    clock = pygame.time.Clock()
    game_scene = GameScenes()
    game = ManageDialogue()  # Initialize the game with dialogue boxes

    while running:
        keys = pygame.key.get_pressed()
        events = pygame.event.get()  # Collect all events once per frame
        
        # Check for quit event in all game states
        for event in events:
            if event.type == QUIT:
                running = False
                pygame.quit()
                return

        if game_state == TITLE_SCREEN:
            draw_title_screen()
            handle_title_screen_events()
        
        elif game_state == GAMEPLAY:
            # Update the game state
            game_scene.update(keys)
            
            # Check for scene changes - trigger relevant dialogues
            if game_scene.scene_change:
                game.check_scene_dialogues(game_scene.current_scene_index)
            
            # Update dialogue based on player position and current scene
            game.update(events, game_scene.current_scene_index, game_scene.player.x)
            
            # Draw everything
            game_scene.draw()        
            game.draw()
            
            pygame.display.flip()  # Update the display

        clock.tick(60)

if __name__ == "__main__":
    main()