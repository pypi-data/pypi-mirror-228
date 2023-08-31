from pesapal_v3 import Pesapal

order_request = {
    "id": "s945e4af-80a5-4ec1-8706-e03f8332fb02",
    "currency": "KES",
    "amount": 350.00,
    "description": "Thank you for this SDK",
    "callback_url": "https://example.com/cancellation",
    "notification_id": "fe078e53-78da-4a83-aa89-e7ded5c456e6",
    "billing_address": {
        "email_address": "john.doe@example.com",
        "phone_number": "0723xxxxxx",
        "country_code": "KE",
        "first_name": "John",
        "middle_name": "",
        "last_name": "Doe",
        "line_1": "Pesapal Limited",
        "line_2": "",
        "city": "",
        "state": "",
        "postal_code": "",
        "zip_code": "",
    },
}

order_tracking_id = "6ab46754-fe9a-4cfa-960b-de3ebcf4601f"


def main():
    key = "qkio1BGGYAXTu2JOfm7XSXNruoZsrqEW"
    secret = "osGQ364R49cXKeOYSpaOnT++rHs="
    client = Pesapal(consumer_key=key, consumer_secret=secret)
    if client._token:
        ipn_url = "https://example.com/ipn/notifications"
        ipn = client.register_ipn_url(ipn_url=ipn_url)
        # if ipn.status != "200":
        #     print(ipn.error)
        # print(ipn)

        # list
        # print(client.get_registered_ipns())
        # make request
        order_request.update({"notification_id": ipn.ipn_id})
        order_request.update({"account": "124353132"})
        order_request.update(
            {
                "subscription_details": {
                    "start_date": "01-09-2023",
                    "end_date": "01-10-2023",
                    "frequency": "DAILY",
                }
            }
        )
        print(
            client.submit_order_request(
                order_request=order_request, is_subscription=True
            )
        )
        print(client.get_transaction_status(order_tracking_id=order_tracking_id))


if __name__ == "__main__":
    main()
