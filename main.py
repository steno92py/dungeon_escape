#!/usr/bin/env python3
"""Dungeon Escape (PgZero)

A simple roguelike game for beginners in Python and game development.

Main features:
- 40x40 tile grid (floor/wall) in an 800x600 window
- Player and 4 slime types with simple animations
- Golden key to collect and a door to advance
- 5 levels with increasing difficulty
- Main menu, pause, game over, victory screens

Allowed dependencies:
- PgZero (framework), math.hypot, random (choice, random, randint)
- Exception: Rect imported from pygame for collisions

How to run:
  python -m pgzero main.py
or (if available)
  pgzrun main.py

Controls:
- Movement: WASD or Arrow keys
- Pause/Resume: ESC or P
- End screens: SPACE to return to the menu
"""

import pgzrun
from math import hypot
from random import choice, random, randint
from pygame import Rect
## Note: only using allowed libraries (PgZero, math, random). No direct pygame usage except Rect.

# Window and tile constants
# The world is a grid of TILE_SIZE cells drawn inside the window.
WIDTH = 800
HEIGHT = 600
TILE_SIZE = 40
GRID_WIDTH = 20
GRID_HEIGHT = 14
HUD_HEIGHT = 40
# Standard size for HUD icons (hearts, key)
HUD_ICON_PX = 32

# Game states
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_VICTORY = "victory"
STATE_PAUSED = "paused"

# Global game variables
# These globals keep the current game state and world entities.
game_state = STATE_MENU
current_level = 1
player = None
enemies = []
walls = []
floor_tiles = []
key_collected = False
door_position = None
key_position = None
key_actor = None
door_actor = None
music_enabled = True
sound_enabled = True
menu_buttons = []
pause_buttons = []
level_time_accum = 0.0
level_times = []


class Animation:
    """Frame-based animation helper for sprites.

    - frames: list of image names (strings) loadable by PgZero
    - fps: frames per second (animation speed)
    """
    
    def __init__(self, frames, fps=8):
        self.frames = frames
        self.fps = fps
        self.current_frame = 0
        self.time_accumulated = 0.0
    
    def update(self, dt):
        """Advance the animation based on elapsed time (dt in seconds)."""
        self.time_accumulated += dt
        frame_duration = 1.0 / self.fps
        
        while self.time_accumulated >= frame_duration:
            self.time_accumulated -= frame_duration
            self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def get_current_frame(self):
        """Return the name of the current frame image."""
        return self.frames[self.current_frame]
    
    def reset(self):
        """Reset to the first frame and clear accumulated time."""
        self.current_frame = 0
        self.time_accumulated = 0.0


class Character:
    """Base class for entities with movement, collisions and animations.

    Responsibilities:
    - manage position, direction and speed
    - axis-aligned collision with walls using Rect (AABB)
    - pick and update the current animation (idle/move)
    """

    def __init__(self, x, y, speed, hitbox_size=20):
        """Initialize the character.

        Parameters:
        - x, y: initial pixel coordinates (center)
        - speed: pixels per second
        - hitbox_size: side of the square hitbox (px)
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.dx = 0
        self.dy = 0
        self.state = "idle"
        self.animations = {}
        self.actor = None
        # Smaller and centered hitbox
        half_size = hitbox_size // 2
        self.hitbox = Rect(x - half_size, y - half_size, hitbox_size, hitbox_size)
    
    def setup_animations(self, idle_frames, move_frames):
        """Register 'idle' and 'move' animations and create the Actor."""
        self.animations["idle"] = Animation(idle_frames, fps=6)
        self.animations["move"] = Animation(move_frames, fps=8)

        # Create actor with first frame and apply scale
        if idle_frames:
            self.actor = Actor(idle_frames[0], (self.x, self.y))
    
    def move(self, dt):
        """Update position using normalized input and handle wall collisions."""
        if abs(self.dx) > 0.01 or abs(self.dy) > 0.01:
            self.state = "move"
        else:
            self.state = "idle"

        # Normalize diagonal movement so diagonals are not faster
        mag = hypot(self.dx, self.dy)
        if mag > 0:
            self.dx /= mag
            self.dy /= mag

        # Calculate new position
        new_x = self.x + self.dx * self.speed * dt
        new_y = self.y + self.dy * self.speed * dt

        # Check collision with walls: create hitbox at new position
        half_size = self.hitbox.width // 2
        new_hitbox = Rect(new_x - half_size, new_y - half_size, self.hitbox.width, self.hitbox.height)
        collision = False

        for wall in walls:
            if new_hitbox.colliderect(wall):
                collision = True
                break

        # Update position if no collision
        if not collision:
            # Keep within screen bounds
            margin = self.hitbox.width // 2
            self.x = max(margin, min(WIDTH - margin, new_x))
            self.y = max(margin, min(HEIGHT - HUD_HEIGHT - margin, new_y))
            self.hitbox.center = (self.x, self.y)

            if self.actor:
                self.actor.pos = (self.x, self.y)
    
    def update_animation(self, dt):
        """Advance the current state's animation and update the Actor image."""
        if self.state in self.animations:
            anim = self.animations[self.state]
            anim.update(dt)
            if self.actor:
                self.actor.image = anim.get_current_frame()
                # Simply update the current frame image
    
    def draw(self):
        """Draw the sprite on screen (if the Actor is present)."""
        if self.actor:
            self.actor.draw()


