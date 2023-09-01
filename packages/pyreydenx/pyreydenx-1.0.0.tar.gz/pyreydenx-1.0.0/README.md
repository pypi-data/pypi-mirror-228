# REYDEN-X

###### Reyden-X is an automated service for promoting live broadcasts on external sites with integrated system of viewers and views management.

- [Website](https://reyden-x.com/en)

- [API Documentation](https://api.reyden-x.com/docs)

### Installation

```bash
pip install pyreydenx
```

### Environment Variables

- REYDENX_EMAIL - Email (Optional)
- REYDENX_PASSWORD - Password (Optional)

### Quickstart

```python
from pyreydenx import Client

from pyreydenx.user import User
from pyreydenx.order import Order

client = Client('email', 'password')

print(User.account(client))
print(User.balance(client))

print(Order.details(client, 12345))
print(Order.get_orders(client, None))
```
