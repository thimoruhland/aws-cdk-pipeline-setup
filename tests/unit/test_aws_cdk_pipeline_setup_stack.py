import aws_cdk as core
import aws_cdk.assertions as assertions

from src.stacks.pipeline_stack_dev import DevPipelineStack

def test_stack_synthesizes():
    app = core.App()
    stack = DevPipelineStack(app, "DevPipelineStack")
    template = assertions.Template.from_stack(stack)
    print(template.to_json())