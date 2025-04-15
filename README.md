# 📸 InstaClone

Full-stack Instagram clone using FastAPI, MongoDB, and Next.js.  
Clean, modular, and easy to scale.
_*This file hath been wrought by GPT. Pray, forgive any follies or errours thou mayst find therein.*_

---

## ⚙️ Stack

| Layer     | Tech      | Notes                     |
|-----------|-----------|---------------------------|
| Frontend  | Next.js   | Runs on port `3000`       |
| Backend   | FastAPI   | Runs on port `5000`       |
| DB        | MongoDB   | NoSQL, embedded docs      |
| Auth      | TBD       | Google/GitHub planned     |
| Media     | TBD       | Local or Firebase storage |

---

## 🚀 Get Started

### 1. Clone
```bash
git clone https://github.com/yourname/instaclone.git
cd instaclone
```

### 2. Backend

```bash
cd backend
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 5000
```

- Docs: [http://localhost:5000/docs](http://localhost:5000/docs)

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

- App: [http://localhost:3000](http://localhost:3000)

---

## ✅ Features

- [x] FastAPI + MongoDB base
- [ ] Monodoc modeling
- [ ] OAuth placeholder
- [ ] Image upload
- [ ] Feed
- [ ] Likes + comments
- [ ] Profiles

---

## 🧠 Notes

- JWT-based auth (rotates fast)
- Local media for now (Firebase later maybe)
- Keeping it MVP-first — no bloat

---

## 🛠 Roadmap

- [ ] Full auth flow
- [ ] Upload route + compression
- [ ] Paginated feed
- [ ] CI/CD (maybe)

---

## 📜 License

MIT — use it, break it, fix it, ship it.

---

## ✌️ Author

Made by [@hellmakima](https://github.com/hellmakima)
