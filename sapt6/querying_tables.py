from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from create_tables import User, PaymentMethod, Transaction, Role

engine = create_engine('postgresql://postgres:admin@localhost/postgres')
Session = sessionmaker(bind=engine)
session = Session()

print ("1. Users with at least one role")
users_with_roles = session.query(User).filter(User.roles.any()).all()
for user in users_with_roles:
    print(f"User with role: {user.username}")

print("2. Users with the 'admin' role")
admin_users = session.query(User).join(User.roles).filter(Role.name == 'admin').all()
for user in admin_users:
    print(f"Admin user: {user.username}")

print("3. Transactions ordered by amount descending")
transactions_by_amount = session.query(Transaction).order_by(desc(Transaction.amount)).all()
for tx in transactions_by_amount:
    print(f"Transaction ID {tx.id}: ${tx.amount:.2f}")

print("4. Most recent 5 transactions")
recent_transactions = session.query(Transaction).order_by(desc(Transaction.created_at)).limit(5).all()
for tx in recent_transactions:
    print(f"Transaction ID {tx.id} at {tx.created_at}")

print("5. Users with transactions")
users_with_transactions = session.query(User).filter(User.transactions.any()).all()
for user in users_with_transactions:
    print(f"User with transactions: {user.username}")

print("6. List all roles that are assigned to more than one user.")
popular_roles = (
    session.query(Role.name, func.count(User.id))
    .join(Role.users)
    .group_by(Role.id)
    .having(func.count(User.id) > 1)
    .all()
)
for role_name, count in popular_roles:
    print(f"Role '{role_name}' is assigned to {count} users")

print("7. Transactions with user info")
transactions_with_users = (
    session.query(Transaction, User.username, User.email)
    .join(Transaction.user)
    .all()
)
for tx, username, email in transactions_with_users:
    print(f"Transaction {tx.id} by {username} ({email}) for ${tx.amount:.2f}")


print("# 8. Users and transaction counts")
user_transaction_counts = (
    session.query(User.username, func.count(Transaction.id).label('tx_count'))
    .outerjoin(User.transactions)
    .group_by(User.id)
    .order_by(desc('tx_count'))
    .all()
)
for username, count in user_transaction_counts:
    print(f"{username} made {count} transaction(s)")


print("# 9. Total amount per payment method")
amount_by_payment_method = (
    session.query(PaymentMethod.name, func.sum(Transaction.amount))
    .join(PaymentMethod.transactions)
    .group_by(PaymentMethod.id)
    .all()
)
for method, total in amount_by_payment_method:
    print(f"{method} total amount: ${total:.2f}")


print("# 10. Transactions with user and payment method names")
transaction_details = (
    session.query(Transaction.id, User.username, PaymentMethod.name)
    .join(Transaction.user)
    .outerjoin(Transaction.payment_method)
    .all()
)
for tx_id, username, payment_name in transaction_details:
    payment_display = payment_name if payment_name else "No Payment Method"
    print(f"Transaction {tx_id} by {username} - Payment: {payment_display}")


print("# 11. Average transaction amount per user (only users with transactions)")
avg_tx_per_user = (
    session.query(User.username, func.avg(Transaction.amount))
    .join(User.transactions)
    .group_by(User.id)
    .all()
)
for username, avg_amount in avg_tx_per_user:
    print(f"{username} - Average Transaction: ${avg_amount:.2f}")

print("# 12. Users with more at least 2 roles")
users_with_many_roles = (
    session.query(User.username, func.count(Role.id))
    .join(User.roles)
    .group_by(User.id)
    .having(func.count(Role.id) > 1)
    .all()
)
for username, role_count in users_with_many_roles:
    print(f"{username} has {role_count} roles")


print("13. List all users who have made at least one transaction using every available payment method")

total_methods = session.query(func.count(PaymentMethod.id)).scalar()

results = (
    session.query(User.username, func.count(func.distinct(Transaction.payment_method_id)).label("used_methods"))
    .join(User.transactions)
    .group_by(User.id)
    .having(func.count(func.distinct(Transaction.payment_method_id)) == total_methods)
    .all()
)

for username, count in results:
    print(f"{username} used all {count} payment methods")