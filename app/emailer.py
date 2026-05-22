# emailer.py

import smtplib

from email.message import EmailMessage

from app.config import (
    GMAIL_SENDER,
    GMAIL_APP_PASSWORD,
    GMAIL_RECIPIENT
)


def send_order_email(order):
    """
    Sends one Gmail notification for a confirmed sales order.

    The subject follows the assessment format:
    Confirmed Order Alert: [Customer Name] - [PO Number]

    The body includes the formatted Part Summary created
    from the order's associated order lines.
    """

    subject = (
        f"Confirmed Order Alert: "
        f"{order['customer']} - {order['po_number']}"
    )

    part_summary = ", ".join(order["parts"])

    body = (
        f"Confirmed sales order found.\n\n"
        f"Order: {order['name']}\n"
        f"Customer: {order['customer']}\n"
        f"PO Number: {order['po_number']}\n"
        f"Order Date: {order['order_date']}\n\n"
        f"Part Summary:\n"
        f"{part_summary}\n"
    )

    message = EmailMessage()
    message["From"] = GMAIL_SENDER
    message["To"] = GMAIL_RECIPIENT
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)
        smtp.send_message(message)