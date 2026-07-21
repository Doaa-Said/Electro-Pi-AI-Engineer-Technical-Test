from livekit.agents import function_tool

ORDERS = {
    "1001": {
        "status": "Preparing",
        "eta": "15 minutes"
    },
    "1002": {
        "status": "Out for delivery",
        "eta": "5 minutes"
    },
    "1003": {
        "status": "Delivered",
        "eta": "Completed"
    }
}


@function_tool
async def get_order_status(order_id: str) -> str:
    """Return the status of an order."""

    order = ORDERS.get(order_id)

    if order is None:
        return f"No order found with ID {order_id}."

    return (
        f"Order {order_id}\n"
        f"Status: {order['status']}\n"
        f"ETA: {order['eta']}"
    )


@function_tool
async def cancel_order(order_id: str) -> str:
    """Cancel an order if possible."""

    order = ORDERS.get(order_id)

    if order is None:
        return f"Order {order_id} does not exist."

    if order["status"] == "Delivered":
        return "Delivered orders cannot be cancelled."

    order["status"] = "Cancelled"

    return f"Order {order_id} has been cancelled."


@function_tool
async def estimate_delivery_time(order_id: str) -> str:
    """Estimate delivery time."""

    order = ORDERS.get(order_id)

    if order is None:
        return "Order not found."

    return order["eta"]