# Actionable Improvements for Custom Agents

Based on the definitive analysis of Test Runs 1 & 2, the following changes are recommended for your `custom-agents` configuration. Incorporating these will solve the "Empty Run" failure and the "Low Quality" success issues.

## 1. Orchestrator Agent Updates (`orchestrator.agent.md`)

**Problem**: Missing chat logs and empty output directories (Test Run 1).
**Fix**: Enforce rigorous logging and error handling.

-   [ ] **Add "Log Verification" Step**:
    *   *Instruction*: "After creating the `agent-output` directory structure, immediately write a `status.md` file to verify write permissions and directory existence."
-   [ ] **Fix Markdown Link Syntax**:
    *   *Instruction*: "When logging actions or file creations, ALWAYS provide a description text in the markdown link. Format: `[File Description](file:///path)` NOT `[](file:///path)`."
-   [ ] **Command Output Capture**:
    *   *Instruction*: "When running terminal commands, you must capture the output using `read_terminal` or internal logging if not automatically captured. Do not just say 'ran command' without validating the result."

## 2. Planner Agent Updates (`planner.agent.md`)

**Problem**: "8-week waterfall" plans for an AI sprint (Test Run 2).
**Fix**: Shift to "Zero to Hero" specific agility.

-   [ ] **Constraint: AI Speed**:
    *   *Instruction*: "Plans must be scoped for IMMEDIATE execution (milliseconds/seconds), not human weeks. Do not create multi-week schedules. Create a 'Day 1 Prototype' plan."
-   [ ] **Hero Feature Priority**:
    *   *Instruction*: "Identify the single most 'Heroic' feature (e.g., Audio Tuner, Emulator) and prioritize it above generic CRUD lists. The prototype MUST include this feature."
-   [ ] **Verification Step**:
    *   *Instruction*: "Before handing off to the Architect, verify that the `agent-output` directory contains the `implementation_plan.md`."

## 3. Architect Agent Updates (`architect.agent.md`)

**Problem**: ASCII diagrams and generic stacks.
**Fix**: Modernize visualization and specificity.

-   [ ] **Mermaid Requirement**:
    *   *Instruction*: "All architecture diagrams must use Mermaid.js syntax for clarity and standard rendering."
-   [ ] **Design System Definition**:
    *   *Instruction*: "Explicitly define the Tailwind colors and fonts in a `tailwind.config.js` snippet BEFORE implementation starts. Do not leave it to the implementer to guess 'neon-green'."

## 4. Implementer Agent Updates (`implementer.agent.md`)

**Problem**: Unused imports, inline JSX duplication, and broken logic (Test Run 2).
**Fix**: Enforce strict coding standards.

-   [ ] **Rule: No Inline Duplication**:
    *   *Instruction*: "If you create a component (e.g., `Header.tsx`), you MUST import and use it in `App.tsx`. Do not re-write the JSX inline."
-   [ ] **Rule: Functional Verification**:
    *   *Instruction*: "After implementing a logic feature (like Search), you must mentally or physically verify: 'Does the input update the state? Does the map use the filtered list?'"
-   [ ] **Rule: No Fake Loading**:
    *   *Instruction*: "Do not add artificial `setTimeout` delays for 'realism' unless you add a visual Loader/Spinner."
-   [ ] **Rule: Type Safety**:
    *   *Instruction*: "Avoid `useState([])`. Use `useState<Game[]>(...` to ensure type safety."

## 5. Global Instruction Updates (`global.instructions.md`)

**Problem**: General lack of robustness and "drift" from the prompt.

-   [ ] **Drift Check**:
    *   *Instruction*: "Every 5 steps, re-read the original PROMPT doc (e.g., `blues-harmonica.md`) to ensure you haven't drifted to a generic template."
-   [ ] **Artifact Integrity**:
    *   *Instruction*: "Before marking a task as Done, verify the file size of the generated artifact. If it is 0 bytes, retry."

## 6. Workflow Updates (`ZeroToHero.workflow.md`)

**Problem**: Fragile start (Test Run 1).

-   [ ] **Initialization Check**:
    *   *Step Update*: Add a step 0: "Validate Environment". Ensure `node`, `npm`, and write permissions are active before starting the heavy lifting.
-   [ ] **Rescue Path**:
    *   *Step Update*: "If `implementation_plan.md` is missing after the Planning phase, HALT and report error to user using `notify_user`. Do not proceed to build nothing."

## Summary of Next Steps for User
1.  Read `testruns/ANALYSIS.md` for the detailed 50-point breakdown.
2.  Apply the changes above to your agent markdown files.
3.  Re-run the Zero to Hero workflow with the prompt `blues-harmonica.md` to verify the "Rescue" or "Success" of the new logic.
