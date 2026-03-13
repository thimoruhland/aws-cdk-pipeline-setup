#!/usr/bin/env python3
import aws_cdk as cdk
from src.stacks.pipeline_stack_dev import DevPipelineStack

app = cdk.App()

project_name = app.node.try_get_context("project_name")
project_slug = app.node.try_get_context("project_slug")
repo_string = app.node.try_get_context("repo_string")
connection_arn = app.node.try_get_context("connection_arn")
stage_configs = app.node.try_get_context("stages")

DevPipelineStack(
    app,
    project_slug,
    project_name=project_name,
    project_slug=project_slug,
    repo_string=repo_string,
    connection_arn=connection_arn,
    stage_configs=stage_configs,
    env=cdk.Environment(
        account=stage_configs["dev"]["account"],
        region=stage_configs["dev"]["region"],
    ),
)

app.synth()