#Project Name: WheelAware
#Ahmed Saeed Ahmed Mohamed - 202211615
#Kazi Mahir Al Wafi - 202211829

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

# Initialize Pygame and OpenGL
pygame.init()
glutInit()
display_width, display_height = 800, 600
pygame.display.set_mode((display_width, display_height), DOUBLEBUF | OPENGL)  
glEnable(GL_DEPTH_TEST)  # Enable depth testing
glDepthFunc(GL_LESS)  # Specify depth test function
glClearColor(0.0, 0.0, 0.0, 1.0)  # Set clear color (black)

def setup_2d():
    """Set up 2D rendering with correct coordinates"""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Use bottom-left origin for consistency with OpenGL
    gluOrtho2D(0, 800, 0, 600)  
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)

def setup_3d():
    """Set up 3D rendering"""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (800/600), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)

def draw_3d_cube(angle):
    """Draw a rotating yellow sphere-like sun"""
    setup_3d()  # Switch to 3D mode
    
    glPushMatrix()
    glLoadIdentity()
    
    # Position in top right corner
    glTranslatef(2.7, 1.8, -5.0)
    # Make the sun smaller
    glScalef(0.5, 0.5, 0.5)
    # Rotate the sun
    glRotatef(angle, 1, 1, 0)

    # Draw a more spherical sun with more faces
    segments = 15  # Increase this number for more smoothness
    rings = 15    # Increase this number for more smoothness

    # Draw the sphere using triangle strips
    for i in range(rings):
        lat0 = math.pi * (-0.5 + float(i) / rings)
        z0 = math.sin(lat0)
        zr0 = math.cos(lat0)

        lat1 = math.pi * (-0.5 + float(i + 1) / rings)
        z1 = math.sin(lat1)
        zr1 = math.cos(lat1)

        glBegin(GL_TRIANGLE_STRIP)
        for j in range(segments + 1):
            lng = 2 * math.pi * float(j) / segments

            x = math.cos(lng)
            y = math.sin(lng)

            # Vary colors for a sun-like appearance
            intensity = 0.8 + 0.2 * math.cos(lng) * math.cos(lat0)
            glColor3f(1.0 * intensity, 1.0 * intensity, 0.0)  # Yellow with shading
            glVertex3f(x * zr0, y * zr0, z0)

            intensity = 0.8 + 0.2 * math.cos(lng) * math.cos(lat1)
            glColor3f(1.0 * intensity, 1.0 * intensity, 0.0)  # Yellow with shading
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

    glPopMatrix()
    setup_2d()  # Switch back to 2D mode

def draw_building(x, y, width, height, color):
    """Draw building with transformations and shadow"""
    glPushMatrix()
    
    # Move to position
    glTranslatef(x, y, 0)
    
    
    # Scale the building
    glScalef(1.0, height/100.0, 1.0) 
    
    # Draw building relative to origin
    vertices = [
        (0, 0),  # Bottom left
        (width, 0),  # Bottom right
        (width, 100),  # Top right
        (0, 100)  # Top left
    ]
    
    # Draw main building
    glBegin(GL_QUADS)
    glColor3f(*color)
    for vertex in vertices:
        glVertex2f(*vertex)
    glEnd()
    
    # Draw shadow with rotation
    shadow_width = width * 0.2
    shadow_color = (color[0] * 0.5, color[1] * 0.5, color[2] * 0.5)
    
    glBegin(GL_QUADS)
    glColor3f(*shadow_color)
    glVertex2f(width, 0)
    glVertex2f(width + shadow_width, 0)
    glVertex2f(width + shadow_width, 100)
    glVertex2f(width, 100)
    glEnd()
    
    glPopMatrix()

# Function to draw windows
def draw_window(x, y, width, height):
    """Draw window with the same static rotation as buildings"""
    glPushMatrix()
    
    # Move to position
    glTranslatef(x, y, 0)

    
    # Draw the window
    vertices = [
        (0, 0),
        (width, 0),
        (width, height),
        (0, height)
    ]
    
    glBegin(GL_QUADS)
    glColor3f(232/255.0, 175/255.0, 131/255.0)  # Light brown color for window
    for vertex in vertices:
        glVertex2f(*vertex)
    glEnd()
    
    glPopMatrix()

