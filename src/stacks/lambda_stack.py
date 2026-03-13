import aws_cdk as cdk
from aws_cdk import Stack, aws_lambda as _lambda
from constructs import Construct


class LambdaStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stage_name: str,
        project_slug: str,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        _lambda.Function(
            self,
            "GeneratorLambda",
            function_name=f"{project_slug}-{stage_name.lower()}-GeneratorLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("src/lambdas/generator_lambda/src"),
        )