import json
import hashlib
import logging

import boto3


logger = logging.getLogger()
logger.setLevel(logging.INFO)

iris_keys = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

# TODO: don't hardcode region or table name. Read from env variable
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


def create_hash(item: dict) -> str:
    join_values = "".join(str(value) for value in item.values())
    return hashlib.md5(join_values.encode("utf-8")).hexdigest()


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

    if not event["body"]:
        return create_output(400, "Invalid body: body is empty.")

    try:
        item = json.loads(event["body"])
    except json.JSONDecodeError:
        return create_output(400, "Invalid body: can't decode body.")

    for key in iris_keys:
        if key not in item:
            return create_output(400, f"Invalid body: missing key {key} in body.")
        try:
            float(item[key])
        except ValueError:
            return create_output(400, f"Invalid body: can't parse {key} to float.")

    item["id"] = create_hash(item)

    try:
        table.put_item(Item=item)
    except Exception as e:
        logger.error(f"Error, can't insert item: {e}")
        return create_output(500, "Internal error: can't insert item in table.")

    return create_output(200, "Item created.")