class Player(Character):
    """Player entity: handles input, health and invulnerability."""

    def __init__(self, x, y):
        """Create the player with default animations and hitbox."""
        # Player sprite pre-scaled to 32x32, hitbox 22 px
        super().__init__(x, y, speed=150, hitbox_size=22)
        self.health = 3
        self.max_health = 3
        self.invulnerable_timer = 0

        # Setup player animations with new character_beige sprites
        self.setup_animations(
            idle_frames=["characters/character_beige_idle", "characters/character_beige_idle"],
            move_frames=["characters/character_beige_walk_a", "characters/character_beige_walk_b"]
        )
    
    def handle_input(self):
        """Read keyboard (WASD/Arrows) and set movement direction."""
        self.dx = 0
        self.dy = 0
        
        if keyboard.left or keyboard.a:
            self.dx = -1
        if keyboard.right or keyboard.d:
            self.dx = 1
        if keyboard.up or keyboard.w:
            self.dy = -1
        if keyboard.down or keyboard.s:
            self.dy = 1
    
    def take_damage(self, amount=1):
        """Apply damage when not invulnerable; play SFX and trigger game over if needed."""
        if self.invulnerable_timer <= 0:
            self.health -= amount
            self.invulnerable_timer = 1.5  # 1.5 seconds of invulnerability
            
            if sound_enabled:
                sounds.hit.play()
            
            if self.health <= 0:
                game_over()
    
    def update(self, dt):
        """Update invulnerability timer, movement and animation."""
        # Update invulnerability timer
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt
        
        self.handle_input()
        self.move(dt)
        self.update_animation(dt)


class Enemy(Character):
    """Base enemy class: each subclass implements `think` (AI)."""

    def __init__(self, x, y, speed):
        """Initialize a generic enemy with speed and hitbox."""
        # Enemy sprite pre-scaled to 32x32, hitbox 20 px
        super().__init__(x, y, speed, hitbox_size=20)
        self.behavior_timer = 0
    
    def think(self, player_pos, dt):
        """Decide enemy dx/dy based on player position (override)."""
        pass
    
    def update(self, dt, player_pos):
        """Update AI, movement and animation."""
        self.think(player_pos, dt)
        self.move(dt)
        self.update_animation(dt)


