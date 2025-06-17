import curses
import random
import time

# Window configuration
stdscr = curses.initscr()
curses.curs_set(0)  # Hide the cursor
sh, sw = 20, 40
w = curses.newwin(sh, sw, 0, 0)  # Create a new window
w.keypad(1)  # Enable keyboard input for the window
w.timeout(100)  # Set the timeout (in milliseconds)

# Draw the borders
w.border(0)  # Add a border with the default character

# Initial position of the Snake
snake_x = sw // 4
snake_y = sh // 2
snake = [
    [snake_y, snake_x],
    [snake_y, snake_x - 1],
    [snake_y, snake_x - 2]
]

# Initial food
food = [sh // 2, sw // 2]
w.addch(food[0], food[1], curses.ACS_PI)  # Represent the food with a symbol

# Snake directions
key = curses.KEY_RIGHT
previous_key = key

# Initial score
score = 0

# Main game loop
while True:
    next_key = w.getch()
    
    # Change direction only if it is not reversed (e.g., if the snake is going right, it cannot immediately go left)
    if next_key == curses.KEY_RIGHT and previous_key != curses.KEY_LEFT:
        key = next_key
    elif next_key == curses.KEY_LEFT and previous_key != curses.KEY_RIGHT:
        key = next_key
    elif next_key == curses.KEY_UP and previous_key != curses.KEY_DOWN:
        key = next_key
    elif next_key == curses.KEY_DOWN and previous_key != curses.KEY_UP:
        key = next_key
    
    previous_key = key  # Update the previous direction

    # Calculate the new head of the Snake based on the direction
    if key == curses.KEY_RIGHT:
        new_head = [snake[0][0], snake[0][1] + 1]
    elif key == curses.KEY_LEFT:
        new_head = [snake[0][0], snake[0][1] - 1]
    elif key == curses.KEY_UP:
        new_head = [snake[0][0] - 1, snake[0][1]]
    elif key == curses.KEY_DOWN:
        new_head = [snake[0][0] + 1, snake[0][1]]

    # Add the new head to the Snake
    snake.insert(0, new_head)

    # Check if the Snake eats the food
    if snake[0] == food:
        food = None
        score += 1  # Increase the score when the food is eaten
        while food is None:
            new_food = [
                random.randint(1, sh - 2),  # To avoid the border
                random.randint(1, sw - 2)   # To avoid the border
            ]
            food = new_food if new_food not in snake else None
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        w.addch(tail[0], tail[1], ' ')

    # Check if the Snake hits itself or the borders
    if (
        snake[0][0] in [0, sh - 1] or  # The top and bottom borders
        snake[0][1] in [0, sw - 1] or  # The left and right borders
        snake[0] in snake[1:]
    ):
        curses.endwin()
        quit()

    # Add the new head of the Snake in the window with the block symbol
    w.addch(snake[0][0], snake[0][1], curses.ACS_BLOCK)

    # Show the score in the window
    w.addstr(0, 2, f'Score: {score}')  # Display the score at the top left