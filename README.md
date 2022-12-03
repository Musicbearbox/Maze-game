# Maze-game
Game:
Maze game provide a random maze, goal of the  player is to control the little bear from the entry to the exit.

-------------------------------------------------------------------------------

Game features:
	Automatically generated map
	Auto-find the shortest path


-------------------------------------------------------------------------------

Libs:
    pygame
    heapdict

-------------------------------------------------------------------------------

Algorithm:
    Automatically generated map:
        prim
        DFS  (deprived)

    Auto-find the shortest path
        A start
        Dijkstra   (deprived)

-------------------------------------------------------------------------------
DataStructure:
    Heapdict:
        It provided a priority queue and make the searching for minimal node in A star  more efficient.
    Dict:
        Compared to the list, it can provide the better search performance in O(1). It was used to check if a node is already in the open list.
        
