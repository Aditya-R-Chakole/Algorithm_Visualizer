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

#_____Recursive_Division_____#
def do_Recursive_Division( screen ,grid, start, end, d, width, height ):
    Speed = utility.Speed

    def get_wall_index( corner, length ):
        assert length >= 3
        wall_pos = randint( corner+1, corner+length-2 )
        if wall_pos%2 == 1:
            wall_pos -= 1
        return wall_pos

    def make_opening( screen, grid, x, y, width, height, wall_x, wall_y ):
        opening = []

        #_____Possible openings_____#
        possible_open = [(randint(x, wall_x -1), wall_y), (randint(wall_x + 1, x + width -1), wall_y),(wall_x, randint(y, wall_y -1)), (wall_x, randint(wall_y + 1, y + height - 1))]
        
        #_____Positions of the margin exactly beside the created wall_____#
        margin_open = [(x, wall_y), (x+width-1, wall_y), (wall_x, y), (wall_x, y + height-1)]

        #_____Positions of the nodes adjecent to margin nodes_____# 
        adj_open = [(x-1, wall_y), (x+width, wall_y), (wall_x, y - 1), (wall_x, y + height)]
        
        #_____Check if created walls have margin positions adjencet ot thme____#
        #_____If yes then open the respective adj position_____# 
        for i in range(4):
            adj_x, adj_y = (adj_open[i][0], adj_open[i][1])
            if utility.is_within_the_grid( grid ,adj_x, adj_y ) and not utility.is_wall( grid, adj_x, adj_y ):
                grid[margin_open[i][0]][margin_open[i][1]].cell_type = 'Blank'
                utility.make_change(screen, grid, margin_open[i][0], margin_open[i][1])
            else:
                opening.append( possible_open[i] )
        ignore_it = randint( 0, len(possible_open)-1 )
        for i in range(len(opening)):
            if i != ignore_it:
                grid[opening[i][0]][opening[i][1]].cell_type = 'Blank'
                utility.make_change(screen, grid, opening[i][0], opening[i][1])
        utility.draw_grid(screen)
            
    #_____If any side of input box is less 2 than return_____#
    if width <= 1 or height <= 1:
        return
        
    #_____Randomly generate wall position_____#
    wall_x, wall_y = (get_wall_index( d[0], width ), get_wall_index( d[1], height ))

    #_____Create walls at Randomly generated position_____#
    for i in range( d[0], d[0]+width ):
        time.sleep(0.025*Speed)
        if (i,wall_y)==start or (i,wall_y)==end :
            continue
        grid[i][wall_y].cell_type = 'Wall'
        utility.make_change(screen, grid, i, wall_y)
        utility.draw_grid(screen)
        
    #_____Create walls at Randomly generated position_____#
    for i in range( d[1], d[1]+height ):
        time.sleep(0.025*Speed)
        if utility.is_start_or_end((wall_x,i), start, end) :
            continue
        grid[wall_x][i].cell_type = 'Wall'
        utility.make_change(screen, grid, wall_x, i)
        utility.draw_grid(screen)
    
    #_____Make openings_____#
    make_opening( screen, grid, d[0], d[1], width, height, wall_x, wall_y )

    time.sleep(0.025*Speed)

    #_____Recursive calls_____#
    do_Recursive_Division( screen ,grid, start, end, d, wall_x-d[0], wall_y-d[1] )
    do_Recursive_Division( screen ,grid, start, end, (d[0], wall_y+1), wall_x-d[0], d[1]+height-wall_y-1 )
    do_Recursive_Division( screen ,grid, start, end, (wall_x+1, d[1]), d[0]+width-wall_x-1, wall_y-d[1] )
    do_Recursive_Division( screen ,grid, start, end, (wall_x+1, wall_y+1), d[0]+width-wall_x-1, d[1]+height-wall_y-1 )

def Recursive_Division( screen ,grid, start, end ):
    Speed = utility.Speed

    #_____Mark the edges the grid as WALLS_____#
    for x in range(NO_OF_BOXS):
        time.sleep(0.025*Speed)
        grid[ x ][ 0 ].cell_type = 'Wall'
        grid[ x ][ NO_OF_BOXS-1 ].cell_type = 'Wall'
        utility.make_change( screen, grid, x, 0 )
        utility.make_change( screen, grid, x, NO_OF_BOXS-1 )
        
    #_____Mark the edges the grid as WALLS_____#
    for y in range(NO_OF_BOXS):
        time.sleep(0.025*Speed)
        grid[ 0 ][ y ].cell_type = 'Wall'
        grid[ NO_OF_BOXS-1 ][ y ].cell_type = 'Wall'
        utility.make_change( screen, grid, 0, y )
        utility.make_change( screen, grid, NO_OF_BOXS-1, y )
    #_____do_Recursive_Division_____#
    do_Recursive_Division( screen ,grid, start, end, (1, 1), NO_OF_BOXS-2, NO_OF_BOXS-2 )

#_____Recursive_Backtracking_____#
def is_open( grid, x, y ):
    if grid[x][y].cell_type != 'Wall':
        return True
    else:
        return False

