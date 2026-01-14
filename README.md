# CoDoc in PlantUML

CoDoc in PlantUML is a real-time collaborative PlantUML editor built with [Reflex](https://reflex.dev/).
It pairs a Monaco-based code editor with an always-on diagram preview—so you can write, share, and review UML diagrams in one place.

## Why CoDoc in PlantUML

- **Fast feedback loop**: Type PlantUML and see the diagram update immediately.
- **Collaboration-first**: Share a link and co-edit the same document in real time.
- **Beginner-friendly examples**: A built-in sidebar provides many ready-to-run snippets (sequence, class, activity, state, JSON/YAML, and more).
- **Comfortable viewing modes**: Split view or focus either the editor or the preview.
- **Zero rendering setup**: Uses a PlantUML server to render diagrams as SVG/PNG.

## Key Features

- **Real-time collaboration**: Multiple users can edit the same diagram document via a shareable URL.
- **Monaco Editor for PlantUML**: Syntax-highlighted editing experience with code-editor ergonomics.
- **Live preview**: Diagram updates as you type (server-rendered image).
- **Examples & Help sidebar**: Click to load starter snippets into the editor.
- **Presence indicators**: Shows active collaborators with lightweight identities.

## Getting Started

This project uses [Poetry](https://python-poetry.org/) for dependency management.
Make sure you have **Python 3.11** and Poetry installed.

### 1) Clone

```bash
git clone https://github.com/milochen0418/codoc_in_plantuml.git
cd codoc_in_plantuml
```

### 2) (Recommended) Ensure Poetry uses Python 3.11

Poetry may auto-select a different Python version (e.g. 3.12+). This project targets **3.11**.

```bash
poetry env use python3.11
poetry env info
```

If `python3.11` is not on your PATH, specify the full executable path:

```bash
poetry env use /absolute/path/to/python3.11
```

### 3) Install dependencies

```bash
poetry install
```

### 4) Run the app

Prefer the repo helper script (it restarts cleanly and uses the expected ports):

```bash
poetry run ./reflex_rerun.sh
```

Then open:

- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## PlantUML Server

By default, diagrams are rendered by generating a URL to a PlantUML server and embedding the resulting image in the preview panel.

### Use the public server (default)

No configuration needed.

### Self-host a server (recommended for privacy/offline)

Start a PlantUML server (Docker example):

```bash
docker run --rm -p 8080:8080 plantuml/plantuml-server:tomcat
```

Point the app to it:

```bash
export CODOC_PLANTUML_SERVER=http://127.0.0.1:8080/plantuml
```

Notes:
- The URL must be reachable from the browser (the preview loads the diagram via an `<img src=...>`).
- If you serve the app over HTTPS, prefer an HTTPS PlantUML server to avoid mixed-content blocking.

## Usage

1) **Create a new document**
     - Opening `/` auto-generates a document ID and redirects you to `/doc/<id>`.

2) **Share and collaborate**
     - Click **Share** to copy the current document URL.
     - Anyone opening the link joins the same doc and can edit in real time.

3) **Switch view modes**
     - Use **Split / Focus Editor / Focus Preview** to match your workflow.

## E2E Tests (Playwright)

The repo includes a test runner. Suites live under `testcases/<suite_name>/run_test.py`.

Run a suite via:

```bash
poetry run ./run_test_suite.sh <suite_name>
```

Artifacts (screenshots/logs) are written to `testcases/<suite_name>/output/`.

## License

MIT License. See [LICENSE](LICENSE).

## Tech Stack

- **Reflex**: Full-stack Python web framework
- **reflex-monaco**: Monaco Editor integration
- **Python 3.11**