def draw_streetlight(x, y):    
    # Draw the pole
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.5, 0.5)  # Pole color
    glVertex2f(x, y)
    glVertex2f(x + 5, y)
    glVertex2f(x + 5, y + 150)
    glVertex2f(x, y + 150)
    glEnd()

    # Draw light fixture
    glColor3f(1.0, 1.0, 0.0)  # Normal bright light
    glBegin(GL_QUADS)
    glVertex2f(x - 10, y + 150)
    glVertex2f(x + 15, y + 150)
    glVertex2f(x + 15, y + 160)
    glVertex2f(x - 10, y + 160)
    glEnd()

    # Enable transparency for the light cone with rotation
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0, 1.0, 0.0, 0.2)  # Soft yellow light with transparency

    # Save current transformation matrix
    glPushMatrix()
    
    # Translate to light source point, rotate, then translate back
    glTranslatef(x + 2.5, y + 155, 0)  # Move to light source
    glRotatef(-13, 0, 0, 1)  # Rotate 15 degrees counter-clockwise (adjust angle as needed)
    glTranslatef(-(x + 2.5), -(y + 155), 0)  # Move back
    
    # Draw the rotated cone-shaped light
    glBegin(GL_TRIANGLES)
    glVertex2f(x + 2.5, y + 155)  # Light source
    glVertex2f(x - 30, 50)  # Left side of light on pavement
    glVertex2f(x + 35, 50)  # Right side of light on pavement
    glEnd()
    
    # Restore transformation matrix
    glPopMatrix()
    
    glDisable(GL_BLEND)  # Disable transparency after drawing

# Function to draw pavement
def draw_pavement():
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)
    # Draw from bottom up
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

class Character:
    def __init__(self, x, y, window_width, window_height, width=30, height=50, character_type="walking"):
        self.x = x
        self.y = window_height - y - height  # This flips the y-coordinate
        self.width = width
        self.height = height

        # Different speeds for different character types
        if character_type == "walking":
            self.base_speed = 5  # Normal walking speed
            self.speed = self.base_speed
        else:  # wheelchair
            self.base_speed = 1 # Slower base speed for wheelchair
            self.speed = self.base_speed 

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

    def move(self, keys, obstacles, current_scene_index=0):  # Add scene index parameter
        # If in the last scene (index 5), prevent all movement
        if current_scene_index == 5:
            return

        # Rest of the movement code remains the same
        original_x = self.x
        original_y = self.y
        
        # Update animation time
        self.animation_time += 1
        if self.animation_time > 10:
            self.animation_frame = (self.animation_frame + 1) % 4
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
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        #Draw the sky gradient
        draw_sky()

        #Draw clouds
        draw_cloud(200, 450, 30)
        draw_cloud(400, 480, 40)
        draw_cloud(600, 450, 35)
        draw_cloud(300, 500, 25)

        # Draw background buildings (back layer)
        # y-coordinate should be close to ground level (50), height extends upward
        draw_building(0, 50, 100, 400, (105/255.0, 105/255.0, 105/255.0))      # Taller building
        draw_building(150, 50, 120, 350, (105/255.0, 105/255.0, 105/255.0))    # Medium height
        draw_building(400, 50, 120, 500, (105/255.0, 105/255.0, 105/255.0))    # Very tall building
        draw_building(600, 50, 120, 200, (105/255.0, 105/255.0, 105/255.0))    # Shorter building
        draw_building(700, 50, 120, 350, (105/255.0, 105/255.0, 105/255.0))    # Medium-tall building

        # Draw front buildings (darker)
        draw_building(100, 50, 100, 300, (50/255.0, 50/255.0, 50/255.0))       # Tall dark building
        draw_building(250, 50, 150, 250, (50/255.0, 50/255.0, 50/255.0))       # Medium dark building
        draw_building(450, 50, 200, 200, (50/255.0, 50/255.0, 50/255.0))       # Medium-tall dark building
        draw_building(700, 50, 80, 340, (50/255.0, 50/255.0, 50/255.0))        # Another tall dark building
        # Draw windows on buildings
        for i in range(3):
            # Building 1 windows
            height = 310
            while height > 50:
                draw_window(117 + i * 25, height, 15, 15)
                height = height - 30
            
            # Building 2 windows
            draw_window(270 + i * 45, 250, 20, 30)
            draw_window(270 + i * 45, 200, 20, 30)
            draw_window(270 + i * 45, 150, 20, 30)
            draw_window(270 + i * 45, 100, 20, 30)

            # Building 3 windows
            draw_window(550 + i * 35, 180, 20, 50)
            draw_window(550 + i * 35, 100, 20, 50)

            # Building 4 windows
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

        # Draw road and pavement last
        draw_road()
        draw_pavement()
        
        for obstacle in self.obstacles:
            obstacle.draw()
    


