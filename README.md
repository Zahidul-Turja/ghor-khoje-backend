# Ghor Khojee – Backend API

This is the **backend** service for **Ghor Khojee**, a rental platform tailored for bachelors in Bangladesh. Built with **Django**, **Django REST Framework**, **JWT**, and **WebSockets (Channels)**, this service powers the core API, chat, authentication, booking, analytics, and more.

---

## Core Features

- 🔐 JWT-based Authentication
- 📬 Real-time Chat with WebSockets
- 📅 Booking System with availability checks
- 📊 Analytics via API
- 📂 Modular app structure (user, place, chat, booking, etc.)
- ⚙️ Dockerized for local and production use
- 🌐 Deployed via Render ASGI setup

---

## Tech Stack

| Tech                        | Purpose              |
| --------------------------- | -------------------- |
| Python                      | Programming language |
| Django                      | Web framework        |
| Django REST Framework (DRF) | API creation         |
| Celery + Redis              | Asynchronous tasks   |
| Django Channels             | WebSocket support    |
| Docker                      | Containerization     |
| PostgreSQL                  | Primary database     |

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Zahidul-Turja/ghor-khoje-backend.git
cd ghor-khoje-backend
```

### 2. Create environment file

Create a `.env` file using the following command

```bash
cp .env.example .env
```

or manually if you prefer and update the values. You do not need the Cloudinary and Neon DB setup for running locally. The variable just need to be there.

### 3. Run Docker Compose (recommended)

You need **Docker**, **Docker compose** and if on `Windows` might need **WSL** as well.

```bash
docker compose -f docker-compose.local.yml up --build
```

This spins up:

- Django app (backend)
- PostgreSQL database
- Redis broker
- Celery worker
- Celery beat scheduler

Migrate the Databases using these commands

First check the name of the backend container using this command

```bash
docker ps
```

Then enter the **bash** with,

```bash
docker exec -it ghorkhojee_web bash
```

and migrate using the existing migration files with the following command

```bash
python manage.py migrate
```

**Create super user**

```bash
python manage.py createsuperuser
```

---

## 📂 Project Highlights

- `place/` – Listings, filtering, search, location metadata
- `user/` – Authentication, user profiles, host registration
- `booking/` – Bookings, appointments, availability logic
- `chat/` – Real-time messaging (WebSocket consumers)
- `feedback/` – Reviews & Ratings
- `utils/` – Reusable services, response handlers, helper functions
- `ghorkhoje/` – Project settings, routing, celery app

---

## 🧠 Celery & Background Tasks

We use **Celery** for background task processing:

- Notifications (email)
- Periodic cleanup or analytics
- Long-running tasks

---

## 🤝 Contributing

Pull requests and contributions are welcome. Please ensure your code follows the existing style and includes tests when applicable.

---

## 🧑 Author

**Zahidul Islam Turja**  
🔗 [LinkedIn](https://linkedin.com/in/zahidul-turja)  
📫 zahidul.turja@gmail.com

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).
