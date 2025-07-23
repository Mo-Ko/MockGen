<p align="center">
  <img src="./docs/mockgen-logo.png" alt="MockGen Logo" width="150"/>
</p>
<h1 align="center">MockGen: AI-Powered REST & GraphQL Mock API Generator</h1>

<p align="center">
  <b>Describe an API in plain English, and get a live, stateful, and mockable REST or GraphQL server in seconds.</b>
  <br>
  <i>Powered by FastAPI, Vue.js, Docker, and your choice of OpenAI's GPT or Google's Gemini.</i>
</p>

<p align="center">
  <a href="https://github.com/Mo-Ko/MockGen/actions/workflows/ci.yml"><img src="https://github.com/Mo-Ko/MockGen/actions/workflows/ci.yml/badge.svg" alt="CI Status"/></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License"/></a>
  <a href="https://github.com/Mo-Ko/MockGen/issues"><img src="https://img.shields.io/github/issues/Mo-Ko/MockGen" alt="GitHub Issues"/></a>
  <a href="https://github.com/Mo-Ko/MockGen/commits/master"><img src="https://img.shields.io/github/last-commit/Mo-Ko/MockGen" alt="Last Commit"/></a>
  <a href="https://github.com/Mo-Ko/MockGen/stargazers"><img src="https://img.shields.io/github/stars/Mo-Ko/MockGen?style=social" alt="GitHub Stars"/></a>
</p>

---

## 🚀 What is MockGen?

**MockGen** is an open-source tool that uses Large Language Models (LLMs) to generate fully functional mock APIs from a simple text description. It instantly creates schemas and deploys live endpoints for both REST (OpenAPI) and GraphQL. The vision is to create truly intelligent, stateful mock servers for developers who need to simulate a backend that doesn't exist yet.

---

## ✨ Core Features

- **AI-Powered Schema Generation**: Instantly create OpenAPI (REST) and SDL (GraphQL) schemas using GPT or Gemini.
- **Dynamic Mock Endpoints**: The generated endpoints are live and interactive from the moment they are created.
- **Service-Oriented Architecture**: A clean backend design separates concerns into services, routers, and configuration for maximum maintainability.
- **Modern Frontend Stack**: The Vue.js frontend is professionally structured with a dedicated API service layer and **Pinia** for state management.
- **Unified FastAPI Backend**: A high-performance Python backend serves both the API mocks and the frontend application on a single port.
- **Dockerized**: A multi-stage Dockerfile provides a simple setup for the entire stack.
- **CI/CD Ready**: Includes a GitHub Actions workflow for linting, testing, and building.

---

## 🏁 Getting Started

### Local Development (Recommended Method)

For the best experience and to access dynamically generated APIs, it is recommended to run the frontend and backend services separately.

**1. Start the Backend (FastAPI):**

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`

# Install dependencies with Poetry
pip install poetry
poetry install

# Configure your environment (add AI API keys)
cp .env.example .env
nano backend/.env

# Run the development server
uvicorn mockapi.main:app --reload
```

The backend will be available at `http://localhost:8000`.

**2. Start the Frontend (Vue.js):**

```bash
# In a new terminal, navigate to the frontend directory
cd frontend

# Install dependencies and run the server
npm install
npm run dev
```

Access the MockGen UI at `http://localhost:5173`.

### Docker Compose

**Note:** Docker Compose now loads environment variables from `backend/.env` and sets `APP_ROOT=/app` inside the container. Healthchecks use `curl`.

```bash
# This will build and run the services. Dynamic endpoint support is being improved.
docker-compose up --build
```

---

## 📚 In-Depth Documentation

- [**Architecture.md**](./docs/Architecture.md): A deep dive into the project's structure and data flow.
- [**Configuration.md**](./docs/Configuration.md): How to configure the application using environment variables and Pydantic settings.
- [**LLM-Integration.md**](./docs/LLM-Integration.md): Details on the AI prompting strategy and future plans with LangChain.

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing & Issues

Contributions, issues, and feature requests are welcome! Please check the [issues page](https://github.com/Mo-Ko/MockGen/issues) for ongoing work.

---

## 🙏 Author

Created by **Mohsin Kokab**

- **GitHub**: [@Mo-Ko](https://github.com/Mo-Ko)
- **LinkedIn**: [Mohsin Kokab](https://www.linkedin.com/in/kokab/)
