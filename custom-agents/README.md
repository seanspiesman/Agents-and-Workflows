# Custom Agents & Workflows

A specialized agentic framework designed for autonomous software development. This repository houses roles, instructions, skills, and standardized workflows that empower the agentic collective to build, maintain, and secure complex applications.

---

## 🤖 Agents
Specialized AI personas, each with a dedicated role and specific toolset. Agents are orchestrated to work together across the SDLC.

| Agent | Role & Description | Primary Tools & Capabilities |
| :--- | :--- | :--- |
| **Orchestrator** | **Master Project Manager**. The central executive that drives the entire SDLC by coordinating specialist agents. | `agent/runSubagent`, Coordination, Handoff Management. |
| **Analyst** | **Technical Investigator**. Specialist for code-level investigation, determination, and fit-gap analysis. | `vscode`, `search`, `web`, `context7`, Code exploration. |
| **Architect** | **System Designer**. Maintains architectural coherence across features and reviews technical debt accumulation. | `rag/rag_search`, `context7`, ADR creation, Design Review. |
| **Implementer** | **Execution Expert**. Coding agent that implements approved plans with a rigorous interaction verification loop. | `playwright`, `ios-simulator`, `rag/rag_search`, `context7`. |
| **Planner** | **Strategy Assistant**. High-rigor planning for upcoming feature changes and atomic task breakdown. | `read/problems`, `search`, `web`, `context7`, Step-by-step planning. |
| **Critic** | **Program Reviewer**. Constructive reviewer that stress-tests planning documents and code quality. | `read/problems`, `search`, `context7`, Rigorous review, Quality Gate. |
| **QA** | **Quality Assurance**. Verifies test coverage and execution before implementation approval. | `playwright`, `ios-simulator`, `rag/rag_search`, `edit/editNotebook`. |
| **DevOps** | **Release Specialist**. responsible for packaging, versioning, deployment readiness, and release execution. | `execute`, `search`, `context7`, Deployment readiness. |
| **Security** | **Audit Specialist**. Comprehensive security audits for architecture, code, dependencies, and compliance. | `read/problems`, `search`, `web`, `context7`, Security audit. |
| **UAT** | **User Validator**. Product Owner persona conducting UAT to verify business value delivery. | `playwright`, `ios-simulator`, `search`, `todo`. |
| **Navigator** | **UX Explorer**. Autonomous explorer that navigates applications and identifies blocking/non-blocking bugs. | `playwright`, `ios-simulator`, `rag/rag_search`, `context7`, UX exploration. |
| **ArcGIS Specialist** | **Mapping SME**. Subject Matter Expert for all things ArcGIS, spatial data, and geographic logic. | `search`, `web`, `context7`, Spatial math, Schema design. |
| **Researcher** | **Domain SME**. Subject Matter Expert that researches domain content, market data, and user needs (non-technical). | `search`, `web`, `context7`, Market research. |
| **Retrospective** | **Pattern Capturer**. Captures lessons learned, architectural decisions, and patterns after implementation completes. | `edit/createFile`, `search`, `web`, `context7`, Pattern capture. |
| **Roadmap** | **Vision Holder**. Strategic vision holder maintaining outcome-focused product roadmap aligned with releases. | `rag/rag_search`, `search`, `web`, `context7`, Strategic vision. |
| **PI (Process Improvement)** | **Workflow Optimizer**. Analyzes retrospectives and systematically improves agent workflows. | `vscode`, `search`, `web`, `context7`, Workflow optimization. |

---

## 🗂️ Collections
Curated groupings of instructions and agents for specific domains.

