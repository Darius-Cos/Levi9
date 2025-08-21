
"""
pip install -U Flask-SQLAlchemy
Reuse the tables created last time, and add methods to fetch, insert, update and delete users (fetch of 1 user also),
to fetch, insert, delete transactions, and to fetch payment methods and roles.
"""
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_tables import Base, User, Role, PaymentMethod, Transaction,parola

app = Flask(__name__)

DATABASE_URL = f"postgresql://postgres:{parola}@localhost/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@app.route("/users", methods=["GET"])
def get_users():
    session = SessionLocal()
    users = session.query(User).all()
    result = [{"id": user.id,
               "username": user.username,
               "email":user.email} for user in users ]
    session.close()
    return jsonify(result)

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    session = SessionLocal()
    user = session.query(User).get(user_id)
    session.close()
    if user:
        return jsonify({"id": user.id,
                        "username": user.username,
                        "email":user.email})
    return jsonify({"error": "User not found"}), 404

@app.route("/createuser", methods=["POST"])
def create_user():
    data = request.get_json()
    session = SessionLocal()
    new_user = User(username=data["username"], email=data.get("email"))
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    session.close()
    return jsonify({"id": new_user.id, "username": new_user.username, "email": new_user.email})

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    session = SessionLocal()
    user = session.query(User).get(user_id)
    if not user:
        session.close()
        return jsonify({"error": "User not found"}), 404
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    session.commit()
    session.close()
    return jsonify({"message": "User updated"})

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    data = request.get_json()
    session = SessionLocal()
    user = session.query(User).get(user_id)
    if not user:
        session.close()
        return jsonify({"error": "User not found"}), 404
    session.delete(user)
    session.commit()
    session.close()
    return jsonify({"message": "User deleted"})


@app.route("/transactions", methods=["GET"])
def get_transactions():
    session = SessionLocal()
    transactions = session.query(Transaction).all()
    result = [
        {
            "id": t.id,
            "amount": float(t.amount),
            "description": t.description,
            "created_at": t.created_at.isoformat(),
            "user_id": t.user_id,
            "payment_method_id": t.payment_method_id
        } for t in transactions
    ]
    session.close()
    return jsonify(result)

@app.route("/transactions/<int:transaction_id>", methods=["GET"])
def get_transaction(transaction_id):
    session = SessionLocal()
    t = session.query(Transaction).get(transaction_id)
    session.close()
    if t:
        return jsonify({
            "id": t.id,
            "amount": float(t.amount),
            "description": t.description,
            "created_at": t.created_at.isoformat(),
            "user_id": t.user_id,
            "payment_method_id": t.payment_method_id
        })
    return jsonify({"error": "Transaction not found"}), 404


@app.route("/createtransaction", methods=["POST"])
def create_transaction():
    data = request.get_json()
    session = SessionLocal()
    new_transaction = Transaction(
        amount=data["amount"],
        description=data.get("description"),
        user_id=data["user_id"],
        payment_method_id=data.get("payment_method_id")

    )
    session.add(new_transaction)
    session.commit()
    session.refresh(new_transaction)
    session.close()
    return jsonify({"id": new_transaction.id})

@app.route("/transactions/<int:transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    data = request.get_json()
    session = SessionLocal()
    transaction = session.query(User).get(transaction_id)
    if not transaction:
        session.close()
        return jsonify({"error": "Transactin not found"}), 404
    transaction.amount = data.get("amount", transaction.amount)
    transaction.user_id = data.get("user_id", transaction.user_id)
    transaction.payment_method_id = data.get("payment_method_id", transaction.payment_method_id)
    session.commit()
    session.close()
    return jsonify({"message": "Transaction updated"})


@app.route("/transactions/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    session = SessionLocal()
    transaction = session.query(Transaction).get(transaction_id)
    if not transaction:
        session.close()
        return jsonify({"error": "Transaction not found"}), 404
    session.delete(transaction)
    session.commit()
    session.close()
    return jsonify({"message": "Transaction deleted"})

@app.route("/paymentmethods", methods=["GET"])
def get_payment_methods():
    session = SessionLocal()
    methods = session.query(PaymentMethod).all()
    result = [{"id": m.id,
               "name": m.name} for m in methods]
    session.close()
    return jsonify(result)

@app.route("/roles", methods=["GET"])
def get_roles():
    session = SessionLocal()
    roles = session.query(Role).all()
    result = [{"id": r.id,
               "name": r.name} for r in roles]
    session.close()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)













































