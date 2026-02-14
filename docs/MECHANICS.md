# Game Mechanics Documentation

Dark Floor is a terminal-based roguelike game. This document details all game mechanics.

## Table of Contents

1. [Player System](#player-system)
2. [Dungeon Generation](#dungeon-generation)
3. [Entities](#entities)
4. [Items & Inventory](#items--inventory)
5. [Visibility & Lighting](#visibility--lighting)
6. [Sound System](#sound-system)
7. [Fog of War](#fog-of-war)
8. [Status Effects](#status-effects)
9. [Game Loop](#game-loop)
10. [World Seed](#world-seed)

---

## Player System

### Health (HP)
- **Starting HP:** 500
- **Decrement:** -1 per movement action
- **Game Over:** Player dies when HP reaches 0 and death screen is shown
- **Death Message:** Customizable when HP <= 0

### Sanity (SAN)
- **Starting Sanity:** 100%
- **Decrement Rate:** -0.01 per game tick
- **Fog Penalty:** -0.02 sanity when standing in fog
- **Restoration:** Items can restore sanity
- **Status:** Affects player color when damaged
- **Game Over:** Player dies when SAN reaches 0 and death screen is shown

### Color System
- **Default Color:** 8 (white)
- **Changes:** Player color changes based on damage state

### Death Cause
- Tracked via `self.death_cause` attribute
- Default: "You don't remember how it happened."

---

## Dungeon Generation

### Algorithm
- **Method:** BSP (Binary Space Partition) room generation
- **Grid Size:** 50x20 (W x H)
- **Room Generation:** Attempts 1200 iterations to place rooms
- **Room Size:** 4-7 width, 3-6 height
- **Connection:** Rooms connected via L-shaped corridors

### Room Placement
- Minimum spacing to prevent overlap
- Prioritizes rooms without adjacency to existing rooms

### Features
- **Exit:** Marked as 'E', teleports to next floor
- **Entities:** 3 + (20 - floor) ÷ 3 enemies spawn in various rooms
- **Items:** 3-8 items placed randomly on walkable tiles
- **Floor Progression:** Each floor is procedurally unique

---

## Entities

### Chaser (X)
- **Color:** 6 (Red)
- **Behavior:** Actively chases player when visible
- **Range:** 10 tiles (Manhattan distance)
- **Cooldown:** max(1, current_floor ÷ 5)
- **Speed:** Moves every cooldown turn
- **Sounds:** Emits "A heavy thud" on movement
- **Visual:** Flashes between 'X' and '?' every ~0.08 seconds
- **Threat:** Instant death on contact

### Stalker (S)
- **Color:** 5 (Magenta)
- **Behavior:** Hunts intelligently, drains sanity
- **Vision:** Uses light-based visibility system
- **Movement:** 30% speed in darkness, chases visible player
- **Sanity Drain:** -0.2 sanity per tick when visible to player
- **Threat:** -5 HP on contact

### Ambusher (#)
- **Color:** 1 (Blue) when inactive, 9 (Yellow) when triggered
- **Trigger Range:** 2 tiles
- **Trigger Visual:** Changes from '#' to 'A' when triggered
- **Sound:** Emits "Got you" on trigger
- **Activation:** Flashes color when active
- **Movement:** Pursues player with 1-turn cooldown
- **Threat:** Instant death on contact

---

## Items & Inventory

### Inventory System
- **Capacity:** 5 items max
- **Slot Selection:** Number keys (1-5)
- **Usage:** Press 'E' to use/toggle selected item

### Item Types

#### Water Bottles (+)
- **Name:** H2O
- **Color:** 7 (White)
- **Effect:** Restore 50 HP
- **Max Stack:** 1
- **Single Use:** Yes (consumed on use)

#### Rainbow Water (*)
- **Name:** H2O
- **Color:** Cycles through 7, 9, 10, 3, 5 (animated)
- **Effect:** Restore 100 HP + 10 SAN
- **Max Stack:** 1
- **Single Use:** Yes (consumed on use)
- **Rarity:** Rare, provides superior healing

#### Vitality Potions (v)
- **Name:** VIT
- **Color:** 9 (Yellow)
- **Effect:** Restore 5 SAN
- **Max Stack:** 1
- **Single Use:** Yes (consumed on use)

#### Bombs (B)
- **Name:** BOM
- **Color:** 11 (Cyan)
- **Effect:** 3x3 explosion around player
  - Destroys walls in explosion radius
  - Kills all entities in explosion radius
  - Creates 5-tile light burst
- **Max Stack:** 1
- **Single Use:** Yes (consumed on use)

#### Flashlight (F)
- **Name:** LIT
- **Color:** 10 (Green)
- **Max Stack:** 800 (charges)
- **Effect:** Toggleable 90° cone light, 7 tiles
- **Consumption:** 1 charge per tick when active
- **Light Type:** Directional based on facing

#### Lantern (L)
- **Name:** LAN
- **Color:** 10 (Green)
- **Max Stack:** 500 (charges)
- **Effect:** Toggleable 360° omnidirectional light, 4 tiles
- **Consumption:** 1 charge per tick when active
- **Light Type:** Full circle illumination

---

## Visibility & Lighting

### Base Visibility Rules
- Player always sees their current tile
- DEBUG mode shows entire map
- Light sources determine vision range

### Light Source Properties
Each light has:
- **Position (p):** Center of light source
- **Angle (a):** 360 = omnidirectional, <360 = cone
- **Direction (d):** (dx, dy) for directional lights
- **Radius (r):** Distance in tiles

### Visibility Calculation
```
Distance = hypot(x_diff, y_diff)
Within Range: distance < radius
Direction Check: 
  - For omnidirectional: always true
  - For directional: dot product > cos(angle/2)
```

### Light Interaction
- Multiple light sources stack
- Directional lights follow player facing
- Bombs create temporary omnidirectional flashes

---

## Sound System

### Sound Emission
Emitted by entities during actions:
- **Parameters:** Position (sx, sy), message, intensity (range)
- **Direction Calculation:** Based on player position relative to source
- **Distance Bands:**
  - < 3 tiles: "DEAFENING"
  - < intensity/2: "Clear"
  - < intensity: "Faint"

### Sound Output Format
`[Volume] Message to the Direction`

**Directions:** North, South, East, West (based on relative position)

### Sound Persistence
- Each unique sound displays for 1.5 seconds
- Duplicate sounds reset timer instead of duplicate
- Displayed on bottom of HUD

---

## Fog of War

### Fog Generation
- **Initial Fog:** Spawns in random tiles (set in gen())
- **Growth Rate:** 15% chance per fog tile per tick
- **Spread:** 1 tile in any direction (8-directional)
- **Shrinking:** Removes 10% of fog tiles when exceeding 20

### Fog Mechanics
- **Visual:** Displayed as '?' characters
- **Sanity Penalty:** -0.02 SAN when standing in fog
- **Visibility:** Blocks normal vision (requires light)
- **Dynamic:** Constantly evolves during gameplay

---

## Status Effects

### Effect System Architecture
- Entities have `effects` list
- Each effect implements `tick(entity, ctx)` and `expired()`
- Effects automatically removed when expired

### Current Effects
*No effects fully implemented in v0.1.0*

### Planned Effects
- Poison: Gradual HP damage over time
- Slow: Reduced movement speed
- Blind: Limited visibility
- Cursed: Stat debuffs

---

## Death Screen

When the player dies (HP ≤ 0 or SAN ≤ 0), the game enters a death screen state.

### Display
- Title message: `YOU ARE STILL HERE`
- Cause of death
- World seed of the run
- Flavor text

### Controls
- **R** → Restart game with a new run
- **Q / ESC** → Quit game

The game is fully paused while on this screen.

---

## Game Loop

The game runs in a single-session loop and returns control on death.
The launcher is responsible for restarting or exiting.

### Restart Flow

1. Player dies  
2. Death screen is shown  
3. Player presses:
   - `R` → Game state resets and a new run starts  
   - `Q` → Program exits cleanly  

No process restart is required.

### Frame Rate
- **Target FPS:** 10 frames per second
- **Frame Time:** ~100ms per frame

### Input Handling
- **Movement:** W/A/S/D keys
- **Facing:** Updated with movement direction
- **Item Selection:** 1-5 number keys
- **Item Usage:** E key

### Update Order
1. Movement (if valid, collect items/change floors)
2. Player stat updates (sanity decay, HP decay)
3. Effect system updates
4. Fog evolution
5. Sound system updates
6. Item system (equipment drain, effect ticks)
7. Entity updates (AI, movement, attacks)
8. Dead entity removal

### Rendering
- Clear screen
- Iterate all tiles
- Check visibility
- Render entities, items, or terrain
- Render HUD:
  - Inventory display
  - Floor, HP, SAN stats
  - Active sound messages
- Refresh and frame rate cap

### Example HUD Layout
```
Line H:   [1:LIT*] [2:H2O] [3:VIT] ...
Line H+1: FL:20 HP:450 SAN:98%
Line H+3: [Clear] A heavy thud to the East
```

---

## Game Constants

| Constant | Value | Purpose |
|----------|-------|---------|
| W | 50 | Grid width |
| H | 20 | Grid height |
| FPS | 10 | Target frames per second |
| DEBUG | False | Show entire map |
| MAX_INVENTORY | 5 | Inventory slots |

---

## Progression System

- **Starting Floor:** 20
- **Floor Decrement:** -1 when reaching exit (E)
- **Difficulty Scaling:** More enemies on lower floors
- **Enemy Count Formula:** 3 + (20 - floor) ÷ 3
- **Goal:** Reach floor 0 to escape the dungeon

---

## World Seed

### Seed System
- The game uses a single global **world seed** to initialize all procedural systems.
- The seed is generated at startup or provided manually.
- The same seed always produces the same dungeon layouts, entity placement, and item distribution.

### Usage
- Seed is displayed on game startup and in the HUD.
- Seed is printed to terminal for debugging and sharing runs.
- Seed is also displayed on the death screen.
- Restart generates a new derived seed.

### Determinism
- All RNG-dependent systems derive from the seed:
  - Dungeon generation
  - Entity spawning
  - Fog initial state
  - Item placement

This allows full reproducibility of runs for:
- Bug reports
- Testing
- Speedrunning
- Daily challenges (future)
