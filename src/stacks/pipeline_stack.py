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
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.connection(
                    "thimoruhland/aws-cdk-pipeline-setup",
                    "main",
                    connection_arn="arn:aws:codeconnections:eu-central-1:735910967196:connection/47dc864b-e5a7-4f37-ac09-54d70e37c623",
                ),
                commands=[
                    "python -m pip install -r requirements.txt",
                    "npm install -g aws-cdk",
                    "cdk synth",
                ],
            ),
        )

        pipeline.add_stage(ApplicationStage(self, "Prod"))