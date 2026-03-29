# ⚙️ Setup e Execução do Projeto (FastAPI)

Guia rápido para instalar e rodar o projeto.

---

# 📋 Pré-requisitos

Instale:

* Docker Desktop → https://www.docker.com/products/docker-desktop/
* Node.js LTS → https://nodejs.org/
* Git → https://git-scm.com/

---

# 🚀 1. Instalação

No terminal:

```powershell
cd full-stack-fastapi-template

cd frontend
npm install
cd ..
```

---

# 🐳 2. Subir o Banco de Dados

```powershell
docker compose up -d db
```

---

# 🧪 3. Rodar os Testes

```powershell
docker compose run --rm `
  -v "./backend/app:/app/backend/app" `
  -v "./backend/tests:/app/backend/tests" `
  backend uv run pytest tests/ -q
```

---

# 🖥️ 4. Rodar o Backend

```powershell
docker compose run --rm -p 8000:8000 `
  -v "./backend/app:/app/backend/app" `
  backend uv run fastapi dev app/main.py --host 0.0.0.0
```

---

# 💻 5. Rodar o Frontend

Em outro terminal:

```powershell
cd frontend
npm run dev
```

---

# 🌍 Acessar o sistema

* Frontend → http://localhost:5173
* Backend → http://localhost:8000

---

# 🔑 Login padrão

```text
admin@example.com
changethis
```

---

# 🛠️ Problemas comuns

## Resetar banco

```powershell
docker compose down -v
docker compose up -d db
```

---

## Ver logs do backend

```powershell
docker compose logs backend
```
