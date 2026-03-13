import aws_cdk as cdk
from aws_cdk import Stack
from aws_cdk import pipelines
from constructs import Construct
from src.stages.application_stage import ApplicationStage


class DevPipelineStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        project_slug: str,
        project_name: str,
        repo_string: str,
        connection_arn: str,
        stage_configs: dict,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        pipeline = pipelines.CodePipeline(
            self,
            f"{project_slug}Pipeline",
            pipeline_name=f"{project_slug}-pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.connection(
                    repo_string,
                    "main",
                    connection_arn=connection_arn,
                ),
                commands=[
                    "python -m pip install -r requirements.txt",
                    "npm install -g aws-cdk",
                    "cdk synth",
                ],
            ),
        )

        dev_env = cdk.Environment(
            account=stage_configs["dev"]["account"],
            region=stage_configs["dev"]["region"],
        )

        prod_env = cdk.Environment(
            account=stage_configs["prod"]["account"],
            region=stage_configs["prod"]["region"],
        )

        dev_stage = ApplicationStage(
            self,
            "dev",
            stage_name="dev",
            project_name=project_name,
            project_slug=project_slug,
            env=dev_env,
        )

        prod_stage = ApplicationStage(
            self,
            "prod",
            stage_name="prod",
            project_name=project_name,
            project_slug=project_slug,
            env=prod_env,
        )

        pipeline.add_stage(dev_stage)

        pipeline.add_stage(
            prod_stage,
            pre=[
                pipelines.ManualApprovalStep(
                    "PromoteToProd"
                )
            ]
        )