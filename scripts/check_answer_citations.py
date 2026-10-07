import re


SOURCE_PATTERN = re.compile(r"\[Source\s+(\d+)\]")


def validate_answer(answer, source_count):
    citations = [
        int(value)
        for value in SOURCE_PATTERN.findall(answer)
    ]

    invalid = [
        value
        for value in citations
        if value < 1 or value > source_count
    ]

    return {
        "has_citation": bool(citations),
        "citations": citations,
        "invalid": invalid,
        "valid": bool(citations) and not invalid,
    }


def main():
    answer = input("Paste answer:\n\n")

    source_count = int(
        input("\nNumber of sources: ")
    )

    result = validate_answer(
        answer,
        source_count,
    )

    print("\n" + "=" * 60)
    print("CITATION VALIDATION")
    print("=" * 60)

    print(f"Has citation: {result['has_citation']}")
    print(f"Citations: {result['citations']}")
    print(f"Invalid: {result['invalid']}")
    print(f"Valid: {result['valid']}")


if __name__ == "__main__":
    main()