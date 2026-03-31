# ================= HIDE ALL WARNINGS =================
import warnings
warnings.filterwarnings("ignore")

# ================= IMPORTS =================
import pygame
import random
import sys
import os

# ================= INIT =================
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 42)
small_font = pygame.font.SysFont(None, 24)

# ================= COLORS =================
BLUE = (135, 206, 235)
GREEN = (0, 180, 0)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)

# ================= HIGH SCORE FILE =================
SCORE_FILE = "highscore.txt"

def load_high_score():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open(SCORE_FILE, "w") as f:
        f.write(str(score))

high_score = load_high_score()

# ================= BIRD =================
bird_x = 80
bird_y = HEIGHT // 2
bird_radius = 14

bird_velocity = 0
GRAVITY = 0.32
FLAP = -6.8
MAX_FALL = 7.5

# ================= PIPE =================
PIPE_WIDTH = 60
PIPE_GAP = 180
PIPE_SPEED = 2.0
PIPE_SPACING = 340

pipes = []

def create_pipe():
    margin = 80
    top = random.randint(
        margin,
        HEIGHT - PIPE_GAP - margin
    )
    return {
        "x": WIDTH,
        "top": top,
        "passed": False
    }

# ================= GAME STATE =================
score = 0
game_over = True   # start screen first

# ================= RESET =================
def reset_game():
    global bird_y, bird_velocity, pipes, score, game_over
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes.clear()
    pipes.append(create_pipe())
    score = 0
    game_over = False

# ================= GAME LOOP =================
while True:
    screen.fill(BLUE)

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()
                else:
                    bird_velocity = FLAP   # reset jump (no stacking)

    # -------- PHYSICS --------
    if not game_over:
        bird_velocity += GRAVITY
        if bird_velocity > MAX_FALL:
            bird_velocity = MAX_FALL
        bird_y += bird_velocity

    # -------- DRAW BIRD --------
    pygame.draw.circle(
        screen,
        YELLOW,
        (bird_x, int(bird_y)),
        bird_radius
    )

    # -------- PIPE LOGIC --------
    if not game_over:
        if len(pipes) == 0 or pipes[-1]["x"] < WIDTH - PIPE_SPACING:
            pipes.append(create_pipe())

        for pipe in pipes:
            pipe["x"] -= PIPE_SPEED

        if pipes and pipes[0]["x"] < -PIPE_WIDTH:
            pipes.pop(0)

    bird_rect = pygame.Rect(
        bird_x - bird_radius,
        bird_y - bird_radius,
        bird_radius * 2,
        bird_radius * 2
    )

    for pipe in pipes:
        top_rect = pygame.Rect(pipe["x"], 0, PIPE_WIDTH, pipe["top"])
        bottom_rect = pygame.Rect(
            pipe["x"],
            pipe["top"] + PIPE_GAP,
            PIPE_WIDTH,
            HEIGHT
        )

        pygame.draw.rect(screen, GREEN, top_rect)
        pygame.draw.rect(screen, GREEN, bottom_rect)

        # COLLISION
        if not game_over and (
            bird_rect.colliderect(top_rect) or
            bird_rect.colliderect(bottom_rect)
        ):
            game_over = True

        # SCORE
        if not pipe["passed"] and pipe["x"] + PIPE_WIDTH < bird_x:
            score += 1
            pipe["passed"] = True

    # -------- SCREEN BOUNDS --------
    if not game_over and (
        bird_y - bird_radius < 0 or
        bird_y + bird_radius > HEIGHT
    ):
        game_over = True

    # -------- HIGH SCORE UPDATE --------
    if game_over:
        if score > high_score:
            high_score = score
            save_high_score(high_score)

    # -------- UI --------
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_text = small_font.render(f"Top Score: {high_score}", True, WHITE)

    screen.blit(score_text, (20, 20))
    screen.blit(high_text, (20, 55))

    if game_over:
        title = font.render("FLAPPY BIRD", True, WHITE)
        over = font.render("GAME OVER", True, WHITE)
        play = small_font.render("Press SPACE to Start / Play", True, WHITE)

        screen.blit(title, (WIDTH//2 - 120, HEIGHT//2 - 100))
        screen.blit(over, (WIDTH//2 - 100, HEIGHT//2 - 40))
        screen.blit(play, (WIDTH//2 - 130, HEIGHT//2 + 10))

    pygame.display.update()
    clock.tick(60)
