# Pathfinding and Maze Generating Algorithm Visualizer

## Introduction 
The Pathfinding and Maze Generating Algorithm Visualizer supports 4 pathfinding algorithms and 3 maze generating algorithms which are inplemented in python using pygame and pygame_gui module.  
- **Pathfinding Algorithms** : [Breadth-first search], [Depth-first search], [Dijkstra's Algorithm], [A* Search]
- **Maze Generating Algorithm** : Basic Randomized maze generator, [Recursive division method], [Recursive Backtracking method]
## Table of Content
- **main.py** : initialization of GUI and main programme loop
- **pathfinding.py** : support 4 pathfinding algorithms
- **maze_generator.py** : support 3 maze generating algorithms
- **utility.py** : initialization of data-structure and some commonly used functions
- **theme.json** : contains all details related to GUI theme
- **Montserrat-Regular.ttf** : contains standard Montserrat-Regular font format
- **GIF folder** : contains all gifs

## Requirements
- [Python 3.9.1]
- [Python-Pygame 2.0.1]
- [Python-Pygame_GUI] 

## RUN
$ python main.py

## Instructions 
- Select a **START** node
- Select an **END** node
- Place the **WALLS** or **GENERATE A MAZE**
- Select a **ALGORITHM** and **Visualize**

## Demo
### Breadth-first search
![BFS](https://user-images.githubusercontent.com/57232967/108251997-207fda80-717e-11eb-8acd-4fb3992fef38.gif)
### Dijkstra's Algorithm
![Dijkstra](https://user-images.githubusercontent.com/57232967/108252165-52913c80-717e-11eb-9658-40cd300108c1.gif)
### A* Search
![A_Star](https://user-images.githubusercontent.com/57232967/108252206-6341b280-717e-11eb-9e81-008a901fc36b.gif)
### Recursive Division method for Maze Generation
![RD](https://user-images.githubusercontent.com/57232967/108252584-d3e8cf00-717e-11eb-9c7f-66b1196d06ec.gif)
### Recursive Backtracking method for Maze Generation
![RB](https://user-images.githubusercontent.com/57232967/108252725-fbd83280-717e-11eb-98ba-d316037cc95b.gif)

## License
[MIT]


[Breadth-first search]: <https://en.wikipedia.org/wiki/Breadth-first_search>
[Depth-first search]: <https://en.wikipedia.org/wiki/Depth-first_search>
[Dijkstra's Algorithm]: <https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm>
[A* Search]: <https://en.wikipedia.org/wiki/A*_search_algorithm>
[Recursive division method]: <https://en.wikipedia.org/wiki/Maze_generation_algorithm>
[Recursive Backtracking method]: <https://en.wikipedia.org/wiki/Maze_generation_algorithm>
[Python 3.9.1]: <https://www.python.org/downloads/>
[Python-Pygame_GUI]: <https://pygame-gui.readthedocs.io/en/latest/>
[Python-Pygame 2.0.1]: <https://pypi.org/project/pygame/>
[MIT]: <https://github.com/Aditya-R-Chakole/Algorithm_Visualizer/blob/main/LICENSE>
