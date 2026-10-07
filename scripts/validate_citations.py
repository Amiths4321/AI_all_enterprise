
import re


SOURCE_PATTERN = re.compile(
    r"\[Source\s+(\d+)\]"
)


def validate(answer, source_count):

    citations = SOURCE_PATTERN.findall(
        answer
    )

    invalid = []

    for citation in citations:

        number = int(citation)

        if number < 1 or number > source_count:
            invalid.append(number)

    return {
        "has_citation": bool(citations),
        "citations": [
            int(value)
            for value in citations
        ],
        "invalid": invalid,
        "valid": not invalid,
    }


def main():

    answer = input(
        "Paste answer:\n"
    )

    source_count = int(
        input(
            "Number of sources: "
        )
    )

    result = validate(
        answer,
        source_count,
    )

    print("\nValidation:")
    print(result)


if __name__ == "__main__":
    main()
