---
name: Non-Blocking Execution
description: Guidelines for running long-lived processes (servers, watchers) without blocking agent execution.
---

# Non-Blocking Execution Skill

Agents often need to run servers (`npm start`), watchers (`npm run watch`), or long builds. Standard execution blocks the agent until the command finishes—which for a server is **never**.

## 1. The Async Pattern

**Trigger**: Any command that runs indefinitely or >10 seconds.
**Tool**: `execute` / `run_command`

### Mandatory Parameters
- **`WaitMsBeforeAsync`**: Set to `2000` (2 seconds).
    - *Why?* Catches immediate startup errors (e.g., "Address in use") while keeping the agent responsive.
    - *Do NOT* use default (synchronous).

### Example
```javascript
// WRONG - Blocks forever
run_command({ CommandLine: "npm start" })

// CORRECT - Returns CommandID after 2 seconds
run_command({ 
    CommandLine: "npm start",
    WaitMsBeforeAsync: 2000 
})
```

## 2. The Verification Loop

Async commands return a `CommandId`. You **MUST** verify they are actually running.

1.  **Launch**: Run with `WaitMsBeforeAsync: 2000`.
2.  **Wait**: Sleep/Tokens (implicit in tool usage).
3.  **Check Status**: Use `command_status` with the `CommandId`.
    - **Status**: Is it `running`?
    - **Output**: Does it say "Server started on localhost:3000"?
4.  **Confirm**: Only proceed once output confirms success.

## 3. Clean Termination

**Trigger**: You are done testing the server.
**Tool**: `send_command_input`

- **Action**: `Terminate: true`
- **Why?**: Leaving zombie servers eats resources and blocks ports for future agents.

## 4. Common Blocking Commands (Watchlist)

Apply this skill AUTOMATICALLY for:
- **Node/JS**: `npm start`, `yarn start`, `npm run dev`, `npm run watch`, `npx expo start`, `npx react-native start`
- **.NET / C#**: `dotnet watch`, `dotnet run`, `dotnet build -t:Run`
- **Flutter / Dart**: `flutter run`
- **Native Mobile**: `./gradlew installDebug`, `xcodebuild -scheme <Schema> run`
- **Python**: `python manage.py runserver`, `uvicorn`, `flask run`
- **JVM**: `./gradlew bootRun`, `mvn spring-boot:run`
- **Rust/Go**: `cargo run`, `cargo watch`, `go run .`
- **Containers**: `docker-compose up` (without -d)
