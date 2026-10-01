from pathlib import Path

from app.core.container import ApplicationContainer


documents = [
    {
        "id": "hr-001",
        "document": (
            "Employees receive 20 days of annual leave "
            "per calendar year."
        ),
        "metadata": {
            "source": "hr_policy.txt",
        },
    },
    {
        "id": "hr-002",
        "document": (
            "Employees must submit annual leave requests "
            "through the HR portal."
        ),
        "metadata": {
            "source": "leave_process.txt",
        },
    },
    {
        "id": "benefits-001",
        "document": (
            "Employees receive health insurance coverage "
            "under the company benefits program."
        ),
        "metadata": {
            "source": "benefits.txt",
        },
    },
]


config_path = Path("configs/development.json")

container = ApplicationContainer(
    documents=documents,
    config_path=str(config_path),
)

service = container.build()


result = service.answer(
    question="How many annual leave days do employees receive?",
    required_evidence=[
        "Employees receive 20 days of annual leave."
    ],
    top_k=10,
    top_n=3,
)


print("\nANSWER")
print(result["answer"])

print("\nEVIDENCE")
print(result["evidence"])