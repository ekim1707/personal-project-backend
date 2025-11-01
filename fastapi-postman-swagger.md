# FastAPI — Swagger & Postman Collection (Concise Guide)

## Where to find your API docs
- **Swagger UI (interactive):** `http://<host>:<port>/docs`
- **ReDoc (read-only):** `http://<host>:<port>/redoc`
- **OpenAPI JSON (source of truth):** `http://<host>:<port>/openapi.json`

> If you mounted FastAPI at a subpath (e.g., `/api`), prefix the routes: `/api/docs`, `/api/redoc`, `/api/openapi.json`.

---

## Export the OpenAPI spec
```bash
# Save the OpenAPI JSON from a running app
curl -s http://localhost:8000/openapi.json -o openapi.json
```

If you need to **generate OpenAPI without running** (e.g., in a script), you can build it explicitly:

```python
# scripts/generate_openapi.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import json

from myapp.main import app  # import your existing FastAPI() instance

openapi_schema = get_openapi(
    title=app.title or "FastAPI",
    version=getattr(app, "version", "0.1.0"),
    description=getattr(app, "description", None),
    routes=app.routes,
)
with open("openapi.json", "w") as f:
    json.dump(openapi_schema, f, indent=2)
print("Wrote openapi.json")
```

Run with: `python scripts/generate_openapi.py`

---

## Create a Postman collection from OpenAPI
**Option A — Postman UI (quickest)**  
1) Open Postman → **Import** → **File/URL** → select `openapi.json`.  
2) Choose **Generate collection** → pick **Base URL** variable if prompted → **Import**.

**Option B — CLI (repeatable in CI)**
```bash
# Requires Node.js
npx openapi-to-postmanv2 -s openapi.json -o fastapi.postman_collection.json --pretty
```

Optional: also create an environment file with your base URL and tokens:
```json
{
  "id": "fastapi-local",
  "name": "fastapi-local",
  "values": [
    { "key": "base_url", "value": "http://localhost:8000", "enabled": true },
    { "key": "token", "value": "{{YOUR_TOKEN}}", "enabled": true }
  ],
  "_postman_variable_scope": "environment",
  "_postman_exported_using": "Postman/CLI"
}
```

---

## Recommended Postman setup
- **Collection Variables**
  - `base_url` = `http://localhost:8000` (or your deployed URL)
  - `token` = bearer/API token if your API uses auth
- **Pre-request Script** (if you need auth):
```js
pm.request.headers.add({
  key: "Authorization",
  value: `Bearer ${pm.environment.get("token")}`
});
```
- **Per-request URLs:** `{{base_url}}/path/to/endpoint`

---

## Keep Swagger (OpenAPI) accurate
- Add metadata to your app:
  ```python
  app = FastAPI(title="Your Service", version="1.2.3", description="API for ...")
  ```
- Document endpoints:
  ```python
  @app.get("/items/{item_id}", response_model=Item, tags=["items"], summary="Get an item")
  async def get_item(item_id: int):
      ...
  ```
- Provide examples & responses:
  ```python
  from fastapi import Body
  @app.post("/items", response_model=Item, tags=["items"])
  async def create_item(payload: ItemCreate = Body(..., example={"name":"Widget","price":9.99})):
      ...
  ```

---

## Troubleshooting
- **404 on `/docs`**: Check `FastAPI(docs_url=None, redoc_url=None)`—re-enable or set custom paths.  
- **Empty/partial OpenAPI**: Ensure all routers are included before generating (`app.include_router(...)`).  
- **Auth not applied in Postman**: Verify `Authorization` header or Postman auth tab; confirm token variable is set.  
- **CORS issues in Swagger UI**: Add `CORSMiddleware` in `main.py`.

```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Quick Checklist
- [ ] Visit `/docs` and `/redoc` to confirm endpoints.  
- [ ] Export `openapi.json` (curl or script).  
- [ ] Import to Postman (UI) **or** build `fastapi.postman_collection.json` via CLI.  
- [ ] Add `base_url` and `token` variables; test key flows.  
- [ ] Keep endpoint metadata up to date (tags, responses, examples).

---

**Paths recap**  
- Swagger UI: `/docs`  
- ReDoc: `/redoc`  
- OpenAPI JSON: `/openapi.json`  
- Postman Collection (generated): `fastapi.postman_collection.json`
