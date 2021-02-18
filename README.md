# Algorithm Visualizer
## Pathfinding and Maze Generating Algorithm Visualizer

### Introduction 
The Pathfinding and Maze Generating Algorithm Visualizer supports 4 pathfinding algorithms and 3 maze generating algorithms which are implemented in python using pygame and pygame_gui module.  
- **Pathfinding Algorithms** : [Breadth-first search], [Depth-first search], [Dijkstra's Algorithm], [A* Search]
- **Maze Generating Algorithm** : Basic Randomized maze generator, [Recursive division method], [Recursive Backtracking method]
### Table of Content
- **main.py** : initialization of GUI and main programme loop
- **pathfinding.py** : support 4 pathfinding algorithms
- **maze_generator.py** : support 3 maze generating algorithms
- **utility.py** : initialization of data-structure and some commonly used functions
- **theme.json** : contains all details related to GUI theme
- **Montserrat-Regular.ttf** : contains standard Montserrat-Regular font format
- **GIF folder** : contains all gifs

### Requirements
- [Python 3.9.1]
- [Python-Pygame 2.0.1]
- [Python-Pygame_GUI] 

### RUN
$ python main.py

### Instructions 
- Select a **START** node
- Select an **END** node
- Place the **WALLS** or **GENERATE A MAZE**
- Select a **ALGORITHM** and **Visualize**

### Demo
#### Breadth-first search
![Bfs](https://user-images.githubusercontent.com/57232967/108347241-4d77d000-7206-11eb-9efa-c68617511ede.gif)

#### Dijkstra's Algorithm
![Dijkstra](https://user-images.githubusercontent.com/57232967/108347296-5c5e8280-7206-11eb-97fd-1db082c16981.gif)

#### A* Search
![A_star](https://user-images.githubusercontent.com/57232967/108347368-6c766200-7206-11eb-92bb-1ca34996c2ac.gif)

#### Recursive Division method for Maze Generation
![RD_Astar](https://user-images.githubusercontent.com/57232967/108347442-8152f580-7206-11eb-918a-4303835a5c28.gif)

#### Recursive Backtracking method for Maze Generation
![RB_Astar](https://user-images.githubusercontent.com/57232967/108347476-8adc5d80-7206-11eb-8916-47ca343cd5b8.gif)

### License
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
