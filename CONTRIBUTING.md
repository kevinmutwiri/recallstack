# Contributing to RecallStack

Thank you for helping improve RecallStack!

## Workflow

1.**Branching**

- `main` → stable, production-ready code  
- `dev` → ongoing development work  
- `feature/*` → new features  
- `fix/*` → bug fixes  

2.**Creating a Branch**

git checkout -b feature/your-feature-name

3.**Committing Changes**

Use clear messages in the format:

```text
type: short description
```

Examples:

```text
feat: add spaced repetition algorithm  
fix: correct flashcard review counter
```

For guidance look at [Common commit types](commitTypes.md)

4.**Pushing & Opening a PR**

```text
git push origin feature/your-feature-name 
```

Then open a pull request to `dev`.

---

Keep the workflow simple: **develop in branches, push to dev, PR for review, merge once approved**.