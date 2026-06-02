# Antigravity Physics Engine Reference

Technical specification for the JavaScript physics engine embedded in `assets/dashboard.html`.

## Overview

The Antigravity engine is a vanilla JS frame-loop physics simulation inspired by Google's gravity Easter egg. It runs at 60 fps via `requestAnimationFrame` and requires no external libraries.

## Physics Constants

| Constant | Value | Effect |
|----------|-------|--------|
| `G` | `0.07` | Upward gravity acceleration (px/frame²) |
| `DAMP` | `0.996` | Velocity damping per frame (friction) |
| `BNC` | `0.45` | Velocity retained on boundary bounce |
| `MOUSE_RADIUS` | `220` | Pixel radius of cursor repulsion force |
| `MOUSE_STRENGTH` | `0.4` | Multiplier for repulsion magnitude |
| `PARTICLE_COUNT` | `80` | Seed particles in the particle system |

## Card Physics Properties

Each tool card is tracked with:

```js
{
  el: HTMLElement,   // DOM element reference
  x: float,         // current X position (px, relative to viewport)
  y: float,         // current Y position (px, relative to viewport)
  vx: float,        // X velocity (px/frame)
  vy: float,        // Y velocity (px/frame)
  origX: float,     // grid-layout X (restore target)
  origY: float,     // grid-layout Y (restore target)
  dragging: bool,   // true while user is dragging
}
```

## Frame Loop (per card, per frame)

```
1. Apply upward gravity:    vy -= G
2. Apply cursor repulsion:  if distance < MOUSE_RADIUS → apply force
3. Apply drag physics:      if dragging → lerp toward cursor
4. Integrate velocity:      x += vx,  y += vy
5. Apply damping:           vx *= DAMP,  vy *= DAMP
6. Boundary check:          if out of viewport → reverse velocity × BNC
7. Clamp to bounds:         keep card fully visible
8. Apply transform:         el.style.transform = translate(x, y)
```

## Particle System

During Antigravity mode, 80 seed particles stream upward:

- Spawn at random X, bottom of viewport
- Rise with slight random X drift
- Fade out before reaching top
- Re-spawn when out of bounds
- Rendered as `<div class="particle">` elements (CSS glow)

## User Controls

| Control | Trigger | Action |
|---------|---------|--------|
| Antigravity button | Click | Toggle physics mode |
| `Ctrl+G` | Keydown | Toggle physics mode |
| Mouse move | `mousemove` | Update repulsion origin |
| Card click+drag | `mousedown` + `mousemove` | Move card freely |
| `Esc` | Keydown | Exit gravity, restore grid |

## Restore Behavior

When Antigravity is toggled off:
1. Frame loop stops
2. All cards CSS-transition back to original grid positions using `transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)`
3. Particle elements are removed from DOM
4. Card velocities reset to zero

## Performance Notes

- Cards use `transform: translate()` only — no `top`/`left` layout (avoids reflow)
- `will-change: transform` set on each card during physics
- Frame loop uses `requestAnimationFrame` cancellation token for clean stop
- All particle divs removed on exit to minimize DOM size

## Extending the Engine

To add more cards (e.g., a 12th tool category):
1. Add a new card `<div>` to the HTML grid
2. The physics engine auto-discovers all `.card` elements on activation
3. No JS changes required — `origX`/`origY` computed from `getBoundingClientRect` on activation
