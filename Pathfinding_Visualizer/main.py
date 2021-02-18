#_____Run this file_____#
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

import pathfinding
import maze_generator
import utility

#_____Constants_____#
WIDTH = utility.WIDTH
HEIGHT = utility.HEIGHT
MENU_WIDTH = utility.MENU_WIDTH
NO_OF_BOXS = utility.NO_OF_BOXS
WIDTH_PER_BOX = utility.WIDTH_PER_BOX
HEIGHT_PER_BOX = utility.HEIGHT_PER_BOX
OPTIONS = utility.OPTIONS
OPTIONS_MAZE = utility.OPTIONS_MAZE
SPEED = utility.SPEED
TIME_DELTA = utility.TIME_DELTA

#_____Colors_____# 
BG = utility.BG
LEAD = utility.LEAD
SPAN = utility.SPAN
RED = utility.RED
BLACK = utility.BLACK
ORANGE = utility.ORANGE
TEAL = utility.TEAL
LIGHT_TEAL = utility.LIGHT_TEAL

#_____Find_The_Path_____#
def find_the_path( screen, grid, start, end, algo ):
    if algo == "Breadth-First Search" :
        pathfinding.bfs( screen, grid, start, end )
    elif algo == "Depth-First Search" :
        pathfinding.dfs( screen, grid, start, end )
    elif algo == "Dijkstra's Algorithm" :
        pathfinding.dijkstra( screen, grid, start, end )
    elif algo == "A* Search" :
        pathfinding.a_star( screen, grid, start, end )
    else :
        print("-----Select an Algorithm-----")

#_____Generate_Maze_____#
def generate_maze( screen, grid, start, end, algo ):
    if algo == "Recursive Division" :
        maze_generator.Recursive_Division( screen, grid, start, end )
    elif algo == "Recursive Backtracking" :
        maze_generator.Recursive_Backtracking( screen, grid, start, end )
    elif algo == "Basic Random Maze" :
        maze_generator.simple_maze( screen, grid, start, end )
    else :
        print("-----Select an Algorithm-----")

#_____Main_____#
if __name__=="__main__":
    grid = utility.make_grid()

    #_____Pygame_Module_____#
    pygame.init()
    screen = pygame.display.set_mode( (WIDTH + MENU_WIDTH, HEIGHT) )
    pygame.display.set_caption("-Pathfinding Visualizer-")
    screen.fill(BG)
    pygame.display.update()

    #_____Pygame_GUI_Module_____#
    manager = pygame_gui.UIManager((WIDTH + MENU_WIDTH, HEIGHT), 'theme.json')
    
    pygame_gui.elements.UITextBox( "  <b>-Pathfinding Visualizer-</b> " , relative_rect  = pygame.Rect((WIDTH + 15, 15), (270, 40)), manager = manager)

    maze_DD = pygame_gui.elements.UIDropDownMenu(options_list = OPTIONS_MAZE, starting_option = "Maze Generation Algorithm", relative_rect = pygame.Rect((WIDTH + 15, 75), (270, 35)), manager=manager, container = None)
    maze_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH + 15, 115), (270, 35)), text='Generate Maze', manager=manager)

    pathfinding_DD = pygame_gui.elements.UIDropDownMenu(options_list = OPTIONS, starting_option = "Pathfinding Algorithm", relative_rect = pygame.Rect((WIDTH + 15, 175), (270, 35)), manager=manager, container = None)
    viz_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH + 15, 215), (270, 35)), text='Visualize', manager=manager)
    
    clear_grid = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH + 15, 275), (270, 35)), text='Clear Grid', manager=manager)

    speed_DD = pygame_gui.elements.UIDropDownMenu(options_list = SPEED, starting_option = "Speed of Visualization", relative_rect = pygame.Rect((WIDTH + 15, 315), (270, 35)), manager=manager, container = None)

    pygame_gui.elements.UITextBox( "           <b>--Instructions--</b> <br/>1.  Select a START node <br/>2. Select an END node<br/>3. Place the WALLS or<br/>    GENERATE A MAZE<br/>4. Select an ALGORITHM <br/>    and Visualize " , relative_rect  = pygame.Rect((WIDTH + 15, 440), (270, 167)), manager = manager)

    background = pygame.Surface((WIDTH + MENU_WIDTH, HEIGHT))
    background.fill( TEAL )
    
    clock = pygame.time.Clock()

    #_____Other_parameters_____#
    count_click = 0
    drag = False

    start = (-1, -1)       
    end = (-1, -1)
    speed = 1
    Drop_Down_Menu_Changed = "None"

    #_____Main_Loop_____#
    run = True
    while run :
        utility.draw_grid(screen)
        manager.update(TIME_DELTA)
        pygame.display.update()

        screen.blit(background, (WIDTH, 0))
        manager.draw_ui(screen)

        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                run = False
            #_____Check if the Mouse Button is pressed_____#
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    count_click += 1
                    drag = True
                    mouse_x, mouse_y = event.pos
                    pos_x = mouse_x//WIDTH_PER_BOX
                    pos_y = mouse_y//HEIGHT_PER_BOX
                    #_____If its the first click, then this Node is the START Node_____#
                    if count_click == 1:  
                        if utility.is_within_the_grid(grid, pos_x, pos_y) :
                            start = (pos_x, pos_y)
                            grid[pos_x][pos_y].cell_type = "Start"
                            utility.make_change(screen, grid, pos_x, pos_y)
                        #_____If the click is outside of the grid, then its not considered for changing the grid_____#
                        else : 
                            count_click -= 1
                    #_____If its the second click, then this Node is the END Node_____#
                    elif count_click == 2: 
                        if utility.is_within_the_grid(grid, pos_x, pos_y) :
                            end = (pos_x, pos_y)
                            grid[pos_x][pos_y].cell_type = "End"
                            utility.make_change(screen, grid, pos_x, pos_y)
                        #_____If the click is outside of the grid, then its not considered for changing the grid_____#
                        else : 
                            count_click -= 1
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drag = False
            #_____If the mouse is in motion and whlie pressing the the left button of the mouse, then create WALLS_____#
            elif event.type == pygame.MOUSEMOTION: 
                mouse_x, mouse_y = event.pos
                pos_x = mouse_x//WIDTH_PER_BOX
                pos_y = mouse_y//HEIGHT_PER_BOX
                
                if utility.is_within_the_grid(grid, pos_x, pos_y) :
                    if drag and count_click>2 and (not utility.is_start_or_end((pos_x, pos_y), start, end) ) :
                        grid[pos_x][pos_y].cell_type = "Wall"
                        utility.make_change(screen, grid, pos_x, pos_y)
            #_____Register the changes made in DROP_DOWN_MENU_____#
            if event.type == pygame.USEREVENT: 
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED :
                    Drop_Down_Menu_Changed = event.text
                    if Drop_Down_Menu_Changed in SPEED :
                        speed = utility.change_speed( Drop_Down_Menu_Changed )
                        utility.Speed = speed
                #_____If any of the GUI buttons is pressed, call the respective function_____#
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:  
                    if event.ui_element == viz_button:
                        find_the_path( screen, grid, start, end, Drop_Down_Menu_Changed )
                    if event.ui_element == maze_button:
                        generate_maze( screen, grid, start, end, Drop_Down_Menu_Changed )
                    if event.ui_element == clear_grid:
                        utility.clear_the_grid( screen, grid )
                        count_click = 0
                        start = (-1, -1)
                        end = (-1, -1)

