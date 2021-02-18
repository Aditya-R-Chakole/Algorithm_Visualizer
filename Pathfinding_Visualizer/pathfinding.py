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

#_____BFS_____#
def bfs(screen, grid, start, end):
    Speed = utility.Speed

    neighbour = [ (1, 0), (-1, 0), (0, -1), (0, 1) ]
    found = False
    q = []

    #_____Add START node to Queue_____#
    q.append(start)

    #_____Loop while there is an element in this queue_____#
    while len(q) > 0 :
        time.sleep(0.025*Speed)
        utility.draw_grid(screen)
        if found :
            break
        
        #_____Get the first element of the queue_____#
        curr = q[0]
        q.pop(0)

        grid[curr[0]][curr[1]].cell_type = 'Lead'
        if not utility.is_start_or_end( curr, start, end ) :
            utility.make_change(screen, grid, curr[0], curr[1])
        
        for nb in neighbour:
            #_____Traverse all the neighbours of 'curr'_____#
            new_x = curr[0] + nb[0]
            new_y = curr[1] + nb[1]

            #_____Check if this node (is_within_the_grid) and (is_not_a_wall) and (is_not_visited)_____#
            #_____Then add this node to queue_____# 
            if utility.is_within_the_grid(grid, new_x, new_y) :
                if (not utility.is_wall(grid, new_x, new_y)) and (utility.is_not_visited(grid, new_x, new_y)) :
                    grid[new_x][new_y].pre_cell = curr
                    q.append( (new_x, new_y) )
                    if not utility.is_start_or_end( (new_x, new_y), start, end ) :
                        grid[new_x][new_y].cell_type = 'Span'
                        utility.make_change(screen, grid, new_x, new_y)
                    if (new_x, new_y)==end :
                        found = True
                        break

    #_____mark_the_final_path_____#
    utility.mark_the_final_path(screen, grid, start, end)

#_____DFS_____#
def dfs(screen, grid, start, end):
    Speed = utility.Speed

    neighbour = [ (0, 1), (-1, 0), (0, -1), (1, 0) ]
    parent_cell = (0, 0)
    q = deque()

    #_____Add START node to Stack_____#
    q.append(start)

    #_____Loop while there is an element in this stack_____#
    while len(q):
        utility.draw_grid(screen)
        time.sleep(0.025*Speed)
        
        #_____Get the topmost element of the stack_____#
        curr = q.pop()

        #_____Check if this node (is_not_a_wall) and (is_not_visited)_____#
        #_____Then add this node to stack_____# 
        if (not utility.is_wall(grid, curr[0], curr[1])) and (utility.is_not_visited(grid, curr[0], curr[1])) :
            grid[curr[0]][curr[1]].pre_cell = parent_cell 
            parent_cell = curr
            if curr == end :
                break
            elif curr != start :
                grid[curr[0]][curr[1]].cell_type = 'Lead'
                utility.make_change(screen, grid, curr[0], curr[1])
            
            #_____Traverse all the neighbours of 'curr'_____#
            for nb in neighbour :
                new_x = curr[0] + nb[0]
                new_y = curr[1] + nb[1]

                #_____Check if this node (is_within_the_grid) and (is_not_a_wall) and (is_not_visited)_____#
                #_____Then add this node to stack_____# 
                if utility.is_within_the_grid(grid, new_x, new_y) :
                    if (not utility.is_wall(grid, new_x, new_y)) and (utility.is_not_visited(grid, new_x, new_y)) :
                        q.append( (new_x, new_y) )

    #_____mark_the_final_path_____#                    
    utility.mark_the_final_path(screen, grid, start, end)

#_____Dijkstra_____#
def is_visited(visited, curr):
    for i in visited:
        if( curr == i ):
            return True
    return False


