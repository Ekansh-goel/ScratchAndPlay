import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 900, 900  # Visible window size
VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 900, 900  # Total scrollable area
display = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Scrollable Scratch to Reveal")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (209, 209, 209)

# Fonts
font = pygame.font.Font(None, 28)
small_font = pygame.font.Font(None, 36)

# Grid settings
GRID_SIZE = 5
CIRCLE_RADIUS = 60
PADDING = 25
SCRATCH_RADIUS = 15  # Radius of the scratch effect

# Scroll settings
SCROLL_SPEED = 5
MAX_SCROLL_X = VIRTUAL_WIDTH - WINDOW_WIDTH
MAX_SCROLL_Y = VIRTUAL_HEIGHT - WINDOW_HEIGHT

# Calculate grid positions
grid = []
start_x = (VIRTUAL_WIDTH - (GRID_SIZE * (2 * CIRCLE_RADIUS + PADDING) - PADDING)) // 2
start_y = (VIRTUAL_HEIGHT - (GRID_SIZE * (2 * CIRCLE_RADIUS + PADDING) - PADDING)) // 2

for row in range(GRID_SIZE):
    grid_row = []
    for col in range(GRID_SIZE):
        x = start_x + col * (2 * CIRCLE_RADIUS + PADDING)
        y = start_y + row * (2 * CIRCLE_RADIUS + PADDING)
        grid_row.append((x, y))
    grid.append(grid_row)

def load_hidden_messages(filename):
    try:
        with open(filename, 'r') as file:
            messages = [line.strip() for line in file.readlines()]
        if len(messages) < GRID_SIZE * GRID_SIZE:
            messages.extend(["Surprise!" for _ in range(GRID_SIZE * GRID_SIZE - len(messages))])
        random.shuffle(messages)  # Randomize the order of messages
        return messages[:GRID_SIZE * GRID_SIZE]
    except Exception as e:
        print(f"Error loading messages: {e}")
        return ["Surprise!" for _ in range(GRID_SIZE * GRID_SIZE)]

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    return lines

# Load and prepare hidden messages
hidden_messages = load_hidden_messages("hidden_messages2.txt")
hidden_surfaces = []
scratch_surfaces = []

# Create message surfaces
for msg in hidden_messages:
    lines = wrap_text(msg, font, 2 * CIRCLE_RADIUS - 10)
    surface = pygame.Surface((2 * CIRCLE_RADIUS, 2 * CIRCLE_RADIUS), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    
    y_offset = (2 * CIRCLE_RADIUS - len(lines) * font.get_linesize()) // 2
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, BLACK)
        text_x = (2 * CIRCLE_RADIUS - text_surface.get_width()) // 2
        text_y = y_offset + i * font.get_linesize()
        surface.blit(text_surface, (text_x, text_y))
    hidden_surfaces.append(surface)

# Create scratch surfaces with masks
scratch_surfaces = []
scratch_masks = []
for _ in range(GRID_SIZE * GRID_SIZE):
    # Create the grey surface
    surface = pygame.Surface((2 * CIRCLE_RADIUS, 2 * CIRCLE_RADIUS), pygame.SRCALPHA)
    pygame.draw.circle(surface, GREY, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
    scratch_surfaces.append(surface)
    
    # Create a mask for tracking scratched areas
    mask = pygame.Surface((2 * CIRCLE_RADIUS, 2 * CIRCLE_RADIUS), pygame.SRCALPHA)
    mask.fill((255, 255, 255, 255))  # White means unscratched
    scratch_masks.append(mask)

def scratch_at_position(pos, mask_surface):
    """Apply scratch effect at the given position"""
    pygame.draw.circle(mask_surface, (0, 0, 0, 0), pos, SCRATCH_RADIUS)

def main():
    clock = pygame.time.Clock()
    scratching = False
    scroll_x, scroll_y = 0, 0
    scroll_speed = SCROLL_SPEED
    
    # For smooth scrolling with mouse
    last_mouse_pos = None
    dragging = False
    last_scratch_pos = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    scratching = True
                    last_scratch_pos = pygame.mouse.get_pos()
                elif event.button == 3:  # Right click
                    dragging = True
                    last_mouse_pos = event.pos
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    scratching = False
                    last_scratch_pos = None
                elif event.button == 3:
                    dragging = False
                    last_mouse_pos = None

        # Handle keyboard scrolling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            scroll_x = max(0, scroll_x - scroll_speed)
        if keys[pygame.K_RIGHT]:
            scroll_x = min(MAX_SCROLL_X, scroll_x + scroll_speed)
        if keys[pygame.K_UP]:
            scroll_y = max(0, scroll_y - scroll_speed)
        if keys[pygame.K_DOWN]:
            scroll_y = min(MAX_SCROLL_Y, scroll_y + scroll_speed)

        # Handle mouse dragging for scrolling
        if dragging and last_mouse_pos is not None:
            current_mouse_pos = pygame.mouse.get_pos()
            dx = last_mouse_pos[0] - current_mouse_pos[0]
            dy = last_mouse_pos[1] - current_mouse_pos[1]
            
            scroll_x = max(0, min(MAX_SCROLL_X, scroll_x + dx))
            scroll_y = max(0, min(MAX_SCROLL_Y, scroll_y + dy))
            
            last_mouse_pos = current_mouse_pos

        # Handle scratching
        if scratching:
            mouse_pos = pygame.mouse.get_pos()
            world_pos = (mouse_pos[0] + scroll_x, mouse_pos[1] + scroll_y)

            for idx, (x, y) in enumerate(sum(grid, [])):
                local_x = world_pos[0] - (x - CIRCLE_RADIUS)
                local_y = world_pos[1] - (y - CIRCLE_RADIUS)
                
                # Check if within circle bounds
                if 0 <= local_x <= 2 * CIRCLE_RADIUS and 0 <= local_y <= 2 * CIRCLE_RADIUS:
                    dist_from_center = ((local_x - CIRCLE_RADIUS) ** 2 + (local_y - CIRCLE_RADIUS) ** 2) ** 0.5
                    if dist_from_center <= CIRCLE_RADIUS:
                        scratch_at_position((local_x, local_y), scratch_masks[idx])

        # Draw everything
        display.fill(WHITE)
        
        # Draw grid items
        for idx, (x, y) in enumerate(sum(grid, [])):
            # Draw hidden message
            display.blit(hidden_surfaces[idx], (x - CIRCLE_RADIUS, y - CIRCLE_RADIUS))
            
            # Apply scratch mask to grey surface
            scratch_surface = scratch_surfaces[idx].copy()
            scratch_surface.blit(scratch_masks[idx], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            display.blit(scratch_surface, (x - CIRCLE_RADIUS, y - CIRCLE_RADIUS))

        # Draw the visible portion
        screen.blit(display, (-scroll_x, -scroll_y))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

