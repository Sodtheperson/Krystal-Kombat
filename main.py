import pygame
import time

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
grounded = True
falling = False
font = pygame.font.Font(None, 36)
velocity = pygame.Vector2(0, 0)
gravity = 1000
jump_strength = -400
ground_y = 500
fall_timer = 0 
last_tap_time = {"a": 0, "d": 0}
sprint = False
base_speed = 300
sprint_speed = 450
double_tap_window = 0.25  # seconds

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
facing = 1

# Hitbox variables
hitbox_active = False
hitbox_timer = 0
hitbox_cooldown_timer = 0
hitbox_duration = 0.2  # seconds
hitbox_cooldown = 0.5  # seconds
hitbox_offset = 60
hitbox_size = pygame.Vector2(60, 40)  # width, height

while running:
    current_time = time.time()
    if hitbox_cooldown_timer > 0:
        hitbox_cooldown_timer -= dt
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Double-tap sprint
            if event.key == pygame.K_a and grounded:
                if current_time - last_tap_time["a"] <= double_tap_window:
                    sprint = True
                last_tap_time["a"] = current_time
            if event.key == pygame.K_d and grounded:
                if current_time - last_tap_time["d"] <= double_tap_window:
                    sprint = True
                last_tap_time["d"] = current_time

            # Hitbox activation
            if event.key == pygame.K_j and hitbox_cooldown_timer <= 0:
                hitbox_active = True
                hitbox_timer = hitbox_duration
                hitbox_cooldown_timer = hitbox_cooldown  # start cooldown
                
    keys = pygame.key.get_pressed()
    if not (keys[pygame.K_a] or keys[pygame.K_d]):
        sprint = False

    # Update facing direction
    if keys[pygame.K_a]:
        facing = -1
    elif keys[pygame.K_d]:
        facing = 1

    # Physics
    if keys[pygame.K_w] and player_pos.y >= ground_y:
        velocity.y = jump_strength
        grounded = False
        
    if falling:
        fall_timer += dt
        # Linear ramp from 1 → 1.25 over 0.2 seconds
        fall_multiplier = 1 + min(fall_timer / 0.15 * 0.25, 0.25)
    else:
        fall_timer = 0
        fall_multiplier = 1
        
    velocity.y += gravity * dt * fall_multiplier
    player_pos += velocity * dt
    falling = velocity.y > 0 and not grounded
    if player_pos.y >= ground_y:
        player_pos.y = ground_y
        velocity.y = 0
        grounded = True
        falling = False
        fall_timer = 0
    
    # Movement
    speed = sprint_speed if sprint else base_speed
    speed = speed * (0.9 if not grounded else 1)
    
    if keys[pygame.K_s]:
        player_pos.y += speed * dt
    if keys[pygame.K_a]:
        player_pos.x -= speed * dt
    if keys[pygame.K_d]:
        player_pos.x += speed * dt

    # Draw
    screen.fill("black")
    pygame.draw.circle(screen, "red", player_pos, 40)

    # Draw facing indicator
    face_offset = 50
    face_box = player_pos + pygame.Vector2(facing * face_offset, 0)
    pygame.draw.rect(screen, "blue", (face_box.x - 10, face_box.y - 10, 20, 20))

    # Draw hitbox if active
    if hitbox_active:
        hb_pos = player_pos + pygame.Vector2(facing * hitbox_offset, 0)
        pygame.draw.rect(screen, "yellow", (hb_pos.x - hitbox_size.x/2, hb_pos.y - hitbox_size.y/2, hitbox_size.x, hitbox_size.y))
        hitbox_timer -= dt
        if hitbox_timer <= 0:
            hitbox_active = False

    # Debug text
    text_surface = font.render(f'{player_pos.x:.1f}, {player_pos.y:.1f}, Sprinting: {sprint}, Grounded: {grounded}, Falling: {falling}', True, (255, 255, 255))
    screen.blit(text_surface, (100, 650))

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
