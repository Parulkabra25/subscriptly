from .client import get_razorpay_client

def create_order(amount_paise):
    client=get_razorpay_client()
    return client.order.create({
        "amount":amount_paise,
        "currency":"INR",
    })
