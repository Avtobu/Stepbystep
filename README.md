# 📚 Stepbystep

A web application for flashcard-based learning. Create decks, study with spaced repetition, and track your progress.

## Tech Stack

- **Backend:** Python / Flask
- **Database:** PostgreSQL
- **Frontend:** Vue.js
- **Deployment:** Docker, Docker Compose

---

## 🚀 Getting Started (Local with Docker)

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Clone the repository

```bash
git clone https://github.com/liorenline/Stepbystep.git
cd Stepbystep
```

### 2. Configure environment variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://postgres:yourpassword@db:5432/stepbystep
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=stepbystep
```

### 3. Build and run

```bash
docker compose up --build
```

The app will be available at **http://localhost:5000**

### 4. Stop the app

```bash
docker compose down
```

To also remove the database volume:

```bash
docker compose down -v
```

---

## ⚠️ Running Locally When the App Is Already Hosted

If the project is already deployed (e.g., on [Fly.io](https://fly.io)), running it locally with Docker is completely fine — they are independent environments.

**Things to keep in mind:**

- Make sure ports don't conflict. The hosted version runs remotely; your local Docker runs on `localhost`.
- Use a **separate `.env`** for local development (don't reuse production secrets/database credentials).
- The local Docker setup creates its own PostgreSQL container — it does **not** connect to the production database unless you explicitly configure it to (which you should avoid).

---

## 🗂 Project Structure

```
Stepbystep/
├── app/                  # Flask application (routes, models, logic)
├── adjustment-front/     # Vue.js frontend
├── instance/             # Flask instance config
├── .env                  # Environment variables (not committed)
├── Dockerfile            # Docker image for the app
├── docker-compose.yml    # Multi-container setup (app + db)
├── fly.toml              # Fly.io deployment config
├── requirements.txt      # Python dependencies
└── run.py                # App entry point
```

---

## 🛠 Development (Without Docker)

### Backend

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask run
```

### Frontend

```bash
cd adjustment-front/TryingNewWorkspace
npm install
npm run dev
```

---

## 📦 Deployment

The app is configured for [Fly.io](https://fly.io) via `fly.toml`.

```bash
fly deploy
```
