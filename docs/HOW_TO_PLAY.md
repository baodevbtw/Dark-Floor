# How to Play Dark Floor

## Starting the Game

```bash
python main.py
```

You can restart endlessly without closing the program.

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

If you can hear it, it’s still far away.  
If you can’t, it’s already here.

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

**Escape the dungeon.**  
*(Death is not the end. It just loops.)*  
*(There is no evidence the **End** exists.)*

1. Keep going down. Stopping is not an option.
2. Trust the exit (**E**), if you want.
3. Watch your **HP** and **SAN**. They are the only proof you still exist.
4. Hoard anything that makes it hurt less.
5. Run from everything else. It knows where you are.

The game does not want you to win.  
It wants you to **continue**.

## Survival Tips

### Health Management
- **Water (+):** Restore 100 HP  
- **Rainbow Water (*):** Restore 200 HP + 10 SAN  
- **Movement cost:** 1 HP per step  
- Critical: Keep HP above 0!

Every step is a decision.  
Standing still keeps you alive.  
Standing still lets *them* get closer.

---

### Sanity Management
- **Vitality (v):** Restore 10 SAN  
- **Constant drain:** -0.01 SAN per tick  
- **Fog penalty:** -0.2 SAN when standing in fog  
- **Stalker drain:** -1 SAN per tick when visible  
- Sanity loss = increased danger

Low sanity causes:
- Shorter vision  
- Fake sounds  
- Faster fog growth  
- More frequent encounters  

At 0 SAN, the game stops pretending to be fair.

The UI still works.  
The rules still apply.  
Only **you** stop understanding them.

---

### Lighting
- **Flashlight (F):** 90° cone, 7 tiles, 800 charges  
  - Uses 1 charge per tick when active  
  - Directional based on your facing  
- **Lantern (L):** 360° circle, 4 tiles, 500 charges  
  - Uses 1 charge per tick when active  
  - Full illumination around you  

Light reveals the dungeon.  
It also reveals **you**.

Nothing in the dark was lost.  
It was only waiting to be noticed.

---

### Combat Strategy
- **Avoid:** Better than fight (no offensive abilities)  
- **Items:** Bombs are your only offensive tool  
- **Bomb (B):** 3x3 explosion, kills enemies and destroys walls  
- **Escape:** Use bombs to clear paths or eliminate threats  

Bombs solve problems.  
They also create new ones.

---

### Enemy Danger Levels

**Chaser (X)** - Medium threat  
- Chases directly when nearby  
- Loud (alerts to sounds)  
- Predictable pattern  

It wants you dead.  
It doesn’t know why.  
It doesn’t need to.

**Stalker (S)** - High threat  
- Hunts intelligently  
- Drains sanity just by seeing you  
- Dangerous in light  

If you see it, it already knows where you are.  
If you don’t, it’s closer.

**Ambusher (#)** - Extreme threat  
- Hides in darkness  
- Instant kill on contact  
- Transforms when triggered  
- Use light to detect  
- If you see a wall blinking, it's already too late  

That wall was never a wall.  
It was a decision you made earlier.

---

## Game Over

When your **HP** or **SAN** reaches 0, the game does not immediately exit.

Instead, a **death screen** is shown.

### Death Screen
Displays:
- Title message: `YOU ARE STILL HERE`
- Cause of death
- World seed of the run
- A reminder that the world will not change without you

### Options
- **R** → Restart  
- **Q / ESC** → Quit  

Restarting does not fix what happened.  
It only proves that it can happen again.

Quitting does not end the game.  
It only ends your memory of it.

---

## Advanced Tips

1. **Sound Strategy:** Listen for enemy sounds to gauge distance and direction  
2. **Fog Zones:** Avoid fog when possible to preserve sanity  
3. **Resource Management:** Plan when to use limited charges on flashlights/lanterns  
4. **Inventory Limits:** You can only carry 5 items - plan pickups  
5. **Floor Difficulty:** Lower floors have more enemies - prepare carefully  

The deeper you go,  
the less the game explains,  
and the more it *expects you to already know*.

Which is strange,  
because you don’t remember learning any of this.