- **[C# & .NET Development](collections/csharp-dotnet-development.md)**: Standards for C# 14, .NET 10, EF Core, and clean API design.
- **[Frontend Web Development](collections/frontend-web-dev.md)**: Essential React, Next.js, and TypeScript resources for modern web apps.
- **[Project Planning](collections/project-planning.md)**: High-rigor planning templates and strategic initiative resources.
- **[Security Best Practices](collections/security-best-practices.md)**: Curation of items focused on vulnerability auditing and OWASP compliance.
- **[Software Engineering Team](collections/software-engineering-team.md)**: Team-wide mandates, engineering standards, and collaboration protocols.
- **[Testing & Automation](collections/testing-automation.md)**: Resources for unit/integration testing and automated quality assurance.

---

## 📜 Instructions
The "core mandates" and technology-specific coding standards that ensure consistency.

### Core & Global
- **[Global Instructions](instructions/global.instructions.md)**: Non-negotiable core mandates and mandatory verification procedures.
- **[Shared Definitions](instructions/definitions.instructions.md)**: Standard terminology (Woodshed, Juke Joint, Zero to Hero) for collective alignment.
- **[Output Standards](instructions/output_standards.md)**: Strict rules for naming conventions (kebab-case) and content efficiency.
- **[Task Implementation](instructions/task-implementation.instructions.md)**: Progressive tracking and change records in `.copilot-tracking`.
- **[Self-Explanatory Commenting](instructions/self-explanatory-code-commenting.instructions.md)**: Emphasis on code clarity and "WHY" vs "WHAT" comments.
- **[Sync Docs with Code](instructions/update-docs-on-code-change.instructions.md)**: Lifecycle for technical documentation during implementation.

### Technical Stacks
- **[C# Development](instructions/csharp.instructions.md)**: C# 14 features, XML doc comments, and ASP.NET Core 10 standards.
- **[Next.js Best Practices](instructions/nextjs.instructions.md)**: App Router, Server Components, and Next.js 16 caching directives.
- **[ReactJS Development](instructions/reactjs.instructions.md)**: Functional hooks, component composition, and React 19+ patterns.
- **[TypeScript 5](instructions/typescript-5-es2022.instructions.md)**: TS 5.x features, ES2022 output targets, and pure ES modules.
- **[.NET MAUI](instructions/dotnet-maui.instructions.md)**: Cross-platform mobile patterns for XAML, MVVM, and SecureStorage.
- **[ArcGIS Specialist](instructions/arcgis-specialist.instructions.md)**: SDK integration, spatial logic, and mapping performance optimization.

### Testing & Safety
- **[Security & OWASP](instructions/security-and-owasp.instructions.md)**: Principles of least privilege, injection prevention, and secure secret management.
- **[Performance Optimization](instructions/performance-optimization.instructions.md)**: Exhaustive checklist for frontend, backend, and database tuning.
- **[Playwright (TypeScript)](instructions/playwright-typescript.instructions.md)**: Role-based locators and accessibility-first testing.
- **[Playwright (.NET)](instructions/playwright-dotnet.instructions.md)**: Playwright integration for .NET test runners.
- **[Markdown Standards](instructions/markdown.instructions.md)**: front-matter requirements and validation rules for content.
- **[Style & Color Guide](instructions/html-css-style-color-guide.instructions.md)**: Accessibility, the 60-30-10 rule, and professional aesthetics.

---

## 🛠️ Skills
Modular capabilities that enhance agent functional intelligence.

- **[Agent Architecture Patterns](skills/agent-architecture-patterns)**: Reflection, Planning, and Multi-Agent patterns.
- **[Engineering Standards](skills/engineering-standards)**: Practical implementation of SOLID, DRY, YAGNI, and KISS.
- **[Testing Patterns](skills/testing-patterns)**: TDD cycle, pyramid strategy, and mocking "iron laws."
- **[Architecture Patterns](skills/architecture-patterns)**: Maintaining system coherence and technical debt management.
- **[Workflow Adherence](skills/workflow-adherence)**: The rule of continuity and autonomous persistence.
- **[Non-Blocking Execution](skills/non-blocking-execution)**: Protocols for multi-step persistence without premature halting.
- **[Web Design Reviewer](skills/web-design-reviewer)**: Visual inspection and fixing of design issues at the source code level.
- **[Web App Testing](skills/webapp-testing)**: Playwright-based E2E verification procedures for web apps.
- **[Security Patterns](skills/security-patterns)**: Secure coding motifs and remediation protocols.
- **[Analysis Methodology](skills/analysis-methodology)**: Fit-gap analysis and root cause investigation.
- **[GitHub Issues](skills/github-issues)**: Automated issue tracking and resolution logic.
- **[NuGet Manager](skills/nuget-manager)**: Package discovery and automated upgrade procedures.
- **[Mermaid Diagramming](skills/mermaid-diagramming)**: Standardized patterns for FLOWCHART and sequence diagrams.
- **[Memory Contract](skills/memory-contract)**: Managing and persisting project context across multiple turns.
- **[Collaboration Tracking](skills/collaboration-tracking)**: Logging of handoffs and tool side-effects in `agent-output/`.
- **[Document Lifecycle](skills/document-lifecycle)**: ID inheritance and status management for project artifacts.
- **[Cross-Repo Contract](skills/cross-repo-contract)**: Standards for cross-repository consistency and communication.
- **[Release Procedures](skills/release-procedures)**: Packaging, versioning, and finalizing deployment-ready code.

---

## 🔄 Workflows
Standardized, multi-phase processes for completing complex SDLC tasks. Organized by directory.

### [Analysis](workflows/analysis/)
- **[API Contract Scaffold](workflows/analysis/APIContractScaffold.workflow.md)**: Generate client SDKs from an OpenAPI/Swagger spec for React, Flutter, and MAUI.
- **[App Navigation](workflows/analysis/AppNavigation.workflow.md)**: Autonomous application exploration, bug discovery, and recursive resolution.
- **[Functionality Analysis](workflows/analysis/FunctionalityAnalysis.workflow.md)**: Deep dive into specific app logic with critique and visual Mermaid diagrams.

### [ArcGIS](workflows/arcgis/)
- **[ArcGIS Model Gen](workflows/arcgis/ArcGISModelGen.workflow.md)**: Generate strongly-typed data models from Feature Layer schemas.
- **[ArcGIS Upgrade](workflows/arcgis/ArcGISUpgrade.workflow.md)**: Automate the upgrade path for ArcGIS SDK versions.
- **[Geo Auth](workflows/arcgis/GeoAuth.workflow.md)**: Configure and validate secure ArcGIS Proxy and OAuth2 flows.
- **[Geo Mock](workflows/arcgis/GeoMock.workflow.md)**: Mock location data and spatial query results for desk-side testing.
- **[Geo Telemetry](workflows/arcgis/GeoTelemetry.workflow.md)**: Standardize tracking for spatial events across platforms.
- **[GP Client Gen](workflows/arcgis/GPClientGen.workflow.md)**: Create type-safe async client wrappers for ArcGIS GP services.
- **[Map A11y](workflows/arcgis/MapA11y.workflow.md)**: Audit color contrast, tap targets, and screen reader labels for maps.
- **[Map-To-UI](workflows/arcgis/MapToUI.workflow.md)**: Auto-generate legend, sidebar, and popup code from ArcGIS Web Maps.
- **[Offline Sync](workflows/arcgis/OfflineSync.workflow.md)**: Set up and validate Geodatabase offline-sync logic.
- **[Spatial Asset Optimize](workflows/arcgis/SpatialAssetOptimize.workflow.md)**: Compress vector tiles and simplify geometries for mobile.
- **[Spatial Audit](workflows/arcgis/SpatialAudit.workflow.md)**: Analyze implementations for performance bottlenecks and errors.
- **[Spatial Logic Port](workflows/arcgis/SpatialLogicPort.workflow.md)**: Port complex spatial business logic between C#, Dart, and TypeScript.
- **[Sync Stress Test](workflows/arcgis/SyncStressTest.workflow.md)**: Simulate intermittent network failures and geodatabase conflicts.
- **[Web-to-EXB Port](workflows/arcgis/WebToEXBPort.workflow.md)**: Port spatial apps to the ArcGIS Experience Builder framework.

### [Core](workflows/core/)
- **[Env Sync](workflows/core/EnvSync.workflow.md)**: Synchronize ArcGIS Portal URLs, Web Map IDs, and feature flags across Dev/Staging/Prod.
- **[Intl Sync](workflows/core/IntlSync.workflow.md)**: Synchronize i18n strings across .resx (MAUI), .arb (Flutter), and .json (React).
- **[Theme Sync](workflows/core/ThemeSync.workflow.md)**: Manage design tokens centrally and auto-update React CSS, Flutter Themes, and MAUI Resources.
- **[Zero-To-Hero](workflows/core/ZeroToHero.workflow.md)**: The standard SDLC model from inception to verification, using iteration loops.

### [Development](workflows/development/)
- **[API Integration](workflows/development/APIIntegration.workflow.md)**: Connecting applications to external or internal API services.
- **[New Feature](workflows/development/NewFeature.workflow.md)**: Sifting context and implementing new features with interaction-first precision.
- **[Spike](workflows/development/Spike.workflow.md)**: Time-boxed research and experimentation to de-risk technical unknowns.
- **[UI Component](workflows/development/UIComponent.workflow.md)**: Designing and implementing reusable UI components with visual verification.

### [Documentation](workflows/documentation/)
- **[Architecture Readme](workflows/documentation/CreateArchitectureReadme.workflow.md)**: Reverse-engineer codebases into high-fidelity `README-ARCH.md` with diagrams.
- **[Documentation Sync](workflows/documentation/DocumentationSync.workflow.md)**: Treat doc updates as first-class citizens, comparing API/symbols against text.

### [Maintenance](workflows/maintenance/)
- **[Bug Fix](workflows/maintenance/BugFix.workflow.md)**: Standardized process for Reproduce -> Root Cause -> Fix -> Verify.
- **[Dependency Upgrade](workflows/maintenance/DependencyUpgrade.workflow.md)**: Automated auditing and safe library updates across the stack.
- **[Log Analyst](workflows/maintenance/LogAnalyst.workflow.md)**: Analyze crash/error logs to find cross-platform root causes.
- **[Logic Extract](workflows/maintenance/LogicExtract.workflow.md)**: Scan projects for business logic to extract into shared libraries.
- **[Refactoring](workflows/maintenance/Refactoring.workflow.md)**: Safe tech debt paydown ensuring behavior parity via Analysis -> Implementation -> Regression.
- **[Web-to-Mobile Port](workflows/maintenance/WebToMobilePort.workflow.md)**: Analyze React components and suggest optimal implementations in Flutter/MAUI.

### [Mobile](workflows/mobile/)
- **[Asset Pipeline](workflows/mobile/AssetPipeline.workflow.md)**: Auto-slice and deploy visual assets to respective platform directories.
- **[Native Interop](workflows/mobile/NativeInterop.workflow.md)**: Generate boilerplate for MethodChannels (Flutter) or DependencyService (MAUI).

### [Quality](workflows/quality/)
- **[Feedback](workflows/quality/Feedback.workflow.md)**: Processing and applying changes from UAT feedback through a structured cycle.
- **[QA Workbench](workflows/quality/QAWorkbench.workflow.md)**: Generate web apps for QA verification using absorbed endpoints and data schemas.
- **[Sync E2E](workflows/quality/SyncE2E.workflow.md)**: Run synchronized web/mobile tests to verify cross-platform data reflection.
- **[Test Coverage](workflows/quality/TestCoverage.workflow.md)**: Systematic expansion of the project's unit and integration test suites.
- **[Widget Testing](workflows/quality/WidgetTesting.workflow.md)**: Combinatorial state-permutation testing for ArcGIS Experience Builder widgets.

### [Security](workflows/security/)
- **[Geo Identity Audit](workflows/security/GeoIdentityAudit.workflow.md)**: Identifies insecure token storage or hardcoded secrets in spatial calls.
- **[Security Remediation](workflows/security/SecurityRemediation.workflow.md)**: Precise sink-to-source vulnerability fixing with rigorous verification.
- **[Spatial Privacy](workflows/security/SpatialPrivacy.workflow.md)**: Monitors for accidental leaks of precise user coordinates to third-party libraries.

---

## 📂 Templates & Reference
- **[Handoff Template](templates/handoff.md)**: Standard structure for dense, no-fluff agent handoffs.
- **[Memory Contract Example](reference/memory-contract-example.md)**: Demonstration of cross-session context management.
- **[Security Reference](reference/security-language-vuln-reference.md)**: Lookup table for common language vulnerabilities.

---

## 🚀 Usage
The framework is designed for autonomous orchestration. Initiated by the **Orchestrator**, the collective follows these **Workflows**, adheres to **Instructions**, and leverages **Skills** to deliver verified, production-ready software.
