import sys

if sys.version_info >= (3, 14):
    raise RuntimeError(
        "This project currently requires Python 3.13 or earlier because pygame font "
        "modules are not working on Python {}.{}. "
        "Recreate the virtual environment with Python 3.13, e.g.:\n"
        "  rm -rf .venv\n"
        "  PYTHON_BIN=python3.13 ./setup.sh".format(
            sys.version_info.major, sys.version_info.minor
        )
    )

import pygame
from path_finding import PathFinding
from ASTAR import AStar as ASTARPathFinder
from DFS import DFS as DFSPathFinder
from BRFS import BrFS as BRFSPathFinder
from DUMMY import Dummy as DummyPathFinder
import heuristics
from world import World
import subprocess

BASE_WIDTH = 1000
BASE_LEFT_PANEL_WIDTH = 220
MIN_UI_SCALE = 0.6

pygame.init()
display_info = pygame.display.Info()
available_w = max(1, display_info.current_w - 80)
available_h = max(1, display_info.current_h - 80)
UI_SCALE = min(1.0, max(MIN_UI_SCALE, min(available_w / BASE_WIDTH, available_h / BASE_WIDTH)))

def scaled(value, minimum=1):
    return max(minimum, int(round(value * UI_SCALE)))

WIDTH = scaled(BASE_WIDTH)
LEFT_PANEL_WIDTH = scaled(BASE_LEFT_PANEL_WIDTH)
GRID_OFFSET_X = LEFT_PANEL_WIDTH
MIN_ROWS = 10
MAX_ROWS = 120
MIN_ANIMATION_SPEED = 1
MAX_ANIMATION_SPEED = 10
DEFAULT_ANIMATION_SPEED = 5
MAX_ANIMATION_POWER = 200
BUTTON_HOLD_REPEAT_MS = 90
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Search Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

current_plan_cost = None
current_expansions = 0
current_search_time = None

class Spot:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(
            win,
            self.color,
            (self.x + GRID_OFFSET_X, self.y, self.width, self.width),
        )

    def __str__(self):
        return "({},{})".format(self.row, self.col)

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap)
            grid[i].append(spot)
    return grid

def make_grid_from_file(filename, width):
    f = open(filename)

    data = json.load(f)

    rows = data['rows']
    grid = []
    gap = width // rows
    
    start = (data['start'][0],data['start'][1])
    end = (data['end'][0],data['end'][1])
    
    barrier = {(ele[0],ele[1]) for ele in data['barrier']}
    
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap)
            if (i,j) in barrier:
                spot.make_barrier()
            elif (i,j) == start:
                spot.make_start()
                start = spot
            elif (i,j) == end:
                spot.make_end()
                end = spot
            grid[i].append(spot)

    return grid, start, end, rows, barrier


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(
            win, GREY, (GRID_OFFSET_X, i * gap), (GRID_OFFSET_X + width, i * gap), 2
        )
        for j in range(rows):
            pygame.draw.line(
                win, GREY, (GRID_OFFSET_X + j * gap, 0), (GRID_OFFSET_X + j * gap, width), 2
            )
    pygame.draw.rect(win, BLACK, (GRID_OFFSET_X, 0, width, width), 3)


def draw_left_panel(win):
    pygame.draw.rect(win, (30, 30, 30), (0, 0, LEFT_PANEL_WIDTH, WIDTH))
    title_font = pygame.font.SysFont("Arial", scaled(24), bold=True)
    text_font = pygame.font.SysFont("Arial", scaled(18))
    lines = [
        ("Comandi", title_font),
        ("Sinistro: start/goal/muri", text_font),
        ("Destro: cancella cella", text_font),
        ("SPACE: avvia ricerca", text_font),
        ("C: reset mappa", text_font),
        ("V: sim on/off", text_font),
        ("Stop Anim: ferma simulazione", text_font),
        ("+/-: velocita sim (1-10)", text_font),
        ("[/] o frecce su/giu: righe", text_font),
        ("Rows +/- solo mappa pulita", text_font),
        ("Sotto: scegli algoritmo", text_font),
    ]

    y = scaled(24)
    for text, font in lines:
        if text:
            surface = font.render(text, True, WHITE)
            win.blit(surface, (scaled(16), y))
        y += scaled(26) if font is title_font else scaled(20)