class Stair:
    def __init__(self, x, y, width, height, steps=10, direction="up", color= (0.5,0.5,0.5)): 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.steps = steps  # Number of steps in the staircase
        self.direction = direction  # Direction of the stair (up or down)
        self.color = color
        
        # Calculate dimensions for each step
        self.step_width = width / steps
        self.step_height = height / steps
    
    def draw(self):
        """Draw a staircase with the specified number of steps."""
        # Base color for the stairs
        
        
        # Draw the filled area under each step
        for i in range(self.steps):
            step_x = self.x + i * self.step_width
            if self.direction == "up":
                step_y = self.y + (i * self.step_height)  # Move up for each step
                # Draw the filled area under the step
                glBegin(GL_QUADS)
                glColor3f(*self.color)
                glVertex2f(step_x, self.y)  # Bottom left of the filled area
                glVertex2f(step_x + self.step_width, self.y)  # Bottom right of the filled area
                glVertex2f(step_x + self.step_width, step_y)  # Top right of the filled area
                glVertex2f(step_x, step_y)  # Top left of the filled area
                glEnd()
            elif self.direction == "down":
                step_y = self.y + (self.steps - i - 1) * self.step_height  # Move down for each step
                # Draw the filled area under the step
                glBegin(GL_QUADS)
                glColor3f(*self.color)
                glVertex2f(step_x, self.y)  # Bottom left of the filled area
                glVertex2f(step_x + self.step_width, self.y)  # Bottom right of the filled area
                glVertex2f(step_x + self.step_width, step_y)  # Top right of the filled area
                glVertex2f(step_x, step_y)  # Top left of the filled area
                glEnd()

            # Draw the step as a filled rectangle
            glBegin(GL_QUADS)
            glColor3f(*self.color)
            
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
    def __init__(self, x, y, width, height, incline=True, color=((0.5, 0.5, 0.5))):  
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.incline = incline  # True = Incline, False = Decline
        self.color = color

    def draw(self):
        """Draw the ramp as a triangle with incline or decline."""
        glColor3f(*self.color)  
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
                
                # Slow down wheelchair user
                if player.character_type == "wheelchair":
                    # Store original speed if not already stored
                    if not hasattr(player, 'original_speed'):
                        player.original_speed = player.speed
                    # Reduce speed while on bumpy road
                    player.speed = player.original_speed * 0.7  # Reduce speed by 70%
                
                # Add a small bumping effect when moving
                if player.velocity_y == 0:
                    # More pronounced bumping for wheelchair
                    bump_intensity = 2.0 if player.character_type == "wheelchair" else 1.5
                    player.y += math.sin(pygame.time.get_ticks() * 0.01) * bump_intensity
                
                return True
        
        # When not on bumpy road, restore original speed if character is wheelchair user
        if player.character_type == "wheelchair" and hasattr(player, 'original_speed'):
            player.speed = player.original_speed
            
        return False
    
