import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")

WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
RED = (255, 80, 80)
BLACK = (0, 0, 0)

PADDLE_WIDTH = 80
PADDLE_HEIGHT = 10
BALL_SIZE = 20

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)


def draw_text(text, x, y):
    img = font.render(text, True, BLACK)
    screen.blit(img, (x, y))


def main():
    running = True

    # Paddle
    paddle_x = WIDTH // 2 - PADDLE_WIDTH // 2
    paddle_y = HEIGHT - 30

    # Balls
    balls = []

    score = 0
    lives = 3
    speed = 2

    spawn_timer = 0

    while running:
        screen.fill(WHITE)
        clock.tick(60)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Mouse control for paddle
        mouse_x = pygame.mouse.get_pos()[0]
        paddle_x = mouse_x - PADDLE_WIDTH // 2

        # Keep paddle in bounds
        paddle_x = max(0, min(WIDTH - PADDLE_WIDTH, paddle_x))

        # Spawn balls
        spawn_timer += 1
        if spawn_timer > 40:  # adjust spawn rate
            x = random.randint(0, WIDTH - BALL_SIZE)
            balls.append([x, 0])
            spawn_timer = 0

        # Move and update balls
        for ball in balls[:]:
            ball[1] += speed  # move down

            # Collision with paddle
            if (
                ball[1] + BALL_SIZE >= paddle_y
                and paddle_x < ball[0] < paddle_x + PADDLE_WIDTH
            ):
                balls.remove(ball)
                score += 1
                continue

            # Missed ball
            if ball[1] > HEIGHT:
                balls.remove(ball)
                lives -= 1

        speed += 0.001

        pygame.draw.rect(
            screen, BLUE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        )

        for ball in balls:
            pygame.draw.circle(screen, RED, (ball[0], ball[1]), BALL_SIZE // 2)

        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Lives: {lives}", 10, 30)

        pygame.display.flip()

        if lives <= 0:
            running = False

    print("Game Over!")
    print("Final Score:", score)

    pygame.quit()

if __name__ == "__main__":
    main()