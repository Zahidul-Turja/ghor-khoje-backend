# 🏠 Ghor Khojee – Backend

This is the **backend** service for **Ghor Khojee**, a rental platform tailored for bachelors in Bangladesh. Built with **Django**, **Django REST Framework**, **JWT**, and **WebSockets (Channels)**, this service powers the core API, chat, authentication, booking, analytics, and more.

---

## 🚀 Features

- 🔐 JWT-based Authentication
- 📬 Real-time Chat with WebSockets
- 📅 Booking System with availability checks
- 📊 Analytics via API
- 📂 Modular app structure (user, place, chat, booking, etc.)
- ⚙️ Dockerized for local and production use
- 🌐 Deployed via Render ASGI setup

---

## 🛠️ Tech Stack

| Tech                        | Purpose                               |
| --------------------------- | ------------------------------------- |
| Python                      | Programming language                  |
| Django                      | Web framework                         |
| Django REST Framework (DRF) | API creation                          |
| Celery + Redis              | Asynchronous tasks                    |
| Django Channels             | WebSocket support                     |
| Docker                      | Containerization                      |
| PostgreSQL                  | Primary database (assumed via Docker) |

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Zahidul-Turja/ghor-khoje-backend.git
cd ghor-khoje-backend
```

### 2. Create environment file

Create a `.env` file (or use `.env.example` if provided) and define required environment variables:

```env
DJANGO_SETTINGS_MODULE=ghorkhoje.settings

SECRET_KEY=your_secret_key__can_leave_like_this_for_testing

# Allowed hosts
ALLOWED_HOSTS=localhost
ENVIRONMENT=development

# Database connection (using the external URL hostname)
HOST_NAME=db
PORT=5432
DATABASE=ghor_khojee_db
DB_USER=ghor_khojee_admin
PASSWORD=zCQrIjQ8uR2wpB9EJfaecz59vED5hwAA
DEBUG=True

# Claudinary
CLOUDINARY_CLOUD_NAME=for_local_its_not_needed__just_the_variable_needs_to_be_present
CLOUDINARY_API_KEY=for_local_its_not_needed__just_the_variable_needs_to_be_present
CLOUDINARY_API_SECRET=for_local_its_not_needed__just_the_variable_needs_to_be_present

# Email settings
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=email_app_password

# Neon Tech
NEON_DB=for_local_its_not_needed__just_the_variable_needs_to_be_present
NEON_DB_NAME=neondb
NEON_DB_USER=for_local_its_not_needed__just_the_variable_needs_to_be_present
NEON_DB_PASSWORD=for_local_its_not_needed__just_the_variable_needs_to_be_present
NEON_DB_HOST=for_local_its_not_needed__just_the_variable_needs_to_be_present
NEON_DB_PORT=5432

```

### 3. Run Docker Compose (recommended)

You need **Docker**, **Docker compose** and if on `Windows` might need **WSL** as well.

```bash
sudo docker compose  up --build
```

This spins up:

- Django app (backend)
- PostgreSQL database
- Redis broker
- Celery worker
- Celery beat scheduler
- Adminer

Migrate the Databases using these commands

First check the name of the backend container using this command
```bash
sudo docker ps
```
Then enter the **bash** with,

```bash
sudo docker exec -it <container_name> bash
```

and now migrate as you would on a regular Django app

```bash
python manage.py makemigrations
python manage.py migrate
```

**Create super user**

```bash
python manage.py createsuperuser
```

#### Note

If you get any `circular import` error while migrating then delete the migration files then comment out these fields inside user app's model.py first:

-

```
// Line 105
    bookmarks = models.ManyToManyField(
        "place.Place", related_name="bookmarks", blank=True
    )

// Line 347
    related_property = models.ForeignKey(
        "place.Place", on_delete=models.CASCADE, null=True, blank=True
    )

```

Now try to migrate again, start with **User** app followed by **Place** then the rest. After all these migrations please uncomment those fields and migrate the **User** again.

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
