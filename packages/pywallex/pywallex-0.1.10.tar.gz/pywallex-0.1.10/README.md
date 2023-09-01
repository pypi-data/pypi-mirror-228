# Wallex SDK

## Project Overview
 The Wallex SDK is a software development kit that provides a set of tools and utilities for integrating with the Wallex payment gateway.

## Table of Contents
 - [Getting Started](#getting-started)
    - [Installation](#installation)
 - [Features](#features)
 - [Contributing](#contributing)
 - [License](#license)

## Getting Started
This section provides instructions on how to get started with the Wallex SDK.

### Installation
```bash
pip install pywallex
```

## Features
 This section describes the main features and capabilities of the Wallex SDK.

### Feature 1: Create payment widget

```python
from pywallex import Widget

widget = Widget(1, 'secret_key')

payment_url = await widget.create_payment(
    Widget.PaymentModel(
        product='client@mail.ru',
        price='Xiaomi 9T',
        quantity=1000,
        message=1,
        description='Hello thanks for order',
        currency='Xiaomi 9T',
        fiat_currency='USDT',
        language='rub',
        uuid='ru'
    )
)  # Returns payment url
```


### Feature 2: Verify payment

```python
from pywallex import Webhook

payment_data = {}  # Replace with actual POST data
payment = Webhook(payment_data)

if payment.is_verified('secret_key') and payment.is_success():
    # Payment success logic
    # For example:
    client = payment.get_client()  # Get client email
    # Update user balance:
    # User.objects.filter(email=client).update(balance=payment.get_amount())
```

### Feature 3: Payouts

```python
from pywallex import Payout

payout = Payout(merchant_id, secret_key)

await payout.crypto_pay(
    Payout.CryptoPayModel(
        address=address,
        amount=amount,
        currency=currency,
    )
)
```

## Contributing
We welcome contributions from the developer community to improve the Wallex SDK. If you are interested in contributing to the Wallex SDK, please follow the steps below:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Make the necessary changes in your branch.
4. Write tests to ensure the changes are working as expected.
5. Submit a pull request with your changes.

## License
The Wallex SDK is licensed under the [MIT License](LICENSE).
