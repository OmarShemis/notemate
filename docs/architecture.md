# Architecture

```mermaid
flowchart LR
User --> Agent
Agent --> Notes
Agent --> Calculator
Agent --> Clock
```

See the source modules and tests for implementation details. External model/API availability is independent of offline test success.
