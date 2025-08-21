import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import requests

# Configurare pagină
st.set_page_config(page_title="Multi-Tab App", layout="wide")

# Configurare conexiune la baza de date
parola = 'Dariusdaniel.123'
DATABASE_URL = f'postgresql://postgres:{parola}@localhost/postgres'

def home():
    st.title("Home Page")
    name = st.text_input("Enter your name: ")
    st.header(f"Hello {name}!")

def about():
    st.title("About You")

    st.header("Birth date")
    selected_date = st.date_input("Select a date:")
    bio = st.text_area("Write a short bio:")
    color = st.selectbox("Favorite color:", ["Red", "Green", "Blue", "Yellow"])
    st.text(f"Your favorite color: {color}")
    st.text(f"Your birthday date: {selected_date}")
    st.text(f"Bio: {bio}")

def calculator():
    st.title("Calculator App")

    if "result" not in st.session_state:
        st.session_state.result = 0
        first_number = st.number_input("Enter first number:")
        second_number = st.number_input("Enter second number:")

    else:
        first_number=st.session_state.result
        second_number=st.number_input("Enter the other number:", value=5.0)

    operation = st.selectbox("Choose an operation:", ["+", "-", "*", "/"])
    if st.button("Calculate"):
        try:
            if operation == "+":
                st.session_state.result = first_number + second_number
            elif operation == "-":
                st.session_state.result = first_number - second_number
            elif operation == "*":
                st.session_state.result = first_number * second_number
            elif operation == "/":
                if second_number == 0:
                    st.error("Error: Division by zero is not allowed!")
                    return
                st.session_state.result = first_number / second_number

            st.success(f"Result: {st.session_state.result}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")



def combined_solutions():
    st.title("Toate soluțiile în tab-uri")

    tab1, tab2, tab3 = st.tabs(["Hello App", "About You", "Calculator"])

    with tab1:
        home()
    with tab2:
        about()
    with tab3:
        calculator()




@st.cache_resource
def get_db_connection():
    """Creează conexiunea la baza de date"""
    try:
        engine = create_engine(DATABASE_URL)
        return engine
    except Exception as e:
        st.error(f"Eroare la conectarea la baza de date: {str(e)}")
        return None


def get_users_data():
    """Obține utilizatorii din baza de date"""
    engine = get_db_connection()
    if engine is None:
        return pd.DataFrame()

    try:
        query = """
        SELECT 
            u.id,
            u.username,
            u.email,
            string_agg(r.name, ', ') as roles
        FROM users u
        LEFT JOIN user_roles ur ON u.id = ur.user_id
        LEFT JOIN roles r ON ur.role_id = r.id
        GROUP BY u.id, u.username, u.email
        ORDER BY u.id
        """
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Eroare la încărcarea utilizatorilor: {str(e)}")
        return pd.DataFrame()


def get_transactions_data():
    """Obține tranzacțiile din baza de date"""
    engine = get_db_connection()
    if engine is None:
        return pd.DataFrame()

    try:
        query = """
        SELECT 
            t.id,
            t.amount,
            t.created_at,
            t.description,
            u.username,
            pm.name as payment_method
        FROM transactions t
        JOIN users u ON t.user_id = u.id
        LEFT JOIN payment_methods pm ON t.payment_method_id = pm.id
        ORDER BY t.created_at DESC
        """
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Eroare la încărcarea tranzacțiilor: {str(e)}")
        return pd.DataFrame()


def get_roles():
    """Obține toate rolurile disponibile"""
    engine = get_db_connection()
    if engine is None:
        return []

    try:
        query = "SELECT id, name FROM roles ORDER BY name"
        df = pd.read_sql(query, engine)
        return df.to_dict('records')
    except Exception as e:
        st.error(f"Eroare la încărcarea rolurilor: {str(e)}")
        return []


def get_payment_methods():
    """Obține toate metodele de plată disponibile"""
    engine = get_db_connection()
    if engine is None:
        return []

    try:
        query = "SELECT id, name FROM payment_methods ORDER BY name"
        df = pd.read_sql(query, engine)
        return df.to_dict('records')
    except Exception as e:
        st.error(f"Eroare la încărcarea metodelor de plată: {str(e)}")
        return []


def add_user(username, email, selected_roles):
    """Adaugă un utilizator nou în baza de date"""
    engine = get_db_connection()
    if engine is None:
        return False

    try:
        with engine.begin() as conn:
            # Inserează utilizatorul
            result = conn.execute(
                text("INSERT INTO users (username, email) VALUES (:username, :email) RETURNING id"),
                {"username": username, "email": email}
            )
            user_id = result.fetchone()[0]

            # Adaugă rolurile
            for role_id in selected_roles:
                conn.execute(
                    text("INSERT INTO user_roles (user_id, role_id) VALUES (:user_id, :role_id)"),
                    {"user_id": user_id, "role_id": role_id}
                )

        return True
    except Exception as e:
        st.error(f"Eroare la adăugarea utilizatorului: {str(e)}")
        return False


