import streamlit as st
import pandas as pd
import expense_tracker

# Set page config
st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

st.title("💰 Expense Tracker Dashboard")
st.markdown("Track and visualize your expenses effortlessly.")

# Sidebar for adding new expenses
with st.sidebar:
    st.header("➕ Add New Expense")
    with st.form("add_expense_form"):
        name = st.text_input("Expense Name", placeholder="e.g. Groceries")
        amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f", step=1.0)
        submitted = st.form_submit_button("Add Expense")
        
        if submitted:
            if name.strip():
                expense_tracker.add_expense(name.strip(), amount)
                st.success(f"Added {name}: ${amount:.2f}")
                st.rerun()
            else:
                st.error("Please enter a valid expense name.")

# Main Dashboard Container
expenses = expense_tracker.load_expenses()
total = expense_tracker.get_total_expense()

# Top metric
st.metric(label="Total Expenses", value=f"${total:.2f}")
st.divider()

if expenses:
    # Convert data into a DataFrame
    df = pd.DataFrame([{"Expense": k, "Amount": v} for k, v in expenses.items()])
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("📋 Expense List")
        st.dataframe(
            df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Expense": st.column_config.TextColumn("Expense Category"),
                "Amount": st.column_config.NumberColumn("Amount ($)", format="$%.2f")
            }
        )
        
    with col2:
        st.subheader("📊 Expense Distribution")
        # Creating a bar chart using streamlit native charts or altair/plotly
        st.bar_chart(df.set_index("Expense"), height=350, use_container_width=True)
else:
    st.info("No expenses recorded yet. Use the sidebar to add your first expense!")
