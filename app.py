#!/usr/bin/env python3
import aws_cdk as cdk
from src.stacks.pipeline_stack_dev import DevPipelineStack
from src.stacks.pipeline_stack_prod import ProdPipelineStack

app = cdk.App()

project_name = app.node.try_get_context("project_name")
project_slug = app.node.try_get_context("project_slug")
repo_string = app.node.try_get_context("repo_string")
connection_arn = app.node.try_get_context("connection_arn")
pipelines_cfg = app.node.try_get_context("pipelines")

DevPipelineStack(
    app,
    f"{project_slug}-dev-pipeline",
    project_name=project_name,
    project_slug=project_slug,
    repo_string=repo_string,
    connection_arn=connection_arn,
    pipeline_cfg=pipelines_cfg["dev"],
    env=cdk.Environment(
        account=pipelines_cfg["dev"]["account"],
        region=pipelines_cfg["dev"]["region"],
    ),
)

ProdPipelineStack(
    app,
    f"{project_slug}-prod-pipeline",
    project_name=project_name,
    project_slug=project_slug,
    repo_string=repo_string,
    connection_arn=connection_arn,
    pipeline_cfg=pipelines_cfg["prod"],
    env=cdk.Environment(
        account=pipelines_cfg["prod"]["account"],
        region=pipelines_cfg["prod"]["region"],
    ),
)

app.synth()