class SlimeNormal(Enemy):
    """Green slime: wanders randomly, chases when close."""

    def __init__(self, x, y):
        super().__init__(x, y, speed=50)
        self.setup_animations(
            idle_frames=["enemies/slime_normal_rest", "enemies/slime_normal_rest"],
            move_frames=["enemies/slime_normal_walk_a", "enemies/slime_normal_walk_b"]
        )
        self.wander_direction()

    def wander_direction(self):
        """Pick a random direction to wander for a while."""
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (0.7, 0.7), (-0.7, 0.7)]
        direction = choice(directions)
        self.dx = direction[0]
        self.dy = direction[1]
        self.behavior_timer = 1.0 + random()

    def think(self, player_pos, dt):
        """Chase within 120 px, otherwise keep wandering."""
        self.behavior_timer -= dt

        # Calculate distance to player
        dist = hypot(player_pos[0] - self.x, player_pos[1] - self.y)

        if dist < 120:  # Chase radius
            # Chase player
            if dist > 0:
                self.dx = (player_pos[0] - self.x) / dist
                self.dy = (player_pos[1] - self.y) / dist
        elif self.behavior_timer <= 0:
            # Wander randomly
            self.wander_direction()


class SlimeFire(Enemy):
    """Fire slime: faster; actively hunts the player."""

    def __init__(self, x, y):
        super().__init__(x, y, speed=80)
        self.setup_animations(
            idle_frames=["enemies/slime_fire_rest", "enemies/slime_fire_rest"],
            move_frames=["enemies/slime_fire_walk_a", "enemies/slime_fire_walk_b"]
        )
        self.patrol_timer = 0

    def think(self, player_pos, dt):
        """Chase within 200 px, otherwise patrol with short intervals."""
        dist = hypot(player_pos[0] - self.x, player_pos[1] - self.y)

        if dist < 200:  # Detection radius
            # Direct pursuit
            if dist > 0:
                self.dx = (player_pos[0] - self.x) / dist
                self.dy = (player_pos[1] - self.y) / dist
        else:
            # Patrol behavior
            self.patrol_timer -= dt
            if self.patrol_timer <= 0:
                self.dx = choice([-1, 0, 1])
                self.dy = choice([-1, 0, 1])
                self.patrol_timer = 2.0


class SlimeBlock(Enemy):
    """Block slime: patrols between two points; attacks when nearby."""

    def __init__(self, x, y):
        super().__init__(x, y, speed=60)
        self.setup_animations(
            idle_frames=["enemies/slime_block_rest", "enemies/slime_block_rest"],
            move_frames=["enemies/slime_block_walk_a", "enemies/slime_block_walk_b"]
        )
        self.patrol_points = [(x - 80, y), (x + 80, y)]
        self.current_target = 0

    def think(self, player_pos, dt):
        """Chase if close to the player; otherwise follow patrol points."""
        dist_to_player = hypot(player_pos[0] - self.x, player_pos[1] - self.y)

        if dist_to_player < 100:  # Attack radius
            # Chase player
            if dist_to_player > 0:
                self.dx = (player_pos[0] - self.x) / dist_to_player
                self.dy = (player_pos[1] - self.y) / dist_to_player
        else:
            # Patrol between points
            target = self.patrol_points[self.current_target]
            dist_to_target = hypot(target[0] - self.x, target[1] - self.y)

            if dist_to_target < 10:  # Reached patrol point
                self.current_target = (self.current_target + 1) % len(self.patrol_points)
                target = self.patrol_points[self.current_target]

            # Move towards patrol point
            if dist_to_target > 0:
                self.dx = (target[0] - self.x) / dist_to_target
                self.dy = (target[1] - self.y) / dist_to_target


class SlimeSpike(Enemy):
    """Spike slime: alternates aggressive chase and erratic movement."""

    def __init__(self, x, y):
        super().__init__(x, y, speed=70)
        self.setup_animations(
            idle_frames=["enemies/slime_spike_rest", "enemies/slime_spike_rest"],
            move_frames=["enemies/slime_spike_walk_a", "enemies/slime_spike_walk_b"]
        )
        self.change_direction_timer = 0
        self.is_aggressive = False

    def think(self, player_pos, dt):
        """Aggressive if the player is within 150 px; otherwise moves unpredictably."""
        self.change_direction_timer -= dt
        dist = hypot(player_pos[0] - self.x, player_pos[1] - self.y)

        if dist < 150:  # Detection radius
            # Aggressive mode: chase player directly
            self.is_aggressive = True
            if dist > 0:
                self.dx = (player_pos[0] - self.x) / dist
                self.dy = (player_pos[1] - self.y) / dist
        else:
            # Erratic movement mode
            if self.change_direction_timer <= 0:
                # Change direction randomly every 0.5-1.5 seconds
                self.dx = choice([-1, -0.7, 0, 0.7, 1])
                self.dy = choice([-1, -0.7, 0, 0.7, 1])
                self.change_direction_timer = 0.5 + random()
                self.is_aggressive = False


