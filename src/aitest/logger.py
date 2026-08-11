import logging

class Logger:
    def __init__(self, name=__name__):
        # Set up logger
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(logging.INFO)

        if not self.__logger.handlers:
            # Log to File
            file_name = f"Logs/{name}.log"
            file_handler = logging.FileHandler(file_name, "w")
            self.__logger.addHandler(file_handler)

    def get_logger(self):
        return self.__logger