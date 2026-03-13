#!/usr/bin/env python3
import aws_cdk as cdk
from src.stacks.pipeline_stack import PipelineStack

app = cdk.App()

PipelineStack(
    app,
    "PipelineStack",
    env=cdk.Environment(
        account="735910967196",
        region="eu-central-1",
    ),
)

app.synth()