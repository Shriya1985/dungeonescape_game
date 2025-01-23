import tkinter as tk
from tkinter import messagebox

# Dungeon map (10x10 grid with two rooms)
dungeon_map = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", ".", ".", ".", ".", ".", ".", "#", ".", "#"],
    ["#", ".", "P", ".", ".", ".", ".", "#", ".", "#"],
    ["#", ".", ".", ".", ".", ".", ".", "#", ".", "#"],
    ["#", ".", ".", ".", ".", ".", ".", "#", ".", "#"],
    ["#", ".", ".", ".", "A", "E", "A", "#", ".", "#"],
    ["#", "#", "#", "#", "#", "#", ".", "#", ".", "#"],
    ["#", ".", ".", "A", ".", ".", ".", ".", ".", "#"],
    ["#", ".", "A", "E", ".", ".", ".", ".", ".", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],  # Room 2 start (exit blocked initially)
]

# Second room (10x10 grid)
second_room = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", ".", ".", ".", ".", ".", ".", "#", ".", "#"],
    ["#", ".", "P", ".", ".", ".", ".", "#", ".", "#"],
    ["#", ".", ".", ".", ".", ".", ".", "#", ".", "#"],
    ["#", ".", ".", ".", ".", ".", ".", "#", ".", "#"],
    ["#", ".", ".", ".", "A", "E", "A", "#", ".", "#"],
    ["#", "#", "#", "#", "#", "#", ".", "#", ".", "#"],
    ["#", ".", ".", "A", ".", ".", ".", ".", ".", "#"],
    ["#", ".", "A", "E", ".", ".", ".", ".", ".", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],  # Exit location
]

# Player's initial position
player_position = [2, 2]

# Health item positions (example positions)
health_items = [(1, 1), (4, 4), (8, 4)]

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Dungeon Escape Game")
root.attributes("-fullscreen", True)  # Full-screen mode

# Frames for different screens
welcome_frame = tk.Frame(root)
story_frame = tk.Frame(root)
game_frame = tk.Frame(root)
victory_frame = tk.Frame(root)

# Health and game state
player_health = 100
game_running = True
enemies_defeated_in_room_1 = False
enemies_defeated_in_room_2 = False


# Function to reveal the exit in the first room
def reveal_exit_in_room_1():
    global dungeon_map
    dungeon_map[7][9] = "."  # Change a wall block to a path for exit in room 1
    render_map()
    messagebox.showinfo("Exit Revealed", "You defeated all enemies in Room 1! The exit is now open.")


# Function to reveal the exit in the second room
def reveal_exit_in_room_2():
    global second_room
    second_room[7][9] = "."  # Change a wall block to a path for exit in room 2
    render_map()
    messagebox.showinfo("Exit Revealed", "You defeated all enemies in Room 2! The exit is now open.")


# Function to show the victory page
def show_victory_page():
    game_frame.pack_forget()  # Hide the game frame
    victory_frame.pack(fill='both', expand=True)  # Show the victory frame
    victory_label = tk.Label(victory_frame, text="""
    Congratulations, Adventurer!

    You have successfully escaped the dungeon and defeated all the enemies!
    Your courage and skill have earned you freedom.

    The dungeon is no more, and you are free to continue your journey. But remember...
    There are more dungeons ahead, and greater challenges await!

    Thank you for playing Dungeon Escape!
    """, font=("Helvetica", 18))
    victory_label.pack(pady=20)
    exit_button = tk.Button(victory_frame, text="Exit", font=("Helvetica", 14), command=root.destroy)
    exit_button.pack(pady=10)


# Function to show game over message
def game_over():
    global game_running
    game_running = False
    messagebox.showinfo("Game Over", "You were defeated by the enemy!")
    root.destroy()


# Function to show victory message
def game_won():
    global game_running
    game_running = False
    show_victory_page()


# Function to render the dungeon map on the grid
def render_map():
    global dungeon_map, second_room
    # Choose which room to render based on the game progress
    if not enemies_defeated_in_room_1:
        current_map = dungeon_map
    else:
        current_map = second_room

    for row in range(10):
        for col in range(10):
            cell = current_map[row][col]
            if cell == "#":
                buttons[row][col].config(text="", bg="gray")
            elif cell == ".":
                buttons[row][col].config(text="", bg="white")
            elif cell == "P":
                buttons[row][col].config(text="P", bg="green")
            elif cell == "E":
                buttons[row][col].config(text="", bg="white")
            elif cell == "A":
                buttons[row][col].config(text="", bg="blue")
            elif (row, col) in health_items:
                buttons[row][col].config(text="", bg="blue")

    # Update health display
    health_label.config(text=f"Health: {player_health}")


