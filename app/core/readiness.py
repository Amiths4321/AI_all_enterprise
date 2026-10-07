class ReadinessChecker:

    def __init__(
        self,
        health_checker,
        repository,
        generator,
    ):
        self.health_checker = (
            health_checker
        )
        self.repository = repository
        self.generator = generator

    def check(self):

        chroma = (
            self.health_checker.check_repository(
                self.repository
            )
        )

        ollama = (
            self.health_checker.check_ollama(
                self.generator
            )
        )

        ready = (
            chroma.healthy
            and ollama.healthy
        )

        return {
            "ready": ready,
            "dependencies": {
                "chroma": {
                    "healthy": chroma.healthy,
                    "detail": chroma.detail,
                },
                "ollama": {
                    "healthy": ollama.healthy,
                    "detail": ollama.detail,
                },
            },
        }