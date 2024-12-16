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

maze = []  # To store the generated maze
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def generate_maze(rows, cols):
    # Initialize the maze with walls (True for wall, False for open space)
    maze = [[[True, True, True, True] for _ in range(cols)] for _ in range(rows)]

    # Create a visited array to track the visited cells
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    def is_valid(x, y):
        """Check if the cell (x, y) is within the bounds of the maze."""
        return 0 <= x < rows and 0 <= y < cols

    def dfs(x, y):
        """Depth-First Search to generate the maze."""
        # Mark the current cell as visited
        visited[x][y] = True

        # Randomize the directions to ensure randomness in maze generation
        directions = random.sample(DIRECTIONS, len(DIRECTIONS))
        
        # Try each direction
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny) and not visited[nx][ny]:
                # Remove wall between current cell and the neighbor
                if dx == -1:  # Move up
                    maze[x][y][0] = False  # Remove top wall of current cell
                    maze[nx][ny][2] = False  # Remove bottom wall of the neighbor
                elif dx == 1:  # Move down
                    maze[x][y][2] = False  # Remove bottom wall of current cell
                    maze[nx][ny][0] = False  # Remove top wall of the neighbor
                elif dy == -1:  # Move left
                    maze[x][y][3] = False  # Remove left wall of current cell
                    maze[nx][ny][1] = False  # Remove right wall of the neighbor
                elif dy == 1:  # Move right
                    maze[x][y][1] = False  # Remove right wall of current cell
                    maze[nx][ny][3] = False  # Remove left wall of the neighbor
                
                # Recursively visit the neighbor
                dfs(nx, ny)

    # Start the DFS from a random position
    start_x, start_y = random.randint(0, rows - 1), random.randint(0, cols - 1)
    dfs(start_x, start_y)
    # MAZE REMEMBER
    # for cols in range(len(maze)):
    #     with open('maze_shape.txt', 'a') as file:
    #         file.write(str(maze[cols])+"\n")
    return maze

def draw_maze():
    """Draw the maze using OpenGL line segments."""
    rows = len(maze)
    cols = len(maze[0])
    cell_size = 2.0 / max(rows, cols)  # Normalize to OpenGL coordinates

    glColor3f(1.0, 1.0, 1.0)  # White walls

    for row in range(rows):
        for col in range(cols):
            x = -1 + col * cell_size
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
    """Draw the player as a red square."""
    glColor3f(1.0, 0.0, 0.0)  # Red player
    glBegin(GL_QUADS)
    glVertex2f(player_x - player_size, player_y + player_size)
    glVertex2f(player_x + player_size, player_y + player_size)
    glVertex2f(player_x + player_size, player_y - player_size)
    glVertex2f(player_x - player_size, player_y - player_size)
    glEnd()

def check_collision(new_x, new_y):
    """Check if the player's new position collides with maze walls."""
    rows, cols = len(maze), len(maze[0])
    cell_size = 2.0 / max(rows, cols)  # Size of each cell in OpenGL coordinates

    # Calculate the player's current and target maze cells
    col = int((new_x + 1) // cell_size)
    row = int((-new_y + 1) // cell_size)

    if row < 0 or row >= rows or col < 0 or col >= cols:
        return True  # Out of bounds

    # Check against the walls of the current cell and adjacent cells
    cell = maze[row][col]
    
    # Check if player is trying to move upwards (colliding with top wall)
    if new_y + player_size > 1 - row * cell_size and cell[0]:  # Top wall
        return True
    
    # Check if player is trying to move right (colliding with right wall)
    if new_x + player_size > -1 + (col + 1) * cell_size and cell[1]:  # Right wall
        return True
    
    # Check if player is trying to move downwards (colliding with bottom wall)
    if new_y - player_size < 1 - (row + 1) * cell_size and cell[2]:  # Bottom wall
        return True
    
    # Check if player is trying to move left (colliding with left wall)
    if new_x - player_size < -1 + col * cell_size and cell[3]:  # Left wall
        return True

    return False


def keyboard(key, x, y):
    """Keyboard callback for player movement."""
    global player_x, player_y

    step = 0.13333333333  # Movement step size

    # Calculate new position based on key press
    if key == b'w':  # Up
        new_x, new_y = player_x, player_y + step
    elif key == b's':  # Down
        new_x, new_y = player_x, player_y - step
    elif key == b'a':  # Left
        new_x, new_y = player_x - step, player_y
    elif key == b'd':  # Right
        new_x, new_y = player_x + step, player_y
    else:
        return

    # Check for collisions with maze walls
    if not check_collision(new_x, new_y):
        player_x, player_y = new_x, new_y

    glutPostRedisplay()

def display():
    """OpenGL display callback function."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Draw the maze
    draw_maze()

    # Draw the player
    draw_player()

    glutSwapBuffers()

def main():
    global maze
    rows, cols = 15, 15  # Maze dimensions changed to 10x10
    maze = generate_maze(rows, cols)

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"OpenGL Random Maze")

    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)  # Orthographic projection

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)  # Register keyboard callback
    glutMainLoop()

if __name__ == "__main__":
    main()
