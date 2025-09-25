from typing import Dict
from models.payment import Payment
from db.mock_db import db  # мок-база

def create_payment_in_db(payment: Payment) -> Payment:
    """Сохраняет платеж в мок-базе"""
    db.payments[payment.payment_id] = payment
    return payment

def get_payment_from_db(payment_id: str) -> Payment:
    """Возвращает платеж по ID или None, если нет"""
    return db.payments.get(payment_id)

def update_payment_in_db(payment: Payment) -> Payment:
    """Обновляет существующий платеж"""
    db.payments[payment.payment_id] = payment
    return payment

def delete_payment_from_db(payment_id: str) -> bool:
    """Удаляет платеж по ID"""
    return db.payments.pop(payment_id, None) is not None
