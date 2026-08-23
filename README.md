# StaffConnect — Internal Staff Portal

A Django web application for employee announcements, profile management, and
content publishing, built for NovaTech Corporation. Containerised with Docker
and ready for deployment to Kubernetes.

## Features
- Employee registration, login/logout, and email-based password reset
- Profile management with department, bio, and avatar upload
- Publish, edit, and delete company announcements (posts)
- Paginated announcements list with author and date
- HR admin panel for managing all users, profiles, and posts
- All secrets loaded from environment variables — nothing hardcoded

## Tech Stack
Python 3.11 · Django 4.2 · SQLite (dev) · Pillow · python-decouple · Docker

---

## 1. Local Setup (without Docker)
⚠️ Python version: This project requires Python 3.11. Newer versions (3.13/3.14) are not fully compatible with Django 4.2 and will cause errors in the admin panel. Create the virtual environment with the correct version, e.g.:
py -3.11 -m venv venv
```bash
git clone <your-repo-url>
cd staffconnect

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env              # then edit .env with your own values

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/`
for the admin panel.

## 2. Environment Variables

All configuration lives in `.env` (see `.env.example` for the full template,
values redacted). Never commit `.env` — it's in `.gitignore`.

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django cryptographic signing key |
| `DEBUG` | `True`/`False` — must be `False` in production |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames |
| `DB_NAME` | SQLite filename (dev) |
| `MAX_AVATAR_SIZE_MB` | Max profile photo upload size |
| `EMAIL_BACKEND` | `console` for dev, `smtp` for real email delivery |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS` | SMTP server settings |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | SMTP credentials (used for password reset emails) |
| `DEFAULT_FROM_EMAIL` | "From" address for outgoing email |

## 3. Docker — Build & Run

```bash
# Build the image
docker build -t staffconnect:v1.0.0 .

# Run the container (reads secrets from .env, never baked into the image)
docker run --rm -p 8000:8000 --env-file .env staffconnect:v1.0.0
```

The app will be available at `http://localhost:8000/`.

Uploaded media persists across restarts via the `/app/media` volume declared
in the Dockerfile — mount a named volume or host directory in production:

```bash
docker run --rm -p 8000:8000 --env-file .env \
  -v staffconnect_media:/app/media \
  staffconnect:v1.0.0
```

## 4. Push to a Registry

```bash
docker tag staffconnect:v1.0.0 <your-dockerhub-username>/staffconnect:v1.0.0
docker push <your-dockerhub-username>/staffconnect:v1.0.0
```

Public registry URL: `https://hub.docker.com/r/<your-dockerhub-username>/staffconnect`

## 5. Project Structure

```
staffconnect/
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── manage.py
├── config/          # settings, root urls, wsgi
├── users/           # Profile model, auth views, password reset
├── posts/           # Post model, CBV CRUD for announcements
├── templates/        # base.html, users/, posts/, 404.html
├── static/css/       # global stylesheet
└── media/            # user-uploaded avatars (gitignored)
```

## 6. Notes on Security
- CSRF tokens on every form; logout and delete are POST-only.
- `@login_required` / `LoginRequiredMixin` on all protected views.
- `UserPassesTestMixin` ensures users can only edit/delete their own posts.
- Avatar uploads are validated server-side (extension whitelist + max size).
- All dependency versions in `requirements.txt` are pinned; Docker base
  image tag is pinned (`python:3.11-slim`, no `:latest`).
