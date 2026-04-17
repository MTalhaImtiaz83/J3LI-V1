# Architecture Pivot: Local Heavy to Cloud Resilient

## Why the Previous Build Failed
1. **Monolithic Weight**: Local Docker requirements were too heavy for consumer hardware.
2. **Fragile Dependencies**: Hard-coded paths for Python and databases caused dramatic failures.
3. **Setup Friction**: Required high technical knowledge to initialize.

## The Resilient Pivot
1. **Headless Databases**: Moving Neo4j and Milvus to managed cloud services (Neo4j Aura / Zilliz).
2. **Agentic Orchestration**: Using Kafka (Chief of Staff) as the build and maintenance layer.
3. **Managed Launch Kit**: A single-file, path-agnostic launcher that handles environment checks automatically.