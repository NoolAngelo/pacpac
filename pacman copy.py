import pygame
import heapq

# Define constants for colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)

# This class represents the bar at the bottom that the player controls
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self, x, y, width, height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

# This creates all the walls in room 1
def setupRoomOne(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list = pygame.sprite.RenderPlain()

    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = [
        [0, 0, 6, 600],
        [0, 0, 600, 6],
        [0, 600, 606, 6],
        [600, 0, 6, 606],
        # Add more walls here...
    ]

    # Loop through the list. Create the wall, add it to the list
    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], blue)
        wall_list.add(wall)
        all_sprites_list.add(wall)

    # return our new list
    return wall_list

# This class represents the player character
class Player(pygame.sprite.Sprite):
    # Set speed vector
    change_x = 0
    change_y = 0

    # Constructor function
    def __init__(self, x, y, filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Set height, width
        self.image = pygame.image.load(filename).convert()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

    # Change the speed of the player
    def changespeed(self, x, y):
        self.change_x = x
        self.change_y = y

    # A* pathfinding algorithm
    def find_path(self, start, goal, walls):
        open_list = []
        closed_set = set()
        came_from = {}

        heapq.heappush(open_list, (0, start))
        g_score = {start: 0}

        while open_list:
            current = heapq.heappop(open_list)[1]

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path

            closed_set.add(current)

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)

                if neighbor in walls:
                    continue

                if not (0 <= neighbor[0] < 600 and 0 <= neighbor[1] < 600):
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbor in closed_set and tentative_g_score >= g_score.get(neighbor, 0):
                    continue

                if tentative_g_score < g_score.get(neighbor, 0) or neighbor not in [i[1] for i in open_list]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    heapq.heappush(open_list, (tentative_g_score + self.heuristic(neighbor, goal), neighbor))

        return None

    # Heuristic function for A*
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Find a new position for the player
    def update(self, walls):
        if self.change_x != 0 or self.change_y != 0:
            start = (self.rect.left // 30, self.rect.top // 30)
            goal = ((self.rect.left + self.change_x) // 30, (self.rect.top + self.change_y) // 30)
            path = self.find_path(start, goal, walls)
            if path:
                next_step = path[-1]
                self.rect.left = next_step[0] * 30
                self.rect.top = next_step[1] * 30

def startGame():
    # Call this function so the Pygame library can initialize itself
    pygame.init()
    
    # Create an 606x606 sized screen
    screen = pygame.display.set_mode([606, 606])

    # Set the title of the window
    pygame.display.set_caption('Pacman')

    # Create a surface we can draw on
    background = pygame.Surface(screen.get_size())

    # Used for converting color maps and such
    background = background.convert()
    
    # Fill the screen with a black background
    background.fill(black)

    clock = pygame.time.Clock()

    pygame.font.init()
    font = pygame.font.Font("freesansbold.ttf", 24)

    all_sprites_list = pygame.sprite.RenderPlain()
    wall_list = setupRoomOne(all_sprites_list)

    # Create the player paddle object
    Pacman = Player(303-16, (7*60)+19, "images/nath.png" )
    all_sprites_list.add(Pacman)

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Pacman.changespeed(-30, 0)
                elif event.key == pygame.K_RIGHT:
                    Pacman.changespeed(30, 0)
                elif event.key == pygame.K_UP:
                    Pacman.changespeed(0, -30)
                elif event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, 30)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    Pacman.changespeed(0, 0)
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    Pacman.changespeed(0, 0)

        Pacman.update(wall_list)

        screen.fill(black)
        wall_list.draw(screen)
        all_sprites_list.draw(screen)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

