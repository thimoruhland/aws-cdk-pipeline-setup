import aws_cdk as cdk
from aws_cdk import Stack
from aws_cdk import pipelines
from constructs import Construct
from src.stages.application_stage import ApplicationStage


class ProdPipelineStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        project_slug: str,
        repo_string: str,
        connection_arn: str,
        pipeline_cfg: dict,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        prod_env = cdk.Environment(
            account=pipeline_cfg["account"],
            region=pipeline_cfg["region"],
        )

        pipeline = pipelines.CodePipeline(
            self,
            f"{project_slug}-prod-pipeline",
            pipeline_name=f"{project_slug}-prod-pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.connection(
                    repo_string,
                    pipeline_cfg["branch"],
                    connection_arn=connection_arn,
                    trigger_on_push=False,
                ),
                commands=[
                    "python -m pip install -r requirements.txt",
                    "npm install -g aws-cdk",
                    "cdk synth",
                ],
            ),
        )

        pipeline.add_stage(
            ApplicationStage(
                self,
                "prod",
                stage_name="prod",
                project_slug=project_slug,
                env=prod_env,
            ),
            pre=[
                pipelines.ManualApprovalStep("ApproveProdDeployment")
            ]
        )