import tkinter as tk
from tkinter import simpledialog, messagebox
from eight_puzzle_logic import EightPuzzleLogic

class EightPuzzleUI:
    def __init__(self, master):
        # Initialize the main window
        self.master = master
        self.master.title("8-Puzzle Game")
        self.master.geometry("360x380")
        self.logic = EightPuzzleLogic()
        self.create_buttons()
        self.master.config(bg="#aed6f1")

    def create_buttons(self):
        # Create buttons for the puzzle tiles
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.update_ui_with_state(self.logic.tiles)

        # Automatic Reset button
        reset_button = tk.Button(self.master, text="Reset (Auto)", width=12, height=1, font=('Arial', 10), command=self.reset)
        reset_button.grid(row=3, column=0, padx=5, pady=5)

        # Manual Reset button
        manual_reset_button = tk.Button(self.master, text="Reset (Manual)", width=12, height=1, font=('Arial', 10), command=self.manual_reset)
        manual_reset_button.grid(row=3, column=2, padx=5, pady=5)

        # Buttons to run solving algorithms
        a_star_button = tk.Button(self.master, text="A*", width=12, height=1, font=('Arial', 10), command=self.run_a_star)
        a_star_button.grid(row=4, column=0, padx=5, pady=5)

        bfs_button = tk.Button(self.master, text="BFS", width=12, height=1, font=('Arial', 10), command=self.run_bfs)
        bfs_button.grid(row=4, column=2, padx=5, pady=5)

    def reset(self):
        # Automatic reset of the puzzle
        self.logic.reset()
        self.update_ui_with_state(self.logic.tiles)

    def manual_reset(self):
        # Manual reset of the puzzle
        self.logic.empty_states()
        self.update_ui_with_state(self.logic.tiles)

        manual_values = []
        try:
            for i in range(3):
                for j in range(3):
                    value = simpledialog.askinteger("Input", f"Enter tile {3*i+j} (0-8):", minvalue=0, maxvalue=8)
                    if value is None:  # User cancelled the input
                        self.reset()
                        return
                    self.logic.set_manual_state(i, j, value)
                    self.update_ui_with_state(self.logic.tiles)
                    manual_values.append(value)

            if len(set(manual_values)) != 9:
                raise ValueError("Each number must be unique!")

            

        except ValueError as ve:
            messagebox.showerror("Invalid Input", str(ve))
            self.reset()

    def update_ui_with_state(self, state):
        # Update the UI with the current puzzle state
        for i in range(3):
            for j in range(3):
                if state[i][j] == self.logic.empty_tile:
                    if self.buttons[i][j]:
                        self.buttons[i][j].grid_forget()
                        self.buttons[i][j] = None
                else:
                    if self.buttons[i][j]:
                        self.buttons[i][j].config(text=str(state[i][j]))
                    else:
                        btn = tk.Button(self.master, text=str(state[i][j]), font=('Arial', 24), width=4, height=2)
                        btn.grid(row=i, column=j, padx=5, pady=5)
                        self.buttons[i][j] = btn

    def animate_solution(self, solution, time):
        # Animate the solution found by a solver
        if solution:
            def step(index):
                if index < len(solution):
                    self.update_ui_with_state(solution[index])
                    self.master.after(time, step, index + 1)  # Update every 'time' milliseconds
            step(0)
        else:
            messagebox.showinfo("Result", "No solution found.")

    def run_a_star(self):
        # Execute A* algorithm and animate the solution
        solution, iterations = self.logic.run_a_star()
        self.animate_solution(solution, 600)
        self.log_solution(solution, iterations)

    def run_bfs(self):
        # Execute BFS algorithm and animate the solution
        solution, iterations = self.logic.run_bfs()
        self.animate_solution(solution, 600)
        self.log_solution(solution, iterations)

    def log_solution(self, solution, iterations):
        if solution:
            print("Solution found:")
            for i, step in enumerate(solution, 1):
                print(f"Step {i}: ")
                for line in step:
                    print(line)
            print(f"Resolved in {len(solution)} steps")
            print(f"Resolved in {iterations} iterations")
        else:
            print(f"No solution found. Made {iterations} iterations.")

if __name__ == "__main__":
    # Create the main window and start the application
    root = tk.Tk()
    game = EightPuzzleUI(root)
    root.mainloop()
