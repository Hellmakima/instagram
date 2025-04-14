# 📸 InstaClone

A full-stack Instagram-like app built with FastAPI, MongoDB, and Next.js.  
Lightweight, modular, and ready to scale.

---

## ⚙️ Tech Stack

| Layer     | Tech        | Notes                           |
|-----------|-------------|---------------------------------|
| Frontend  | Next.js     | React-based, fast, SEO-friendly |
| Backend   | FastAPI     | Blazing-fast Python API         |
| Database  | MongoDB     | NoSQL, using embedded docs      |
| Auth      | OAuth (TBD) | Google, GitHub planned          |
| Media     | Local / TBD | Firebase or local file storage  |

---

## 🚧 Project Structure

```
.
├── backend/
│   ├── app/                  # FastAPI app
│   ├── models/               # MongoDB schemas
│   ├── routes/               # API endpoints
│   ├── auth/                 # OAuth/JWT logic
│   └── main.py               # App entrypoint
│
├── frontend/
│   ├── pages/                # Next.js pages
│   ├── components/           # Reusable UI parts
│   └── utils/                # API calls, helpers
│
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone Repo

```bash
git clone https://github.com/yourname/instaclone.git
cd instaclone
```

### 2. Run Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

- API Docs: `http://localhost:8000/docs`

### 3. Run Frontend

```bash
cd frontend
npm install
npm run dev
```

- App: `http://localhost:3000`

---

## ✅ Current Features

- [x] FastAPI + MongoDB setup
- [x] Basic OAuth integration
- [x] Monodoc data modeling
- [ ] Media upload (TBD)
- [ ] Post feed
- [ ] Comments + Likes
- [ ] User profiles

---

## 💡 Dev Notes

- Auth tokens handled via JWT (rotate + expire fast).
- Monorepo layout, can split later if needed.
- Media stored locally or via Firebase (no AWS for now).
- Scoped MVP: get core Insta-like functionality working first.

---

## 🛠 To-Do (Roadmap)

- [ ] Full auth flow w/ fallback email login
- [ ] Image upload route + compression
- [ ] Feed pagination + sorting
- [ ] Story system (optional stretch)
- [ ] CI/CD (GitHub Actions, optional)

---

## 📜 License

MIT — do whatever you want, just don't DMCA me if it blows up.

---

## ✌️ Author

Made by [@hellmakima](https://github.com/hellmakima)
