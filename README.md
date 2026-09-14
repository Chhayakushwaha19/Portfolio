# Chhaya Kushwaha — Full-Stack Developer Portfolio

A dark-themed (with light mode) developer portfolio: static frontend +
FastAPI backend backed by a SQL database for the contact form.

## Structure

```
dev-portfolio/
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   ├── js/script.js
│   └── assets/avatar-placeholder.svg   ← replace with your real photo
└── backend/
    ├── main.py         (FastAPI app + routes)
    ├── database.py      (SQLAlchemy engine/session)
    ├── models.py         (SQL table definition)
    ├── schemas.py        (request/response validation)
    └── requirements.txt
```

## 1. Run the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

This starts the API at `http://127.0.0.1:8000` and automatically creates
`portfolio.db` — a SQLite database — with a `contact_messages` table on
first run. No separate database server needed.

Check it's working:
- `http://127.0.0.1:8000/api/health`
- `http://127.0.0.1:8000/docs` — interactive API docs (Swagger UI)

To use PostgreSQL/MySQL instead of SQLite later, set an environment
variable before starting the server:
```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/portfolio"
```

## 2. Run the frontend

Open `frontend/index.html` directly in a browser, or serve it:

```bash
cd frontend
python -m http.server 5500
```

Visit `http://127.0.0.1:5500`. The contact form posts to
`http://127.0.0.1:8000/api/contact` — update `API_BASE` at the top of
`js/script.js` once you deploy the backend somewhere else.

## 3. Personalize it

- **Photo**: replace `frontend/assets/avatar-placeholder.svg` with your
  own image (e.g. `profile.jpg`), then update the `src` on `#hero-photo`
  in `index.html` to match.
- **GitHub links**: every `github.com/yourusername` placeholder (in
  `index.html` and `backend/main.py`) — swap in your real GitHub URL.
- **Projects**: edit the three sample cards in `index.html` (and the
  matching `PROJECTS` list in `backend/main.py`) with your real repos,
  descriptions, and tech tags.
- **Resume/CV**: if you want a "Download résumé" button, drop a PDF into
  `frontend/assets/` and link to it from the hero actions.
- **Colors**: the whole palette is defined as CSS variables at the top
  of `style.css` (`:root` for dark, `html[data-theme="light"]` for
  light) — change the `--accent` and `--bg` values to restyle everything
  at once.

## Notes on the contact form

- Submissions are validated with Pydantic and stored as rows in the
  `contact_messages` SQL table (id, name, email, message, created_at).
- `GET /api/contact` lists saved messages — handy for local development,
  but it has **no authentication**. Protect or remove this route before
  deploying publicly.
- To get actual email notifications when someone writes in, add an SMTP
  or email-API call inside the `create_contact` function in `main.py`.

## Features included

- Dark/light theme toggle (persisted in the browser)
- Typing animation cycling through your roles
- Scroll-reveal animations on each section (skipped automatically if the
  visitor's OS has "reduce motion" turned on)
- Fully responsive layout, down to small phones, with a mobile nav menu
- Project cards, skills terminal panel, education timeline, and a
  GitHub/LinkedIn "Connect" section
