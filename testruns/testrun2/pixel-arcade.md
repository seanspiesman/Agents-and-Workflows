# Zero to Hero Request: "The Pixel Arcade" Portal

**Workflow Activation**: Please initiate the **Zero to Hero Workflow** (Phase 1).

## Vision: The "Pixel Arcade"
I want to build the ultimate modern web hub for Retro Gaming enthusiasts (NES, SNES, Sega Genesis era). This uses nostalgia as a hook but delivers a **futuristic, premium user experience**. Think "Ready Player One" meets high-end museum curation. It should blend 8-bit charm with 2024 web performance and aesthetics.

## Core Objective
Create a "Hero" quality application that serves as the definitive sanctuary for playing, discussing, and preserving retro games.

## Key Features Required
1.  **"The Cartridge Shelf" (Library)**: A visually stunning, 3D-interactive library of classic games. Users can "pull" a cartridge off the shelf to view details, box art, and lore.
2.  **Web-Based Emulator Integration**: A seamless, in-browser playback engine for classic ROMs (using WASM/JS libraries) with zero latency.
3.  **"High Score Hall of Fame"**: A global leaderboard system that validates competitive runs and immortalizes top players with digital trophies.
4.  **"The Cheat Code Vault"**: A wiki-style database of famous cheats (Konami Code, Game Genie codes), accessible via a specialized search terminal UI.
5.  **EXTRA EXCITING FEATURE: "The AI Game Master"**: An intelligent assistant that challenges the user ("Finish Level 1-1 in under 30 seconds") or recommends hidden gems based on their playstyle ("If you liked Metroid, try this obscure Castlevania hack").

## Aesthetics & Design Language
-   **Vibe**: "Cyberpunk Arcade". Dark mode default. Neon purples, hot pinks, electric blues. CRT scanline overlays on images.
-   **Typography**: Pixel-art fonts (e.g., Press Start 2P) for massive headers, distinct modern monospaced fonts (JetBrains Mono) for data/code.
-   **Interactivity**: Glitch effects on hover, 8-bit sound effects on clicks, smooth parallax scrolling.

## Technical Constraints
-   **Stack**: **Vite + React + TypeScript (TSX)**.
-   **Styling**: TailwindCSS.
-   **Animation**: Framer Motion (for smooth transitions) + Three.js (optional, for the 3D cartridge shelf if feasible).
-   **Local Only**: Ensure this runs perfectly on localhost.