def add_transaction(user_id, amount, description, payment_method_id):
    """Adaugă o tranzacție nouă în baza de date"""
    engine = get_db_connection()
    if engine is None:
        return False

    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                INSERT INTO transactions (user_id, amount, description, payment_method_id, created_at) 
                VALUES (:user_id, :amount, :description, :payment_method_id, :created_at)
                """),
                {
                    "user_id": user_id,
                    "amount": amount,
                    "description": description,
                    "payment_method_id": payment_method_id if payment_method_id > 0 else None,
                    "created_at": datetime.now()
                }
            )
        return True
    except Exception as e:
        st.error(f"Eroare la adăugarea tranzacției: {str(e)}")
        return False


def api_integration():
    st.title("🌐 API Integration - Database Management")

    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 View Users",
        "💳 View Transactions",
        "➕ Add User",
        "💰 Add Transaction"
    ])

    with tab1:
        st.header("👥 Users Table")

        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🔄 Refresh Users", key="refresh_users"):
                st.rerun()

        with st.spinner("Loading users..."):
            users_df = get_users_data()

        if not users_df.empty:
            st.dataframe(
                users_df,
                use_container_width=True,
                column_config={
                    "id": "ID",
                    "username": "Username",
                    "email": "Email",
                    "roles": "Roles"
                }
            )
            st.info(f"Total users: {len(users_df)}")
        else:
            st.warning("No users found or database connection error.")

    with tab2:
        st.header("💳 Transactions Table")

        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🔄 Refresh Transactions", key="refresh_transactions"):
                st.rerun()

        with st.spinner("Loading transactions..."):
            transactions_df = get_transactions_data()

        if not transactions_df.empty:
            st.dataframe(
                transactions_df,
                use_container_width=True,
                column_config={
                    "id": "ID",
                    "amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
                    "created_at": "Date",
                    "description": "Description",
                    "username": "User",
                    "payment_method": "Payment Method"
                }
            )

            # Statistici
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Transactions", len(transactions_df))
            with col2:
                total_amount = transactions_df['amount'].sum()
                st.metric("Total Amount", f"${total_amount:.2f}")
            with col3:
                avg_amount = transactions_df['amount'].mean()
                st.metric("Average Amount", f"${avg_amount:.2f}")
        else:
            st.warning("No transactions found or database connection error.")

    with tab3:
        st.header("➕ Add New User")

        with st.form("add_user_form"):
            st.subheader("User Information")

            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username *", placeholder="Enter username")
            with col2:
                email = st.text_input("Email", placeholder="user@example.com")

            st.subheader("Assign Roles")
            roles = get_roles()
            if roles:
                selected_roles = st.multiselect(
                    "Select roles for this user:",
                    options=[role['id'] for role in roles],
                    format_func=lambda x: next(role['name'] for role in roles if role['id'] == x),
                    help="You can select multiple roles"
                )
            else:
                selected_roles = []
                st.warning("No roles available")

            submitted = st.form_submit_button("👤 Add User", type="primary")

            if submitted:
                if username.strip():
                    with st.spinner("Adding user..."):
                        if add_user(username.strip(), email.strip() or None, selected_roles):
                            st.success(f"✅ User '{username}' added successfully!")
                            st.balloons()
                        else:
                            st.error("❌ Failed to add user. Please try again.")
                else:
                    st.error("❌ Username is required!")

    with tab4:
        st.header("💰 Add New Transaction")

        # Obține utilizatorii pentru dropdown
        users_df = get_users_data()
        payment_methods = get_payment_methods()

        if users_df.empty:
            st.error("No users available. Please add users first.")
            return

        with st.form("add_transaction_form"):
            st.subheader("Transaction Information")

            col1, col2 = st.columns(2)
            with col1:
                selected_user = st.selectbox(
                    "Select User *",
                    options=users_df['id'].tolist(),
                    format_func=lambda x: users_df[users_df['id'] == x]['username'].iloc[0],
                    help="Choose the user for this transaction"
                )

            with col2:
                amount = st.number_input(
                    "Amount *",
                    min_value=0.01,
                    value=10.0,
                    format="%.2f",
                    help="Enter the transaction amount"
                )

            description = st.text_area(
                "Description",
                placeholder="Optional transaction description...",
                height=80
            )

            payment_method_options = [0] + [pm['id'] for pm in payment_methods]
            payment_method_labels = ["No payment method"] + [pm['name'] for pm in payment_methods]

            selected_payment_method = st.selectbox(
                "Payment Method",
                options=payment_method_options,
                format_func=lambda x: payment_method_labels[payment_method_options.index(x)],
                help="Select a payment method (optional)"
            )

            submitted = st.form_submit_button("💳 Add Transaction", type="primary")

            if submitted:
                if selected_user and amount > 0:
                    with st.spinner("Adding transaction..."):
                        if add_transaction(
                                selected_user,
                                amount,
                                description.strip() or None,
                                selected_payment_method
                        ):
                            st.success(f"✅ Transaction of ${amount:.2f} added successfully!")
                            st.balloons()
                        else:
                            st.error("❌ Failed to add transaction. Please try again.")
                else:
                    st.error("❌ Please select a user and enter a valid amount!")


pages = [
    st.Page(home, title="Home", icon="🏠"),
    st.Page(about, title="About", icon="👤"),
    st.Page(calculator, title="Calculator", icon="🔢"),
    st.Page(combined_solutions, title="Combined Tabs", icon="📊"),
    st.Page(api_integration, title="API Integration", icon="🌐")
]

pg = st.navigation(pages, position="sidebar", expanded=True)
pg.run()