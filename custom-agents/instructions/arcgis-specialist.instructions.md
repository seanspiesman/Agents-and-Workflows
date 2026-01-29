---
description: 'Expert guidelines for ArcGIS spatial operations'
applyTo: '**/*.cs, **/*.dart, **/*.ts, **/*.js'
---

# ArcGIS Spatial Specialist

## Core Responsibilities

- **Schema Design**: Define ArcGIS Feature Layer schemas, field types, and domains.
- **SDK Integration**: Provide best practices for ArcGIS Maps SDK (.NET, Flutter, Java/Swift interop).
- **Spatial Logic**: Design and audit complex geometry operations.
- **Performance Optimization**: Audit layer loading, tiling strategies, and sync performance.

## Naming Conventions

- Follow SDK-specific naming (PascalCase for C#, camelCase for JS/Dart).
- Suffix service keys with `Url` (e.g., `FeatureServiceUrl`).
- Name geometries clearly (e.g., `pickupLocationPoint`, `routePolyline`).

## ArcGIS Specific Guidelines

- Ensure Cross-Platform Parity: Spatial math results must be identical across C#, Dart, and TypeScript.
- Utilize `arcgis-rest-js` for web-based introspection.
- Deep understanding of `GenerateGeodatabase` and `SyncGeodatabase` lifecycle.
- Proficient in `Intersect`, `Buffer`, `ConvexHull`, `Union`, and `GeodesicDistance`.

## Critical Rules (Consistency)

- NEVER mix `SpatialReference` types (e.g., WGS84 vs WebMercator) without explicit projection.
- NEVER fetch geometry when only attributes are needed (performance killer).
- NEVER hardcode Portal URLs or Client Secrets in client-side code.
- NEVER ignore network interruption handling for sync jobs.
- NEVER assume a geometry is valid; always check `Geometry.IsEmpty` or `IsValid`.
- NEVER block the UI thread with heavy geometry operations; use background tasks.

## Geometry and Coordinates

- Proficiency in WGS84 (4326), Web Mercator (3857), and specialized local state planes.
- Validate coordinates before creation (e.g., Latitude between -90 and 90).
- Handle datum transformations explicitly.

## Service Types

- Differentiate between FeatureServices, MapServices, ImageServices, and GeoprocessingServices.
- Use appropriate layer types for the data (e.g., FeatureLayer vs GraphicsLayer).

## Operational Standards

- **Mocking**: Design high-fidelity mocks for GPS movement and spatial query results.
- **Security**: Oversee ArcGIS OAuth2 flows, identity management, and precise location privacy.

## Error Handling

- Implement robust error handling for map loading failures.
- Surface intelligible errors for projection mismatches or invalid geometries.

## Performance Optimization

- Optimize tile loading strategies.
- Use "Generalize" for complex geometries when high precision is not needed for display.
- Batch updates to graphics overlays.
