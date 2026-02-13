# Game Architecture

This document describes the codebase structure and design patterns.

## File Organization

```
Dark-Floor/
├── main.py              # Entry point, version, game runner
├── src/
│   └── darkfloor.py     # Complete game engine
├── docs/
│   ├── MECHANICS.md     # Game mechanics reference
│   ├── ARCHITECTURE.md  # This file
│   └── VERSIONING.md    # Version strategy
├── README.md            # Project overview
├── CONTRIBUTING.md      # Contribution guide
├── CHANGELOG.md         # Version history
└── requirements.txt     # Dependencies
```

## Core Classes

### Player
Represents the player character.

```python
class Player:
    hp: int              # Current health points (500 max)
    san: float           # Sanity percentage (100% max)
    effects: List        # Active status effects
    color: int           # Color pair index
    death_cause: str     # Message when dying
```

### Game (Context)
Central game state passed between systems.

```python
class Game:
    player: Player       # Player instance
    pos: Tuple[int, int] # Player position
    grid: List[List]     # 2D map
    entities: List       # Active enemies
    inv: List            # Inventory items
    face: Tuple[int, int]# Facing direction
    floor: int           # Current floor (20 → 0)
    fog: Set             # Fog of war tiles
    sounds: SoundSystem  # Sound manager
```

### Entity
Base class for enemies.

```python
class Entity:
    x, y: int           # Position
    char: str           # Display character
    color: int          # Color pair
    dead: bool          # Death flag
    effects: List       # Status effects
```

**Subclasses:**
- `Chaser`: Aggressive, direct pursuit
- `Stalker`: Intelligent hunter, sanity drain
- `Ambusher`: Camouflaged trap enemy

### Item
Base class for inventory items.

```python
class Item:
    char: str           # Display character
    name: str           # Item name
    color: int          # Color pair
    v: int              # Value (health/charges/stack)
    on: bool            # Active state
```

**Subclasses:**
- `Water`, `RainbowWater`: HP restore
- `Vit`: Sanity restore
- `Bomb`: Area damage
- `Flashlight`, `Lantern`: Lighting

### SoundSystem
Manages audio events.

```python
class SoundSystem:
    active_sounds: List  # Currently playing sounds
    
    emit(sx, sy, msg, intensity, ctx)  # Emit sound
    update()                          # Expire old sounds
```

## Core Systems

### Dungeon Generation (`gen(floor)`)
- BSP room placement algorithm
- Procedural connection via corridors
- Entity and item spawning
- Returns: `(grid, player_start, entities, fog)`

### Visibility System (`visible(ctx, x, y)`)
- Checks if tile is visible to player
- Light source calculations
- Cone vs omnidirectional lighting
- DEBUG mode bypass

### Fog System (`update_fog(ctx)`)
- Probabilistic fog growth
- Fog shrinking when dense
- Sanity penalty application
- Returns updated fog set

### Game Loop (`main(scr)`)
- Curses terminal initialization
- Color pair setup
- Input handling
- Update order: movement → effects → AI → rendering
- Frame rate limiting

## Design Patterns

### Context Pattern
Game state (ctx) passed to all systems for access to:
- Player, entities, grid, sounds, lights
- Decouples systems while sharing state

### Effect System
- `tick(entity, ctx)`: Update effect
- `expired()`: Check if should remove
- Automatic cleanup in update()

### Visibility Delegation
- Items have `get_v(ctx)` for dynamic rendering
- Entities can customize appearance
- Supports animation via time checks

### Item Stack Management
- `max_stack`: Charge capacity
- `v`: Current value
- Automatic removal when depleted

## Key Algorithms

### Manhattan Distance
Used by Chaser detection and pathfinding:
```
distance = |x1 - x2| + |y1 - y2|
```

### Euclidean Distance
Used in sound and light calculations:
```
distance = sqrt((x1-x2)² + (y1-y2)²)
```

### Directional Lighting
Cone check using dot product:
```
visible = dot(to_tile, facing) > cos(angle/2)
```

### Pathfinding
Simple greedy movement toward target:
```
- Move ±1 in x if target further
- Move ±1 in y if target further
- Check bounds and wall collision
```

## Technical Constraints

### Terminal-based
- Limited to curses API
- 50x20 character grid
- 16 color pairs
- ~10 FPS performance target

### Python Specifics
- No external dependencies (except windows-curses)
- Compact code style for quick iteration
- Single file (darkfloor.py) for portability

## Future Architecture Improvements

### Planned Refactoring
1. Separate game logic from rendering
2. Move to class-based entity system
3. Configuration file for constants
4. Save/load serialization

### Modding Support
- Item type registry (ITEM_TYPES dict)
- Entity factory pattern ready
- Configuration-driven content
