#_____imports_____#
from dataclasses import dataclass
from collections import deque
from queue import PriorityQueue
from random import randint, choice

import pygame
import pygame_gui
import time
import queue
import math  

#_____Constants_____#
WIDTH = 620
HEIGHT = 620
MENU_WIDTH = 300
NO_OF_BOXS = 31
WIDTH_PER_BOX = WIDTH//NO_OF_BOXS
HEIGHT_PER_BOX = HEIGHT//NO_OF_BOXS
OPTIONS = ["Breadth-First Search", "Depth-First Search", "Dijkstra's Algorithm", "A* Search"]
OPTIONS_MAZE = [ "Basic Random Maze","Recursive Division", "Recursive Backtracking" ]
SPEED = ["Slow", "Average", "Fast" ]
TIME_DELTA = pygame.time.Clock().tick(60)/1000.0

#_____Colors_____# 
BG = (90,118,165)
LEAD = (71,50,123)
SPAN = (30,58,103)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 165 ,0)
TEAL = (50,78,123)
LIGHT_TEAL = (150,178,223)
FINAL_PATH = (63,195,128)

#_____Speed of Visualization_____#
Speed = 1

#_____Datastructure_____# 
@dataclass
class BOX:
    start_x: int
    start_y: int
    width : int
    height : int
    cell_type : str
    pre_cell : (-1, -1)
    score : float
    g_score : float
    h_score : float

#_____General_Functions_____#
#_____Check if the given node is within the grid_____#
def is_within_the_grid( grid, x, y ): 
    if (x >= 0)and(x < NO_OF_BOXS)and(y >= 0)and(y < NO_OF_BOXS):
        return True
    return False

#_____Check if the given node is a WALL_____#
def is_wall( grid, x, y ): 
    if grid[x][y].cell_type == 'Wall':
        return True
    return False

#_____Check if the given node is visited earlier_____#
def is_not_visited( grid, x, y ): 
    if grid[x][y].pre_cell == (-1, -1):
        return True
    return False

#_____Check if the given node is START or END_____#
def is_start_or_end( node, start, end ): 
    if node==start or node==end :
        return True
    return False

#_____make_grid_____#
def make_grid( ):
    grid = []
    for i in range(NO_OF_BOXS):
        grid.append([])
        for j in range(NO_OF_BOXS):
            temp = BOX(i*WIDTH_PER_BOX, j*HEIGHT_PER_BOX, WIDTH_PER_BOX, HEIGHT_PER_BOX, "Blank", (-1, -1), 1000000, 1000000, 1000000)
            grid[i].append(temp)

    return grid

#_____make_change_____#
def make_change(screen, grid, pos_x, pos_y):
    #_____Finding the position of box from grid index_____#
    x = pos_x*WIDTH_PER_BOX
    y = pos_y*HEIGHT_PER_BOX
    width_of_box = grid[pos_x][pos_y].width
    height_of_box = grid[pos_x][pos_y].height

    #_____make appropriate changes_____#
    if grid[pos_x][pos_y].cell_type == 'Blank':
        pygame.draw.rect(screen, BG, (x, y, width_of_box, height_of_box))
    elif grid[pos_x][pos_y].cell_type == 'Start':
        pygame.draw.rect(screen, ORANGE, (x, y, width_of_box, height_of_box))
    elif grid[pos_x][pos_y].cell_type == 'End':
        pygame.draw.rect(screen, RED, (x, y, width_of_box, height_of_box))
    elif grid[pos_x][pos_y].cell_type == 'Wall':
        pygame.draw.rect(screen, BLACK, (x, y, width_of_box, height_of_box))
    elif grid[pos_x][pos_y].cell_type == 'Lead':
        pygame.draw.rect(screen, LEAD, (x, y, width_of_box, height_of_box))
    elif grid[pos_x][pos_y].cell_type == 'Span':
        pygame.draw.circle( screen, SPAN, (x + WIDTH_PER_BOX//2, y + HEIGHT_PER_BOX//2), (HEIGHT_PER_BOX//(3)) )
    elif grid[pos_x][pos_y].cell_type == 'Final_Path':
        pygame.draw.rect(screen, FINAL_PATH, (x, y, width_of_box, height_of_box))

    pygame.display.update()
    
#_____draw_grid()_____#
def draw_grid(screen): # Draw grid lines
    for i in range(NO_OF_BOXS+1):
        pygame.draw.line(screen, TEAL, (0, i*HEIGHT_PER_BOX), (WIDTH, i*HEIGHT_PER_BOX))
        
    for j in range(NO_OF_BOXS+1):
        pygame.draw.line(screen, TEAL, (j*WIDTH_PER_BOX, 0), (j*WIDTH_PER_BOX, HEIGHT))

#_____Reset the Grid_____#
def clear_the_grid( screen, grid ): 
    count_click = 0
    screen.fill(BG)
    draw_grid(screen)
    for i in range(NO_OF_BOXS):
        for j in range(NO_OF_BOXS):
            grid[i][j].cell_type = "Blank"
            grid[i][j].pre_cell = (-1, -1)
            grid[i][j].score = 1000000
            grid[i][j].g_score = 1000000
            grid[i][j].h_score = 1000000

#_____Mark_The_Final_Path_____#
def mark_the_final_path( screen, grid, start, end ): 
    final = []
    curr = end
    while curr != start :
        final.append(curr)
        temp = curr
        curr = grid[temp[0]][temp[1]].pre_cell
    final.append(start)
    
    for i in final[:: -1]:
        time.sleep(0.025)
        if is_start_or_end(i, start, end):
            continue
        grid[i[0]][i[1]].cell_type = 'Final_Path'
        make_change(screen, grid, i[0], i[1])
        draw_grid(screen)

#_____Speed_____#
#_____Changes the speed parameter of the visualization_____#
def change_speed( Drop_Down_Menu_Changed ): 
    if Drop_Down_Menu_Changed == 'Slow': 
        return 3
    elif Drop_Down_Menu_Changed == 'Fast': 
        return 0.33
    elif Drop_Down_Menu_Changed == 'Average':
        return 1
    
