# How to Play Dark Floor

## Starting the Game

```bash
python main.py
```

## Controls

### Movement
| Key | Action |
|-----|--------|
| **W** | Move Up |
| **S** | Move Down |
| **A** | Move Left |
| **D** | Move Right |

**Note:** Movement direction also determines your facing direction for directional light sources (like flashlights).

### Interaction
| Key | Action |
|-----|--------|
| **1-5** | Select inventory slot |
| **E** | Use/toggle selected item |

## HUD Explanation

### Inventory Bar (Top)
```
[1:LIT*] [2:H2O] [3:VIT] ...
```
- Number + Colon = Slot number
- Name = Item name
- Asterisk (*) = Item is currently active/toggled on
- Selected item is highlighted

### Stats Bar
```
FL:20 HP:450 SAN:98.5%
```
- **FL:** Current floor (20 = start, 0 = escape)
- **HP:** Health points (0 = death)
- **SAN:** Sanity percentage (decreases constantly)

### Sound Messages
```
[Faint] A heavy thud to the East
```
Sound events display at bottom, with:
- **Volume:** DEAFENING (close), Clear (medium), Faint (far)
- **Direction:** North, South, East, West (relative to player)

## Symbols

| Symbol | Meaning |
|--------|---------|
| @      | You (player) |
| #      | Wall |
| .      | Floor (walkable) |
| E      | Exit (go to next floor) |
| ?      | Fog (obscured area) |
| X      | Chaser (red enemy) |
| S      | Stalker (magenta enemy) |
| #/A    | Ambusher (blue/yellow enemy) |
| +      | Water bottle |
| *      | Rainbow water |
| v      | Vitality potion |
| B      | Bomb |
| F      | Flashlight |
| L      | Lantern |

## Objective

**Escape the dungeon!**

1. Navigate from **Floor 20** down to **Floor 0**
2. Find the exit (**E**) on each floor
3. Manage your **HP** and **SAN** (sanity)
4. Collect items to aid survival
5. Avoid or evade enemies

## Survival Tips

### Health Management
- **Water (+):** Restore 100 HP
- **Rainbow Water (*):** Restore 250 HP + 40 SAN (rare)
- **Movement cost:** 1 HP per step
- Critical: Keep HP above 0!

### Sanity Management
- **Vitality (v):** Restore 10 SAN
- **Constant drain:** -0.01 SAN per tick
- **Fog penalty:** -0.2 SAN when standing in fog
- **Stalker drain:** -1 SAN per tick when visible
- Sanity loss = increased danger

### Lighting
- **Flashlight (F):** 90° cone, 7 tiles, 800 charges
  - Uses 1 charge per tick when active
  - Directional based on your facing
- **Lantern (L):** 360° circle, 4 tiles, 500 charges
  - Uses 1 charge per tick when active
  - Full illumination around you
- **Strategy:** Use lights to see threats, toggle off to conserve

### Combat Strategy
- **Avoid:** Better than fight (no offensive abilities)
- **Items:** Bombs are your only offensive tool
- **Bomb (B):** 3x3 explosion, kills enemies and destroys walls
- **Escape:** Use bombs to clear paths or eliminate threats

### Enemy Danger Levels

**Chaser (X)** - Medium threat
- Chases directly when nearby
- Loud (alerts to sounds)
- Predictable pattern

**Stalker (S)** - High threat
- Hunts intelligently
- Drains sanity just by seeing you
- Dangerous in light

**Ambusher (#)** - Extreme threat
- Hides in darkness
- Instant kill on contact
- Transforms when triggered
- Use light to detect

## Game Over

The game ends when:
- Your **HP** reaches 0 (enemy contact, starvation)
- You willingly quit with Ctrl+C

## Advanced Tips

1. **Sound Strategy:** Listen for enemy sounds to gauge distance and direction
2. **Fog Zones:** Avoid fog when possible to preserve sanity
3. **Resource Management:** Plan when to use limited charges on flashlights/lanterns
4. **Inventory Limits:** You can only carry 5 items - plan pickups
5. **Floor Difficulty:** Lower floors have more enemies - prepare carefully
