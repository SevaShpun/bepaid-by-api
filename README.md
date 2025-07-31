# bepaid-by-api
Платежная система https://bepaid.by/

<a href="https://bepaid.by/" target="_blank"><img src="https://i.ibb.co/q3pgK5JS/bepaid-logot.png"></a>

### 1. Создаем виртуальное окружение

Windows
```bash
python -m venv venv
```

Linux
```bash
python3 -m venv venv
```
### 2. Переходим в виртуальное окружение

Windows
```bash
source venv/Scripts/activate
```

Linux
```bash
source venv/bin/activate
```

### 3. Переименовать `.env_dist` в `.env`

### 4. В `.env` файле указываем ваши данные

```bash
TOKEN="MERCHANT_TOKEN"
SHOP_ID=SHOP_ID
SITE_URL="SITE_URL"
```

# 📚 Пример

## Создаем транзакцию и получаем json

```python
import asyncio
import os
from random import randint

from dotenv import load_dotenv
from src.bepaid import BepaidClient

load_dotenv()

# Load and validate required environment variables
TOKEN = os.getenv("TOKEN")
SHOP_ID = os.getenv("SHOP_ID")
SITE_URL = os.getenv("SITE_URL")

if not all([TOKEN, SHOP_ID, SITE_URL]):
    raise EnvironmentError("Missing required environment variables: TOKEN, SHOP_ID, or SITE_URL")

bepaid = BepaidClient(token=TOKEN, shop_id=int(SHOP_ID), site_url=SITE_URL)


def generate_payment_data() -> dict:
    return {
        "test": True,
        "transaction_type": "payment",
        "bot": "BepaidClientSimple",
        "pay_id": randint(1000000, 9000000),
        "tracking_id": randint(1000000, 9000000),
        "user_id": 7777777,
        "user": "SevaShpun",
        "amount": 1*100,  # 1.00 BYN
        "currency": "BYN",
        "order_description": "Оплата",
        "description": "Оплата товара",
        "language": "ru"
    }


async def create_payment_link():
    data = generate_payment_data()
    await bepaid.create_payment(data=data, debug=True)


async def main():
    await create_payment_link()

if __name__ == "__main__":
    asyncio.run(main())
```


## Получаем результат транзакции в json

```python
import asyncio
import os
from random import randint

from dotenv import load_dotenv
from src.bepaid import BepaidClient

load_dotenv()

# Load and validate required environment variables
TOKEN = os.getenv("TOKEN")
SHOP_ID = os.getenv("SHOP_ID")
SITE_URL = os.getenv("SITE_URL")

if not all([TOKEN, SHOP_ID, SITE_URL]):
    raise EnvironmentError("Missing required environment variables: TOKEN, SHOP_ID, or SITE_URL")

bepaid = BepaidClient(token=TOKEN, shop_id=int(SHOP_ID), site_url=SITE_URL)


async def get_payment_status():
    checkout_token = '5afba1ddc460c9aaee582eb962g7cab6fb151965e4e8d5afca49e9df1e1fa50f'
    await bepaid.get_payment_status(checkout_token=checkout_token, debug=True)


async def main():
    await get_payment_status()

if __name__ == "__main__":
    asyncio.run(main())
```

### Весь код находится в `main.py`

## 🚀 Запуск скрипта

```python
python -B main.py
```
