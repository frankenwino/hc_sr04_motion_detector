# Documentation Index — HC-SR04 Motion Detector

## How to Use (AI Assistants)

Start here. Navigate to specific files based on your question.

- Architecture → `architecture.md`
- Components → `components.md`
- CLI/APIs → `interfaces.md`
- Config/data → `data_models.md`
- Runtime behavior → `workflows.md`
- Libraries → `dependencies.md`
- Project facts → `codebase_info.md`
- Improvements → `review_notes.md`

## Project Summary

Raspberry Pi HC-SR04 ultrasonic distance sensor detector. Polls distance, triggers configurable action (log/command/sound) when object is within threshold. Python 3.11+, gpiozero, TOML config.

## Documentation Files

| File | Purpose |
|------|---------|
| [codebase_info.md](codebase_info.md) | Tech stack, structure, entry points |
| [architecture.md](architecture.md) | Design, detection loop pattern |
| [components.md](components.md) | Module responsibilities |
| [interfaces.md](interfaces.md) | CLI, TOML schema, Python APIs, wiring |
| [data_models.md](data_models.md) | Config dataclass, runtime state |
| [workflows.md](workflows.md) | Startup, detection cycle, shutdown |
| [dependencies.md](dependencies.md) | Libraries, system requirements |
| [review_notes.md](review_notes.md) | Gaps and recommendations |
