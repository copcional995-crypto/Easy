# main.py
import os
import asyncio
import uuid
from datetime import datetime
from fastapi import FastAPI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

# ------------- CONFIG -------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SECRET_ADMIN_KEY = os.getenv("SECRET_ADMIN_KEY", "cambia_esto")
PLATFORM_WALLET_ADDRESS = "TQ9ZK11iPrzbLY5agT8LgzexAZ1y7ENatK"  # Wallet USDT
PORT = int(os.getenv("PORT", 8000))
DAILY_RETURN_PERCENT = 0.10  # 10% diario
# -----------------------------------

# ---------- DB (SQLite simple) ----------
DATABASE_URL = "sqlite:///./db.sqlite3"
engine = sa.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = sa.MetaData()

users = sa.Table(
    "users", metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("telegram_id", sa.String, unique=True, nullable=False),
    sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
)

balances = sa.Table(
    "balances", metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("user_id", sa.String, sa.ForeignKey("users.id")),
    sa.Column("asset", sa.String, default="USDT"),
    sa.Column("amount", sa.Float, default=0.0),
    sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
)

investments = sa.Table(
    "investments", metadata,
    sa.Column
