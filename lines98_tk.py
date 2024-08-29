import tkinter as tk
import random
import time

class Lines98Game:
    def __init__(self, master):
        self.master = master
        self.master.title("Lines 98")
        self.cell_size = 40
        self.grid_size = 9
        self.canvas = tk.Canvas(master, width=self.cell_size*self.grid_size, height=self.cell_size*self.grid_size)
        self.canvas.pack()

        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.selected_cell = None
        self.colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'cyan']
        self.score = 0
        self.score_label = tk.Label(master, text=f"Score: {self.score}")
        self.score_label.pack()

        self.new_game_button = tk.Button(master, text="New Game", command=self.new_game)
        self.new_game_button.pack()

        self.initialize_grid()
        self.draw_grid()
        self.canvas.bind("<Button-1>", self.on_click)

    def initialize_grid(self):
        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for _ in range(5):
            self.add_new_ball()

    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x, y = j * self.cell_size, i * self.cell_size
                self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill="white", outline="gray")
                if self.grid[i][j]:
                    self.draw_ball(i, j)

    def draw_ball(self, i, j):
        x, y = j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size // 2
        color = self.grid[i][j]
        self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=color, outline=color)

    def add_new_ball(self):
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i][j] is None]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = random.choice(self.colors)
            self.check_lines_after_new_ball(i, j)

    def check_lines_after_new_ball(self, i, j):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        to_remove = set()
        for di, dj in directions:
            line = self.check_line(i, j, di, dj)
            if len(line) >= 5:
                to_remove.update(line)
        if to_remove:
            for ri, rj in to_remove:
                self.grid[ri][rj] = None
            self.score += len(to_remove)
            self.score_label.config(text=f"Score: {self.score}")
            self.draw_grid()

    def on_click(self, event):
        i, j = event.y // self.cell_size, event.x // self.cell_size
        if self.selected_cell:
            if self.grid[i][j] is None:
                self.move_ball(self.selected_cell, (i, j))
                self.selected_cell = None
            elif self.grid[i][j]:
                self.canvas.delete("selected_ball")
                self.selected_cell = (i, j)
                self.animate_selection(i, j)
        elif self.grid[i][j]:
            self.selected_cell = (i, j)
            self.animate_selection(i, j)
        self.draw_grid()

    def animate_selection(self, i, j):
        x, y = j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size // 2
        color = self.grid[i][j]
        for size in range(15, 20, 1):
            self.canvas.delete("selected_ball")
            self.canvas.create_oval(x - size, y - size, x + size, y + size, fill=color, outline="white", width=2, tags="selected_ball")
            self.master.update()
            time.sleep(0.05)
        for size in range(20, 15, -1):
            self.canvas.delete("selected_ball")
            self.canvas.create_oval(x - size, y - size, x + size, y + size, fill=color, outline="white", width=2, tags="selected_ball")
            self.master.update()
            time.sleep(0.05)

    def move_ball(self, start, end):
        si, sj = start
        ei, ej = end
        path = self.find_path(start, end)
        if path:
            self.animate_move(path)
            self.grid[ei][ej] = self.grid[si][sj]
            self.grid[si][sj] = None
            lines_completed = self.check_lines()
            if not lines_completed:
                for _ in range(3):
                    self.add_new_ball()
            self.draw_grid()

    def find_path(self, start, end):
        queue = [start]
        visited = set([start])
        parent = {start: None}
        while queue:
            current = queue.pop(0)
            if current == end:
                path = []
                while current:
                    path.append(current)
                    current = parent[current]
                return path[::-1]
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = current[0] + di, current[1] + dj
                if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size and self.grid[ni][nj] is None and (ni, nj) not in visited:
                    queue.append((ni, nj))
                    visited.add((ni, nj))
                    parent[(ni, nj)] = current
        return None

    def animate_move(self, path):
        color = self.grid[path[0][0]][path[0][1]]
        for i, (ri, rj) in enumerate(path):
            self.canvas.delete("ball")
            x, y = rj * self.cell_size + self.cell_size // 2, ri * self.cell_size + self.cell_size // 2
            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=color, outline=color, tags="ball")
            self.master.update()
            time.sleep(0.1)
            if i > 0:
                prev_ri, prev_rj = path[i-1]
                prev_x, prev_y = prev_rj * self.cell_size, prev_ri * self.cell_size
                self.canvas.create_rectangle(prev_x, prev_y, prev_x + self.cell_size, prev_y + self.cell_size, fill="white", outline="gray")

    def check_lines(self):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        to_remove = set()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j]:
                    for di, dj in directions:
                        line = self.check_line(i, j, di, dj)
                        if len(line) >= 5:
                            to_remove.update(line)
        if to_remove:
            for i, j in to_remove:
                self.grid[i][j] = None
            self.score += len(to_remove)
            self.score_label.config(text=f"Score: {self.score}")
            return True
        return False

    def check_line(self, i, j, di, dj):
        color = self.grid[i][j]
        line = [(i, j)]
        for step in range(1, 5):
            ni, nj = i + step * di, j + step * dj
            if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size and self.grid[ni][nj] == color:
                line.append((ni, nj))
            else:
                break
        return line if len(line) >= 5 else []

    def new_game(self):
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.selected_cell = None
        self.initialize_grid()
        self.draw_grid()

if __name__ == "__main__":
    root = tk.Tk()
    game = Lines98Game(root)
    root.mainloop()
