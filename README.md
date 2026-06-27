# Nyx Local

Nyx Local is a local-first Python project prepared for modular growth.

This initial sprint creates only the project foundation. No business logic, AI behavior, memory system, or integrations are implemented yet.

## Project Structure

- `main.py`: Minimal project entry point.
- `src/nyx_local/`: Main Python package.
- `src/nyx_local/core/`: Cross-cutting foundation code and shared primitives for future sprints.
- `src/nyx_local/domain/`: Future domain models, rules, and entities.
- `src/nyx_local/application/`: Future application use cases and orchestration.
- `src/nyx_local/infrastructure/`: Future adapters for persistence, local resources, and external systems.
- `src/nyx_local/interfaces/`: Future input and output boundaries such as CLI, API, or UI adapters.
- `config/`: Future configuration templates and environment examples.
- `docs/`: Project documentation and architectural notes.
- `scripts/`: Utility scripts for development and maintenance.
- `tests/`: Automated tests organized separately from production code.

## Architectural Notes

The project uses a `src/` layout to keep import behavior predictable and to separate production code from repository tooling.

The package is divided into layers so future features can be added through clear boundaries:

- Domain code should not depend on infrastructure.
- Application code should coordinate use cases without owning external details.
- Infrastructure code should contain implementation details for external systems.
- Interfaces should expose ways to interact with the application without embedding business rules.

## Development

Python 3.13 or newer is required.

## Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv

.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

pip install -r requirements.txt

pip install -r requirements-dev.txt
```

Run:

```powershell
python main.py
```

Generate package:

```powershell
python scripts/package_project.py
```

## Git / Pull Request Flow

To prepare a Sprint for review:

```powershell
python scripts/prepare_pr.py branch-name
```

The script will:

- verify Git;
- create the branch;
- run tests;
- generate a clean package;
- show changed files;
- suggest a commit;
- guide push and Pull Request creation.

## Manual Setup

Install runtime dependencies:

```bash
pip install -r requirements.txt
```

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the minimal entry point:

```bash
python main.py
```