# Function to move the player
def move_player(event):
    global player_position, player_health, game_running, health_items, enemies_defeated_in_room_1, enemies_defeated_in_room_2
    if not game_running:
        return

    row, col = player_position
    new_row, new_col = row, col

    # Determine new position based on W, A, S, D keys
    if event.keysym == "w" and row > 0:
        new_row = row - 1
    elif event.keysym == "s" and row < 9:
        new_row = row + 1
    elif event.keysym == "a" and col > 0:
        new_col = col - 1
    elif event.keysym == "d" and col < 9:
        new_col = col + 1
    elif event.keysym == "Up" and row > 0:
        new_row = row - 1
    elif event.keysym == "Down" and row < 9:
        new_row = row + 1
    elif event.keysym == "Left" and col > 0:
        new_col = col - 1
    elif event.keysym == "Right" and col < 9:
        new_col = col + 1

    # Check if the new position is valid (not a wall)
    if (not enemies_defeated_in_room_1 and dungeon_map[new_row][new_col] != "#") or (
        enemies_defeated_in_room_1 and second_room[new_row][new_col] != "#"):

        # Check for interactions
        if (not enemies_defeated_in_room_1 and dungeon_map[new_row][new_col] == "E") or \
                (enemies_defeated_in_room_1 and second_room[new_row][new_col] == "E"):
            player_health -= 50
            if player_health <= 0:
                game_over()
                return
            messagebox.showwarning("Enemy Encounter", "You lost 50 health fighting the enemy!")
            if not enemies_defeated_in_room_1:
                dungeon_map[new_row][new_col] = "."  # Remove the enemy from the map
            else:
                second_room[new_row][new_col] = "."  # Remove the enemy from the map

            # Check if all enemies are defeated in the current room
            if not enemies_defeated_in_room_1:
                enemies_remaining = any("E" in row for row in dungeon_map)
                if not enemies_remaining:
                    enemies_defeated_in_room_1 = True
                    reveal_exit_in_room_1()
            else:
                enemies_remaining = any("E" in row for row in second_room)
                if not enemies_remaining:
                    enemies_defeated_in_room_2 = True
                    reveal_exit_in_room_2()

        elif (new_row, new_col) in health_items:
            health_items.remove((new_row, new_col))  # Remove the collected health item
            player_health += 20  # Increase health by 20
            messagebox.showinfo("Health Collected", "You collected a health item!")

        elif (new_row, new_col) == (7, 9) and enemies_defeated_in_room_2:
            game_won()
            return

        # Update the map
        if not enemies_defeated_in_room_1:
            dungeon_map[row][col] = "."  # Clear the old position
            dungeon_map[new_row][new_col] = "P"  # Set the new position
        else:
            second_room[row][col] = "."
            second_room[new_row][new_col] = "P"
        player_position = [new_row, new_col]

        render_map()


# Function to switch to the story screen
def show_story_screen():
    welcome_frame.pack_forget()  # Hide the welcome frame
    story_frame.pack(fill='both', expand=True)  # Show the story frame


# Function to switch to the game screen
def show_game_screen():
    story_frame.pack_forget()  # Hide the story frame
    game_frame.pack(fill='both', expand=True)  # Show the game frame
    render_map()  # Render the dungeon map


# Function to show instructions
def show_instructions():
    instructions = (
        "Instructions:\n"
        "- Use W, A, S, D keys to move.\n"
        "- Defeat enemies to open exits.\n"
        "- Collect health items.\n"
        "- Reach the exit to win the game!"
    )
    messagebox.showinfo("Instructions", instructions)

# Function to close the game
def close_game():
    root.quit()  # Close the Tkinter window

# --- Welcome Screen ---
welcome_label = tk.Label(welcome_frame, text="Welcome to Dungeon Escape!", font=("Helvetica", 16))
welcome_label.pack(pady=20)

start_button = tk.Button(welcome_frame, text="Start Game", font=("Helvetica", 14), command=show_story_screen)
start_button.pack(pady=10)

instructions_button = tk.Button(welcome_frame, text="Instructions", font=("Helvetica", 14), command=show_instructions)
instructions_button.pack(pady=10)

welcome_frame.pack()  # Show the welcome screen initially

# --- Story Screen ---
story_label = tk.Label(story_frame, text="""
You are a fearless adventurer seeking fame and fortune.
Legends speak of a dungeon filled with treasures and guarded by fearsome creatures.
 Many have entered; none have returned.
Now, it’s your turn to face the challenge. 
To escape, you must defeat the enemies, solve the dungeon’s mysteries, and find the way out.

Will you survive and claim the treasure, or will the dungeon claim you as its next victim?

Your journey begins now.""", font=("Helvetica", 16))
story_label.pack(pady=20)

start_game_button = tk.Button(story_frame, text="Start Game", font=("Helvetica", 14), command=show_game_screen)
start_game_button.pack(pady=10)

story_frame.pack_forget()  # Initially hide the story screen

# --- Game Screen ---
# Create the grid of buttons (10x10 dungeon)
buttons = [[None for _ in range(10)] for _ in range(10)]
for row in range(10):
    for col in range(10):
        buttons[row][col] = tk.Button(game_frame, width=10, height=5)  # Adjust width and height for larger buttons
        buttons[row][col].grid(row=row, column=col, sticky="nsew")  # Make the buttons expand with the window

# Adjust the grid configuration to be resizable
for i in range(10):
    game_frame.grid_columnconfigure(i, weight=1, uniform="equal")
    game_frame.grid_rowconfigure(i, weight=1, uniform="equal")

# Health display
health_label = tk.Label(game_frame, text=f"Health: {player_health}", font=("Helvetica", 14))
health_label.grid(row=10, column=0, columnspan=10, pady=10)

# Close button for the game screen
close_button = tk.Button(game_frame, text="Close", font=("Helvetica", 14), command=close_game)
close_button.grid(row=11, column=0, columnspan=10, pady=10)

# Bind keyboard events to the root window for W, A, S, D keys
root.bind("<w>", move_player)
root.bind("<s>", move_player)
root.bind("<a>", move_player)
root.bind("<d>", move_player)

root.bind("<Up>", move_player)
root.bind("<Down>", move_player)
root.bind("<Left>", move_player)
root.bind("<Right>", move_player)

# Start the Tkinter main loop
root.mainloop()