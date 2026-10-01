import hashlib
import json


def build_cache_key(
    question: str,
    user_id: str,
    role: str,
    department: str,
    top_k: int,
    top_n: int,
) -> str:

    payload = {
        "question": question,
        "user_id": user_id,
        "role": role,
        "department": department,
        "top_k": top_k,
        "top_n": top_n,
    }

    serialized = json.dumps(
        payload,
        sort_keys=True,
    )

    return hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()