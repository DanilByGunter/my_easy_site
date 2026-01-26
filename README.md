# Personal Website

A full-stack personal website with FastAPI backend and vanilla JavaScript frontend.

## Architecture

```
my_easy_site/
├── backend/                 # FastAPI backend
│   ├── app/                 # Application code
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── repositories/    # Data access layer
│   │   ├── services/        # Business logic
│   │   ├── routers/         # API endpoints
│   │   └── utils/           # Utilities
│   ├── Dockerfile           # Backend container
│   ├── seed_db.py          # Database seeding
│   └── requirements.txt    # Python dependencies
├── frontend/               # Static frontend
│   ├── index.html          # Main HTML file
│   ├── app.js             # JavaScript application
│   ├── styles.css         # Styles
│   └── assets/            # Static assets
├── docker-compose.yml      # Full stack deployment
└── README.md              # This file
```

## Features

- **Vinyl Collection**: Search and filter by genre
- **Books**: Browse by genre with dynamic spine widths
- **Coffee**: Brands and reviews with ratings
- **Figures**: Animated display
- **Projects**: GitHub-style cards
- **Research**: Publications and infographics
- **Plants**: Botanical information
- **Media**: Contact links and external resources

## Data Contract

The backend API (`/api/v1/all`) returns JSON that exactly matches the frontend's `window.DATA` structure:

```json
{
  "about": { "bio": "..." },
  "vinylGenres": ["Electronic", "Rock", ...],
  "vinyl": [{ "id": "...", "artist": "...", "title": "...", "genres": [...], "year": 2023 }],
  "books": [{ "id": "...", "title": "...", "author": "...", "genre": "..." }],
  "coffeeBrands": [{ "id": "...", "name": "..." }],
  "coffee": [{ "id": "...", "brandId": "...", "name": "...", "reviews": [...] }],
  "figures": [{ "id": "...", "name": "...", "brand": "..." }],
  "projects": [{ "id": "...", "name": "...", "desc": "...", "tags": [...] }],
  "publications": [{ "id": "...", "title": "...", "venue": "...", "year": 2023 }],
  "infographics": [{ "id": "...", "topic": "...", "title": "..." }],
  "plants": [{ "id": "...", "family": "...", "genus": "...", "species": "...", "commonName": "..." }],
  "media": {
    "externalWishUrl": "...",
    "links": [{ "type": "...", "label": "...", "value": "..." }]
  }
}
```

## Development

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Node.js (for frontend tooling, optional)

### Backend Setup

1. Create virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Run database migrations:
```bash
# Use Alembic or your migration tool
```

5. Seed database:
```bash
python seed_db.py
```

6. Run development server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

The frontend is static and can be served directly:

```bash
cd frontend
# Serve with Python
python -m http.server 8000

# Or use any static file server
npx serve .
```

### API Testing

```bash
curl http://localhost:8000/api/v1/all
```

## Production Deployment

### Using Docker Compose (Recommended)

**ВАЖНО**: Перед запуском необходимо задать учетные данные для базы данных PostgreSQL.

1. **Настройка переменных окружения для базы данных**:

Создайте файл `.env` в корневой директории проекта и укажите свои учетные данные:

```bash
# Создайте .env файл в корне проекта (my_easy_site/.env)
cat > .env << 'EOF'
# PostgreSQL Database Configuration
POSTGRES_USER=your_db_username
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=personal_site

# Security Configuration (опционально)
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
CORS_ORIGINS=http://localhost,http://127.0.0.1,https://your-domain.com
EOF
```

**Замените следующие значения на свои**:
- `your_db_username` - имя пользователя PostgreSQL (например: `myuser`)
- `your_secure_password_here` - надежный пароль (например: `MySecurePass123!`)
- `your-domain.com` - ваш домен (если планируете развертывание в интернете)

2. **Запуск всех сервисов**:
```bash
docker-compose up -d --build
```

3. **Создание и применение миграций базы данных** (первый запуск):
```bash
# Создание первой миграции
docker-compose exec backend alembic revision --autogenerate -m "Initial migration"

# Применение миграций
docker-compose exec backend alembic upgrade head
```

4. **Заполнение базы данных тестовыми данными** (первый запуск):
```bash
docker-compose exec backend python seed_db.py
```

5. **Доступ к приложению**:
- **Frontend**: http://localhost (обслуживается nginx)
- **Backend API**: http://localhost/api/v1/all
- **Health check**: http://localhost/health
- **База данных**: localhost:5432 (доступна извне для администрирования)

### Подключение к базе данных

Вы можете подключиться к PostgreSQL используя любой клиент:
- **Host**: localhost
- **Port**: 5432
- **Database**: значение из `POSTGRES_DB`
- **Username**: значение из `POSTGRES_USER`
- **Password**: значение из `POSTGRES_PASSWORD`

### Architecture Overview

Production setup включает:
- **nginx**: Reverse proxy, статические файлы, security headers
- **backend**: FastAPI приложение с PostgreSQL
- **frontend**: Статические файлы через nginx
- **db**: PostgreSQL база данных с persistent storage

### Security Features

- CORS ограничения для production доменов
- Rate limiting через nginx
- Security headers (CSP, X-Frame-Options, etc.)
- Валидация и санитизация входных данных
- Защита от SQL injection через SQLAlchemy ORM
- Read-only API без аутентификации
- Trusted host middleware
- Production docs отключены

### Manual Deployment

1. Set up PostgreSQL database
2. Configure environment variables
3. Install Python dependencies
4. Run database migrations
5. Seed initial data
6. Start the application with Gunicorn/Uvicorn

## Security Considerations

- CORS is configured for production (restrict origins in `.env`)
- No authentication required for public API (read-only)
- Database credentials via environment variables
- Non-root user in Docker containers
- Health checks for both services
- PostgreSQL connection pooling

## Telegram Bot Integration

Data modifications (create/update/delete) are designed to be performed via Telegram bot. The API is read-only for the public frontend.

## Technologies

- **Backend**: FastAPI, SQLAlchemy, Pydantic, PostgreSQL
- **Frontend**: Vanilla JavaScript, CSS Grid/Flexbox
- **Deployment**: Docker, Docker Compose
- **Database**: PostgreSQL with asyncpg

## License

MIT
