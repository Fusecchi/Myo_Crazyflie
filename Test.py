# import pandas as pd
#
# read_file = pd.read_csv(r'~/Pyo/pyomyo-main/examples/data/vals%d.txt')
# read_file.to_csv(r'~/Pyo/pyomyo-main/examples/data/vals%d.csv')
import pygame

pygame.init()

# Set up the window
window_size = (400, 300)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pygame Time Lapse")

# Set up the font
font = pygame.font.SysFont(None, 48)

# Set up the start time
start_time = pygame.time.get_ticks()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the time elapsed since the start
    elapsed_time = pygame.time.get_ticks() - start_time

    # Render the text
    text = font.render(str(elapsed_time/1000), True, (255, 255, 255))

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the text
    screen.blit(text, (50, 50))

    # Update the screen
    pygame.display.update()
