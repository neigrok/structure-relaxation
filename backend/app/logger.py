import logging


def setup_logger() -> logging.Logger:
    # Remove default handlers
    logging.getLogger().handlers = []

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Main app logger
    logger = logging.getLogger("structure_relaxation")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(handler)

    # Force uvicorn to use same format
    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.handlers = [handler]
        uvicorn_logger.propagate = False

    return logger


logger = setup_logger()
