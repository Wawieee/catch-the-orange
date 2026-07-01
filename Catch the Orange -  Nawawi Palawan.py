import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 540, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Orange")

SKY_TOP       = (74, 184, 240)
SKY_BOT       = (135, 206, 235)
WHITE         = (255, 255, 255)
CLOUD_COLOR   = (240, 248, 255)
ORANGE_DARK   = (230, 92, 0)
ORANGE_MID    = (255, 140, 0)
ORANGE_LIGHT  = (255, 208, 80)
LEAF_GREEN    = (58, 170, 53)
STEM_BROWN    = (139, 94, 60)
BASKET_LIGHT  = (200, 149, 58)
BASKET_DARK   = (155, 107, 32)
RIM_COLOR     = (232, 168, 64)
BLACK         = (0, 0, 0)
HUD_BG        = (10, 50, 100, 160)
HUD_TEXT      = (255, 213, 128)
PARTICLE_COLS = [(255, 140, 0), (255, 208, 80), (255, 107, 0), (255, 179, 71), (255, 255, 200)]

PADDLE_WIDTH  = 90
PADDLE_HEIGHT = 28
BALL_R        = 15

clock = pygame.time.Clock()
font_big   = pygame.font.SysFont("Arial", 28, bold=True)
font_med   = pygame.font.SysFont("Arial", 20)
font_small = pygame.font.SysFont("Arial", 15)



def draw_gradient_bg(surface):
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))


def draw_sunbeams(surface):
    cx, cy = WIDTH // 2, -30
    beam_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for i in range(12):
        angle = math.radians(i * 30)
        spread = math.radians(7)
        pts = [
            (cx, cy),
            (cx + math.cos(angle - spread) * 1200, cy + math.sin(angle - spread) * 1200),
            (cx + math.cos(angle + spread) * 1200, cy + math.sin(angle + spread) * 1200),
        ]
        pygame.draw.polygon(beam_surf, (255, 255, 255, 18), pts)
    surface.blit(beam_surf, (0, 0))


def draw_cloud(surface, x, y, r):
    offsets = [(0, 0, r), (int(r * 0.9), int(-r * 0.2), int(r * 0.75)),
               (int(-r * 0.8), int(r * 0.1), int(r * 0.65)),
               (int(r * 1.7), int(r * 0.1), int(r * 0.6))]
    for ox, oy, cr in offsets:
        pygame.draw.circle(surface, CLOUD_COLOR, (int(x + ox), int(y + oy)), cr)


