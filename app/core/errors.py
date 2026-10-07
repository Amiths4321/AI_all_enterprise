class ApplicationError(Exception):

    code = "application_error"


class AuthenticationError(
    ApplicationError
):

    code = "authentication_error"


class AuthorizationError(
    ApplicationError
):

    code = "authorization_error"


class RetrievalError(
    ApplicationError
):

    code = "retrieval_error"


class GenerationError(
    ApplicationError
):

    code = "generation_error"


class DependencyError(
    ApplicationError
):

    code = "dependency_error"


class ConfigurationError(
    ApplicationError
):

    code = "configuration_error"