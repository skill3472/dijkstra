from tkinter import messagebox, Tk
import pygame
import sys

w = 1000
h = 1000

gap = 2

columns = 50
rows = 50

grid_w = w // columns
grid_h = h // rows

grid = []
queue = []
path = []

class Cell:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.end = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None
    
    def draw(self, window, color):
        pygame.draw.rect(window, color, (self.x * grid_w, self.y * grid_h, grid_w - gap, grid_w - gap))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])

# Create the grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Cell(i, j))
    grid.append(arr)

# Set Neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()

# Starting box
start_box = grid[0][0]
start_box.start = True
start_box.visited = True
queue.append(start_box)

window = pygame.display.set_mode((w, h))

def main():
    begin_search = False
    end_box_set = False
    searching = True
    end_box = None

    while True:
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Draw walls
                if event.buttons[0]:
                    i = x // grid_w
                    j = y // grid_h
                    grid[i][j].wall = True
                # Set end
                if event.buttons[2] and not end_box_set:
                    i = x // grid_w
                    j = y // grid_h
                    end_box = grid[i][j]
                    end_box.end = True
                    end_box_set = True
            # Start
            if event.type == pygame.KEYDOWN and end_box_set:
                begin_search = True

        # Algorithm
        if begin_search:
            if len(queue) > 0 and searching:
                selbox = queue.pop(0)
                selbox.visited = True
                if selbox == end_box:
                    searching = False
                    if selbox.prior != None:
                        while selbox.prior != start_box:
                            path.append(selbox.prior)
                            selbox = selbox.prior
                else:
                    for neighbour in selbox.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            queue.append(neighbour)

            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No solution", "There is no possible solution!")
                    searching = False

        window.fill((0,0,0))
        
        # Draws the cells
        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (20, 20, 20))

                if box in path:
                    box.draw(window, (0, 0, 200))
                if box.queued:
                    box.draw(window, (200, 200, 0))
                if box.visited:
                    box.draw(window, (0, 200, 200))
                
                if box.start:
                    box.draw(window, (200, 0, 200))
                if box.wall:
                    box.draw(window, (200, 0, 0))
                if box.end:
                    box.draw(window, (0, 0, 200))

        pygame.display.flip()

main()