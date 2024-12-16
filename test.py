import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Window dimensions
window_width = 750
window_height = 750

# Player variables
player_x, player_y = -0.93333333, 0.93333333  # Initial position of the player
player_size = 0.05  # Player's size
displacement= 0.0666666666

maze = []  # To store the generated maze
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def generate_maze(rows, cols):
    # Initialize the maze with walls (True for wall, False for open space)
    maze = [[[True, True, True, True] for _ in range(cols)] for _ in range(rows)]

    # Track the visited cells
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    def is_valid(x, y):
        #Check if the cell (x, y) is within the bounds of the maze
        return 0 <= x < rows and 0 <= y < cols

    def dfs(x, y):
        visited[x][y] = True
        # Randomize the directions to ensure randomness in maze generation
        directions = random.sample(DIRECTIONS, len(DIRECTIONS))

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny) and not visited[nx][ny]:

                # Remove wall between current cell and neighbor
                if dx == -1:  # Move up
                    maze[x][y][0] = False  # Remove top wall of current
                    maze[nx][ny][2] = False  # Remove bottom wall of neighbor
                elif dx == 1:  # Move down
                    maze[x][y][2] = False  # Remove bottom wall of current
                    maze[nx][ny][0] = False  # Remove top wall of neighbor
                elif dy == -1:  # Move left
                    maze[x][y][3] = False  # Remove left wall of current
                    maze[nx][ny][1] = False  # Remove right wall of neighbor
                elif dy == 1:  # Move right
                    maze[x][y][1] = False  # Remove right wall of current
                    maze[nx][ny][3] = False  # Remove left wall of neighbor
                dfs(nx, ny)

    # Start DFS from random position
    start_x, start_y = random.randint(0, rows - 1), random.randint(0, cols - 1)
    dfs(start_x, start_y)
    # MAZE REMEMBER
    # for cols in range(len(maze)):
    #     with open('maze_shape.txt', 'a') as file:
    #         file.write(str(maze[cols])+"\n")
    return maze

def draw_maze():
    #Draw the maze using OpenGL line segments
    rows = len(maze)
    cols = len(maze[0])
    cell_size = 2.0 / max(rows, cols)  # Normalize to OpenGL coordinates

    glColor3f(1.0, 1.0, 1.0)  # White walls

    for row in range(rows):
        for col in range(cols):
            x =  col * cell_size -1
            y = 1 - row * cell_size

            # Draw walls if they exist
            if maze[row][col][0]:  # Top wall
                glBegin(GL_LINES)
                glVertex2f(x, y)
                glVertex2f(x + cell_size, y)
                glEnd()
            if maze[row][col][1]:  # Right wall
                glBegin(GL_LINES)
                glVertex2f(x + cell_size, y)
                glVertex2f(x + cell_size, y - cell_size)
                glEnd()
            if maze[row][col][2]:  # Bottom wall
                glBegin(GL_LINES)
                glVertex2f(x, y - cell_size)
                glVertex2f(x + cell_size, y - cell_size)
                glEnd()
            if maze[row][col][3]:  # Left wall
                glBegin(GL_LINES)
                glVertex2f(x, y)
                glVertex2f(x, y - cell_size)
                glEnd()


def draw_player():
    #Draw the player as a red square
    glColor3f(1.0, 0.0, 0.0)  # Red player
    glBegin(GL_QUADS)
    glVertex2f(player_x - player_size, player_y + player_size)
    glVertex2f(player_x + player_size, player_y + player_size)
    glVertex2f(player_x + player_size, player_y - player_size)
    glVertex2f(player_x - player_size, player_y - player_size)
    glEnd()


def check_collision(new_x, new_y):
    #Check if the player's new position collides with maze walls
    rows, cols = len(maze), len(maze[0])
    cell_size = 2.0 / max(rows, cols)
    
    # Calculate Player's current cell
    row = int((1 - new_y) // cell_size)
    col = int((new_x + 1) // cell_size)

    if row < 0 or row >= rows or col < 0 or col >= cols:
        return player_x, player_y

    # Check for walls
    if new_x < player_x and not maze[row][col+1][3]:  # Left
        while col >= 0 and not maze[row][col][1]:
            col -= 1
        return displacement -1 + (col + 1) * cell_size, player_y

    if new_x > player_x and not maze[row][col-1][1]:  # Right
        while col < cols and not maze[row][col][3]:
            col += 1
        return -displacement -1 + col * cell_size, player_y

    if new_y > player_y and not maze[row+1][col][0]:  # Up
        while row >= 0 and not maze[row][col][2]:
            row -= 1
        return player_x, - displacement + 1 - (row + 1) * cell_size

    if new_y < player_y and not maze[row-1][col][2]:  # Down
        while row < rows and not maze[row][col][0]:
            row += 1
        return player_x, displacement + 1 - row * cell_size

    return player_x, player_y


def keyboard(key, x, y):
    #Keyboard callback for player movement
    global player_x, player_y
    step = 2.0 / max(len(maze), len(maze[0]))

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


def display():
    #OpenGL display callback function
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    draw_maze()

    draw_player()

    glutSwapBuffers()


def main():
    global maze
    rows, cols = 15, 15  # Maze dimensions
    maze = generate_maze(rows, cols)

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Maze Dasher")

    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == "__main__":
    main()