def check_adj_pos( screen, grid, x, y, width, height, check_list ):
    direction = []

    #_____If x>0 and (x-1) is within the grid and not visited then we can move to left, thus append it to the queue_____#
    if x > 0:
        if not is_open(grid, 2*(x-1)+1, 2*y+1):
            direction.append( 'L' )
    
    #_____If y>0 and (y-1) is within the grid and not visited then we can move to up, thus append it to the queue_____#
    if y > 0:
        if not is_open( grid, 2*x+1, 2*(y-1)+1 ):
            direction.append( 'U' )

    #_____If (x < width-1) and (x+1) is within the grid and not visited then we can move to right, thus append it to the queue_____#
    if x < width-1 :
        if not is_open(grid, 2*(x+1)+1, 2*y+1):
            direction.append( 'R' )

    #_____If (y < height-1) and (y+1) is within the grid and not visited then we can move to down, thus append it to the queue_____#
    if y < height-1:
        if not is_open( grid, 2*x+1, 2*(y+1)+1 ):
            direction.append( 'D' )
    
    #_____If there is any element in the queue, mark them open in there respective direction and return_____# 
    if len(direction):
        chosen_dir = choice(direction)
        if chosen_dir == 'L':
            check_list.append( (x-1, y) )
            grid[2*x][2*y+1].cell_type = 'Blank'
            grid[2*(x-1)+1][2*y+1].cell_type = 'Blank'
            utility.make_change(screen, grid, 2*x, 2*y+1)
            utility.make_change(screen, grid, 2*(x-1)+1, 2*y+1)
            utility.draw_grid(screen)
        elif chosen_dir == 'U':
            check_list.append( (x, y-1) )
            grid[2*x+1][2*(y-1)+1].cell_type = 'Blank'
            grid[2*x+1][2*y].cell_type = 'Blank'
            utility.make_change(screen, grid, 2*x+1, 2*(y-1)+1)
            utility.make_change(screen, grid, 2*x+1, 2*y)
            utility.draw_grid(screen)
        elif chosen_dir == 'R':
            check_list.append( (x+1, y) )
            grid[2*x+2][2*y+1].cell_type = 'Blank'
            grid[2*(x+1)+1][2*y+1].cell_type = 'Blank'
            utility.make_change(screen, grid, 2*x+2, 2*y+1)
            utility.make_change(screen, grid, 2*(x+1)+1, 2*y+1)
            utility.draw_grid(screen)
        elif chosen_dir == 'D':
            check_list.append( (x, y+1) )
            grid[2*x+1][2*y+2].cell_type = 'Blank'
            grid[2*x+1][2*(y+1)+1].cell_type = 'Blank'
            utility.make_change(screen, grid, 2*x+1, 2*y+2)
            utility.make_change(screen, grid, 2*x+1, 2*(y+1)+1)
            utility.draw_grid(screen)
        return True
    else:
        return False

def do_Recursive_Backtracking( screen, grid, start, end, width, height ):
    Speed = utility.Speed

    #_____Randomly generate a start node and make it open_____#
    maze_start = (randint(0, width-1), randint(0, height-1))
    grid[2*maze_start[0] + 1][2*maze_start[1] + 1].cell_type = 'Blank'
    utility.make_change(screen, grid, 2*maze_start[0] + 1, 2*maze_start[1] + 1)
    utility.draw_grid(screen)  

    #_____Adding this start node to queue and looping while there is an element in the queue_____#
    check_list = []
    check_list.append(maze_start)
    while len(check_list):
        time.sleep(0.025*Speed)
        top_entry = check_list[-1]
        if not check_adj_pos( screen, grid, top_entry[0], top_entry[1], width, height, check_list ):
            check_list.remove(top_entry)

def Recursive_Backtracking( screen, grid, start, end ):
    Speed = utility.Speed

    #_____loop through all the nodes of the grid and make them WALL_____#  
    for i in range(NO_OF_BOXS//2 + 1):
        for j in range(NO_OF_BOXS):
            if (i,j)==start or (i,j)==end :
                continue
            grid[ i ][ j ].cell_type = 'Wall'
            utility.make_change(screen, grid, i, j)
            utility.draw_grid(screen)
            if (NO_OF_BOXS-1-i,NO_OF_BOXS-1-j)==start or (NO_OF_BOXS-1-i,NO_OF_BOXS-1-j)==end :
                continue
            grid[ NO_OF_BOXS-1-i ][ NO_OF_BOXS-1-j ].cell_type = 'Wall'
            utility.make_change(screen, grid, NO_OF_BOXS-1-i, NO_OF_BOXS-1-j)
            utility.draw_grid(screen)


    #_____do_Recursive_Backtracking_____#
    do_Recursive_Backtracking( screen, grid, start, end, (NO_OF_BOXS-1)/2, (NO_OF_BOXS-1)/2 )  

#_____Simple_Randomized_Maze_____#
def simple_maze( screen, grid, start, end ):
    Speed = utility.Speed

    #_____used for the random generation of 0 and 1 with 25-75 ratio_____# 
    weighted_random = [0, 1, 1, 1]

    #_____loop through all the nodes of the grid_____#
    for i in range(NO_OF_BOXS):
        for j in range(NO_OF_BOXS):

            #_____Make changes according to the position of the node_____#
            if utility.is_start_or_end( (i, j), start, end ) :
                continue
            if i==0 or j==0 or i==NO_OF_BOXS-1 or j==NO_OF_BOXS-1:
                grid[ i ][ j ].cell_type = 'Wall'
            else:
                new_cell_type = choice(weighted_random)
                if new_cell_type == 0 :
                    grid[ i ][ j ].cell_type = 'Wall'

    #_____Mark the changes that were made in the loop_____#
    for i in range(NO_OF_BOXS):
        for j in range(NO_OF_BOXS):
            time.sleep(0.025*Speed)
            utility.make_change(screen, grid, i, j)
            utility.draw_grid(screen) 

