# Test Platform Integration

This repository is a test project, not the test platform itself.

It provides the automation code and suite metadata that a platform-side Local Agent can execute. The platform is responsible for task creation, scheduling, executor management, report indexing, and AI analysis.

## Responsibilities

This repository owns:

- API automation tests under `API_Automation/`.
- iOS UI automation tests under `UI_Automation/`.
- Performance scripts under `Performance/`.
- Test data, page objects, fixtures, and assertions.
- `test-platform.yml`, which describes executable suites and required capabilities.

This repository does not own:

- Multi-project management.
- Platform authentication or authorization.
- Platform database tables.
- Generic task scheduling.
- Generic Local Agent implementation.
- Long-term executor lifecycle management.

## Execution Model

```text
TestPlatform
  -> creates a task with project, suite, environment, and optional app artifact

Local Agent
  -> reads test-platform.yml
  -> downloads or locates the ipa/app artifact when needed
  -> runs the selected suite command
  -> collects logs, screenshots, and Allure results
  -> uploads results back to TestPlatform

iOS-Automation-Framework
  -> contains the test code and produces test outputs
```

## App Artifacts

UI suites can test an app package passed by the platform as:

- `app_path`: local `.ipa` or `.app` path.
- `app_url`: remote artifact URL downloaded by the Local Agent.

The test code should read the final local app path from local configuration or environment variables prepared by the Local Agent.

## Output Convention

Platform-triggered runs should write outputs under:

```text
Reports/platform/{task_id}/
├── logs.txt
├── allure-results/
├── allure-report/
└── screenshots/
```

The Local Agent owns log capture and upload. This repository only needs to make sure suite commands can write deterministic report paths.