def refresh_rows_controls(rows, enabled):
    value_bg = "dimgray" if enabled else "gray30"
    step_bg = "darkslateblue" if enabled else "gray30"
    rows_value_button.change_text("Rows: {}".format(rows), bg=value_bg)
    rows_minus_button.change_text("-", bg=step_bg)
    rows_plus_button.change_text("+", bg=step_bg)


def refresh_simulation_control(enabled):
    if enabled:
        simulation_button.change_text("Sim Search: ON", bg="darkgreen")
    else:
        simulation_button.change_text("Sim Search: OFF", bg="gray30")


def refresh_speed_controls(speed):
    speed_bg = "teal"
    speed_minus_button.change_text("-", bg=speed_bg)
    speed_plus_button.change_text("+", bg=speed_bg)
    speed_value_button.change_text("Speed: {}".format(speed), bg="dimgray")


def refresh_algorithm_dropdown(selected_name, expanded):
    arrow = "^" if expanded else "v"
    algorithm_dropdown_button.change_text("Algo: {} {}".format(selected_name, arrow), bg="navy")
    for key, button in algorithm_option_buttons.items():
        if key == selected_name:
            button.change_text(key, bg="darkgreen")
        else:
            button.change_text(key, bg="gray25")


def draw(
    win,
    grid,
    rows,
    width,
    rows_editable=True,
    simulation_mode=False,
    animation_speed=DEFAULT_ANIMATION_SPEED,
    selected_algorithm="ASTAR",
    algorithm_menu_open=False,
):
    win.fill(WHITE)
    draw_left_panel(win)
    refresh_rows_controls(rows, rows_editable)
    refresh_simulation_control(simulation_mode)
    refresh_speed_controls(animation_speed)
    refresh_algorithm_dropdown(selected_algorithm, algorithm_menu_open)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    
    save_map_button.show()
    load_map_button.show()
    clear_search_button.show()
    simulation_button.show()
    stop_animation_button.show()
    speed_minus_button.show()
    speed_value_button.show()
    speed_plus_button.show()
    rows_minus_button.show()
    rows_value_button.show()
    rows_plus_button.show()
    algorithm_dropdown_button.show()
    if algorithm_menu_open:
        for button in algorithm_option_buttons.values():
            button.show()

    draw_search_stats(win, width)
    pygame.display.update()


def draw_search_stats(win, width):
    panel_w = scaled(250)
    panel_h = scaled(98)
    x = WIDTH - panel_w - scaled(12)
    y = WIDTH - panel_h - scaled(12)
    pygame.draw.rect(win, (25, 25, 25), (x, y, panel_w, panel_h))
    pygame.draw.rect(win, WHITE, (x, y, panel_w, panel_h), 2)
    font = pygame.font.SysFont("Arial", scaled(18))
    cost_value = "-" if current_plan_cost is None else str(current_plan_cost)
    time_value = "-" if current_search_time is None else "{:.4f} s".format(current_search_time)
    line1 = font.render("Costo piano: {}".format(cost_value), True, WHITE)
    line2 = font.render("Espansioni: {}".format(current_expansions), True, WHITE)
    line3 = font.render("Tempo: {}".format(time_value), True, WHITE)
    win.blit(line1, (x + scaled(10), y + scaled(12)))
    win.blit(line2, (x + scaled(10), y + scaled(40)))
    win.blit(line3, (x + scaled(10), y + scaled(68)))