def dijkstra(screen, grid, start, end):
    Speed = utility.Speed

    neighbour = [ (1, 0), (-1, 0), (0, -1), (0, 1) ]
    visited = []
    q = PriorityQueue()

    #_____Add START node to PriorityQueue_____#
    grid[start[0]][start[1]].score = 0
    q.put( (grid[start[0]][start[1]].score, start) )

    #_____Loop while there is an element in this PriorityQueue_____#
    while not q.empty():
        utility.draw_grid(screen)
        time.sleep(0.025*Speed)

        #_____Get the topmost element of the PriorityQueue_____#
        curr_tup = q.get()
        curr = curr_tup[1]
        if curr == end :
            break
        if is_visited( visited, curr ):
            continue
        visited.append( curr )

        if not utility.is_start_or_end(curr, start, end) :
            grid[curr[0]][curr[1]].cell_type = 'Lead'
            utility.make_change(screen, grid, curr[0], curr[1])
        temp_score = grid[curr[0]][curr[1]].score + 1

        #_____Traverse all the neighbours of 'curr'_____#
        for nb in neighbour:
            new_x = curr[0] + nb[0]
            new_y = curr[1] + nb[1]

            #_____Check if this node (is_within_the_grid) and (is_not_a_wall) and (is_not_visited)_____#
            #_____And have less score(distance) than previous of its score Then add this node to PriorityQueue with new score(distance)_____# 
            if utility.is_within_the_grid(grid, new_x, new_y) :
                if not utility.is_wall(grid, new_x, new_y)  and (grid[new_x][new_y].score > temp_score) :
                    grid[new_x][new_y].score = temp_score
                    grid[new_x][new_y].pre_cell = curr
                    q.put( (grid[new_x][new_y].score, (new_x, new_y)) )
                    if not utility.is_start_or_end( (new_x, new_y), start, end ) :
                        grid[new_x][new_y].cell_type = 'Span'
                        utility.make_change(screen, grid, new_x, new_y)
    
    #_____mark_the_final_path_____#
    utility.mark_the_final_path(screen, grid, start, end)

#_____A_STAR_____#
#_____Claculate the h_score between two nodes_____#
def h( p1, p2 ):
    (x1, y1) = p1
    (x2, y2) = p2
    temp_x = float(x1 - x2)*(x1 - x2)
    temp_y = float(y1 - y2)*(y1 - y2)
    return math.sqrt(temp_x + temp_y)
    

def is_visited(visited, curr):
    for i in visited:
        if( curr == i ):
            return True
    return False

def a_star(screen, grid, start, end):
    Speed = utility.Speed

    neighbour = [ (1, 0), (-1, 0), (0, -1), (0, 1) ]
    visited = []
    q = PriorityQueue()

    #_____Add START node to PriorityQueue_____#
    grid[start[0]][start[1]].g_score = 0 
    grid[start[0]][start[1]].h_score = h(start, end) 
    grid[start[0]][start[1]].score = h(start, end) 
    q.put( (grid[start[0]][start[1]].score, start) )

    #_____Loop while there is an element in this PriorityQueue_____#
    while not q.empty():
        utility.draw_grid(screen)
        time.sleep(0.025*Speed)

        #_____Get the topmost element of the PriorityQueue_____#
        curr_tup = q.get()
        curr = curr_tup[1]
        if curr == end :
            print("ALL_DONE")
            break

        if is_visited( visited, curr ):
            continue
        
        visited.append( curr )
        if curr!=start and curr!=end :
            grid[curr[0]][curr[1]].cell_type = 'Lead'
            utility.make_change(screen, grid, curr[0], curr[1])

        temp_g_score = grid[curr[0]][curr[1]].g_score + 1 

        #_____Traverse all the neighbours of 'curr'_____#
        for nb in neighbour:
            new_x = curr[0] + nb[0]
            new_y = curr[1] + nb[1]

            #_____Check if this node (is_within_the_grid) and (is_not_a_wall) and (is_not_visited)_____#
            #_____And have less overall score(distance) than previous of its score Then add this node to PriorityQueue with new overall score(distance)_____# 
            #_____overall score(distance) = g_function + h_function_____#
            if utility.is_within_the_grid(grid, new_x, new_y) :
                condition = (grid[new_x][new_y].score > ( temp_g_score + h( (new_x, new_y), end ) ))
                if not utility.is_wall(grid, new_x, new_y)  and condition :
                    grid[new_x][new_y].g_score = temp_g_score
                    grid[new_x][new_y].h_score = h( (new_x, new_y), end )
                    grid[new_x][new_y].score = grid[new_x][new_y].g_score + grid[new_x][new_y].h_score
                    grid[new_x][new_y].pre_cell = curr
                    q.put( (grid[new_x][new_y].score, (new_x, new_y)) )
                    if not utility.is_start_or_end((new_x, new_y), start, end) :
                        grid[new_x][new_y].cell_type = 'Span'
                        utility.make_change(screen, grid, new_x, new_y)
    
    #_____mark_the_final_path_____#
    utility.mark_the_final_path(screen, grid, start, end)
