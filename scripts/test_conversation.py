import json
import urllib.error
import urllib.request


BASE_URL = "http://127.0.0.1:8000"
SESSION_ID = "conversation-test"


def chat(question):
    payload = {
        "session_id": SESSION_ID,
        "question": question,
        "mode": "multivector",
        "expand": False,
    }

    request = urllib.request.Request(
        BASE_URL + "/chat",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=120,
        ) as response:
            return response.status, json.loads(
                response.read().decode("utf-8")
            )

    except urllib.error.HTTPError as exc:
        print(
            f"HTTP {exc.code}: "
            f"{exc.read().decode('utf-8')}"
        )
        return exc.code, {}


def main():
    print("=" * 80)
    print("ENTERPRISE RAG CONVERSATION TEST")
    print("=" * 80)

    questions = [
        "What is the main purpose of this handbook?",
        "Who is it intended for?",
        "How can they use the details?",
    ]

    for index, question in enumerate(
        questions,
        start=1,
    ):
        print(f"\n[{index}] User:")
        print(question)

        status, data = chat(question)

        if status != 200:
            print(f"FAILED: HTTP {status}")
            raise SystemExit(1)

        answer = data.get("answer", "")

        print("\nAssistant:")
        print(answer)

        if not answer.strip():
            print("\nFAILED: empty answer")
            raise SystemExit(1)

    print("\n" + "=" * 80)
    print("CONVERSATION TEST PASSED")
    print("=" * 80)


if __name__ == "__main__":
    main()