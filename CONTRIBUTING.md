# Contributing to RecallStack

Thank you for helping improve RecallStack!

---

## Workflow

1. **Branching**

- `main` → stable, production-ready code  
- `dev` → ongoing development work  
- `feature/*` → new features  
- `fix/*` → bug fixes  

2. **Creating a Branch**

```bash
git checkout -b feature/your-feature-name
````

3. **Committing Changes**

Use clear messages in the format:

```text
type: short description
```

Examples:

```text
feat: add spaced repetition algorithm  
fix: correct flashcard review counter
```

> For guidance, see [Common commit types](commitTypes.md).

4. **Pushing & Opening a PR**

```bash
git push origin feature/your-feature-name 
```

Then open a pull request to `dev`.

---

## Local Development Setup

1. **Install dependencies**

```bash
make venv # Create a virtual environment
make install
```

This installs both backend (Python) and frontend (Node.js) dependencies.
> Ensure you have **Python 3.12+** and **Node.js 22.x LTS** installed.

2. **Run the development servers**

### Running the App

Open two terminals:

```bash
# Terminal 1: start the Django backend (default: http://127.0.0.1:8000)
make backend
```

```bash
## Terminal 2: start the React frontend (default: http://localhost:5173)
make frontend
```

> Note on virtual environments: The Python backend uses a project-local virtual environment at `backend/.venv`. You do not need to activate it manually — all `make` commands handle it automatically.

Now you can visit the frontend in your browser, which will talk to the backend API.

3. **Linting & Formatting**

```bash
# Check linting
make lint

# Auto-fix formatting
make format
```

4. **Testing**

```bash
make test
```

This runs:

* **Backend tests** with `pytest`
* **Frontend tests** with `vitest`

---

## Best Practices

* Keep pull requests **small and focused**.
* Always run **tests + linting** before committing.
* Update documentation if your change affects usage.

---

Keep the workflow simple: **develop in branches, push to dev, PR for review, merge once approved**.
