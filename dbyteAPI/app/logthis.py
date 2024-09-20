import logging
import uuid

class APILogger:
    def __init__(self):
        self.logger = logging.getLogger("dbyteLog")
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('dbyteLog: %(asctime)s - %(run_id)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log(self, level, message):
        run_id = str(uuid.uuid4())
        extra = {'run_id': run_id}
        self.logger.log(level, message, extra=extra)

# Usage example
if __name__ == "__main__":
    api_logger = APILogger()
    api_logger.log(logging.INFO, "This is an info message")
    api_logger.log(logging.ERROR, "This is an error message")
