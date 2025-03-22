import pygame
import sys
from agent import Agent
from environment import Environment

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRID_SIZE = 40
STATUS_WIDTH = 200
BACKGROUND_COLOR = (255, 255, 255)
BARRIER_COLOR = (0, 0, 0)
TASK_COLOR = (255, 0, 0)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)        
BUTTON_TEXT_COLOR = (255, 255, 255)
PATH_COLOR = (0, 150, 255, 128)
EXPLORED_COLOR = (200, 200, 255, 80)
MOVEMENT_DELAY = 200

def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH + STATUS_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame AI Grid Simulation - A* Algorithm")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    environment = Environment(WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, num_tasks=5, num_barriers=15)
    agent = Agent(environment, GRID_SIZE)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(agent)

    button_width, button_height = 160, 40
    button_margin = 10
    
    button_x = WINDOW_WIDTH + (STATUS_WIDTH - button_width) // 2
    
    start_y = WINDOW_HEIGHT - button_height - button_margin
    button_rect = pygame.Rect(button_x, start_y, button_width, button_height)
    
    restart_button_rect = pygame.Rect(button_x, start_y - button_height - button_margin, button_width, button_height)
    
    pause_button_rect = pygame.Rect(button_x, start_y - 2 * (button_height + button_margin), button_width, button_height)
    
    simulation_started = False
    paused = False
    step_count = 0
    current_target = None
    show_exploration = True
    
    task_costs = {}
    total_cost = 0
    cost_to_current_task = 0

    last_move_time = pygame.time.get_ticks()

    def reset_simulation():
        nonlocal environment, agent, all_sprites, simulation_started, paused, step_count, current_target
        nonlocal task_costs, total_cost, cost_to_current_task
        environment = Environment(WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, num_tasks=5, num_barriers=15)
        agent = Agent(environment, GRID_SIZE)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(agent)
        simulation_started = False
        paused = False
        step_count = 0
        current_target = None
        task_costs = {}
        total_cost = 0
        cost_to_current_task = 0

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not simulation_started and button_rect.collidepoint(event.pos):
                    simulation_started = True
                    if environment.task_locations:
                        agent.find_nearest_task()
                        if agent.path and environment.task_locations:
                            for task_pos in environment.task_locations:
                                if task_pos in agent.path:
                                    current_target = task_pos
                                    cost_to_current_task = len(agent.path)
                                    break
                elif restart_button_rect.collidepoint(event.pos):
                    reset_simulation()
                elif pause_button_rect.collidepoint(event.pos):
                    paused = not paused

        screen.fill(BACKGROUND_COLOR)

        for x in range(environment.columns):
            for y in range(environment.rows):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)

        if show_exploration and agent.explored_nodes:
            for pos in agent.explored_nodes:
                explored_rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                s.fill(EXPLORED_COLOR)
                screen.blit(s, explored_rect)

        if agent.moving and agent.path:
            for pos in agent.path:
                path_rect = pygame.Rect(pos[0] * GRID_SIZE + GRID_SIZE//4, 
                                       pos[1] * GRID_SIZE + GRID_SIZE//4, 
                                       GRID_SIZE//2, GRID_SIZE//2)
                pygame.draw.rect(screen, PATH_COLOR, path_rect, 0, border_radius=GRID_SIZE//4)

        for (bx, by) in environment.barrier_locations:
            barrier_rect = pygame.Rect(bx * GRID_SIZE, by * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BARRIER_COLOR, barrier_rect)

        for (tx, ty), task_number in environment.task_locations.items():
            task_rect = pygame.Rect(tx * GRID_SIZE, ty * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, TASK_COLOR, task_rect)
            task_num_surface = font.render(str(task_number), True, (255, 255, 255))
            task_num_rect = task_num_surface.get_rect(center=task_rect.center)
            screen.blit(task_num_surface, task_num_rect)

        all_sprites.draw(screen)

        status_x = WINDOW_WIDTH + 10
        algorithm_text = "Algorithm: A* Search"
        task_status_text = f"Tasks Completed: {agent.task_completed}"
        position_text = f"Position: {agent.position}"
        completed_tasks_text = f"Completed Tasks: {agent.completed_tasks}"
        steps_text = f"Steps Taken: {step_count}"
        current_cost_text = f"Current Path Cost: {cost_to_current_task}"
        total_cost_text = f"Total Path Cost: {total_cost}"
        target_text = f"Current Target: {'None' if current_target is None else environment.task_locations.get(current_target, 'None')}"
        
        task_cost_texts = []
        for task_num, cost in task_costs.items():
            task_cost_texts.append(f"Task {task_num} Cost: {cost}")
        
        algorithm_surface = font.render(algorithm_text, True, TEXT_COLOR)
        status_surface = font.render(task_status_text, True, TEXT_COLOR)
        position_surface = font.render(position_text, True, TEXT_COLOR)
        completed_tasks_surface = font.render(completed_tasks_text, True, TEXT_COLOR)
        steps_surface = font.render(steps_text, True, TEXT_COLOR)
        current_cost_surface = font.render(current_cost_text, True, TEXT_COLOR)
        total_cost_surface = font.render(total_cost_text, True, TEXT_COLOR)
        target_surface = font.render(target_text, True, TEXT_COLOR)

        screen.blit(algorithm_surface, (status_x, 20))
        screen.blit(status_surface, (status_x, 50))
        screen.blit(position_surface, (status_x, 80))
        screen.blit(completed_tasks_surface, (status_x, 110))
        screen.blit(steps_surface, (status_x, 140))
        screen.blit(current_cost_surface, (status_x, 170))
        screen.blit(total_cost_surface, (status_x, 200))
        screen.blit(target_surface, (status_x, 230))
        
        y_offset = 260
        for task_cost_text in task_cost_texts:
            task_cost_surface = font.render(task_cost_text, True, TEXT_COLOR)
            screen.blit(task_cost_surface, (status_x, y_offset))
            y_offset += 30

        if not simulation_started:
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                button_color = BUTTON_HOVER_COLOR
            else:
                button_color = BUTTON_COLOR
            pygame.draw.rect(screen, button_color, button_rect)
            button_text = font.render("Start", True, BUTTON_TEXT_COLOR)
            text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, text_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        restart_button_color = BUTTON_HOVER_COLOR if restart_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, restart_button_color, restart_button_rect)
        restart_text = font.render("Restart", True, BUTTON_TEXT_COLOR)
        restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
        screen.blit(restart_text, restart_text_rect)
        
        pause_button_color = BUTTON_HOVER_COLOR if pause_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, pause_button_color, pause_button_rect)
        pause_text = font.render("Resume" if paused else "Pause", True, BUTTON_TEXT_COLOR)
        pause_text_rect = pause_text.get_rect(center=pause_button_rect.center)
        screen.blit(pause_text, pause_text_rect)

        if simulation_started and not paused:
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time > MOVEMENT_DELAY:
                if not agent.moving and environment.task_locations:
                    agent.find_nearest_task()
                    if agent.path and environment.task_locations:
                        for task_pos in environment.task_locations:
                            if task_pos in agent.path:
                                current_target = task_pos
                                cost_to_current_task = len(agent.path)
                                break
                elif agent.moving:
                    if agent.path and len(agent.path) == 1:
                        next_pos = agent.path[0]
                        if next_pos in environment.task_locations:
                            task_num = environment.task_locations[next_pos]
                            task_costs[task_num] = cost_to_current_task
                            total_cost += cost_to_current_task
                    
                    agent.move()
                    step_count += 1
                    
                    if current_target not in environment.task_locations:
                        current_target = None
                        cost_to_current_task = 0
                
                last_move_time = current_time

        pygame.draw.line(screen, (0, 0, 0), (WINDOW_WIDTH, 0), (WINDOW_WIDTH, WINDOW_HEIGHT))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()