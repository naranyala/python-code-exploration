import asyncio
import platform
import pyray as rl
import random
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 8
BALL_RADIUS = 8
INITIAL_BALL_SPEED = 5.0
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 20
BRICK_PADDING = 5
BRICK_OFFSET_TOP = 60
BRICK_OFFSET_LEFT = 35

# Game state enumeration
class GameState:
    PLAYING = 0
    GAME_OVER = 1
    VICTORY = 2

# Game objects
class Ball:
    def __init__(self, x, y, dx, dy, radius, active):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = radius
        self.active = active

class Brick:
    def __init__(self, x, y, width, height, active, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.active = active
        self.color = color

# Game state variables
paddle_x = float(SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2)
ball = Ball(
    x=float(SCREEN_WIDTH / 2),
    y=float(SCREEN_HEIGHT - 30),
    dx=INITIAL_BALL_SPEED,
    dy=-INITIAL_BALL_SPEED,
    radius=float(BALL_RADIUS),
    active=True
)
bricks = []
score = 0
lives = 3
game_state = GameState.PLAYING

# Initialize bricks
def init_bricks():
    global bricks
    colors = [rl.RED, rl.ORANGE, rl.YELLOW, rl.GREEN, rl.BLUE]
    bricks = []

    for r in range(BRICK_ROWS):
        for c in range(BRICK_COLS):
            brick_x = float(BRICK_OFFSET_LEFT + c * (BRICK_WIDTH + BRICK_PADDING))
            brick_y = float(BRICK_OFFSET_TOP + r * (BRICK_HEIGHT + BRICK_PADDING))
            bricks.append(Brick(
                x=brick_x,
                y=brick_y,
                width=float(BRICK_WIDTH),
                height=float(BRICK_HEIGHT),
                active=True,
                color=colors[r % len(colors)]
            ))

# Reset ball position
def reset_ball():
    global ball
    ball.x = float(SCREEN_WIDTH / 2)
    ball.y = float(SCREEN_HEIGHT - 30)
    ball.dx = INITIAL_BALL_SPEED * (1.0 if random.randint(0, 1) == 0 else -1.0)
    ball.dy = -INITIAL_BALL_SPEED
    ball.active = True

# Initialize game
def init_game():
    global paddle_x, score, lives, game_state
    paddle_x = float(SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2)
    score = 0
    lives = 3
    game_state = GameState.PLAYING
    init_bricks()
    reset_ball()

# Collision detection: ball vs brick
def check_ball_brick_collision(ball, brick):
    global score
    if not brick.active:
        return False

    # Find closest point on brick to ball center
    closest_x = max(brick.x, min(ball.x, brick.x + brick.width))
    closest_y = max(brick.y, min(ball.y, brick.y + brick.height))

    # Calculate distance
    dx = ball.x - closest_x
    dy = ball.y - closest_y
    distance = math.sqrt(dx * dx + dy * dy)

    if distance < ball.radius:
        brick.active = False
        score += 10

        # Determine bounce direction
        if ball.x < brick.x or ball.x > brick.x + brick.width:
            ball.dx = -ball.dx
        else:
            ball.dy = -ball.dy
        return True
    return False

# Update game logic
def update_game():
    global paddle_x, lives, game_state
    if game_state != GameState.PLAYING:
        if rl.is_key_pressed(rl.KeyboardKey.KEY_R):
            init_game()
        return

    # Move paddle
    if rl.is_key_down(rl.KeyboardKey.KEY_LEFT):
        paddle_x = max(0.0, paddle_x - float(PADDLE_SPEED))
    if rl.is_key_down(rl.KeyboardKey.KEY_RIGHT):
        paddle_x = min(float(SCREEN_WIDTH - PADDLE_WIDTH), paddle_x + float(PADDLE_SPEED))

    # Move ball
    if ball.active:
        ball.x += ball.dx
        ball.y += ball.dy

        # Wall collisions
        if ball.x - ball.radius <= 0 or ball.x + ball.radius >= float(SCREEN_WIDTH):
            ball.dx = -ball.dx
        if ball.y - ball.radius <= 0:
            ball.dy = -ball.dy

        # Paddle collision
        if (ball.y + ball.radius >= float(SCREEN_HEIGHT - PADDLE_HEIGHT) and
            ball.y - ball.radius <= float(SCREEN_HEIGHT) and
            ball.x >= paddle_x and ball.x <= paddle_x + float(PADDLE_WIDTH)):
            ball.dy = -abs(ball.dy)  # Always bounce up

            # Add spin based on where ball hits paddle
            hit_pos = (ball.x - paddle_x) / float(PADDLE_WIDTH)
            ball.dx = 8.0 * (hit_pos - 0.5)  # -4 to 4

        # Brick collisions
        for brick in bricks:
            check_ball_brick_collision(ball, brick)

        # Ball out of bounds
        if ball.y > float(SCREEN_HEIGHT):
            lives -= 1
            if lives <= 0:
                game_state = GameState.GAME_OVER
            else:
                reset_ball()

    # Check victory condition
    if all(not brick.active for brick in bricks):
        game_state = GameState.VICTORY

# Draw game
def draw_game():
    # Clear background
    rl.clear_background(rl.BLACK)

    # Draw paddle
    rl.draw_rectangle(
        int(paddle_x), int(SCREEN_HEIGHT - PADDLE_HEIGHT),
        int(PADDLE_WIDTH), int(PADDLE_HEIGHT), rl.WHITE
    )

    # Draw ball
    if ball.active:
        rl.draw_circle(int(ball.x), int(ball.y), float(BALL_RADIUS), rl.YELLOW)

    # Draw bricks
    for brick in bricks:
        if brick.active:
            rl.draw_rectangle(
                int(brick.x), int(brick.y),
                int(brick.width), int(brick.height),
                brick.color
            )

    # Draw UI
    rl.draw_text(f"Score: {score}", 10, 10, 20, rl.WHITE)
    rl.draw_text(f"Lives: {lives}", 10, 40, 20, rl.WHITE)

    # Draw game state messages
    if game_state == GameState.GAME_OVER:
        rl.draw_text(
            "GAME OVER! Press R to restart",
            int(SCREEN_WIDTH / 2 - 150), int(SCREEN_HEIGHT / 2), 20, rl.RED
        )
    elif game_state == GameState.VICTORY:
        rl.draw_text(
            "YOU WIN! Press R to play again",
            int(SCREEN_WIDTH / 2 - 150), int(SCREEN_HEIGHT / 2), 20, rl.GREEN
        )

def setup():
    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Breakout")
    rl.set_target_fps(60)
    init_game()
    return True

def update_loop():
    if rl.window_should_close():
        return False
    update_game()
    rl.begin_drawing()
    draw_game()
    rl.end_drawing()
    return True

async def main():
    setup()
    FPS = 60
    while update_loop():
        await asyncio.sleep(1.0 / FPS)
    rl.close_window()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
