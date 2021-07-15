import json
import logging

logger = logging.getLogger()


def create_output(status_code: int, message: str) -> dict:
    logger.info(message)
    return {
        "statusCode": status_code,
        "body": json.dumps(
            {
                "message": message,
            }
        ),
    }
