import time
import pygame
import random
from cell import Cell

# only for cells
def draw_objects():
    for i in range(len(list_species)):
        if list_species[i]:
            for Cell in list_species[i]:
                pygame.draw.circle(window_screen, list_color[i], Cell.position(), Cell.cell_radius)

def action_cell():
    for i in range(len(list_species)):
        if list_species[i]:
            # if not negative, cell species has food [target]
            if list_food_index[i] >= 0:
                for Cell in list_species[i]:
                    list_species[list_food_index[i]], list_species[i] = Cell.action(list_species[list_food_index[i]], list_species[i])
            else:
                # if the cell has no food [target], then it will do nothing as it is a plant
                pass

def add_species(startpop, color, food, *args):
    # custom arguments: cell_radius, cell_speed, cell_hunger, cell_hunger_loss, cell_range, cell_hunger_gain
    default_arg = [3, 1, 1000, 2, 200, 100]

    list_color.append(color)
    list_food_index.append(food)

    for i in range(len(args)):
        default_arg[i] = args[i]
    # cell creation

    list_species.append([])

    for i in range(startpop):
        # randomly spawns cell within borders of window along with random direction
        cell_x = random.randrange(default_arg[0], window_width - default_arg[0], default_arg[0])
        cell_y = random.randrange(default_arg[0], window_height - default_arg[0], default_arg[0])

        # adds Cell -> list of cells -> list of species

        list_species[len(list_species)-1].append(Cell(cell_x, cell_y, default_arg[0], default_arg[1], window_width,
                 window_height, default_arg[2], default_arg[3], default_arg[4], default_arg[5]))

def remove_cell_zero_hunger():
    list_cell_tmp = []
    # for every cell list in species list
    for i in range(len(list_species)):
        if list_species[i]:
            for Cell in list_species[i]:
                if Cell.cell_hunger > 0:
                    list_cell_tmp.append(Cell)

            list_species[i] = list(list_cell_tmp)
            list_cell_tmp = []

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREEN_DARK = (2, 189, 2)
RED = (255, 0, 0)
RED_LIGHT = (255,100, 100)
GREY_LIGHT = (215, 219, 224)
PINK = (245, 66, 224)

# constant variables
list_species = []
list_color = []
list_food_index = []

list_direction = ['N', 'S', 'E', 'W']  # list of all directions a cell may go

# pygame init
pygame.init()
pygame.font.init()
window_width, window_height = 1200, 750  # screen width and height
window_screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Test')
font_TNR = pygame.font.SysFont('Times New Roman', 15)
window_screen.fill(WHITE)
pygame.display.flip()

add_species(5, RED, -1) # has no food [target]
add_species(5, GREEN, 0) # food [target] is species 0

# pygame window
run_game = True
while run_game:

    action_cell()

    # draw
    window_screen.fill(WHITE)
    draw_objects()

    pygame.display.flip()

    # remove cells with zero hunger
    remove_cell_zero_hunger()

    # if program is exited, quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
            break

    time.sleep(0.02)

pygame.quit()