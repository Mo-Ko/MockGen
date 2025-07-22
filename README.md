<p align="center">
  <img src="https://raw.githubusercontent.com/Mo-Ko/MockGen/main/docs/logo.png" alt="MockGen Logo" width="120"/>
</p>
<h1 align="center">MockGen: AI-Powered REST & GraphQL Mock API Generator </h1>

<p align="center">
  <b>Instantly generate REST or GraphQL APIs with GPT or Gemini from a simple prompt file.

<br>
  <i>Perfect for developers, testers, and teams simulating APIs before the backend is ready.</i></b>
</p>

<p align="center">
  <a href="#features"><img src="https://img.shields.io/badge/AI%20API%20Generator-GPT%20%7C%20Gemini-blueviolet" alt="AI API Generator"/></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License"/></a>
  <a href="https://github.com/Mo-Ko/MockGen/issues"><img src="https://img.shields.io/github/issues/Mo-Ko/MockGen" alt="GitHub Issues"/></a>
  <a href="https://github.com/Mo-Ko/MockGen/commits/master"><img src="https://img.shields.io/github/last-commit/Mo-Ko/MockGen" alt="Last Commit"/></a>
  <a href="https://github.com/Mo-Ko/MockGen/stargazers"><img src="https://img.shields.io/github/stars/Mo-Ko/MockGen?style=social" alt="GitHub Stars"/></a>
  <a href="https://github.com/Mo-Ko/MockGen/fork"><img src="https://img.shields.io/github/forks/Mo-Ko/MockGen?style=social" alt="GitHub Forks"/></a>
  <a href="https://github.com/Mo-Ko/MockGen/graphs/contributors"><img src="https://img.shields.io/github/contributors/Mo-Ko/MockGen" alt="GitHub Contributors"/></a>
</p>


<!-- SEO Meta Tags -->
<meta name="description" content="MockGen is an open-source AI-powered mock API generator. Instantly generate fake REST and GraphQL APIs with GPT or Gemini, serve OpenAPI or GraphQL mock servers, and simulate endpoints using Docker and FastAPI."/>
<meta name="keywords" content="mock api generator, ai api generator, graphql mock server, generate graphql api, fake REST APIs with LLM, OpenAPI mock server with AI, GraphQL API generator, mock server with Docker, MockGen, open source"/>

---


## 🚀 What is MockGen?

**MockGen** is an open-source tool that uses Large Language Models (LLMs) like GPT or Gemini to generate fully functional mock REST APIs from a simple `.prompt` file. It instantly creates endpoints, schemas, and logic—no backend code required. Serve both static and dynamic endpoints, manage everything via a React frontend, and run the whole stack with Docker.

---

## ✨ Features

- **AI-Powered Mock API Generator**: Instantly create fake REST and GraphQL APIs using GPT or Gemini
- **Prompt-Driven**: Define endpoints and logic in a simple `.prompt` file (OpenAPI-like or DSL)
- **GraphQL Support**: Define and simulate GraphQL schemas and queries using `.prompt` files
- **Dynamic & Static Endpoints**: Serve both static and LLM-generated responses
- **Unified FastAPI Backend**: All traffic (frontend & backend) via FastAPI on port 8000
- **React Frontend**: Manage prompts and endpoints visually
- **Dockerized**: Multi-stage Docker build (Node + Python), easy to run anywhere
- **Configurable**: Supports `.env`, `config.py`, and environment overrides
- **Great for Teams**: Simulate APIs before the real backend exists

---

## 🏁 Quick Start (Docker Compose)

```bash
git clone https://github.com/Mo-Ko/MockGen.git
cd MockGen
docker-compose up --build
```

- Access the app at [http://localhost:8000](http://localhost:8000)
- Frontend and backend are both served from the same port!

---

## 📁 Project Structure

```
MockGen/
├── backend/
│   ├── src/
│   ├── pyproject.toml
│   └── ...
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── docs/
    ├── PromptSpec.md
    ├── Architecture.md
    ├── Configuration.md
    └── LLM-Integration.md
```

---

## ⚙️ Configuration

- **.env**: Set environment variables (see `.env.example`)
- **config.py**: Advanced config for backend
- **APP_ROOT**: Root directory for the app (default: `/app`)
- **STATIC_DIR**: Where built frontend assets are served from (default: `/app/static`)

See [docs/Configuration.md](docs/Configuration.md) for full details.

---

## 🤖 LLM Integration

- Supports **OpenAI GPT** and **Google Gemini** (configurable)
- LLMs generate response schemas, fake data, and dynamic logic for both REST and GraphQL
- Fallback strategies if LLM is unavailable
- See [docs/LLM-Integration.md](docs/LLM-Integration.md) for details

---

## 🔌 Advanced Usage & Endpoints

- Serve static files from `/static`
- All generated API endpoints under `/mock/`
- Health check at `/health`
- See [docs/Architecture.md](docs/Architecture.md) for internal details

---

## 📦 Dependencies

- Python 3.10+
- FastAPI, Uvicorn, Poetry
- Node.js (for frontend build)
- See [`backend/pyproject.toml`](backend/pyproject.toml) for backend deps
- See [`frontend/package.json`](frontend/package.json) for frontend deps

---

## 📝 License

MIT License. Anyone can use, fork, and build on this project. Please credit the original author.

---

## 🤝 Contributing & Issues

- PRs and issues welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) (coming soon)
- For bugs, open an issue on GitHub

---

## 🙏 Credits / Author

Created by **Mohsin Kokab**  
Email: moko.lums@gmail.com  
GitHub: [Mo-Ko](https://github.com/Mo-Ko)  
LinkedIn: [Mohsin Kokab](https://www.linkedin.com/in/kokab/)
