from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, Table, DateTime, Float, CheckConstraint
)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime, timedelta
import random

if __name__ == "__main__":
    engine = create_engine('postgresql://postgres:admin@localhost/postgres')