def draw_orange(surface, x, y, r, rotation=0):
    ix, iy = int(x), int(y)
    # shadow
    shadow_surf = pygame.Surface((r * 4, r * 2), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surf, (0, 0, 0, 35),
                        (r // 2, r // 2, r * 3, r))
    surface.blit(shadow_surf, (ix - r + r // 2, iy + int(r * 0.6)))

    for i, (col, radius_factor) in enumerate([
        (ORANGE_DARK,  1.0),
        (ORANGE_MID,   0.82),
        (ORANGE_LIGHT, 0.55),
    ]):
        cr = int(r * radius_factor)
        ox = int(-r * 0.28 * (1 - radius_factor / 1.0))
        oy = int(-r * 0.28 * (1 - radius_factor / 1.0))
        pygame.draw.circle(surface, col, (ix + ox, iy + oy), cr)

    hl_surf = pygame.Surface((r, r), pygame.SRCALPHA)
    pygame.draw.ellipse(hl_surf, (255, 255, 255, 90),
                        (0, 0, int(r * 0.55), int(r * 0.38)))
    surface.blit(hl_surf, (ix - int(r * 0.52), iy - int(r * 0.52)))

    stem_x, stem_y = ix + 1, iy - r
    pygame.draw.line(surface, STEM_BROWN,
                     (stem_x, stem_y), (stem_x + 2, stem_y - 7), 2)

    lx, ly = stem_x + 6, stem_y - 5
    leaf_pts = []
    for a in range(12):
        angle = math.radians(a * 30) + rotation
        ex = lx + math.cos(angle) * 7
        ey = ly + math.sin(angle) * 3.5
        leaf_pts.append((ex, ey))
    pygame.draw.polygon(surface, LEAF_GREEN, leaf_pts)


def draw_basket(surface, x, y):
    bw, bh = PADDLE_WIDTH, PADDLE_HEIGHT
    ix, iy = int(x), int(y)

    pts = [(ix, iy), (ix + bw, iy), (ix + bw - 7, iy + bh), (ix + 7, iy + bh)]
    pygame.draw.polygon(surface, BASKET_DARK, pts)

    for i in range(1, 4):
        yy = iy + (bh * i) // 4
        pygame.draw.line(surface, (0, 0, 0, 60),
                         (ix + i * 2, yy), (ix + bw - i * 2, yy), 1)

    for i in range(-2, 9):
        sx = ix + i * 13
        pygame.draw.line(surface, (0, 0, 0, 45),
                         (sx, iy), (sx + int(bh * 0.55), iy + bh), 1)

    for row in range(bh // 2):
        alpha = int(60 * (1 - row / (bh / 2)))
        t = row / (bh / 2)
        r = int(BASKET_LIGHT[0] + (BASKET_DARK[0] - BASKET_LIGHT[0]) * t)
        g = int(BASKET_LIGHT[1] + (BASKET_DARK[1] - BASKET_LIGHT[1]) * t)
        b = int(BASKET_LIGHT[2] + (BASKET_DARK[2] - BASKET_LIGHT[2]) * t)
        left  = ix + int(row * 7 / bh)
        right = ix + bw - int(row * 7 / bh)
        pygame.draw.line(surface, (r, g, b), (left, iy + row), (right, iy + row))

    rim_rect = pygame.Rect(ix - 3, iy - 5, bw + 6, 9)
    pygame.draw.rect(surface, RIM_COLOR, rim_rect, border_radius=4)
    pygame.draw.rect(surface, BASKET_DARK, rim_rect, width=1, border_radius=4)


def draw_hud(surface, score, lives):
    hud = pygame.Surface((150, 58), pygame.SRCALPHA)
    pygame.draw.rect(hud, (10, 50, 100, 155), hud.get_rect(), border_radius=10)
    surface.blit(hud, (8, 8))

    label = font_small.render("Score", True, WHITE)
    surface.blit(label, (20, 16))
    val = font_big.render(str(score), True, HUD_TEXT)
    surface.blit(val, (20, 32))

    for i in range(3):
        alive = i < lives
        col = ORANGE_MID if alive else (120, 120, 120)
        ox = WIDTH - 24 - i * 28
        pygame.draw.circle(surface, col, (ox, 30), 10)
        if alive:
            pygame.draw.polygon(surface, LEAF_GREEN, [
                (ox + 4, 21), (ox + 10, 17), (ox + 12, 24)
            ])


def draw_title_screen(surface, score=None):
    draw_gradient_bg(surface)
    draw_sunbeams(surface)
    for cl in title_clouds:
        draw_cloud(surface, cl[0], cl[1], cl[2])

    title1 = font_big.render("CATCH THE", True, BLACK)
    title2 = pygame.font.SysFont("Arial", 52, bold=True).render("ORANGE", True, ORANGE_MID)
    surface.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 90))
    surface.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 125))

    draw_orange(surface, WIDTH // 2, 250, 40)

    if score is not None:
        go = font_big.render("Game Over!", True, (200, 40, 40))
        sc = font_med.render(f"Final Score: {score}", True, BLACK)
        surface.blit(go, (WIDTH // 2 - go.get_width() // 2, 310))
        surface.blit(sc, (WIDTH // 2 - sc.get_width() // 2, 348))
        prompt = font_med.render("Press SPACE or click to play again", True, BLACK)
    else:
        prompt = font_med.render("Press SPACE or click to start", True, BLACK)
    surface.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 400))



class Cloud:
    def __init__(self, offscreen=False):
        self.r = random.randint(28, 52)
        self.x = random.randint(-50, WIDTH + 50) if not offscreen else -self.r * 2
        self.y = random.randint(20, int(HEIGHT * 0.42))
        self.speed = 0.18 + random.random() * 0.18

    def update(self):
        self.x += self.speed
        if self.x - self.r * 2 > WIDTH:
            self.x = -self.r * 2
            self.y = random.randint(20, int(HEIGHT * 0.42))

    def draw(self, surface):
        draw_cloud(surface, self.x, self.y, self.r)



class Particle:
    def __init__(self, x, y):
        angle = random.uniform(0, math.pi * 2)
        sp = random.uniform(1.5, 4.5)
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * sp
        self.vy = math.sin(angle) * sp - 2.5
        self.r = random.randint(3, 6)
        self.color = random.choice(PARTICLE_COLS)
        self.life = random.randint(24, 44)
        self.max_life = self.life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.18
        self.life -= 1

    def draw(self, surface):
        alpha = int(255 * self.life / self.max_life)
        s = pygame.Surface((self.r * 2, self.r * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (self.r, self.r), self.r)
        surface.blit(s, (int(self.x) - self.r, int(self.y) - self.r))



title_clouds = [
    (80,  80,  38),
    (460, 60,  30),
    (260, 170, 44),
    (520, 200, 34),
    (30,  200, 28),
]



def main():
    game_state = "title" 
    final_score = None

    paddle_x = WIDTH // 2 - PADDLE_WIDTH // 2
    paddle_y = HEIGHT - 40
    balls = []
    clouds = [Cloud() for _ in range(4)]
    particles = []
    score = 0
    lives = 3
    speed = 2.2
    spawn_timer = 0
    rotations = {}

    pygame.mouse.set_visible(False)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if game_state in ("title", "gameover"):
                    if event.type == pygame.KEYDOWN and event.key != pygame.K_SPACE:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return
                        continue
                    # start / restart
                    game_state  = "playing"
                    balls       = []
                    particles   = []
                    rotations   = {}
                    score       = 0
                    lives       = 3
                    speed       = 2.2
                    spawn_timer = 0

        if game_state in ("title", "gameover"):
            draw_title_screen(screen, final_score if game_state == "gameover" else None)
            pygame.display.flip()
            continue


        mouse_x = pygame.mouse.get_pos()[0]
        paddle_x = mouse_x - PADDLE_WIDTH // 2
        paddle_x = max(0, min(WIDTH - PADDLE_WIDTH, paddle_x))

        spawn_timer += 1
        spawn_interval = max(18, int(40 - score * 0.25))
        if spawn_timer >= spawn_interval:
            bx = random.randint(BALL_R, WIDTH - BALL_R)
            balls.append([bx, -BALL_R])
            rotations[id(balls[-1])] = 0.0
            spawn_timer = 0

        new_balls = []
        for ball in balls:
            ball[1] += speed
            bid = id(ball)
            rotations[bid] = rotations.get(bid, 0.0) + 0.04

            if (ball[1] + BALL_R >= paddle_y and
                    paddle_x + 5 < ball[0] < paddle_x + PADDLE_WIDTH - 5):
                score += 1
                for _ in range(10):
                    particles.append(Particle(ball[0], paddle_y))
                rotations.pop(bid, None)
                continue

            if ball[1] - BALL_R > HEIGHT:
                lives -= 1
                rotations.pop(bid, None)
                continue

            new_balls.append(ball)

        balls = new_balls
        speed = 2.2 + score * 0.045

        particles = [p for p in particles if p.life > 0]
        for p in particles:
            p.update()

        for cl in clouds:
            cl.update()

        draw_gradient_bg(screen)
        draw_sunbeams(screen)
        for cl in clouds:
            cl.draw(screen)

        for ball in balls:
            draw_orange(screen, ball[0], ball[1], BALL_R,
                        rotation=rotations.get(id(ball), 0.0))

        for p in particles:
            p.draw(screen)

        draw_basket(screen, paddle_x, paddle_y)
        draw_hud(screen, score, lives)

        mx, my = pygame.mouse.get_pos()
        pygame.draw.circle(screen, (255, 255, 255, 180), (mx, my), 4)

        pygame.display.flip()

        if lives <= 0:
            final_score = score
            game_state  = "gameover"


if __name__ == "__main__":
    main()