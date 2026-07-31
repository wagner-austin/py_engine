# py_engine

A small Pygame game engine with pluggable game modes, scene management and a
layer/effects pipeline. Version 1.5.3.

**Dormant** — last commit 2025-03-29. Kept as a reference implementation of the
scene/manager/plugin pattern; the same shape was carried forward into
`~/PROJECTS/merlins_revenge/`.

## Run

```bash
pip install pygame
python main.py
```

`main.py` initialises Pygame, loads plugins, constructs the managers, then
registers the scenes.

**Input is mouse/touch only.** Scene navigation and gameplay were deliberately
built without keyboard bindings, so anything expecting key events will find none.

## Architecture

Three manager objects own the runtime, constructed in `main.py`:

| Manager | Responsibility |
|---------|----------------|
| `SceneManager` | which scene is active, transitions between them |
| `InputManager` | mouse/touch events, routed to the active scene |
| `LayerManager` | draw ordering across the layer stack |

Scenes subclass `base_scene.py`:

- `menu_scene.py` — entry menu
- `game_mode_selection_scene.py` — picks a game mode
- `play_scene.py` — hosts the selected mode

Game modes are the swappable unit — `game_modes/space_shooter/` and
`game_modes/tower_defense/` both plug into the same `play_scene`.

## Layout

```
main.py         entry point — init, load plugins, build managers, register scenes
core/           config and engine primitives
managers/       scene, input and layer managers
scenes/         base_scene + the four concrete scenes
game_modes/     space_shooter/, tower_defense/ — the pluggable gameplay
plugins/        plugin_loader.py + plugins.py — discovery and registration
layers/         layer stack implementations
transitions/    scene transition effects
effects/        visual effects
themes/         theme definitions
ui/             widgets
assets/         images, fonts
tools/          dev helpers
```

`temp.txt` at the root is scratch, not used by the engine.