class Pillar:
    def __init__(self, x, y, width, height, color= (0.5,0.5,0.5)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        """Draws the pillar."""
        """Draws a rectangular pillar as an obstacle."""
        glColor3f(*self.color)
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
            {"id": "scene0_color1", "text": "You can change color of obstacles by pressing on the following keys: ", "x": 10, "y": 450},
            {"id": "scene0_color2", "text": "G --> Grey(Default) R-->Red Y-->Yellow", "x": 10, "y": 450},
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
            {"id": "scene2_intro", "text": "A few bumps won’t slow him down much. Not yet.", "x": 10, "y": 450},
            {"id": "scene2_ms", "text": "MS can cause balance issues, making uneven surfaces challenging,... ", "x": 10, "y": 450},
             {"id": "scene2_ms", "text": "...even at this young age.", "x": 10, "y": 450},
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
            {"id": "scene5_transition2", "text": "Especially with the lack of accibilty in many public spaces...", "x": 10, "y": 450},
            {"id": "scene5_transition2", "text": "...like the missing ramp here.", "x": 10, "y": 450},
            {"id": "scene5_transition3", "text": "Sadly, many places still forget about accessibility. ", "x": 10, "y": 450},
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

class Coin:
    def __init__(self, x, y, size=30):
        self.x = x
        self.y = y
        self.size = size
        self.collected = False
        self.scale = 1.0
        self.alpha = 1.0  # Transparency for fade-out effect
        self.rotation = 0  # Track rotation angle
        self.oscillation = 0  # For up/down floating effect
        
    def update(self):
        # Update rotation for spinning effect
        self.rotation = (self.rotation + 2) % 360
        
        # Add floating oscillation
        self.oscillation = math.sin(pygame.time.get_ticks() * 0.002) * 5
        
        if self.collected:
            # If collected, increase size and fade out
            self.scale += 0.05
            self.alpha -= 0.05
            
    def draw(self):
        if self.collected and self.alpha <= 0:
            return  # Fully disappeared
            
        self.update()
        
        # Enable blending for transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Save the current matrix
        glPushMatrix()
        
        # Move to coin position including oscillation for floating effect
        coin_center_x = self.x + self.size/2
        coin_center_y = self.y + self.size/2 + self.oscillation
        
        # Translate to center point for rotation
        glTranslatef(coin_center_x, coin_center_y, 0)
        
        # Apply rotation around Y axis (simulated with scaling)
        rot_rad = math.radians(self.rotation)
        # Scale X based on rotation to simulate perspective
        scale_x = abs(math.cos(rot_rad)) * 0.7 + 0.3  # Range from 0.3 to 1.0
        
        # Apply scaling
        glScalef(scale_x * self.scale, 1.0 * self.scale, 1.0)
        
        # Draw main coin body (gold)
        self.draw_3d_coin(0, 0, self.size/2, self.alpha)
        
        # Restore the matrix
        glPopMatrix()
        
        glDisable(GL_BLEND)
        
    def draw_3d_coin(self, cx, cy, radius, alpha):
        """Draw a 3D-looking coin with proper shading"""
        segments = 30
        inner_radius = radius * 0.85
        
        # Draw outer edge (rim) - slightly darker gold
        glBegin(GL_TRIANGLE_STRIP)
        rim_color = (0.8, 0.6, 0.0, alpha)  # Darker gold for edge
        face_color = (1.0, 0.8, 0.0, alpha)  # Brighter gold for face
        
        for i in range(segments + 1):
            angle = 2.0 * math.pi * i / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            x_inner = inner_radius * math.cos(angle)
            y_inner = inner_radius * math.sin(angle)
            
            # Edge point
            glColor4f(*rim_color)
            glVertex2f(x, y)
            
            # Inner face point
            glColor4f(*face_color)
            glVertex2f(x_inner, y_inner)
        glEnd()
        
        # Draw coin face
        glBegin(GL_TRIANGLE_FAN)
        # Center is bright
        glColor4f(1.0, 0.9, 0.2, alpha)
        glVertex2f(0, 0)
        
        # Edges are slightly darker
        glColor4f(0.9, 0.75, 0.1, alpha)
        for i in range(segments + 1):
            angle = 2.0 * math.pi * i / segments
            x = inner_radius * math.cos(angle)
            y = inner_radius * math.sin(angle)
            glVertex2f(x, y)
        glEnd()
        
        # Draw a reflective highlight
        self.draw_highlight(0, 0, radius * 0.5, alpha)
    
    def draw_highlight(self, cx, cy, radius, alpha):
        """Draw a highlight on the coin to enhance 3D appearance"""
        segments = 20
        rot_rad = math.radians(self.rotation)
        
        # Highlight position shifts with rotation for 3D effect
        highlight_x = radius * 0.5 * math.cos(rot_rad)
        highlight_y = radius * 0.5 * math.sin(rot_rad)
        
        glBegin(GL_TRIANGLE_FAN)
        # Bright center
        glColor4f(1.0, 1.0, 1.0, alpha * 0.7)
        glVertex2f(highlight_x, highlight_y)
        
        # Faded edges for smooth highlight
        glColor4f(1.0, 1.0, 1.0, 0.0)
        for i in range(segments + 1):
            angle = 2.0 * math.pi * i / segments
            x = highlight_x + (radius * 0.3) * math.cos(angle)
            y = highlight_y + (radius * 0.3) * math.sin(angle)
            glVertex2f(x, y)
        glEnd()

    def collides_with(self, player):
        """Detect collision with the player."""
        if self.collected:
            return False
            
        # Convert player coordinates to match the OpenGL coordinate system
        # In OpenGL y increases upward, but your player position y increases downward
        player_y_converted = player.window_height - player.y - player.height
        
        # Center of the coin
        coin_center_x = self.x + self.size/2
        coin_center_y = self.y + self.size/2 + self.oscillation  # Include oscillation
        
        # Check if the player's bounding box overlaps with the coin's circle
        # Find the closest point on the rectangle to the circle's center
        closest_x = max(player.x, min(coin_center_x, player.x + player.width))
        closest_y = max(player_y_converted, min(coin_center_y, player_y_converted + player.height))
        
        # Calculate distance between closest point and circle's center
        distance_x = coin_center_x - closest_x
        distance_y = coin_center_y - closest_y
        distance = math.sqrt(distance_x * distance_x + distance_y * distance_y)
        
        # Collision occurs if distance is less than circle's radius
        if distance < self.size/2:
            self.collected = True
            return True
            
        return False

class GameScenes:
    def __init__(self):
        self.player = Character(50, 100, 800, 600, character_type="walking")  # Start with walking character
        self.current_scene_index = 0  # Start with the first scene
        self.previous_scene_index = 0  # Track the previous scene
        self.scenes = [
            # Part 1 (walking) 
            Scene([Stair(150, 50, 550, 350), Pillar(700,50,150,350), Coin(270, 170), Coin(430, 270), Coin(600, 370)]),  
            Scene([Pillar(0, 50, 150, 350), Stair(150, 50, 550, 350, 10,"down"),  Coin(610, 150), Coin(440, 250), Coin(270, 350),  Coin(750, 70)]),
            Scene([BumpyRoad(100,50,100,20),Coin(135, 80), BumpyRoad(250,50,100,20),Coin(285, 80), BumpyRoad(400,50,100,20),Coin(440, 80), BumpyRoad(550,50,100,20), Coin(590, 80)]), 
            # Part 2 (wheelchair)
            Scene([Ramp(150, 50, 700, 50, True)]), 
            Scene([BumpyRoad(100,50,100,20),Coin(135, 80), BumpyRoad(250,50,100,20),Coin(285, 80), BumpyRoad(400,50,100,20),Coin(440, 80), BumpyRoad(550,50,100,20), Coin(590, 80)]), 
            Scene([Stair(150, 50, 550, 350), Pillar(700,50,150,350)])
        ]
        self.scene_change = False  # Flag to track scene changes
        self.wheelchair_transition_triggered = False  # Flag to track if we've done the wheelchair transition
        
    def update(self, keys):
        self.previous_scene_index = self.current_scene_index
        current_scene = self.scenes[self.current_scene_index]
        # Pass the current scene index to the move method
        self.player.move(keys, current_scene.obstacles, self.current_scene_index)

        # Update coins in the current scene and check for collisions
        coins_to_remove = []
        for obstacle in current_scene.obstacles:
            if isinstance(obstacle, Coin):
                # Check for collision with player
                obstacle.collides_with(self.player)
                
                # Mark fully faded coins for removal
                if obstacle.collected and obstacle.alpha <= 0:
                    coins_to_remove.append(obstacle)
        
        # Remove fully faded coins
        for coin in coins_to_remove:
            current_scene.obstacles.remove(coin)

        # Scene transition logic
        if self.player.x > 750:
            self.current_scene_index = (self.current_scene_index + 1) % len(self.scenes)
            self.player.x = 50
            self.scene_change = True
            
            # Check if we're transitioning from scene 3 to scene 4 (index 2 to 3)
            if self.previous_scene_index == 2 and self.current_scene_index == 3 and not self.wheelchair_transition_triggered:
                # Change to wheelchair character
                self.player.character_type = "wheelchair"
                self.player.base_speed = 2  # Set slower base speed
                self.player.speed = self.player.base_speed  # Update current speed
                self.wheelchair_transition_triggered = True
                
        else:
            self.scene_change = False

    def draw(self):
        """Draw the current scene and player."""
        # Get the current scene and draw its background first
        current_scene = self.scenes[self.current_scene_index]
        current_scene.draw()  # This assumes Scene class has a draw_background method
        
        # Then draw all obstacles including coins
        for obstacle in current_scene.obstacles:
            obstacle.draw()
        
        # Draw the player
        self.player.draw()

def main():
    pygame.init()
    glutInit()
    screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("WheelAware")
    
    # Initialize game objects
    game_scene = GameScenes()
    game = ManageDialogue()
    
    angle = 0
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Clear both color and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Handle events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        # Get keyboard state
        keys = pygame.key.get_pressed()

        # User can press on Y, G, R to change colors of the stair, ramp, and pillar (Yellow, Grey, Red)
        if keys[pygame.K_r]: #if R key is pressed
            for obj in game_scene.scenes[game_scene.current_scene_index].obstacles:
                if isinstance(obj, Stair):
                    obj.color = (0.5, 0.0, 0.0) # Change stair to red
                elif isinstance(obj, Ramp):
                    obj.color = (0.5, 0.0, 0.0) # Change ramp to red
                elif isinstance(obj, Pillar):
                    obj.color = (0.5, 0.0, 0.0)  # Change ramp to red
        if keys[pygame.K_y]: #if R key is pressed
            for obj in game_scene.scenes[game_scene.current_scene_index].obstacles:
                if isinstance(obj, Stair):
                    obj.color = (0.85, 0.65, 0.13) # Change stair to red
                elif isinstance(obj, Ramp):
                    obj.color = (0.85, 0.65, 0.13)  # Change ramp to red
                elif isinstance(obj, Pillar):
                    obj.color = (0.85, 0.65, 0.13)  # Change ramp to red
        if keys[pygame.K_g]: #if R key is pressed
            for obj in game_scene.scenes[game_scene.current_scene_index].obstacles:
                if isinstance(obj, Stair):
                    obj.color = (0.5,0.5,0.5)  # Change stair to red
                elif isinstance(obj, Ramp):
                    obj.color = (0.5,0.5,0.5)  # Change ramp to red
                elif isinstance(obj, Pillar):
                    obj.color = (0.5,0.5,0.5)  # Change ramp to red

        # Set up 2D rendering with bottom-left origin
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, 800, 0, 600)  # Changed to use bottom-left origin
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Update and draw game elements
        game_scene.update(keys)
        if game_scene.scene_change:
            game.check_scene_dialogues(game_scene.current_scene_index)
        game.update(events, game_scene.current_scene_index, game_scene.player.x)
        
        # Draw game elements (this will draw the background with proper building heights)
        game_scene.draw()
        game.draw()
        
        # Draw 3D sun cube
        setup_3d()
        draw_3d_cube(angle)
        angle += 1
        
        # Return to 2D for UI
        setup_2d()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    
if __name__ == "__main__":
    main()