from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, Table, DateTime, Float, CheckConstraint
)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime, timedelta
import random

Base = declarative_base()
user_roles = Table(
    'user_roles', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('role_id', ForeignKey('roles.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=True)

    roles = relationship("Role", secondary=user_roles, back_populates="users")
    transactions = relationship("Transaction", back_populates="user")

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    users = relationship("User", secondary=user_roles, back_populates="roles")

class PaymentMethod(Base):
    __tablename__ = 'payment_methods'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    transactions = relationship("Transaction", back_populates="payment_method")

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    description = Column(String(200), nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    payment_method_id = Column(Integer, ForeignKey('payment_methods.id'), nullable=True)

    user = relationship("User", back_populates="transactions")
    payment_method = relationship("PaymentMethod", back_populates="transactions")

    __table_args__ = (
        CheckConstraint('amount >= 0', name='check_positive_amount'),
    )


if __name__ == "__main__":
    engine = create_engine('postgresql://postgres:admin@localhost/postgres')

    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    role_admin = Role(name="admin")
    role_editor = Role(name="editor")
    role_viewer = Role(name="viewer")
    roles = [role_admin, role_editor, role_viewer]
    session.add_all(roles)
    session.commit()

    methods = [PaymentMethod(name=n) for n in ["Credit Card", "PayPal", "Bank Transfer"]]
    session.add_all(methods)
    session.commit()

    users = []

    for i in range(10):
        user = User(username=f"user{i}", email=f"user{i}@example.com")
        if i == 0:
            pass  # 0 roles
        elif i == 1:
            user.roles.append(role_admin)
        elif i == 2:
            user.roles.extend([role_admin, role_editor])
        elif i == 3:
            user.roles.extend([role_admin, role_editor, role_viewer])
        else:
            assigned = random.sample(roles, random.randint(0, 3))
            user.roles.extend(assigned)

        users.append(user)

    session.add_all(users)
    session.commit()

    for i in range(20):
        user = random.choice(users)
        amount = round(random.uniform(10, 500), 2)
        created_at = datetime.now() - timedelta(days=random.randint(0, 30))
        description = None if i % 4 == 0 else f"Transaction {i}"
        payment_method = None if i % 5 == 0 else random.choice(methods)

        tx = Transaction(
            amount=amount,
            created_at=created_at,
            description=description,
            user=user,
            payment_method=payment_method
        )
        session.add(tx)

    session.commit()