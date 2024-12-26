import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def denormalize(x, old_min, old_max, new_min, new_max):
    # Map range [-1, 1] to [0, 750]
    return ((x - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min


def draw_midpoint_line(x1, y1, x2, y2):
    # Map normalized to window coords
    x1 = int(denormalize(x1, -1, 1, -750, window_width))
    y1 = int(denormalize(y1, -1, 1, -750, window_height))
    x2 = int(denormalize(x2, -1, 1, -750, window_width))
    y2 = int(denormalize(y2, -1, 1, -750, window_height))


    dx = x2 - x1
    dy = y2 - y1

    # Determine the direction of the line
    y_larger_than_x = abs(dy) > abs(dx)
    if y_larger_than_x:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1

    d = 2 * abs(dy) - abs(dx)
    if y1 < y2:
        y_step = 1
    else:
        y_step = -1

    temp_y = y1
    glBegin(GL_POINTS)
    for x in range(x1, x2 + 1):
        if y_larger_than_x:
            glVertex2f(temp_y / window_width, x / window_height)
        else:
            glVertex2f(x / window_width, temp_y / window_height)
        if d > 0:
            temp_y += y_step
            d -= 2 * abs(dx)
        d += 2 * abs(dy)
    glEnd()



def draw_midpoint_circle(cx, cy, radius):
    # Map normalized to window coords
    cx = int(denormalize(cx, -1, 1, 0, window_width))
    cy = int(denormalize(cy, -1, 1, 0, window_height))
    radius = int(radius * (window_width / 2))  # Scale radius to window size

    x = 0
    y = radius
    d = 1 - radius

    glBegin(GL_POINTS)
    while x <= y:
        # Plot the 8 symmetric points
        glVertex2f((cx + x) / window_width, (cy + y) / window_height)
        glVertex2f((cx - x) / window_width, (cy + y) / window_height)
        glVertex2f((cx + x) / window_width, (cy - y) / window_height)
        glVertex2f((cx - x) / window_width, (cy - y) / window_height)
        glVertex2f((cx + y) / window_width, (cy + x) / window_height)
        glVertex2f((cx - y) / window_width, (cy + x) / window_height)
        glVertex2f((cx + y) / window_width, (cy - x) / window_height)
        glVertex2f((cx - y) / window_width, (cy - x) / window_height)

        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
    glEnd()

def draw_player():
    x1 = player_x - player_size
    x2 = player_x + player_size
    y1 = player_y - player_size
    y2 = player_y + player_size
    
    # Draw the four edges
    glColor3f(1.0, 0.0, 0.0) # red player

    draw_midpoint_line(x1, y1, x2, y1)  # Bottom edge
    draw_midpoint_line(x2, y1, x2, y2)  # Right edge
    draw_midpoint_line(x2, y2, x1, y2)  # Top edge
    draw_midpoint_line(x1, y2, x1, y1)  # Left edge

    glColor3f(1.0, 1.0, 1.0)


def generate_maze(rows, cols):
    # Initialize the maze with walls (True for wall, False for no wall)
    maze = []
    for temp1 in range(rows):
        row = []
        for temp2 in range(cols):
            # Starts with walls on all four sides: [Top, Right, Bottom, Left]
            cell = [True, True, True, True]
            row.append(cell)
        maze.append(row)

    visited = []
    for _ in range(rows):
        # All cells marked as not visited
        row = [False] * cols
        visited.append(row)

    def is_valid(x, y):
        # Check if the cell (x, y) is within the bounds of the maze
        return 0 <= x < rows and 0 <= y < cols

    def dfs_maze_create(x, y):
        visited[x][y] = True
        # Randomize to ensure randomness in maze generation
        directions = random.sample(DIRECTIONS, len(DIRECTIONS))

        for x_direct, y_direct in directions:
            neigh_x, neigh_y = x + x_direct, y + y_direct
            if is_valid(neigh_x, neigh_y) and not visited[neigh_x][neigh_y]:

                if x_direct == -1:  # Move up
                    maze[x][y][0] = False  # Remove top wall of current
                    maze[neigh_x][neigh_y][2] = False  # Remove bottom wall of neighbor
                elif x_direct == 1:  # Move down
                    maze[x][y][2] = False  # Remove bottom wall of current
                    maze[neigh_x][neigh_y][0] = False  # Remove top wall of neighbor
                elif y_direct == -1:  # Move left
                    maze[x][y][3] = False  # Remove left wall of current
                    maze[neigh_x][neigh_y][1] = False  # Remove right wall of neighbor
                elif y_direct == 1:  # Move right
                    maze[x][y][1] = False  # Remove right wall of current
                    maze[neigh_x][neigh_y][3] = False  # Remove left wall of neighbor
                dfs_maze_create(neigh_x, neigh_y)

    # Start dfs_maze_create from random position
    start_x, start_y = random.randint(0, rows - 1), random.randint(0, cols - 1)
    dfs_maze_create(start_x, start_y)

    # MAZE REMEMBER
    # for cols in range(len(maze)):
    #     with open('maze_shape.txt', 'a') as file:
    #         file.write(str(maze[cols])+"\n")

    maze_level_1  = [[[True, False, False, True], [True, False, False, False], [True, True, False, False], [True, False, False, True], [True, False, True, False], [True, False, False, False], [True, True, False, False], [True, False, False, True], [True, False, False, False], [True, True, False, False], [True, False, False, True], [True, True, False, False], [True, False, False, True], [True, True, False, False], [True, True, True, True]],
    [[False, True, False, True], [False, True, False, True], [False, True, False, True], [False, False, True, True], [True, True, False, False], [False, False, True, True], [False, True, False, False], [False, True, False, True], [False, True, False, True], [False, False, True, True], [False, True, False, False], [False, False, True, True], [False, True, False, False], [False, False, True, True], [True, True, False, False]],
    [[False, True, False, True], [False, True, False, True], [False, False, True, True], [True, False, True, False], [False, True, True, False], [True, False, False, True], [False, True, True, False], [False, True, True, True], [False, False, False, True], [True, True, False, False], [False, True, True, True], [True, False, False, True], [False, False, True, False], [True, True, True, False], [False, True, False, True]],
    [[False, True, False, True], [False, False, True, True], [True, False, True, False], [True, True, False, False], [True, False, True, True], [False, False, True, False], [True, False, False, False], [True, True, False, False], [False, True, True, True], [False, False, True, True], [True, False, True, False], [False, True, True, False], [True, False, False, True], [True, False, True, False], [False, True, False, False]],
    [[False, True, False, True], [True, False, False, True], [True, False, True, False], [False, True, True, False], [True, False, False, True], [True, False, True, False], [False, True, False, False], [False, False, True, True], [True, False, False, False], [True, False, True, False], [True, False, True, False], [True, True, False, False], [False, True, False, True], [True, True, False, True], [False, True, False, True]],
    [[False, True, False, True], [False, True, False, True], [True, False, False, True], [True, False, True, False], [False, True, True, False], [True, True, False, True], [False, True, False, True], [True, True, False, True], [False, False, True, True], [True, False, True, False], [True, True, False, False], [False, True, False, True], [False, False, False, True], [False, False, True, False], [False, True, True, False]],
    [[False, True, True, True], [False, True, False, True], [False, True, False, True], [True, False, False, True], [True, False, True, False], [False, False, True, False], [False, True, True, False], [False, False, True, True], [True, False, True, False], [True, True, False, False], [False, False, False, True], [False, True, True, False], [False, False, True, True], [True, False, False, False], [True, True, False, False]],
    [[True, False, False, True], [False, True, True, False], [False, True, False, True], [False, False, True, True], [True, False, True, False], [True, False, True, False], [True, False, True, False], [True, False, True, False], [True, False, True, False], [False, True, True, False], [False, True, False, True], [True, False, False, True], [True, True, False, False], [False, True, True, True], [False, True, False, True]],
    [[False, False, True, True], [True, True, False, False], [False, True, False, True], [True, False, False, True], [True, False, True, False], [True, False, True, False], [True, False, False, False], [True, False, True, False], [True, True, False, False], [True, True, False, True], [False, False, True, True], [False, True, True, False], [False, False, True, True], [True, True, False, False], [False, True, False, True]],
    [[True, True, False, True], [False, False, True, True], [False, True, True, False], [False, True, False, True], [True, False, False, True], [True, True, False, False], [False, False, False, True], [True, True, False, False], [False, False, True, True], [False, True, False, False], [True, False, False, True], [True, False, False, False], [True, False, True, False], [False, True, False, False], [False, True, False, True]],
    [[False, False, False, True], [True, False, False, False], [True, True, True, False], [False, True, False, True], [False, True, False, True], [False, True, False, True], [False, True, True, True], [False, True, False, True], [True, False, False, True], [False, False, True, False], [False, True, True, False], [False, False, True, True], [True, True, False, False], [False, False, True, True], [False, True, False, False]],
    [[False, True, False, True], [False, False, True, True], [True, False, True, False], [False, True, True, False], [False, True, False, True], [False, False, True, True], [True, False, True, False], [False, True, False, False], [False, True, False, True], [True, False, False, True], [True, False, True, False], [True, True, False, False], [False, False, True, True], [True, True, False, False], [False, True, False, True]],
    [[False, False, True, True], [True, False, True, False], [True, False, True, False], [True, True, False, False], [False, False, True, True], [True, False, True, False], [True, True, False, False], [False, True, True, True], [False, False, True, True], [False, True, True, False], [True, True, False, True], [False, False, True, True], [True, True, False, False], [False, False, True, True], [False, True, True, False]],
    [[True, True, False, True], [True, False, False, True], [True, True, False, False], [False, False, True, True], [True, True, False, False], [True, False, False, True], [False, True, True, False], [True, False, False, True], [True, False, True, False], [True, True, False, False], [False, False, False, True], [True, True, False, False], [False, True, False, True], [True, False, True, True], [True, True, False, False]],
    [[False, False, True, True], [False, True, True, False], [False, False, True, True], [True, False, True, False], [False, True, True, False], [False, False, True, True], [True, False, True, False], [False, True, True, False], [True, True, True, True], [False, False, True, True], [False, True, True, False], [False, False, True, True], [False, False, True, False], [True, False, True, False], [False, True, True, False]]]
    

    maze_level_2 = [[[True, False, False, True], [True, False, True, False], [True, False, False, False], [True, False, True, False], [True, True, False, False], [True, True, True, True], [True, False, False, True], [True, False, False, False], [True, True, False, False], [True, False, True, True], [True, False, False, False], [True, False, False, False], [True, False, True, False], [True, False, True, False], [True, True, False, False]],
    [[False, False, True, True], [True, True, False, False], [False, True, False, True], [True, False, False, True], [False, True, True, False], [True, False, False, True], [False, False, False, False], [False, True, True, False], [False, False, True, True], [True, True, False, False], [False, True, True, True], [False, False, True, True], [True, True, False, False], [True, True, False, True], [False, True, False, True]],
    [[True, False, True, True], [False, False, True, False], [False, True, False, False], [False, False, True, True], [True, False, False, False], [False, True, True, False], [False, True, False, True], [True, False, False, True], [True, True, False, False], [False, False, True, True], [True, False, False, False], [True, False, True, False], [False, True, True, False], [False, False, False, True], [False, True, True, False]],
    [[True, False, False, True], [True, False, True, False], [False, True, True, False], [True, False, True, True], [False, True, False, False], [True, False, True, True], [False, True, False, False], [False, True, True, True], [False, False, True, True], [True, False, False, False], [False, False, False, False], [True, False, True, False], [True, True, False, False], [False, True, False, True], [True, True, False, True]],
    [[False, False, True, True], [True, True, False, False], [True, False, False, True], [True, True, False, False], [False, False, False, True], [True, False, False, False], [False, False, True, False], [True, True, True, False], [True, False, False, True], [False, True, True, False], [False, False, False, True], [True, False, True, False], [False, True, True, False], [False, True, False, True], [False, True, False, True]],
    [[True, True, False, True], [False, False, True, True], [False, True, True, False], [False, True, False, True], [False, True, False, True], [False, False, True, True], [True, False, False, False], [True, True, False, False], [False, True, False, True], [True, False, True, True], [False, True, True, False], [True, False, False, True], [True, True, False, False], [False, True, False, True], [False, True, False, True]],
    [[False, False, False, True], [True, False, False, False], [True, True, True, False], [False, True, False, True], [False, False, True, True], [True, False, True, False], [False, True, True, False], [False, True, False, True], [False, False, True, True], [True, False, True, False], [True, True, False, False], [False, True, False, True], [False, True, False, True], [False, False, True, True], [False, True, False, False]],
    [[False, True, False, True], [False, True, False, True], [True, False, False, True], [False, True, True, False], [True, False, True, True], [True, False, True, False], [True, True, False, False], [False, False, True, True], [True, False, False, False], [True, True, False, False], [False, True, False, True], [False, True, False, True], [False, False, False, True], [True, True, True, False], [False, True, False, True]],
    [[False, True, False, True], [False, True, False, True], [False, False, True, True], [True, False, True, False], [True, True, False, False], [True, False, False, True], [False, True, True, False], [True, True, False, True], [False, False, False, True], [False, True, True, False], [False, True, False, True], [False, True, False, True], [False, False, True, True], [True, False, True, False], [False, True, True, False]],
    [[False, False, True, True], [False, False, False, False], [True, False, True, False], [True, True, False, False], [False, False, True, True], [False, True, True, False], [True, False, False, True], [False, False, True, False], [False, True, True, False], [True, False, False, True], [False, True, False, False], [False, True, False, True], [True, False, False, True], [True, False, True, False], [True, True, False, False]],
    [[True, False, False, True], [False, True, False, False], [True, False, False, True], [False, False, True, False], [True, False, False, False], [True, True, False, False], [False, False, True, True], [True, True, False, False], [True, False, False, True], [False, True, True, False], [False, True, True, True], [False, True, False, True], [False, True, False, True], [True, False, False, True], [False, True, True, False]],
    [[False, True, False, True], [False, True, False, True], [False, True, False, True], [True, False, False, True], [False, True, True, False], [False, True, False, True], [True, False, True, True], [False, True, True, False], [False, True, False, True], [True, False, False, True], [True, False, False, False], [False, True, True, False], [False, True, False, True], [False, False, True, True], [True, True, False, False]],
    [[False, True, False, True], [False, True, False, True], [False, True, False, True], [False, False, True, True], [True, True, False, False], [False, False, True, True], [True, False, True, False], [True, False, True, False], [False, True, True, False], [False, True, False, True], [False, False, True, True], [True, False, True, False], [False, False, True, False], [True, True, True, False], [False, True, False, True]],
    [[False, True, False, True], [False, True, True, True], [False, False, True, True], [True, True, False, False], [False, True, False, True], [True, True, True, True], [True, False, False, True], [True, True, False, False], [True, False, False, True], [False, True, True, False], [True, False, False, True], [True, False, True, False], [True, True, False, False], [True, False, False, True], [False, True, False, False]],
    [[False, False, True, True], [True, False, True, False], [True, False, True, False], [False, True, True, False], [False, False, True, True], [True, False, True, False], [False, True, True, False], [False, False, True, True], [False, False, True, False], [True, False, True, False], [False, True, True, False], [True, False, True, True], [False, False, True, False], [False, True, True, False], [False, True, True, True]]]


    # return maze
    return maze_level_1


def draw_maze():
    rows = len(maze)
    cols = len(maze[0])
    cell_size = 2.0 / max(rows, cols)  # Normalize to OpenGL coordinates

    glColor3f(1.0, 1.0, 1.0)  # White walls

    for row in range(rows):
        for col in range(cols):
            x = col * cell_size - 1
            y = 1 - row * cell_size

            # Draw walls if they exist
            if maze[row][col][0]:  # Top wall
                draw_midpoint_line(x, y, x + cell_size, y)
            if maze[row][col][1]:  # Right wall
                draw_midpoint_line(x + cell_size, y, x + cell_size, y - cell_size)
            if maze[row][col][2]:  # Bottom wall
                draw_midpoint_line(x, y - cell_size, x + cell_size, y - cell_size)
            if maze[row][col][3]:  # Left wall
                draw_midpoint_line(x, y, x, y - cell_size)


def check_collision(new_x, new_y):
    # Check if the player's new position collides with maze walls
    rows, cols = len(maze), len(maze[0])
    cell_size = 2.0 / max(rows, cols)

    # Calculate Player's current cell
    row = int((1 - new_y) // cell_size)
    col = int((new_x + 1) // cell_size)

    if row < 0 or row >= rows or col < 0 or col >= cols:
        return player_x, player_y

    # Check for walls
    if new_x < player_x and not maze[row][col + 1][3]:  # Left
        while col >= 0 and not maze[row][col][1]:
            col -= 1
        return displacement - 1 + (col + 1) * cell_size, player_y

    if new_x > player_x and not maze[row][col - 1][1]:  # Right
        while col < cols and not maze[row][col][3]:
            col += 1
        return -displacement - 1 + col * cell_size, player_y

    if new_y > player_y and not maze[row + 1][col][0]:  # Up
        while row >= 0 and not maze[row][col][2]:
            row -= 1
        return player_x, - displacement + 1 - (row + 1) * cell_size

    if new_y < player_y and not maze[row - 1][col][2]:  # Down
        while row < rows and not maze[row][col][0]:
            row += 1
        return player_x, displacement + 1 - row * cell_size

    return player_x, player_y

def keyboard(key, x, y):
    global player_x, player_y, step

    if game_pause:
        return


    if key == b'a':  # Move left
        new_x, new_y = player_x - step, player_y
        player_x, player_y = check_collision(new_x, new_y)

    elif key == b'd':  # Move right
        new_x, new_y = player_x + step, player_y
        player_x, player_y = check_collision(new_x, new_y)

    elif key == b'w':  # Move up
        new_x, new_y = player_x, player_y + step
        player_x, player_y = check_collision(new_x, new_y)

    elif key == b's':  # Move down
        new_x, new_y = player_x, player_y - step
        player_x, player_y = check_collision(new_x, new_y)
    glutPostRedisplay()



# Global variables

game_pause = False
game_over = False


def draw_button(x, y, width, height, color, shape):
    glColor3f(*color)
    if shape == "arrow":  # Restart button (Left Arrow)
        draw_midpoint_line(x - width, y, x + width, y)
        draw_midpoint_line(x - width, y, x, y + height)
        draw_midpoint_line(x - width, y, x, y - height)
    elif shape == "play":  # Play button (Triangle)
        draw_midpoint_line(x - width, y - height, x - width, y + height)
        draw_midpoint_line(x - width, y - height, x + width, y)
        draw_midpoint_line(x - width, y + height, x + width, y)
    elif shape == "pause":  # Pause button (Two lines)
        draw_midpoint_line(x - width, y + height, x - width, y - height)
        draw_midpoint_line(x + width, y + height, x + width, y - height)
    elif shape == "cross":  # Exit button (Cross)
        draw_midpoint_line(x - width, y + height, x + width, y - height)
        draw_midpoint_line(x + width, y + height, x - width, y - height)


def draw_buttons():
    button_width = 0.045
    button_height = 0.045
    spacing = 0.15  # Spacing between buttons
    start_x = 0.93
    start_y = 0.93

    # Restart button
    draw_button(start_x, start_y, button_width, button_height, (0.0, 0.0, 1.0), "arrow")

    # Play/Pause button
    if game_pause:
        draw_button(start_x, start_y - spacing, button_width, button_height, (0.0, 1.0, 0.0), "play")
    else:
        draw_button(start_x, start_y - spacing, button_width / 3, button_height, (0.0, 1.0, 0.0), "pause")

    # Exit button
    draw_button(start_x, start_y - 2 * spacing, button_width, button_height, (1.0, 0.0, 0.0), "cross")


def mouse_click(button, state, x, y):
    global game_pause, game_over, player_x, player_y, maze
    if state == GLUT_DOWN:
        # Convert mouse coordinates to OpenGL coordinates
        opengl_x = (x / window_width) * 2 - 1
        opengl_y = 1 - (y / window_height) * 2

        # Check button boundaries
        restart_bounds = (0.88, 0.98, 0.88, 0.98)
        play_pause_bounds = (0.88, 0.98, 0.73, 0.83)
        exit_bounds = (0.88, 0.98, 0.58, 0.68)

        if restart_bounds[0] < opengl_x < restart_bounds[1] and restart_bounds[2] < opengl_y < restart_bounds[3]:
            # Restart the game
            game_over = False
            game_pause = False
            player_x, player_y = -0.93333333, 0.93333333  # Reset player position
            maze = generate_maze(rows, cols)  # Regenerate the maze
            print("Game Restarted")

        elif play_pause_bounds[0] < opengl_x < play_pause_bounds[1] and play_pause_bounds[2] < opengl_y < play_pause_bounds[3]:
            # Toggle play/pause
            game_pause = not game_pause
            print("Game Paused" if game_pause else "Game Resumed")

        elif exit_bounds[0] < opengl_x < exit_bounds[1] and exit_bounds[2] < opengl_y < exit_bounds[3]:
            # Exit the game
            print("Game Exited")
            glutLeaveMainLoop()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    draw_maze()
    draw_player()

    draw_buttons()
    glutSwapBuffers()


# Window dimensions
window_width = 750
window_height = 750


maze = []  # To store the generated maze
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

rows, cols = 15, 15  # Maze dimensions
maze = generate_maze(rows, cols)
step = 2.0 / max(len(maze), len(maze[0]))

# Player variables
player_x, player_y = -0.93333333, 0.93333333 # Initial position of the player
player_size = 0.05  # Player's size
displacement= 0.0666666666


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(window_width, window_height)
glutCreateWindow(b"Maze Dasher")
glClearColor(0.1, 0.1, 0.1, 1.0)  # Gray background
gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse_click)
glutMainLoop()