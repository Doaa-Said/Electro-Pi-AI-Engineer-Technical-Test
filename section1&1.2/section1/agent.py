from livekit.agents import Agent

from prompts import SYSTEM_PROMPT

from tools import (
    get_order_status,
    cancel_order,
    estimate_delivery_time,
)


class FoodSupportAgent(Agent):

    def __init__(self):
        super().__init__(
            instructions=SYSTEM_PROMPT,
            tools=[
                get_order_status,
                cancel_order,
                estimate_delivery_time,
            ],
        )