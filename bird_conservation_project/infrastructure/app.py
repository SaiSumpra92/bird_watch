#!/usr/bin/env python3
import os
from aws_cdk import core

from bird_conservation_stack import BirdConservationStack

app = core.App()
BirdConservationStack(app, "BirdConservationStack",
    env=core.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
)

app.synth()