import boto3
import logging
import os
import yaml
import json

from my_lambda_package.utility import Utility


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _load_config(filename='config.yaml'):
    """Loads the configuration file."""
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)), 'r') as f:
        config = yaml.load(f)
        logger.info('Loaded config: {0}'.format(config))
    return config


APPLICABLE_RESOURCES = ["AWS::EC2::Instance"]


def evaluate_compliance(configuration_item):
    if configuration_item["resourceType"] not in APPLICABLE_RESOURCES:
        return "NOT_APPLICABLE"

    # user_name = configuration_item["configuration"]["userName"]

    # iam = boto3.client("iam")
    # mfa = iam.list_mfa_devices(UserName=user_name)

    # if len(mfa["MFADevices"]) > 0:
    return "COMPLIANT"
    # else:
    #     return "NON_COMPLIANT"


def handler(event, context):
    invoking_event = json.loads(event["invokingEvent"])
    logger.info(invoking_event)
    configuration_item = invoking_event["configurationItem"]
    result_token = "No token found."
    if "resultToken" in event:
        result_token = event["resultToken"]

    config = boto3.client("config")
    config.put_evaluations(
        Evaluations=[
            {
                "ComplianceResourceType":
                    configuration_item["resourceType"],
                "ComplianceResourceId":
                    configuration_item["resourceId"],
                "ComplianceType":
                    evaluate_compliance(configuration_item),
                "Annotation":
                    "Foo bar",
                "OrderingTimestamp":
                    configuration_item["configurationItemCaptureTime"]
            },
        ],
        ResultToken=result_token
    )


if __name__ == '__main__':
    from my_lambda_package.localcontext import LocalContext
    handler(None, LocalContext())
