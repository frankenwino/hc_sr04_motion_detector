# Architecture

## Design Pattern

Single-process polling loop. Sensor abstracted via gpiozero, actions are pluggable callables.

## System Architecture

```mermaid
graph TB
    subgraph Entry["__main__.py"]
        CLI[CLI Args] --> CFG[load_config]
        CFG --> LOG[Setup Logging]
    end

    subgraph Components
        SENS[UltrasonicSensor<br/>gpiozero]
        DET[Detector Loop]
        ACT[Action<br/>log / command / sound]
    end

    LOG --> SENS
    LOG --> ACT
    LOG --> DET
    DET --> SENS
    DET --> ACT
```

## Detection Loop

```mermaid
sequenceDiagram
    participant D as Detector
    participant S as Sensor
    participant A as Action

    loop Forever
        D->>S: measure()
        S-->>D: distance_cm
        alt distance < threshold
            D->>A: action(distance)
            D->>D: sleep(cooldown)
        else
            D->>D: sleep(interval)
        end
    end
```

## Key Design Decisions

- **gpiozero.DistanceSensor** — handles ultrasonic timing internally, returns meters (converted to cm)
- **Pluggable actions** — factory function returns callable based on config
- **Lazy pygame import** — only imported if action="sound"
- **`float('inf')` on error** — measurement failures don't trigger false detections
