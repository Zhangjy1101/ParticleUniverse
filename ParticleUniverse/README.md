# Dynamic Particle Universe - Interactive Particle Art Installation

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.5.0-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

An interactive particle art installation created with Python and Pygame. Users can interact with a dynamic particle system using mouse and keyboard inputs to create beautiful visual patterns and animations.

## Features

- **Rich Particle System** - 500+ diverse particles with 4 different types
- **Multi-mode Interaction** - 5 unique interaction modes responding to mouse and keyboard inputs
- **Dynamic Visual Effects** - Particle glow, trails, pulsation, and color transformations
- **Immersive Environment** - Twinkling starfield background with smooth animations
- **Real-time Control** - Adjustable particle count, system reset, instant mode switching

## Quick Start

### Prerequisites

- Python 3.7 or higher
- Pygame 2.5.0
- VS Code (recommended) or any Python IDE

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd ParticleUniverse
2. **Install dependencies**
   pip install -r requirements.txt
3. **Run the application**
   python main.py

1.How to Use
  Basic Interaction
   Mouse Movement - Move your mouse around the screen to observe particles responding to your position
   Mouse Click - Left-click to generate new particles at cursor position and enhance interaction effects
   Continuous Interaction - Particles continuously respond to your presence, creating dynamic art patterns

2.Keyboard Controls
  Key	Function
   SPACE	Cycle through interaction modes
   R	Reset particle system
   +	Increase particle count (up to 1000)
   -	Decrease particle count (minimum 100)
ESC	Quit application
Interaction Modes
Attract Mode

Particles are attracted to mouse position
Mouse click enhances attraction force
Creates centripetal flow patterns

Repel Mode

Particles flee from mouse position
Mouse click enhances repulsion force
Creates ripple diffusion effects

Orbit Mode

Particles orbit around mouse position
Mouse click modifies orbital characteristics
Forms planetary ring-like structures

Color Mode

Mouse position influences particle colors
Gradient effects based on distance and angle
Mouse click creates color explosions

Chaos Mode

Random mixture of physical behaviors
Includes special effects like teleportation
Creates unpredictable dynamic patterns

Enjoy your interactive journey with the Particle Universe!