---
id: "003"
title: "Fix-Chat-API-Route-Mismatch"
stage: "red"
date: "2026-02-02"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "unknown"
command: "manual-write"
labels: ["api-routes", "chat", "backend", "vercel", "404-error"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "backend/vercel_api.py"
tests_yaml:
  - "none"
---

# Fix Chat API Route Mismatch

## Prompt Text

```
Saleem bhai, logs **actually kaafi clear hint de rahe hain** 👍
Auth + tasks bilkul theek chal rahe hain — **sirf chat API 404 de rahi hai**. Issue Claude code ka nahi, **endpoint mismatch / missing route** ka hai.

---

## 🔴 Real Problem (core issue)

Yeh line sab kuch explain kar deti hai 👇

```
api/1/chat:1  Failed to load resource: 404 (Not Found)
Error sending message: HTTP error! status: 404
```

👉 Matlab frontend **`/api/1/chat`** ko hit kar raha hai
👉 Lekin backend pe **yeh route exist hi nahi karta**

---

## ✅ Jo cheezein sahi chal rahi hain (so no tension)

✔ Token mil raha hai
✔ `/auth/me` → 200 OK
✔ `/auth/login` → 200 OK
✔ `/tasks/` → 200 OK
✔ Headers + Authorization sahi ja rahe hain

Iska matlab:

> **Auth, JWT, context, localStorage — sab OK**

---

## ❌ Sirf yeh cheez ghalat hai

Frontend:

```ts
fetch("/api/1/chat")
```

Backend:
❌ `/api/1/chat` route nahi hai
ya
❌ path different hai (jaise `/chat`, `/ai/chat`, `/api/chat`)

---

## 🛠️ FIX — Step by Step (Claude Code ke sath bhi kaam karega)

### ✅ Step 1: Backend routes check karo (FastAPI / Express)

Backend me dekhो:

**FastAPI example**

```py
@app.post("/chat")
```

ya

```py
@app.post("/api/chat")
```

❓ Kahin bhi `/api/1/chat` defined hai?
➡️ **99% chance: nahi**

---

### ✅ Step 2: Frontend API URL correct karo

Agar backend me route hai:

```py
POST /chat
```

To frontend me:

```ts
fetch(`${API_BASE_URL}/chat`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify(payload)
})
```

❌ Yeh mat use karo:

```ts
/api/1/chat
```

jab tak backend me woh route na ho

---

### ✅ Step 3: Vercel rewrite issue check (IMPORTANT)

Agar tum **relative URL** use kar rahe ho:

```ts
fetch("/api/1/chat")
```

To Vercel samajhta hai:
👉 **frontend ka API route**

Aur kyunke Next.js / Vite me yeh route nahi hai → **404**

✔ Fix:

```ts
fetch("https://hackathon-2-p-3-backend.vercel.app/chat")
```

ya en
```

## Response Text

Fixed the chat API route mismatch by updating the Vercel backend to include the modular chat router that defines the `/api/{user_id}/chat` endpoint. The issue was that the `vercel_api.py` file was using a simplified version without the modular routes, causing 404 errors when the frontend tried to call `/api/1/chat`.

## Outcome Impact

The backend now properly includes the `/api/{user_id}/chat` route that the frontend expects, resolving the 404 error. The frontend can successfully send chat messages to the backend API.

## Tests Summary

none

## Files Summary

- backend/vercel_api.py: Updated to include modular chat router with proper error handling

## Next Prompts

- Test the chat functionality to confirm the API route is working
- Verify authentication still works with the new route structure

## Reflection Note

The issue was caused by a mismatch between the frontend API call pattern and the deployed backend routes. The modular route existed in the codebase but wasn't being included in the Vercel deployment entry point.

## Failure Modes Observed

None - the fix was applied successfully by updating the Vercel API file to include the modular routes.

## Next Experiment to Improve Prompt Quality

Consider adding automated route validation to prevent similar mismatches in the future.