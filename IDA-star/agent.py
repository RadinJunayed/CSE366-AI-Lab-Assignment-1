import pygame
import copy

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
        self.nodes_expanded = 0
        self.explored_nodes = set()
        self.max_depth = 100

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
        
        bound = self.heuristic(start, goal)
        
        path = [start]
        
        local_explored = set([start])
        
        while bound < self.max_depth:
            temp_bound = float('inf')
            
            found, new_path, new_bound, explored = self._search(path, 0, bound, goal, local_explored)
            
            local_explored.update(explored)
            
            if found:
                self.explored_nodes = local_explored
                self.nodes_expanded = len(local_explored)
                return new_path
            
            if new_bound == float('inf'):
                self.explored_nodes = local_explored
                self.nodes_expanded = len(local_explored)
                return None
            
            bound = new_bound
        
        self.explored_nodes = local_explored
        self.nodes_expanded = len(local_explored)
        return None

    def _search(self, path, g, bound, goal, explored_set):
        current = path[-1]
        
        f = g + self.heuristic(current, goal)
        
        if f > bound:
            return False, None, f, explored_set
        
        if current == goal:
            return True, list(path), bound, explored_set
        
        min_bound = float('inf')
        local_explored = set(explored_set)
        
        for neighbor in self.get_neighbors(*current):
            if neighbor in path:
                continue
            
            local_explored.add(neighbor)
            path.append(neighbor)
            
            found, new_path, new_bound, updated_explored = self._search(
                path, g + 1, bound, goal, local_explored
            )
            
            local_explored.update(updated_explored)
            
            if found:
                return True, new_path, bound, local_explored
            
            if new_bound < min_bound:
                min_bound = new_bound
            
            path.pop()
        
        return False, None, min_bound, local_explored

    def get_neighbors(self, x, y):
        neighbors = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny):
                neighbors.append((nx, ny))
        return neighbors