def _wrap_text(text, max_chars=46):
    words = str(text).split()
    if not words:
        return [""]
    lines = []
    current = words[0]
    for word in words[1:]:
        if len(current) + 1 + len(word) <= max_chars:
            current += " " + word
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def show_alert(win, title, message):
    overlay = pygame.Surface((WIDTH, WIDTH), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    box_w = scaled(620)
    box_h = scaled(260)
    box_rect = pygame.Rect((WIDTH - box_w) // 2, (WIDTH - box_h) // 2, box_w, box_h)
    alert_clock = pygame.time.Clock()
    title_font = pygame.font.SysFont("Arial", scaled(28), bold=True)
    text_font = pygame.font.SysFont("Arial", scaled(20))
    hint_font = pygame.font.SysFont("Arial", scaled(16))

    message_lines = []
    for paragraph in str(message).split("\n"):
        message_lines.extend(_wrap_text(paragraph, max_chars=52))
    if not message_lines:
        message_lines = ["Unknown error."]

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_SPACE):
                waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                waiting = False

        win.blit(overlay, (0, 0))
        pygame.draw.rect(win, (245, 245, 245), box_rect, border_radius=10)
        pygame.draw.rect(win, (180, 30, 30), box_rect, 3, border_radius=10)

        title_surface = title_font.render(title, True, (130, 0, 0))
        win.blit(title_surface, (box_rect.x + scaled(24), box_rect.y + scaled(20)))

        y = box_rect.y + scaled(72)
        for line in message_lines[:6]:
            txt = text_font.render(line, True, (20, 20, 20))
            win.blit(txt, (box_rect.x + scaled(24), y))
            y += scaled(30)

        hint = hint_font.render("Press ENTER/ESC/SPACE or click to continue", True, (70, 70, 70))
        win.blit(hint, (box_rect.x + scaled(24), box_rect.bottom - scaled(34)))
        pygame.display.update()
        alert_clock.tick(60)

    return True


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos

    row = (x - GRID_OFFSET_X) // gap
    col = y // gap

    return row, col


def is_valid_cell(row, col, rows):
    return 0 <= row < rows and 0 <= col < rows

def mark_spots(start, end, grid, plan):
    
    x = start.row
    y = start.col
    for a in plan:
        if a == 'N':
            y+=1
        elif a == 'S':
            y-=1
        elif a == 'E':
            x+=1
        elif a == 'W':
            x-=1
        spot = grid[x][y]
        if spot != start and spot != end:
            spot.make_path()         

def mark_expanded(exp, grid, start=None, end=None):
    for e in exp:
        spot = grid[e[0]][e[1]]
        if spot != start and spot != end:
            spot.make_closed()


def _handle_animation_control_event(event, animation_speed):
    if event.type == pygame.QUIT:
        return animation_speed, False, False
    if stop_animation_button.clicked(event):
        return animation_speed, True, True
    if speed_minus_button.clicked(event):
        animation_speed = max(MIN_ANIMATION_SPEED, animation_speed - 1)
    if speed_plus_button.clicked(event):
        animation_speed = min(MAX_ANIMATION_SPEED, animation_speed + 1)
    if event.type == pygame.KEYDOWN:
        if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
            animation_speed = max(MIN_ANIMATION_SPEED, animation_speed - 1)
        if event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
            animation_speed = min(MAX_ANIMATION_SPEED, animation_speed + 1)
    return animation_speed, True, False


def _compute_animation_delays(animation_speed):
    # Delay per frame (not per single cell).
    effective_speed = _effective_animation_speed(animation_speed)
    normalized = (effective_speed - MIN_ANIMATION_SPEED) / float(MAX_ANIMATION_POWER - MIN_ANIMATION_SPEED)
    expansion_delay_ms = int(130 - (130 * normalized))
    path_delay_ms = int(180 - (180 * normalized))
    return max(0, expansion_delay_ms), max(0, path_delay_ms)


def _steps_per_frame(animation_speed):
    effective_speed = _effective_animation_speed(animation_speed)
    normalized = (effective_speed - MIN_ANIMATION_SPEED) / float(MAX_ANIMATION_POWER - MIN_ANIMATION_SPEED)
    return 1 + int(39 * normalized)


def _effective_animation_speed(animation_speed):
    if MAX_ANIMATION_SPEED == MIN_ANIMATION_SPEED:
        return MIN_ANIMATION_SPEED
    ratio = (animation_speed - MIN_ANIMATION_SPEED) / float(MAX_ANIMATION_SPEED - MIN_ANIMATION_SPEED)
    return MIN_ANIMATION_SPEED + ratio * (MAX_ANIMATION_POWER - MIN_ANIMATION_SPEED)


def _wait_with_live_controls(
    win,
    grid,
    rows,
    width,
    rows_editable,
    simulation_mode,
    animation_speed,
    base_delay_ms,
    selected_algorithm,
):
    elapsed = 0
    wait_clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            animation_speed, keep_running, stop_requested = _handle_animation_control_event(event, animation_speed)
            if not keep_running:
                return animation_speed, False, False
            if stop_requested:
                return animation_speed, True, True
        if elapsed >= base_delay_ms:
            return animation_speed, True, False
        draw(
            win,
            grid,
            rows,
            width,
            rows_editable,
            simulation_mode,
            animation_speed,
            selected_algorithm,
            False,
        )
        elapsed += wait_clock.tick(240)


def animate_search(
    win,
    grid,
    rows,
    width,
    start,
    end,
    expanded_sequence,
    plan,
    rows_editable,
    simulation_mode,
    animation_speed,
    selected_algorithm,
):
    # Expansion animation (batched for high-speed mode).
    exp_idx = 0
    while exp_idx < len(expanded_sequence):
        for event in pygame.event.get():
            animation_speed, keep_running, stop_requested = _handle_animation_control_event(event, animation_speed)
            if not keep_running:
                return animation_speed, False, False
            if stop_requested:
                return animation_speed, True, True

        expansion_delay_ms, _ = _compute_animation_delays(animation_speed)
        batch = _steps_per_frame(animation_speed)
        for _ in range(batch):
            if exp_idx >= len(expanded_sequence):
                break
            e = expanded_sequence[exp_idx]
            spot = grid[e[0]][e[1]]
            if spot != start and spot != end:
                spot.make_closed()
            exp_idx += 1

        draw(
            win,
            grid,
            rows,
            width,
            rows_editable,
            simulation_mode,
            animation_speed,
            selected_algorithm,
            False,
        )
        if expansion_delay_ms > 0:
            animation_speed, keep_running, stop_requested = _wait_with_live_controls(
                win,
                grid,
                rows,
                width,
                rows_editable,
                simulation_mode,
                animation_speed,
                expansion_delay_ms,
                selected_algorithm,
            )
            if not keep_running:
                return animation_speed, False, False
            if stop_requested:
                return animation_speed, True, True

    # Path animation (batched for high-speed mode).
    if plan is not None:
        x = start.row
        y = start.col
        plan_idx = 0
        while plan_idx < len(plan):
            for event in pygame.event.get():
                animation_speed, keep_running, stop_requested = _handle_animation_control_event(event, animation_speed)
                if not keep_running:
                    return animation_speed, False, False
                if stop_requested:
                    return animation_speed, True, True

            _, path_delay_ms = _compute_animation_delays(animation_speed)
            batch = _steps_per_frame(animation_speed)
            for _ in range(batch):
                if plan_idx >= len(plan):
                    break
                action = plan[plan_idx]
                if action == "N":
                    y += 1
                elif action == "S":
                    y -= 1
                elif action == "E":
                    x += 1
                elif action == "W":
                    x -= 1
                spot = grid[x][y]
                if spot != start and spot != end:
                    spot.make_path()
                plan_idx += 1

            draw(
                win,
                grid,
                rows,
                width,
                rows_editable,
                simulation_mode,
                animation_speed,
                selected_algorithm,
                False,
            )
            if path_delay_ms > 0:
                animation_speed, keep_running, stop_requested = _wait_with_live_controls(
                    win,
                    grid,
                    rows,
                    width,
                    rows_editable,
                    simulation_mode,
                    animation_speed,
                    path_delay_ms,
                    selected_algorithm,
                )
                if not keep_running:
                    return animation_speed, False, False
                if stop_requested:
                    return animation_speed, True, True

    return animation_speed, True, False


def clear_search_visuals(grid, start=None, end=None):
    for row in grid:
        for spot in row:
            if spot.is_closed() or spot.color == PURPLE or spot.is_open():
                spot.reset()
    if start is not None:
        start.make_start()
    if end is not None:
        end.make_end()
import json
def save_to_file(grid, start, end, filename="temp.json"):
    barrier = list()
    for x in grid:
        for spot in x:
            if spot.is_barrier():
                barrier.append((spot.row,spot.col))
    res = {"rows":len(grid), "start": (start.row,start.col), "end": (end.row,end.col), "barrier":barrier}
    data = json.dumps(res,indent=4)
    with open(filename,"w") as data_file:
        data_file.write(data)

def load_from_file(filename, width):
    return make_grid_from_file(filename, width)


def ask_map_file():
    apple_script = 'POSIX path of (choose file with prompt "Select map JSON file")'
    try:
        result = subprocess.run(
            ["osascript", "-e", apple_script],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    path = result.stdout.strip()
    return path if path else None

class Button:
    """Create a button, then blit the surface in the while loop"""
 
    def __init__(self, text,  pos, font, bg="black", feedback=""):
        self.x, self.y = scaled(pos[0]), scaled(pos[1])
        self.font = pygame.font.SysFont("Arial", scaled(font, minimum=8))
        self.default_text = text
        self.default_bg = bg
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)
 
    def change_text(self, text, bg="black"):
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
 
    def show(self):
        WIN.blit(self.surface, (self.x, self.y))
 
    def click(self, event, grid, start, end):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    if grid is not None and start is not None and end is not None:
                        save_to_file(grid, start, end, "tempmap.json")
                        self.change_text(self.feedback, bg="red")  

    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

save_map_button = Button(
    "Save Map",
    (16, 360),
    font=20,
    bg="navy",
    feedback="Saved")

load_map_button = Button(
    "Load Map",
    (16, 420),
    font=20,
    bg="navy",
    feedback="Loaded")

clear_search_button = Button(
    "Clear Search",
    (16, 470),
    font=20,
    bg="maroon",
    feedback="Cleared")

simulation_button = Button(
    "Sim Search: OFF",
    (16, 520),
    font=18,
    bg="gray30")

stop_animation_button = Button(
    "Stop Anim",
    (16, 570),
    font=18,
    bg="firebrick4")

speed_minus_button = Button(
    "-",
    (16, 620),
    font=24,
    bg="teal")

speed_value_button = Button(
    "Speed: {}".format(DEFAULT_ANIMATION_SPEED),
    (66, 622),
    font=18,
    bg="dimgray")

speed_plus_button = Button(
    "+",
    (176, 620),
    font=24,
    bg="teal")

rows_minus_button = Button(
    "-",
    (16, 670),
    font=24,
    bg="darkslateblue")

rows_value_button = Button(
    "Rows: 50",
    (66, 672),
    font=18,
    bg="dimgray")

rows_plus_button = Button(
    "+",
    (176, 670),
    font=24,
    bg="darkslateblue")

ALGORITHM_NAMES = ["ASTAR", "ASTARW4", "DFS", "BRFS", "DUMMY"]
algorithm_dropdown_button = Button("Algo: ASTAR v", (16, 760), font=18, bg="navy")
algorithm_option_buttons = {
    name: Button(name, (16, 805 + (i * 40)), font=18, bg="gray25")
    for i, name in enumerate(ALGORITHM_NAMES)
}

clock = pygame.time.Clock()
import click
import time


def build_search_algorithm(name):
    if name == 'DFS':
        return DFSPathFinder(True)
    if name == 'BRFS':
        return BRFSPathFinder(True)
    if name == 'ASTARW4':
        return ASTARPathFinder(heuristics.manhattan, True, w=4)
    if name == 'DUMMY':
        return DummyPathFinder(True)
    return ASTARPathFinder(heuristics.manhattan, True)


@click.command()
@click.option('-w', '--width', default = WIDTH-LEFT_PANEL_WIDTH, help = "Grid width")
@click.option('-r', '--rows', default = 50, help = "Number of rows/columns in the map")
@click.option('-s', '--search_algorithm', default = "ASTAR", help = "Search algorithm to be used")
@click.option('-f', '--filename', default = None, help = "Initialize map with data from file")
def main(width, rows, search_algorithm, filename = None):
    global current_plan_cost, current_expansions, current_search_time
    win = WIN
    start = None
    end = None
    ROWS = rows
    width = min(width, WIDTH - LEFT_PANEL_WIDTH)
    current_map_file = filename if filename is not None else "tempmap.json"
    selected_algorithm = search_algorithm if search_algorithm in ALGORITHM_NAMES else "ASTAR"
    algorithm_menu_open = False
    simulation_mode = True
    animation_speed = DEFAULT_ANIMATION_SPEED
    last_speed_repeat_ms = 0
    last_rows_repeat_ms = 0
    search_solver = build_search_algorithm(selected_algorithm)
    if filename is not None:
        grid, start, end, rows, wall = make_grid_from_file(filename,width)
        ROWS = rows
    else:
        grid = make_grid(rows, width)
        wall = set()

    def apply_rows_delta(delta, editable):
        nonlocal rows, ROWS, grid, wall, start, end
        if not editable:
            print("Rows modificabili solo con mappa pulita (no start/goal/muri).")
            return
        new_rows = max(MIN_ROWS, min(MAX_ROWS, rows + delta))
        if new_rows == rows:
            return
        rows = new_rows
        ROWS = rows
        grid = make_grid(rows, width)
        wall = set()
        start = None
        end = None
        search_solver.reset_expanded()

    run = True
    
    while run:
        rows_editable = (start is None and end is None and len(wall) == 0)
        draw(
            win,
            grid,
            rows,
            width,
            rows_editable,
            simulation_mode,
            animation_speed,
            selected_algorithm,
            algorithm_menu_open,
        )
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            save_map_button.click(event, grid, start, end)
            if load_map_button.clicked(event):
                start = None
                end = None
                rows = ROWS
                grid = make_grid(rows, width)
                wall = set()
                search_solver.reset_expanded()
                current_plan_cost = None
                current_expansions = 0
                current_search_time = None
                selected_file = ask_map_file()
                if selected_file is not None:
                    try:
                        grid, start, end, rows, wall = load_from_file(selected_file, width)
                        ROWS = rows
                        current_map_file = selected_file
                        load_map_button.change_text(
                            load_map_button.default_text, bg=load_map_button.default_bg
                        )
                    except FileNotFoundError:
                        print("Map file not found: {}".format(selected_file))
                    except (KeyError, ValueError, TypeError, json.JSONDecodeError):
                        print("Invalid map file format: {}".format(selected_file))
            if clear_search_button.clicked(event):
                clear_search_visuals(grid, start, end)
                search_solver.reset_expanded()
                current_plan_cost = None
                current_expansions = 0
                current_search_time = None
            if simulation_button.clicked(event):
                simulation_mode = not simulation_mode
            if speed_minus_button.clicked(event):
                animation_speed = max(MIN_ANIMATION_SPEED, animation_speed - 1)
                last_speed_repeat_ms = pygame.time.get_ticks()
            if speed_plus_button.clicked(event):
                animation_speed = min(MAX_ANIMATION_SPEED, animation_speed + 1)
                last_speed_repeat_ms = pygame.time.get_ticks()
            if algorithm_dropdown_button.clicked(event):
                algorithm_menu_open = not algorithm_menu_open
            elif algorithm_menu_open:
                changed_algorithm = False
                for key, button in algorithm_option_buttons.items():
                    if button.clicked(event):
                        selected_algorithm = key
                        search_solver = build_search_algorithm(selected_algorithm)
                        algorithm_menu_open = False
                        changed_algorithm = True
                        break
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not changed_algorithm:
                    if not algorithm_dropdown_button.rect.collidepoint(event.pos):
                        algorithm_menu_open = False
            if rows_minus_button.clicked(event):
                apply_rows_delta(-1, rows_editable)
                last_rows_repeat_ms = pygame.time.get_ticks()
            if rows_plus_button.clicked(event):
                apply_rows_delta(1, rows_editable)
                last_rows_repeat_ms = pygame.time.get_ticks()
            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                grid_pixel_size = (width // rows) * rows
                if GRID_OFFSET_X <= pos[0] < GRID_OFFSET_X + grid_pixel_size and 0 <= pos[1] < grid_pixel_size:
                    row, col = get_clicked_pos(pos, rows, width)
                    if not is_valid_cell(row, col, rows):
                        continue
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()
                        
                    elif not end and spot != start:
                        end = spot
                        end.make_end()

                    elif spot != end and spot != start:
                        spot.make_barrier()
                        wall.add((row,col))

            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                grid_pixel_size = (width // rows) * rows
                if GRID_OFFSET_X <= pos[0] < GRID_OFFSET_X + grid_pixel_size and 0 <= pos[1] < grid_pixel_size:
                    row, col = get_clicked_pos(pos, rows, width)
                    if not is_valid_cell(row, col, rows):
                        continue
                    spot = grid[row][col]
                    spot.reset()
                    wall.discard((row,col))
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    try:
                        clear_search_visuals(grid, start, end)
                        world = World(rows-1,rows-1,wall)
                        p = PathFinding((start.row,start.col),(end.row,end.col),world)
                        now = time.time()
                        plan = search_solver.solve(p)
                        now = time.time() - now
                        print("Number of Expansion: {} in {} seconds".format(search_solver.expanded,now))
                        current_expansions = search_solver.expanded
                        current_search_time = now
                        if simulation_mode:
                            animation_speed, ok, interrupted = animate_search(
                                win,
                                grid,
                                rows,
                                width,
                                start,
                                end,
                                search_solver.expanded_sequence,
                                plan,
                                start is None and end is None and len(wall) == 0,
                                simulation_mode,
                                animation_speed,
                                selected_algorithm,
                            )
                            if not ok:
                                run = False
                                break
                            if interrupted:
                                print("Animazione interrotta.")
                        else:
                            mark_expanded(search_solver.expanded_states, grid, start, end)
                        if plan is not None:
                            print(plan)
                            print("Cost of the plan is: {}".format(len(plan)))
                            current_plan_cost = len(plan)
                            if not simulation_mode:
                                mark_spots(start,end,grid,plan)
                        else:
                            current_plan_cost = None
                        draw(
                            win,
                            grid,
                            rows,
                            width,
                            start is None and end is None and len(wall) == 0,
                            simulation_mode,
                            animation_speed,
                            selected_algorithm,
                            algorithm_menu_open,
                        )
                    except NotImplementedError as exc:
                        print("NotImplementedError: {}".format(exc))
                        show_alert(
                            win,
                            "Metodo non implementato",
                            "Una o piu funzioni richieste non sono implementate.\n{}".format(exc),
                        )
                if event.key == pygame.K_v:
                    simulation_mode = not simulation_mode
                if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    animation_speed = max(MIN_ANIMATION_SPEED, animation_speed - 1)
                if event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                    animation_speed = min(MAX_ANIMATION_SPEED, animation_speed + 1)
                if event.key == pygame.K_LEFTBRACKET:
                    apply_rows_delta(-1, rows_editable)
                if event.key == pygame.K_RIGHTBRACKET:
                    apply_rows_delta(1, rows_editable)
                if event.key == pygame.K_DOWN:
                    apply_rows_delta(-1, rows_editable)
                if event.key == pygame.K_UP:
                    apply_rows_delta(1, rows_editable)
                if event.key == pygame.K_ESCAPE and algorithm_menu_open:
                    algorithm_menu_open = False
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, width)
                    wall = set()
                    current_plan_cost = None
                    current_expansions = 0
                    current_search_time = None

        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            now_ms = pygame.time.get_ticks()

            if speed_minus_button.rect.collidepoint(mouse_pos) or speed_plus_button.rect.collidepoint(mouse_pos):
                if now_ms - last_speed_repeat_ms >= BUTTON_HOLD_REPEAT_MS:
                    if speed_minus_button.rect.collidepoint(mouse_pos):
                        animation_speed = max(MIN_ANIMATION_SPEED, animation_speed - 1)
                    elif speed_plus_button.rect.collidepoint(mouse_pos):
                        animation_speed = min(MAX_ANIMATION_SPEED, animation_speed + 1)
                    last_speed_repeat_ms = now_ms

            if rows_minus_button.rect.collidepoint(mouse_pos) or rows_plus_button.rect.collidepoint(mouse_pos):
                if now_ms - last_rows_repeat_ms >= BUTTON_HOLD_REPEAT_MS:
                    if rows_minus_button.rect.collidepoint(mouse_pos):
                        apply_rows_delta(-1, rows_editable)
                    elif rows_plus_button.rect.collidepoint(mouse_pos):
                        apply_rows_delta(1, rows_editable)
                    last_rows_repeat_ms = now_ms

    pygame.quit()

if __name__ == '__main__':
    main()
