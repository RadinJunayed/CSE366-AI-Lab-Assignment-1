import pygame
import heapq

class Agent(pygame.sprite.Sprite):
    def __init__(self, environment, grid_size):
        super().__init__()
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.grid_size = grid_size
        self.environment = environment
        self.position = [0, 0]
        self.rect.topleft = (0, 0)
        self.task_completed = 0
        self.completed_tasks = []
        self.path = []
        self.moving = False
        self.explored_nodes = set()
        self.nodes_expanded = 0

    def move(self):
        if self.path:
            next_position = self.path.pop(0)
            self.position = list(next_position)
            self.rect.topleft = (self.position[0] * self.grid_size, self.position[1] * self.grid_size)
            self.check_task_completion()
        else:
            self.moving = False

    def check_task_completion(self):
        position_tuple = tuple(self.position)
        if position_tuple in self.environment.task_locations:
            task_number = self.environment.task_locations.pop(position_tuple)
            self.task_completed += 1
            self.completed_tasks.append(task_number)

    def find_nearest_task(self):
        nearest_task = None
        shortest_path = None
        self.nodes_expanded = 0
        self.explored_nodes = set()
        
        for task_position in self.environment.task_locations.keys():
            path = self.find_path_to(task_position)
            if path:
                if not shortest_path or len(path) < len(shortest_path):
                    shortest_path = path
                    nearest_task = task_position
        
        if shortest_path:
            self.path = shortest_path[1:]
            self.moving = True

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path_to(self, target):
        start = tuple(self.position)
        goal = target
        
        open_set = []
        heapq.heappush(open_set, (self.heuristic(start, goal), 0, start))
        
        came_from = {}
        
        g_score = {start: 0}
        
        f_score = {start: self.heuristic(start, goal)}
        
        counter = 1
        
        local_explored = set()
        
        while open_set:
            _, _, current = heapq.heappop(open_set)
            self.nodes_expanded += 1
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                self.explored_nodes = local_explored
                return path
            
            local_explored.add(current)
            
            for neighbor in self.get_neighbors(*current):
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score_neighbor = tentative_g_score + self.heuristic(neighbor, goal)
                    f_score[neighbor] = f_score_neighbor
                    
                    if not any(pos == neighbor for _, _, pos in open_set):
                        heapq.heappush(open_set, (f_score_neighbor, counter, neighbor))
                        counter += 1
        
        self.explored_nodes = local_explored
        return None

    def get_neighbors(self, x, y):
        neighbors = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny):
                neighbors.append((nx, ny))
        return neighbors