class MenuButton:
    """Clickable button with label, rect and associated action."""
    
    def __init__(self, text, x, y, width, height, action):
        """Create a button centered at (x, y).

        - text: visible label
        - width/height: clickable rect size
        - action: string identifier for the action
        """
        self.text = text
        self.rect = Rect(x - width//2, y - height//2, width, height)
        self.action = action
        self.hovered = False
    
    def check_hover(self, mouse_pos):
        """Set hover state when the mouse is over the button."""
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def draw(self):
        """Draw the button and label, with a hover effect."""
        color = (100, 100, 120) if self.hovered else (60, 60, 80)
        screen.draw.filled_rect(self.rect, color)
        screen.draw.rect(self.rect, (200, 200, 220))
        screen.draw.text(
            self.text,
            center=self.rect.center,
            fontsize=24,
            color=(255, 255, 255)
        )


def generate_level(level_num):
    """Generate a dungeon level and place entities.

    Steps:
    1) Create border walls + some random internal walls
    2) Compute the list of free floor tiles
    3) Place player, key, door and enemies on free tiles only

    level_num: int (1..5) used to tune difficulty
    """
    global walls, floor_tiles, enemies, key_position, door_position, player, key_actor, door_actor
    
    walls.clear()
    floor_tiles.clear()
    enemies.clear()
    
    # 1) Create border walls (a rectangle around the play area)
    for x in range(GRID_WIDTH):
        walls.append(Rect(x * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
        walls.append(Rect(x * TILE_SIZE, (GRID_HEIGHT - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    for y in range(1, GRID_HEIGHT - 1):
        walls.append(Rect(0, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        walls.append(Rect((GRID_WIDTH - 1) * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    # Difficulty tuning per level (kid-friendly, explicit numbers)
    walls_by_level = {1: 7, 2: 9, 3: 12, 4: 15, 5: 18}
    enemy_count_by_level = {1: 3, 2: 4, 3: 6, 4: 7, 5: 9}

    internal_walls = walls_by_level.get(level_num, 18)
    enemy_count = enemy_count_by_level.get(level_num, 9)

    # Add some random internal walls
    for _ in range(internal_walls):
        x = randint(2, GRID_WIDTH - 3)
        y = randint(2, GRID_HEIGHT - 3)
        walls.append(Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    # 2) Create floor tiles (all non-wall cells in the grid)
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            tile_rect = Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            is_wall = any(wall.colliderect(tile_rect) for wall in walls)
            if not is_wall:
                floor_tiles.append((x * TILE_SIZE, y * TILE_SIZE))
    
    # Helper: choose always-free tiles and use their centers for spawns
    free_tiles = set(floor_tiles)
    TILE_HALF = TILE_SIZE // 2

    def tile_center(tile_pos):
        tx, ty = tile_pos
        return (tx + TILE_HALF, ty + TILE_HALF)

    def distance(a, b):
        return hypot(a[0] - b[0], a[1] - b[1])

    def take_free_tile(min_dist_px=0, from_pos=None):
        # Try to pick a tile far enough from from_pos (if provided)
        if not free_tiles:
            # Safety: if nothing free (shouldn't happen), fall back to center
            return (WIDTH // 2, (HEIGHT - HUD_HEIGHT) // 2)
        candidates = list(free_tiles)
        # Shuffle-by-choice: sample up to len(candidates) tries
        for _ in range(len(candidates)):
            t = choice(candidates)
            c = tile_center(t)
            if from_pos is None or distance(c, from_pos) >= min_dist_px:
                free_tiles.discard(t)
                return c
        # If no candidate met the distance, just take any
        t = candidates[0]
        free_tiles.discard(t)
        return tile_center(t)

    # 3) Place player on a guaranteed free tile (no health reset here)
    player_pos = take_free_tile()
    if player is None:
        player = Player(player_pos[0], player_pos[1])
    else:
        player.x, player.y = player_pos
        player.dx, player.dy = 0, 0
        player.state = "idle"
        player.invulnerable_timer = 0
        player.hitbox.center = (player.x, player.y)
        if player.actor:
            player.actor.pos = (player.x, player.y)
    
    # Place key far from player (at least 6 tiles away)
    key_position = take_free_tile(min_dist_px=6 * TILE_SIZE, from_pos=(player.x, player.y))
    # Create key actor (pre-scaled to 32x32)
    key_actor = Actor("key_yellow", key_position)

    # Keep door position stable-ish: pick a free tile near the right side
    # Try to pick a tile roughly to the right-center area
    preferred = sorted(list(free_tiles), key=lambda t: (-t[0], abs((t[1]+TILE_HALF) - HEIGHT//2)))
    door_tile = preferred[0] if preferred else None
    if door_tile:
        free_tiles.discard(door_tile)
        door_position = tile_center(door_tile)
    else:
        door_position = (WIDTH - 100, HEIGHT // 2)
    # Create door actor (already 40x40 = 1 tile)
    door_actor = Actor("door_closed", door_position)
    
    # Spawn enemies based on level on guaranteed free tiles
    for i in range(enemy_count):
        ex, ey = take_free_tile(min_dist_px=2 * TILE_SIZE, from_pos=(player.x, player.y))
        enemy_type = choose_enemy_type(level_num)
        if enemy_type == 0:
            enemies.append(SlimeNormal(ex, ey))
        elif enemy_type == 1:
            enemies.append(SlimeFire(ex, ey))
        elif enemy_type == 2:
            enemies.append(SlimeBlock(ex, ey))
        else:
            enemies.append(SlimeSpike(ex, ey))


def choose_enemy_type(level_num):
    """Return 0=SlimeNormal, 1=SlimeFire, 2=SlimeBlock, 3=SlimeSpike with level-based weights.

    The weighting ramps up difficulty at higher levels by introducing
    more aggressive slime types.
    """
    r = random()
    if level_num <= 1:
        return 0  # only SlimeNormal
    elif level_num == 2:
        # 70% SlimeNormal, 30% SlimeFire
        return 0 if r < 0.7 else 1
    elif level_num == 3:
        # 40% SlimeNormal, 35% SlimeFire, 25% SlimeBlock
        return 0 if r < 0.4 else (1 if r < 0.75 else 2)
    elif level_num == 4:
        # 25% SlimeNormal, 35% SlimeFire, 25% SlimeBlock, 15% SlimeSpike
        if r < 0.25:
            return 0
        elif r < 0.60:
            return 1
        elif r < 0.85:
            return 2
        else:
            return 3
    else:
        # Level 5+: 15% SlimeNormal, 30% SlimeFire, 30% SlimeBlock, 25% SlimeSpike
        if r < 0.15:
            return 0
        elif r < 0.45:
            return 1
        elif r < 0.75:
            return 2
        else:
            return 3


def create_menu():
    """Create the main menu buttons (labels are in Italian by choice)."""
    global menu_buttons
    menu_buttons = [
        MenuButton("Avvia Partita", WIDTH//2, 250, 200, 50, "start"),
        MenuButton("Musica ON/OFF", WIDTH//2, 320, 200, 50, "toggle_music"),
        MenuButton("Suoni ON/OFF", WIDTH//2, 390, 200, 50, "toggle_sound"),
        MenuButton("Esci", WIDTH//2, 460, 200, 50, "exit")
    ]


def create_pause_menu():
    """Create the pause menu buttons (Resume, Exit)."""
    global pause_buttons
    panel_w, panel_h = 420, 200
    cx, cy = WIDTH // 2, HEIGHT // 2
    by = cy - 20
    pause_buttons = [
        MenuButton("Riprendi Partita", cx, by, 260, 50, "resume"),
        MenuButton("Esci", cx, by + 70, 260, 50, "quit_to_menu"),
    ]


def pause_game():
    """Enter pause state and show the pause menu."""
    global game_state
    game_state = STATE_PAUSED
    create_pause_menu()


def resume_game():
    """Resume the game from pause."""
    global game_state
    game_state = STATE_PLAYING


def quit_to_menu():
    """Exit the current run and return to the main menu."""
    global game_state
    game_state = STATE_MENU
    create_menu()
    stop_background_music()


def start_game():
    """Start a new game.

    - Reset level, player, per-level timers
    - Start music/SFX if enabled
    """
    global game_state, current_level, key_collected, player, level_time_accum, level_times
    game_state = STATE_PLAYING
    current_level = 1
    key_collected = False
    player = None  # reset player so health returns to max for a new game
    level_times = []
    level_time_accum = 0.0
    generate_level(current_level)
    
    if music_enabled:
        start_background_music()
    
    if sound_enabled:
        sounds.start.play()


def toggle_music():
    """Toggle background music only (looping track)."""
    global music_enabled
    music_enabled = not music_enabled
    if music_enabled:
        start_background_music()
    else:
        stop_background_music()
    if sound_enabled:
        sounds.toggle.play()


def toggle_sound():
    """Toggle sound effects only (hit, pickup, etc.)."""
    global sound_enabled
    sound_enabled = not sound_enabled
    if sound_enabled:
        sounds.toggle.play()


def game_over():
    """Handle game over: save time, stop music and play SFX."""
    global game_state, level_time_accum, level_times
    # Save current level time at the moment of defeat
    level_times.append(level_time_accum)
    level_time_accum = 0.0
    game_state = STATE_GAME_OVER
    stop_background_music()
    if sound_enabled:
        sounds.gameover.play()


def victory():
    """Handle victory: show screen and play victory SFX."""
    global game_state
    game_state = STATE_VICTORY
    if sound_enabled:
        sounds.victory.play()


def next_level():
    """Advance to the next level, saving the time of the level just finished."""
    global current_level, key_collected, level_time_accum, level_times
    # Save completed level time
    level_times.append(level_time_accum)
    level_time_accum = 0.0
    current_level += 1
    key_collected = False
    
    if current_level > 5:  # Win after 5 levels
        victory()
    else:
        generate_level(current_level)
        if sound_enabled:
            sounds.nextlevel.play()


def update(dt):
    """Update game logic for the current state.

    Parameters:
    - dt: delta time in seconds since the last frame
    """
    global key_collected, level_time_accum
    
    if game_state == STATE_MENU:
        # Hover is handled by on_mouse_move(pos); nothing to update here
        return
    
    elif game_state == STATE_PLAYING:
        # Accumulate current level time
        level_time_accum += dt
        # Update player
        player.update(dt)
        
        # Update enemies
        for enemy in enemies:
            enemy.update(dt, (player.x, player.y))
            
            # Check collision with player
            if enemy.hitbox.colliderect(player.hitbox):
                player.take_damage()
        
        # Check key collection (sprite 32x32, area pickup 24x24 centrata)
        if not key_collected and key_position:
            key_pickup_size = 24
            half = key_pickup_size // 2
            key_rect = Rect(key_position[0] - half, key_position[1] - half, key_pickup_size, key_pickup_size)
            if player.hitbox.colliderect(key_rect):
                key_collected = True
                if sound_enabled:
                    sounds.pickup.play()
                # Update door image when key is collected
                if door_actor:
                    door_actor.image = "door_open"

        # Check door interaction (hitbox 40x40 = 1 tile)
        if key_collected and door_position:
            door_rect = Rect(door_position[0] - 20, door_position[1] - 20, 40, 40)
            if player.hitbox.colliderect(door_rect):
                next_level()


def draw():
    """Render the appropriate scene based on the current game state."""
    screen.clear()
    
    if game_state == STATE_MENU:
        draw_menu()
    elif game_state == STATE_PLAYING:
        draw_game()
    elif game_state == STATE_GAME_OVER:
        draw_game_over()
    elif game_state == STATE_VICTORY:
        draw_victory()
    elif game_state == STATE_PAUSED:
        # Draw game behind and overlay pause menu
        draw_game()
        draw_pause()


def draw_menu():
    """Main menu screen: title, audio status and clickable buttons."""
    screen.fill((20, 20, 30))

    # Title (keep in English)
    screen.draw.text(
        "DUNGEON ESCAPE",
        center=(WIDTH//2, 100),
        fontsize=48,
        color=(255, 255, 255)
    )

    # Audio status (Italian with ON/OFF)
    audio_status = (
        f"Musica: {'ON' if music_enabled else 'OFF'} | "
        f"Suoni: {'ON' if sound_enabled else 'OFF'}"
    )
    screen.draw.text(
        audio_status,
        center=(WIDTH//2, 150),
        fontsize=20,
        color=(200, 200, 200)
    )
    
    # Draw buttons
    for button in menu_buttons:
        button.draw()


def draw_game():
    """Draw the game world (tiles, entities) and the HUD."""
    screen.fill((30, 25, 35))
    
    # Draw floor tiles
    for x, y in floor_tiles:
        screen.blit("floor", (x, y))
    
    # Draw walls
    for wall in walls:
        screen.blit("wall", (wall.x, wall.y))
    
    # Draw key if not collected (using scaled actor)
    if not key_collected and key_actor:
        key_actor.draw()

    # Draw door (using scaled actor)
    if door_actor:
        door_actor.draw()
    
    # Draw enemies
    for enemy in enemies:
        enemy.draw()
    
    # Draw player (with invulnerability flashing)
    if player.invulnerable_timer <= 0 or int(player.invulnerable_timer * 10) % 2 == 0:
        player.draw()
    
    # Draw HUD
    draw_hud()


def draw_pause():
    """Draw the pause overlay panel with buttons."""
    # Central panel
    panel_w, panel_h = 460, 220
    cx, cy = WIDTH // 2, HEIGHT // 2
    panel_rect = Rect(cx - panel_w//2, cy - panel_h//2, panel_w, panel_h)
    screen.draw.filled_rect(panel_rect, (20, 20, 25))
    screen.draw.rect(panel_rect, (200, 200, 220))

    # Pause title
    screen.draw.text(
        "PAUSA",
        center=(cx, cy - panel_h//2 + 30),
        fontsize=40,
        color=(255, 255, 255)
    )

    # Buttons
    for button in pause_buttons:
        button.draw()


def draw_hud():
    """Draw the bottom HUD: hearts, key icon and level label."""
    # HUD background
    screen.draw.filled_rect(
        Rect(0, HEIGHT - HUD_HEIGHT, WIDTH, HUD_HEIGHT),
        (40, 40, 50)
    )
    
    # Draw health hearts
    y_center = HEIGHT - HUD_HEIGHT + (HUD_HEIGHT - HUD_ICON_PX) // 2
    for i in range(player.max_health):
        x = 20 + i * 35
        y = y_center
        if i < player.health:
            screen.blit("hud_heart", (x, y))
        else:
            screen.blit("hud_heart_empty", (x, y))

    # Draw key indicator in HUD (sprite 32x32 already scaled)
    if key_collected:
        screen.blit("key_yellow", (WIDTH - 100, y_center))

    # Level number (Italian)
    screen.draw.text(
        f"Livello {current_level}",
        center=(WIDTH//2, HEIGHT - HUD_HEIGHT//2),
        fontsize=24,
        color=(255, 255, 255)
    )


def draw_game_over():
    """Game over screen: level reached and total time of the run."""
    screen.fill((40, 20, 20))
    
    screen.draw.text(
        "FINE PARTITA",
        center=(WIDTH//2, HEIGHT//2 - 50),
        fontsize=64,
        color=(255, 100, 100)
    )
    
    screen.draw.text(
        f"Hai raggiunto il livello {current_level}",
        center=(WIDTH//2, HEIGHT//2 + 20),
        fontsize=32,
        color=(200, 200, 200)
    )
    # Total game time
    total_seconds = sum(level_times)
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    screen.draw.text(
        f"Tempo totale: {minutes:02d}:{seconds:05.2f}",
        center=(WIDTH//2, HEIGHT//2 + 60),
        fontsize=28,
        color=(220, 220, 220)
    )
    
    screen.draw.text(
        "Premi SPAZIO per tornare al menu",
        center=(WIDTH//2, HEIGHT//2 + 80),
        fontsize=24,
        color=(180, 180, 180)
    )


def draw_victory():
    """Victory screen with total time of the run."""
    screen.fill((20, 40, 20))
    
    screen.draw.text(
        "VITTORIA!",
        center=(WIDTH//2, HEIGHT//2 - 50),
        fontsize=64,
        color=(100, 255, 100)
    )
    
    screen.draw.text(
        "Sei scappato dal dungeon!",
        center=(WIDTH//2, HEIGHT//2 + 20),
        fontsize=32,
        color=(200, 200, 200)
    )
    # Total game time
    total_seconds = sum(level_times)
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    screen.draw.text(
        f"Tempo totale: {minutes:02d}:{seconds:05.2f}",
        center=(WIDTH//2, HEIGHT//2 + 60),
        fontsize=28,
        color=(220, 220, 220)
    )
    
    screen.draw.text(
        "Premi SPAZIO per tornare al menu",
        center=(WIDTH//2, HEIGHT//2 + 80),
        fontsize=24,
        color=(180, 180, 180)
    )


def on_mouse_down(pos, button):
    """Handle mouse clicks in the main menu and pause menu."""
    if game_state == STATE_MENU:
        for menu_button in menu_buttons:
            if menu_button.rect.collidepoint(pos):
                if menu_button.action == "start":
                    start_game()
                elif menu_button.action == "toggle_music":
                    toggle_music()
                elif menu_button.action == "toggle_sound":
                    toggle_sound()
                elif menu_button.action == "exit":
                    exit()
    elif game_state == STATE_PAUSED:
        for menu_button in pause_buttons:
            if menu_button.rect.collidepoint(pos):
                if menu_button.action == "resume":
                    resume_game()
                elif menu_button.action == "quit_to_menu":
                    quit_to_menu()


def on_key_down(key):
    """Handle special keys: SPACE (end screens), ESC/P (pause)."""
    global game_state
    
    if key == keys.SPACE:
        if game_state in [STATE_GAME_OVER, STATE_VICTORY]:
            game_state = STATE_MENU
            create_menu()
            stop_background_music()
    # ESC or P to pause/resume during gameplay
    if key in (keys.ESCAPE, keys.P):
        if game_state == STATE_PLAYING:
            pause_game()
        elif game_state == STATE_PAUSED:
            resume_game()


# Initialize the game
create_menu()
def start_background_music():
    """Start the looping background music (if available)."""
    try:
        sounds.background.play(-1)
    except Exception:
        pass


def stop_background_music():
    """Stop the background music, ignoring any errors."""
    try:
        sounds.background.stop()
    except Exception:
        pass

def on_mouse_move(pos):
    """Update the hover effect for buttons in the menu and pause screens."""
    if game_state == STATE_MENU:
        for button in menu_buttons:
            button.check_hover(pos)
    elif game_state == STATE_PAUSED:
        for button in pause_buttons:
            button.check_hover(pos)

# Run info: in some macOS/Conda environments, direct startup
# with `python main.py` may not open the window.
# Use one of the following official PgZero commands instead.
if __name__ == '__main__':
    print("Per avviare il gioco usa:")
    print("  python -m pgzero main.py")
    print("  oppure")
    print("  pgzrun main.py")
