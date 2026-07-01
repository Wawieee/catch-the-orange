import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Watermelon (Free Palestine)")

SKY_TOP        = (144, 238, 144)
SKY_BOT        = (204, 255, 178)
WHITE          = (255, 255, 255)
CLOUD_COLOR    = (240, 255, 240)
WM_RIND_DARK   = (34, 120, 34)
WM_RIND_MID    = (60, 179, 60)
WM_RIND_LIGHT  = (120, 220, 80)
WM_FLESH       = (220, 50, 60)
WM_FLESH_LIGHT = (255, 105, 110)
WM_WHITE_RIND  = (230, 255, 220)
SEED_COLOR     = (30, 20, 20)
STEM_BROWN     = (100, 60, 20)
LEAF_GREEN     = (40, 140, 40)
BASKET_LIGHT   = (200, 149, 58)
BASKET_DARK    = (155, 107, 32)
RIM_COLOR      = (232, 168, 64)
BLACK          = (0, 0, 0)
HUD_TEXT       = (180, 255, 140)
PARTICLE_COLS  = [(220, 50, 60), (255, 105, 110), (60, 179, 60), (120, 220, 80), (255, 255, 200)]

PADDLE_WIDTH   = 90
PADDLE_HEIGHT  = 28
BALL_R         = 18

clock      = pygame.time.Clock()
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
        angle  = math.radians(i * 30)
        spread = math.radians(7)
        pts = [
            (cx, cy),
            (cx + math.cos(angle - spread) * 1200, cy + math.sin(angle - spread) * 1200),
            (cx + math.cos(angle + spread) * 1200, cy + math.sin(angle + spread) * 1200),
        ]
        pygame.draw.polygon(beam_surf, (255, 255, 255, 14), pts)
    surface.blit(beam_surf, (0, 0))


def draw_cloud(surface, x, y, r):
    offsets = [(0, 0, r), (int(r * 0.9), int(-r * 0.2), int(r * 0.75)),
               (int(-r * 0.8), int(r * 0.1), int(r * 0.65)),
               (int(r * 1.7), int(r * 0.1), int(r * 0.6))]
    for ox, oy, cr in offsets:
        pygame.draw.circle(surface, CLOUD_COLOR, (int(x + ox), int(y + oy)), cr)


