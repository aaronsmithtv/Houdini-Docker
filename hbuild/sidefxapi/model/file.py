from requests import Response


class File:
    """
    Pass parameters of this type to API functions as a way of uploading
    large files. Note that these File parameters must be specified by keyword
    arguments when calling the functions.
    """
    def __init__(self, filename: str):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, "rb")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def read(self, size=-1):
        return self.file.read(size)

    def seek(self, offset, whence=0):
        self.file.seek(offset, whence)

    def tell(self):
        return self.file.tell()


class ResponseFile:
    """This object is returned from API functions that stream binary content.
    Call the API function from a `with` statement, and call the read method
    on the object to read the data in chunks.
    """
    def __init__(self, response: Response):
        self.response = response

    def __enter__(self):
        return self.response.raw

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.response.close()
