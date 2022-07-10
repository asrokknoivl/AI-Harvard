
import os
class Node:
    def __init__(self , state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier: #LIFO
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_stata(self , state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception('Frontier is empty')
        else:    
            node = self.frontier.pop()
            # self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier): #FIFO
    def remove(self):
        if self.empty():
            raise Exception('Frontier is empty')
        else:    
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class Maze:
    def __init__(self ,mazeName):
        with open(mazeName) as file:
            maze = file.read()
        if maze.count('A') != 1:
            raise Exception('The maze must have exactly one starting point')    
        if maze.count('B') != 1:
            raise Exception('The maze must have exactly one ending point')    
        maze = maze.splitlines()
        self.height = len(maze)
        self.width = max(len(row) for row in maze)
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if maze[i][j] == 'A':
                        row.append(False)
                        self.starting_point = (i,j)
                    elif maze[i][j] == 'B':
                        row.append(False)
                        self.ending_point = (i,j)
                    elif maze[i][j] == ' ':
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        for i,row in enumerate(self.walls):
            for j,col in enumerate(row):
                if col == True:
                    print(' O ', end='')
                elif (i, j) == self.starting_point:
                    print(' + ', end='')
                elif (i, j) == self.ending_point:
                    print(' - ', end='')
                elif solution is not None and (i, j) in solution:
                    print(' . ', end='')
                else:
                    print('   ', end='')
            print()
    def children(self , state):
        row,col = state
        possible_moves = []
        directions = [
            ('up' , (row - 1 , col)),
            ('down' , (row + 1 , col)),
            ('right' , (row , col + 1)),
            ('left', (row, col - 1)),
        ]
        for action, (r,c) in directions:
            if 0 <= r < self.height and 0 <= col < self.width and not self.walls[r][c]:
                possible_moves.append((action, (r, c)))
        return possible_moves


    def solve(self, algorithm):
        alg = ''
        self.explored_states = 0
        self.explored = set()
        start = Node(state = self.starting_point , parent = None , action = None)
        if algorithm == '1':
            frontier = StackFrontier() #DFS
            alg = 'DFS'
        else:
            frontier = QueueFrontier() #BFS
            alg = 'BFS'
        frontier.add(start)

        while True:
            if frontier.empty():
                raise Exception("the maze has no solutions")

            node = frontier.remove()
            self.explored_states += 1

            if node.state == self.ending_point:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                cells.reverse()
                actions.reverse()
                self.solution = (actions, cells, alg)
                return
            self.explored.add(node.state)

            for action, state in self.children(node.state):
                if not frontier.contains_stata(state) and state not in self.explored:
                    child = Node(state=state, action=action, parent=node)
                    frontier.add(child)

    def save_maze(self ,filename, show_solution = True, show_explored = False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)
        solution = self.solution[1] if self.solution is not None else None
        for i,row in enumerate(self.walls):
            for j,col in enumerate(row):
                if col:
                    fill = (30,30,30)
                elif (i, j) == self.starting_point:
                    fill = (0,200,80)
                elif (i, j) == self.ending_point:
                    fill = (180, 0, 0)
                elif solution is not None and show_solution and (i,j) in solution:
                    fill = (90,90,90)
                elif solution is not None and show_explored and (i,j) in self.explored:
                    fill = (150,60,30)
                else:
                    fill = (255,255,255)

                draw.rectangle(((j * cell_size + cell_border , i * cell_size + cell_border),
                                ((j+1) * cell_size) - cell_border , (i+1) * cell_size - cell_border)
                               , fill = fill)

        img.save(filename)


def run():

    filename = input('Enter the name the maze, without the extinsion:\n>> ')
    if not os.path.exists(filename):
        os.mkdir(filename)
    maze = Maze(f'{filename}.txt')
    print("Maze : unsolved")
    print()
    print("(+) : starting point\n(-) : Ending point")

    print()

    maze.print()

    print()

    search = input('Choose an algorithm to try solving the maze with:\n(1)- DFS\n(2)- BFS\n>> ')
    while search not in ['1','2']:
        search = input("invalid response\n>>")
    print()
    print('Solving...')
    maze.solve(search)
    maze.print()
    algorithm = maze.solution[2]
    maze.save_maze(f'{filename}/{filename}-unsolved.png')

    print()

    print(f"Maze: Solved\nAlgorithm: {algorithm}")
    print("Nodes explored: ", maze.explored_states)
    print()
    maze.print()
    maze.save_maze(f'{filename}/{filename}-solved-solution-{algorithm}.png' , show_solution =True)
    maze.save_maze(f'{filename}/{filename}-solved-explored_nodes-{algorithm}.png' , show_explored =True)

if __name__ == '__main__':
    run()