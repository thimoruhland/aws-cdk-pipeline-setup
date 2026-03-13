import aws_cdk as cdk
from aws_cdk import Stage
from constructs import Construct
from src.stacks.lambda_stack import LambdaStack


class ApplicationStage(Stage):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        stage_name: str,
        project_name: str,
        project_slug: str,
        env: cdk.Environment,
        **kwargs
    ):
        super().__init__(scope, construct_id, env=env, **kwargs)

        LambdaStack(
            self,
            f"{project_slug}-{stage_name.capitalize()}",
            stage_name=stage_name,
            project_name=project_name,
            project_slug=project_slug,
            env=env,
        )