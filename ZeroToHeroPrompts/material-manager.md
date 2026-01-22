# Zero to Hero Request: "Material Manager" Workshop

**Workflow Activation**: Please initiate the **Zero to Hero Workflow** (Phase 1).

## Vision: "The Digital Foreman"
I want to build the ultimate inventory management solution for high-end craftsmen and woodworkers. This isn't just a database; it's a **precision tool** that feels as reliable as a table saw. The app should utilize a "Reactive" architecture where the user interface and data layer are bound to a single source of truth, ensuring zero-latency updates. Think "Iron Man's Workshop Interface" meets "This Old House".

## Core Objective
Create a "Hero" quality application that serves as the definitive source of truth for raw materials, with a specialized focus on **algorithmic optimization** of stock. The app must be accessible on **Mobile Devices** and adaptable for **Web Browsers**.

## Key Features Required
1.  **"The Stockpile" (Live Inventory)**: A high-performance, real-time dashboard displaying the master list of materials. It must reflect changes instantly across the app without manual refreshes (using a centralized state store).
2.  **"The Precision Gauge" (Smart Entry)**: An intelligent input form for adding materials. It handles "Hybrid Logic" for dimensions—allowing users to select standard presets (1/4", 1/2", 3/4") or toggle a custom input for non-standard sizes.
3.  **"The Reactive Data Engine" (Architecture)**: A verified architectural pattern where UI components strictly observe a decoupled Data/State layer. Changes to the state must propagate immediately to all active views.
4.  **"The Gatekeeper" (Identity)**: A robust onboarding flow that securely identifies the user on launch or redirects to a setup wizard if no identity is found locally.
5.  **EXTRA EXCITING FEATURE: "The Master Cutter" (Plan Optimizer)**: A complex algorithmic engine where users input their project plans via a dedicated form.
    -   **Input**: User defines required pieces (Dimensions: L x W) and **Grain Direction** constraints (Horizontal, Vertical, or Any).
    -   **Process**: The algorithm calculates the most effective layout to cut these pieces from the existing stock to minimize waste, strictly adhering to grain direction rules.
    -   **Output**: A rich **Interactive Cut Visualizer**.
        -   **Visual UI**: A graphical representation of the board showing exactly where cuts are made and piece orientation.
        -   **Tools**: Must function as a "Graphical Tool" allowing the user to inspect and potentially interact with the layout (e.g., visualize grain direction, swap pieces).

## Aesthetics & Design Language
-   **Vibe**: "Industrial Precision". Dark slate grays, blueprint blues, and "Safety Orange" accents for actions.
-   **Typography**: Technical sans-serif (e.g., Roboto or Inter) for maximum legibility in a dusty shop environment. Monospaced numbers for dimensions.
-   **Interactivity**: Solid, mechanical transitions. Snappy feedback on button presses. Visual metaphors for wood grain or textures where appropriate but subtle.

## Technical Constraints
-   **Platform Targets**: **Mobile (iOS/Android) + Web Browser**.
-   **Stack Selection**: Open to **Analyst Recommendation** (e.g., React+Vite [PWA], React Native/Expo, or Flutter).
-   **Architecture - Local-First, Cloud-Ready**:
    -   **Data Persistence**: Initial version must be **100% Offline/Local** (using LocalStorage, IndexedDB, or similar).
    -   **Abstraction Layer**: Must use the **Repository Pattern** or **Adapter Pattern** to strictly decouple the UI and Business Logic from the specific data source.
    -   **Future-Proofing**: The codebase must be structured such that swapping the "Local Storage Adapter" for a "Cloud API Adapter" in Phase 2 would require **zero changes** to the UI or Feature logic.
-   **State Management**:
    -   Must use a global, reactive store to ensure the "Live-Sync" experience.
-   **Validation**:
    -   Strict validation logic (e.g., Thickness > 0).
-   **Local Only**: Ensure this runs perfectly on the local simulator/device/browser.