def draw_watermelon(surface, x, y, r, rotation=0):
    ix, iy = int(x), int(y)

    shadow_surf = pygame.Surface((r * 4, r * 2), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surf, (0, 0, 0, 30),
                        (r // 2, r // 2, r * 3, r))
    surface.blit(shadow_surf, (ix - r + r // 2, iy + int(r * 0.65)))

    pygame.draw.circle(surface, WM_RIND_DARK, (ix, iy), r)

    stripe_surf = pygame.Surface((r * 2 + 4, r * 2 + 4), pygame.SRCALPHA)
    sc = r + 2
    for stripe_angle in range(0, 360, 45):
        a1 = math.radians(stripe_angle + rotation * 30)
        a2 = math.radians(stripe_angle + 18 + rotation * 30)
        pts = [(sc, sc)]
        for a in [a1 + i * (a2 - a1) / 8 for i in range(9)]:
            pts.append((sc + math.cos(a) * r, sc + math.sin(a) * r))
        pygame.draw.polygon(stripe_surf, (*WM_RIND_MID, 200), pts)
    surface.blit(stripe_surf, (ix - r - 2, iy - r - 2))

    pygame.draw.circle(surface, WM_WHITE_RIND, (ix, iy), int(r * 0.88))

    pygame.draw.circle(surface, WM_FLESH, (ix, iy), int(r * 0.80))

    pygame.draw.circle(surface, WM_FLESH_LIGHT, (ix - int(r * 0.25), iy - int(r * 0.25)), int(r * 0.45))

    seed_positions = [
        (-0.25, -0.15), (0.20, -0.25), (0.10, 0.25),
        (-0.20, 0.20),  (0.30, 0.10),
    ]
    for sx_frac, sy_frac in seed_positions:
        seed_w = max(3, int(r * 0.14))
        seed_h = max(2, int(r * 0.08))

        base_angle = math.atan2(sy_frac, sx_frac) + rotation
        dist = math.hypot(sx_frac, sy_frac) * r
        seed_x = ix + int(math.cos(base_angle) * dist)
        seed_y = iy + int(math.sin(base_angle) * dist)
        seed_surf = pygame.Surface((seed_w, seed_h), pygame.SRCALPHA)
        pygame.draw.ellipse(seed_surf, SEED_COLOR, (0, 0, seed_w, seed_h))
        rotated = pygame.transform.rotate(seed_surf, -math.degrees(base_angle))
        rr = rotated.get_rect(center=(seed_x, seed_y))
        surface.blit(rotated, rr)

    hl_surf = pygame.Surface((r, r), pygame.SRCALPHA)
    pygame.draw.ellipse(hl_surf, (255, 255, 255, 70),
                        (0, 0, int(r * 0.5), int(r * 0.32)))
    surface.blit(hl_surf, (ix - int(r * 0.48), iy - int(r * 0.48)))

    stem_x, stem_y = ix, iy - r
    pygame.draw.line(surface, STEM_BROWN,
                     (stem_x, stem_y), (stem_x + 3, stem_y - 8), 2)
    pygame.draw.arc(surface, STEM_BROWN,
                    pygame.Rect(stem_x, stem_y - 12, 10, 8),
                    math.radians(0), math.radians(200), 2)

    lx, ly = stem_x + 8, stem_y - 9
    leaf_pts = []
    for a in range(12):
        angle = math.radians(a * 30) + rotation * 0.5
        ex = lx + math.cos(angle) * 8
        ey = ly + math.sin(angle) * 4
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
    pygame.draw.rect(hud, (10, 80, 30, 155), hud.get_rect(), border_radius=10)
    surface.blit(hud, (8, 8))

    label = font_small.render("Score", True, WHITE)
    surface.blit(label, (20, 16))
    val = font_big.render(str(score), True, HUD_TEXT)
    surface.blit(val, (20, 32))

    for i in range(3):
        alive = i < lives
        ox = WIDTH - 24 - i * 28
        outer_col = WM_RIND_MID if alive else (120, 120, 120)
        inner_col = WM_FLESH    if alive else (160, 160, 160)
        pygame.draw.circle(surface, outer_col, (ox, 30), 10)
        pygame.draw.circle(surface, inner_col, (ox, 30), 7)
        if alive:
            pygame.draw.line(surface, STEM_BROWN, (ox, 20), (ox + 2, 15), 2)


def draw_title_screen(surface, score=None):
    draw_gradient_bg(surface)
    draw_sunbeams(surface)

    for cl in title_clouds:
        draw_cloud(surface, cl[0], cl[1], cl[2])

    title_small = pygame.font.SysFont("Arial", 42, bold=True)
    title_big = pygame.font.SysFont("Arial", 64, bold=True)
    subtitle = pygame.font.SysFont("Arial", 24, bold=True)
    prompt_font = pygame.font.SysFont("Arial", 28, bold=True)

    shadow_offset = 3

    shadow1 = title_small.render("CATCH THE", True, (40, 40, 40))
    shadow2 = title_big.render("WATERMELON", True, (40, 40, 40))

    surface.blit(shadow1, (WIDTH//2-shadow1.get_width()//2+shadow_offset, 92))
    surface.blit(shadow2, (WIDTH//2-shadow2.get_width()//2+shadow_offset, 132))

    title1 = title_small.render("CATCH THE", True, WM_RIND_DARK)
    title2 = title_big.render("WATERMELON", True, WM_FLESH)

    surface.blit(title1, (WIDTH//2-title1.get_width()//2, 90))
    surface.blit(title2, (WIDTH//2-title2.get_width()//2, 130))

    title3 = subtitle.render("(Free Palestine)", True, WM_RIND_DARK)
    surface.blit(title3, (WIDTH//2-title3.get_width()//2, 215))

    draw_watermelon(surface, WIDTH//2, 325, 56)


    if score is not None:
        go = font_big.render("Game Over!", True, (180, 30, 30))
        sc = font_med.render(f"Final Score: {score}", True, WM_RIND_DARK)
        surface.blit(go, (WIDTH // 2 - go.get_width() // 2, 428))
        surface.blit(sc, (WIDTH // 2 - sc.get_width() // 2, 462))
        prompt = font_med.render("Press SPACE or click to play again", True, BLACK)
    else:
        prompt = font_med.render("Press SPACE or click to start", True, BLACK)
    surface.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 520))




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
        self.r  = random.randint(3, 6)
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
    game_state  = "title"
    final_score = None

    paddle_x    = WIDTH // 2 - PADDLE_WIDTH // 2
    paddle_y    = HEIGHT - 40
    balls       = []
    clouds      = [Cloud() for _ in range(4)]
    particles   = []
    score       = 0
    lives       = 3
    speed       = 2.2
    spawn_timer = 0
    rotations   = {}

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

        mouse_x  = pygame.mouse.get_pos()[0]
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
            rotations[bid] = rotations.get(bid, 0.0) + 0.035

            if (ball[1] + BALL_R >= paddle_y and
                    paddle_x + 5 < ball[0] < paddle_x + PADDLE_WIDTH - 5):
                score += 1
                for _ in range(12):
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
            draw_watermelon(screen, ball[0], ball[1], BALL_R,
                            rotation=rotations.get(id(ball), 0.0))

        for p in particles:
            p.draw(screen)

        draw_basket(screen, paddle_x, paddle_y)
        draw_hud(screen, score, lives)

        mx, my = pygame.mouse.get_pos()
        pygame.draw.circle(screen, (255, 255, 255), (mx, my), 4)

        pygame.display.flip()

        if lives <= 0:
            final_score = score
            game_state  = "gameover"


if __name__ == "__main__":
    main()