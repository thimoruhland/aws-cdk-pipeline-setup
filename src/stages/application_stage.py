from aws_cdk import Stage
from constructs import Construct
from src.stacks.lambda_stack import LambdaStack


class ApplicationStage(Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        LambdaStack(self, "LambdaStack")