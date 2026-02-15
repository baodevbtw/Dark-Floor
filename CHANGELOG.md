# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0-alpha.4] - 2026-02-15

### Added
- In-game help menu (`H`) that pauses the game and displays `src/help.txt`.
- Death screen with restart (`R`) and quit (`Q`) options.
- Directional sound system with distance-based volume messages.

### Changed
- Sound messages are now deduplicated and refresh their lifetime instead of stacking.

---

## [0.1.0-alpha.3] - 2026-02-14

### Added
- Global world seed system for reproducible dungeon generation.
- Seed is displayed on game startup.
- Seed is logged in terminal for debugging and sharing runs.

### Changed
- Dungeon and RNG initialization now derive from a single seed value.

### Fixed
- Random state is no longer implicitly global; all procedural systems now share the same deterministic source.

---

## [0.1.0-alpha.2] - 2026-02-14

### Fixed
- Prevented crashes when dungeon generation produces no valid rooms.
- Bounded fog growth to avoid unbounded memory usage while preserving spread behavior.
- Fixed entity update loop to avoid list mutation during iteration.
- Vitamin item now correctly increases player SAN.

---

## [0.1.0-alpha.1] - 2026-02-14

### Added
- Centralized stat limits in `Player`:
  - `MAX_HP = 1000`
  - `MAX_SAN = 100`
- New Player API methods:
  - `clamp_stats()`
  - `change_hp(amount)`
  - `change_san(amount)`

### Changed
- All HP and SAN modifications now go through the Player API.
- Stat updates are clamped after every modification.

### Fixed
- Player HP can no longer drop below 0 from movement drain or enemy attacks.
- Player SAN can no longer drop below 0 from fog or Stalker effects.
- Player HP can no longer exceed the maximum from items (Water, Rainbow Water).

---

## [0.1.0-alpha] - 2026-02-13

### Added
- Initial project setup with GitHub repository
- Basic roguelike terminal game framework
- Player character with HP (500) and sanity (100%) system
- Fog of war mechanics with dynamic generation
- Sound system with directional audio cues
- Game entities (Chaser, Stalker, Ambusher) with unique behaviors
- Effect system framework for status effects
- Dungeon generation with BSP algorithm
- 6 item types: Water, Rainbow Water, Vitality, Bomb, Flashlight, Lantern
- Lighting system with directional and omnidirectional lights
- Comprehensive documentation:
  - MECHANICS.md: Complete game mechanics reference
  - ARCHITECTURE.md: Codebase structure and design patterns
  - VERSIONING.md: Semantic versioning strategy
- GitHub Actions CI/CD pipeline for Python tests and linting
- Semantic versioning (0.1.0)
- MIT License
- Contributing guidelines
