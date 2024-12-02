import streamlit as st
import pandas as pd
from database import connect_to_db
import plotly.express as px

# Title of the app
st.title("Customer Insights and Segmentation Dashboard")

# Connect to the database
conn = connect_to_db()
if conn.is_connected():
    st.write("Database connection is active")
else:
    st.error("Database connection is not active")
cursor = conn.cursor(dictionary=True)

# Sidebar menu
menu = ["View ", "Add Entry", "Update Entry", "Delete Entry", "Visualizations", "RFM Analysis", "Segmentation"]
choice = st.sidebar.selectbox("Menu", menu)

# View Data
if choice == "View Data":
    st.subheader("View Customer Data")
    query = "SELECT * FROM customer_data"
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    st.dataframe(df)

# Add Entry
elif choice == "Add Entry":
    st.subheader("Add New Customer Entry")
    with st.form("add_form"):
        invoice_number = st.text_input("Invoice Number")
        customer_id = st.text_input("Customer ID")
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.number_input("Age", min_value=1, max_value=120)
        category = st.text_input("Category")
        quantity = st.number_input("Quantity", min_value=1)
        price = st.number_input("Price", min_value=0.0)
        payment_method = st.text_input("Payment Method")
        invoice_date = st.date_input("Invoice Date")
        shopping_mall = st.text_input("Shopping Mall")
        location = st.text_input("Location")
        submitted = st.form_submit_button("Add Entry")

        if submitted:
            query = """
                INSERT INTO customer_data (invoice_number, customer_id, gender, age, category, quantity, price, payment_method, invoice_date, shopping_mall, location)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (invoice_number, customer_id, gender, age, category, quantity, price, payment_method, invoice_date, shopping_mall, location)
            cursor.execute(query, values)
            conn.commit()
            st.success("New entry added successfully!")

# Update Entry
elif choice == "Update Entry":
    st.subheader("Update Customer Entry")

    # Step 1: Fetch Data
    customer_id = st.text_input("Enter Customer ID to Update")
    if st.button("Fetch Data"):
        # Fetch the data for the entered customer ID
        query = "SELECT * FROM customer_data WHERE customer_id = %s"
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()
        
        # Debug: Show fetched data
        st.write("Fetched Data:", result)
        
        if result:
            # Store fetched data in session state
            st.session_state["result"] = result
        else:
            st.error("Customer ID not found.")

    # Step 2: Display Update Form
    if "result" in st.session_state and st.session_state["result"]:
        result = st.session_state["result"]

        # Display form with pre-filled values
        with st.form("update_form"):
            age = st.number_input("Age", value=result["age"], min_value=1, max_value=120)
            category = st.text_input("Category", value=result["category"])
            location = st.text_input("Location", value=result["location"])
            submitted = st.form_submit_button("Update Entry")
            st.write(submitted)

        # Step 3: Handle Update Click
        if submitted:
            st.write(submitted)
            st.write(f"Updating customer: {customer_id} with Age: {age}, Category: {category}, Location: {location}")
            try:
                update_query = """
                    UPDATE customer_data
                    SET age = %s, category = %s, location = %s
                    WHERE customer_id = %s
                """
                cursor.execute(update_query, (age, category, location, customer_id))
                conn.commit()
                st.success("Entry updated successfully!")
                
                # Clear session state after update
                del st.session_state["result"]
            except Exception as e:
                st.error(f"Error updating entry: {e}")

# Delete Entry
elif choice == "Delete Entry":
    st.subheader("Delete Customer Entry")
    customer_id = st.text_input("Enter Customer ID to Delete")
    if st.button("Delete Entry"):
        query = "DELETE FROM customer_data WHERE customer_id = %s"
        cursor.execute(query, (customer_id,))
        conn.commit()
        st.success("Entry deleted successfully!")


# Close the database connection
conn.close()
