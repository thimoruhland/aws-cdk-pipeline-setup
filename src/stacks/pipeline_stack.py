from aws_cdk import Stack
from constructs import Construct
from aws_cdk import pipelines
from src.stages.application_stage import ApplicationStage


class PipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        pipeline = pipelines.CodePipeline(
            self,
            "CdkPipeline",
            pipeline_name="aws-cdk-pipeline-setup-dev",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.connection(
                    "thimoruhland/aws-cdk-pipeline-setup",
                    "main",
                    connection_arn="arn:aws:codeconnections:eu-central-1:735910967196:connection/6e7a13bc-e807-4c94-9f5a-c46681d94a1a",
                ),
                commands=[
                    "pip install -r requirements.txt",
                    "npm install -g aws-cdk",
                    "cdk synth",
                ],
            ),
        )

        pipeline.add_stage(ApplicationStage(self, "Prod"))