import httpx
r = httpx.post("http://localhost:8000/api/v1/search", json={"query": "kawthar"})
print(r.status_code)
print(r.text[:800])
