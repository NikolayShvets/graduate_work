from yookassa import Payment


def create_payment(amount: float, currency: str, description: str, return_url: str):
    try:
        payment = Payment.create({
            "amount": {
                "value": amount,
                "currency": currency,
            },
            "confirmation": {
                "type": "redirect",
                "return_url": return_url
            },
            "capture": True,
            "description": description,
            "save_payment_method": True
        })
        return payment
    except Exception as e:
        print(f"Произошла ошибка при создании платежа: {e}")
        return None


# Функция для получения списка платежей
def list_payments(limit: int = 10):
    try:
        payments = Payment.list(limit=limit)
        return payments
    except Exception as e:
        print(f"Произошла ошибка при получении списка платежей: {e}")
        return None


# Функция для получения одного платежа
def get_payment(payment_id: str):
    try:
        payment = Payment.find_one(payment_id)
        return payment
    except Exception as e:
        print(f"Произошла ошибка при получении платежа: {e}")
        return None


# Функция для получения статуса платежа
def get_payment_status(payment_id: str):
    payment = get_payment(payment_id)
    if payment:
        return payment.status
    return None


# Функция для отмены платежа
def cancel_payment(payment_id: str):
    try:
        payment = get_payment(payment_id)
        if payment and payment.status == 'waiting_for_capture':
            payment.cancel()
            print(f"Платеж {payment_id} успешно отменен.")
        else:
            print(f"Платеж {payment_id} невозможно отменить. Текущий статус: {payment.status}.")
    except Exception as e:
        print(f"Произошла ошибка при отмене платежа: {e}")
