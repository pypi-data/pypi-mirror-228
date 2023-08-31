# pesapal
Unofficial SDK wrapper for the pesapal v3 payments API.

## Requirements
- python v3.11+

## Installation

```
pip install pesapal_v3
```

## Usage

```python
from pesapal_v3 import Pesapal

client = Pesapal(consumer_key, consumer_secret)

```

## Supported endpoints

### Register IPN

```python
resp = client.register_ipn(endpoint="https://example.com/notifications/payments)

if resp.status != "200":
  # error occured registering your IPN
  print(resp.error)
else:
  # IPN successfully registered
```

### List registered IPNs
```python
ipns = client.get_all_ipns()
print(ipns)
```

### Submit order request
```python
order_request = {
    "id": "s945e4af-80a5-4ec1-8706-e03f8332fb04",
    "currency": "KES",
    "amount": 350.00,
    "description": "Thank you for this SDK",
    "callback_url": "https://example.com/cancellation",
    "notification_id": "fe078e53-78da-4a83-aa89-e7ded5c456e6"
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
        "zip_code": ""
    }

}
request = client.submit_order_request(order_request)
```

### Transaction status
```python
status = client.get_transaction_status(order_tracking_id="b945e4af-80a5-4ec1-8706-e03f8332fb04")
```

### Subscriptions
```python
# TODO
```

### Refund
```
refund =
{
    "confirmation_code": "AA11BB22",
    "amount": "100.00",
    "username": "John Doe",
    "remarks": "Service not offered"
}

client.refund(refund)
```

## Support

For any issues, bugs you can raise an issue on the project issues board.

For compliments and _gigs_ you can reach out to the developer via email `martinmshale@gmail.com`.

For service level issues, reach out to Pesapal.

Lastly, I need the developer juice to produce more of these open source solutions. Be among the few who have supported these effort by _buying me a coffee_.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/musale)
