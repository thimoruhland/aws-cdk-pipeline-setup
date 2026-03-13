from aws_cdk import Stack, aws_lambda as _lambda
from constructs import Construct


class LambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Haupt-Lambda
        generator_lambda = _lambda.Function(
            self,
            "GeneratorLambda",
            function_name="generator-lambda",  # fester Name
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("src/lambdas/generator_lambda/src"),
        )