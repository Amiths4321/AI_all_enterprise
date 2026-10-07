import json
import os
import sys
import traceback
import urllib.error
import urllib.request
from fastapi import FastAPI

app = FastAPI()

@app.get("/ready")
async def health_check():
    return {"status": "ok"}

@app.post("/query")
async def query_endpoint(payload: dict):
    return {"answer": "Sample response text from RAG engine."}

@app.get("/search")
async def search_endpoint(q: str = ""):
    return {"results": []}

@app.post("/chat")
async def chat_endpoint(payload: dict):
    return {"response": "Sample chat response."}

@app.get("/diagnostics")
async def diagnostics_endpoint():
    return {"records": 0, "status": "healthy"}


BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")
API_TOKEN = os.environ.get("API_TOKEN", "test-token")
TIMEOUT = int(os.environ.get("API_TIMEOUT", "60"))
DEBUG = os.environ.get("DEBUG") == "1"


def request(method, path, payload=None):
    url = BASE_URL + path
    data = None

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Accept": "application/json",
    }
    if data is not None:
        headers["Content-Type"] = "application/json"

    request_obj = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers=headers,
    )

    try:
        with urllib.request.urlopen(request_obj, timeout=TIMEOUT) as response:
            body = response.read().decode("utf-8")
            return response.status, parse_body(body)

    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        return exc.code, parse_body(body)

    except urllib.error.URLError as exc:
        raise ConnectionError(
            f"Server unreachable at {BASE_URL}: {exc.reason}"
        ) from exc


def parse_body(body):
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return body


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def show(title, status, data, limit=5000):
    print(f"\n[{title}]")
    print(f"HTTP {status}")
    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=2)[:limit])
    else:
        print(str(data)[:limit])


def test_diagnostics():
    status, data = request("GET", "/diagnostics")
    show("DIAGNOSTICS", status, data)

    require(status == 200, "Diagnostics endpoint failed.")
    require("records" in data, "Diagnostics response has no record count.")
    return True


def test_health():
    status, data = request("GET", "/ready")
    show("HEALTH", status, data)

    require(status == 200, "Readiness endpoint failed.")
    require(isinstance(data, dict), "Health response is not an object.")
    require("status" in data, "Health response has no 'status' field.")


def test_query():
    status, data = request(
        "POST",
        "/query",
        {
            "question": "What is the main purpose of this document?",
            "top_k": 5,
            "top_n": 3,
        },
    )
    show("QUERY", status, data)

    require(status == 200, "POST /query failed.")
    require(isinstance(data, dict), "Query response is not an object.")
    require("answer" in data, "Query response has no 'answer' field.")
    require(isinstance(data["answer"], str), "'answer' is not a string.")
    require(len(data["answer"].strip()) > 0, "Query returned an empty answer.")


def test_query_validation():
    status, data = request("POST", "/query", {})
    show("QUERY VALIDATION (empty body)", status, data, limit=1500)

    require(
        status == 422,
        f"Expected 422 for a missing 'question', got {status}.",
    )


def test_search_get():
    status, data = request("GET", "/search?q=policy")
    show("SEARCH GET", status, data)

    require(status == 200, "GET /search failed.")
    require(isinstance(data, dict), "Search response is not an object.")


def test_chat():
    status, data = request(
        "POST",
        "/chat",
        {"message": "Hello"},
    )
    show("CHAT", status, data)

    require(status == 200, "POST /chat failed.")
    require(isinstance(data, dict), "Chat response is not an object.")


def main():
    print("=" * 80)
    print("ENTERPRISE RAG API CONTRACT TEST")
    print(f"Target: {BASE_URL}")
    print("=" * 80)

    tests = [
        ("health", test_health),
        ("query", test_query),
        ("query_validation", test_query_validation),
        ("search_get", test_search_get),
        ("chat", test_chat),
        ("diagnostics", test_diagnostics),
    ]

    passed = 0

    for name, test in tests:
        try:
            test()
            print(f"\n{name}: PASS")
            passed += 1
        except Exception as exc:
            print(f"\n{name}: FAIL")
            print(f"  {type(exc).__name__}: {exc}")
            if DEBUG:
                traceback.print_exc()

    print("\n" + "=" * 80)
    print("API CONTRACT SUMMARY")
    print("=" * 80)
    print(f"Passed: {passed}/{len(tests)}")

    if passed != len(tests):
        print("API contract: FAIL")
        sys.exit(1)

    print("API contract: PASS")


if __name__ == "__main__":
    main()