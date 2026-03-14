import aws_cdk as core
import aws_cdk.assertions as assertions

from src.stacks.pipeline_stack_dev import DevPipelineStack

def test_stack_synthesizes():
    app = core.App()
    stack = DevPipelineStack(
        app,
        "DevPipelineStack",
        project_name="test-project",
        project_slug="test-slug",
        repo_string="test/repo",
        connection_arn="arn:aws:codestar-connections:us-east-1:123456789012:connection/test-connection",
        pipeline_cfg={
            "account": "735910967196",
            "region": "eu-central-1",
            "branch": "devlop"
        }
    )
    template = assertions.Template.from_stack(stack)
    print(template.to_json())