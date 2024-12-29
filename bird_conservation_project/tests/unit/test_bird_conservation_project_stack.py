import aws_cdk as core
import aws_cdk.assertions as assertions

from bird_conservation_project.bird_conservation_project.bird_conservation_project_stack import BirdConservationProjectStack

# example tests. To run these tests, uncomment this file along with the example
# resource in bird_conservation_project/bird_conservation_project_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = BirdConservationProjectStack(app, "bird-conservation-project")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
