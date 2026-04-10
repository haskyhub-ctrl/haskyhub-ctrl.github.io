# Fire Escape Game Improvement Plan

## Overview
This plan outlines improvements to the fire escape game based on user requirements:
1. Fix UI issues (headings, rounded corners)
2. Enhance visual design (better graphics, characters, effects)
3. Fix game logic (prevent walking through obstacles)
4. Redesign maps as mazes with multiple paths requiring obstacle overcoming
5. Implement limited vision/fog of war mechanics
6. Fix lesson font issues
7. Adjust fire/smoke mechanics
8. Design 15 maps total

## Tasks

### 1. UI Fixes
- Fix heading fonts and remove extra characters in lessons
- Ensure proper border-radius for UI elements
- Fix any font display issues

### 2. Visual Enhancements
- Improve character sprites and animations
- Enhance fire and smoke visual effects
- Better item icons and visual feedback
- Improved background and environmental details

### 3. Game Logic Fixes
- Prevent player from walking through walls/obstacles without proper items
- Ensure exit is only reachable after overcoming required obstacles
- Fix collision detection

### 4. Map Redesign
- Convert existing maps to maze-style layouts
- Create 2-3 possible paths to exit, all requiring obstacle interaction
- Increase map size
- Place items strategically far from start
- Design 15 total maps with progressive difficulty

### 5. Limited Vision Mechanics
- Implement fog of war that limits player vision
- Player must explore to reveal map
- Vision improves with certain items or actions

### 6. Fire/Smoke Mechanics
- Fire spreads every 3 seconds
- Fire extinguisher extinguishes 5 fire tiles
- Wet towel provides 10 seconds of smoke protection
- Adjust spread rates and durations

### 7. Lesson System Fix
- Fix font rendering in educational tips
- Remove any extra characters or encoding issues

## Implementation Order
1. First fix critical bugs (walking through walls)
2. Implement fog of war/limited vision
3. Redesign maps as mazes
4. Enhance visual elements
5. Adjust fire/smoke mechanics
6. Fix lesson font issues
7. Polish and test

## Files to Modify
- frontend/js/game-escape.js (main game logic)
- frontend/js/game-levels.js (map data)
- frontend/css/games.css (styling)
- frontend/game-escape.html (structure if needed)