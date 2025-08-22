# RecallStack

> Your ultimate learning companion for Computer Science & Software Engineering  

## About

RecallStack is an application designed to help learners in the CS and Software Engineering fields retain and recall knowledge more effectively. It leverages spaced repetition, interactive flashcards, and progress tracking to make studying both efficient and engaging.

### Tech Stack

- [React](https://react.dev/) – Frontend UI library
- [Tailwind CSS](https://tailwindcss.com/) – Utility-first CSS framework  
- [Django REST Framework](https://www.django-rest-framework.org/) – Backend API framework for Django  

## Project Status

🚧 **Currently under active development**

## Local Development

To get started quickly:

```bash
# Create a virtual environment
make venv

# Install backend & frontend dependencies
make install

# Run linters
make lint

# Auto-format code
make format

# Run all tests
make test
```

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

Now you can visit the frontend in your browser, which will talk to the backend API.

> Note on virtual environments: The Python backend uses a project-local virtual environment at `backend/.venv`. You do not need to activate it manually — all `make` commands handle it automatically.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on our workflow, branching strategy, and contribution guidelines.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.