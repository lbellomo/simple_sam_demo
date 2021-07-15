import json
import logging
from typing import List

import boto3

from dummy_model import Model

logger = logging.getLogger()
logger.setLevel(logging.INFO)

model = Model()
iris_keys = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

dynamodb = boto3.resource("dynamodb", region_name="sa-east-1")
table = dynamodb.Table("iris_table")


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


def parse_records(records: List[dict]) -> List[dict]:
    """Extract and parse the items from the event's records."""
    items = list()
    for record in records:
        if record["eventName"] != "INSERT":
            continue

        new_image = record["dynamodb"]["NewImage"]

        item = dict()
        for k, dict_v in new_image.items():

            # get the first value from the dict
            v = [i for i in dict_v.values()][0]

            if k != "id":
                # try
                v = float(v)

            item[k] = v
        items.append(item)
    return items


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

    context: object, required
        Lambda Context runtime methods and attributes

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict
    """
    items = parse_records(event["Records"])

    for item in items:
        # make prediction
        X = [[item[k] for k in iris_keys]]
        y = model.predict(X)[0]

        # update item
        try:
            table.update_item(
                Key={"id": item["id"]},
                UpdateExpression="set pred_target=:y",
                ExpressionAttributeValues={
                    ":y": y,
                },
                ReturnValues="UPDATED_NEW",
            )
        except Exception as e:
            logger.error(f"Error, can't update item: {e}")
            return create_output(500, "Internal error: can't update item in table.")

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
                # "location": ip.text.replace("\n", "")
            }
        ),
    }
