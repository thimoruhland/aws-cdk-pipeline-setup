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
        *,
        project_name: str,
        project_slug: str,
        repo_string: str,
        connection_arn: str,
        pipeline_cfg: dict,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        dev_env = cdk.Environment(
            account=pipeline_cfg["account"],
            region=pipeline_cfg["region"],
        )

        source = pipelines.CodePipelineSource.connection(
            repo_string,
            pipeline_cfg["branch"],
            connection_arn=connection_arn,
            trigger_on_push=True,
        )

        pipeline = pipelines.CodePipeline(
            self,
            f"{project_slug}-dev-pipeline-construct",
            pipeline_name=f"{project_slug}-dev-pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=source,
                install_commands=[
                    "python -m pip install -r requirements.txt",
                    "python -m pip install -r requirements-dev.txt",
                    "npm install -g aws-cdk",
                ],
                commands=[
                    "cdk synth",
                ],
            ),
        )

        pipeline.add_wave(
            "QualityChecks",
            pre=[
                pipelines.ShellStep(
                    "RuffCheck",
                    input=source,
                    install_commands=[
                        "python -m pip install -r requirements.txt",
                        "python -m pip install -r requirements-dev.txt",
                    ],
                    commands=[
                        "ruff check src",
                    ],
                ),
                pipelines.ShellStep(
                    "MypyCheck",
                    input=source,
                    install_commands=[
                        "python -m pip install -r requirements.txt",
                        "python -m pip install -r requirements-dev.txt",
                    ],
                    commands=[
                        "mypy src",
                    ],
                ),
                pipelines.ShellStep(
                    "Pytest",
                    input=source,
                    install_commands=[
                        "python -m pip install -r requirements.txt",
                        "python -m pip install -r requirements-dev.txt",
                    ],
                    commands=[
                        "pytest",
                    ],
                ),
            ],
        )

        pipeline.add_stage(
            ApplicationStage(
                self,
                "dev",
                stage_name="dev",
                project_slug=project_slug,
                env=dev_env,
            )
        )