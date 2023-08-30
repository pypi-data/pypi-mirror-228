class VolStreetException(Exception):
    """Base class for other exceptions."""

    def __init__(self, message="VolStreet Exception", code=500):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ApiKeyNotFound(VolStreetException):
    """Exception raised for missing API Key in the environment variables."""

    def __init__(self, message="API Key not found", code=404):
        super().__init__(message, code)


class OptionModelInputError(VolStreetException):
    """Exception raised for errors in the inputs for Black Scholes model."""

    def __init__(self, message="Invalid inputs for Black Scholes model", code=3500):
        super().__init__(message, code)


class ScripsLocationError(VolStreetException):
    """Exception raised when unable to locate something in the scrips file."""

    def __init__(
        self, message="Could not index scrips file", code=501, additional_info=""
    ):
        additional_info = (
            f"\nAdditional info: {additional_info}" if additional_info else ""
        )
        message = message + additional_info
        super().__init__(message, code)
