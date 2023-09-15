class InvalidUploadDirectoryException(Exception):
    "Raised when the given path is either a file or the directory doesn't exists"

    def __init__(
        self, message="The given path either doesn't exists or is not a directory"
    ) -> None:
        self.message = message
        super().__init__(self.message)
