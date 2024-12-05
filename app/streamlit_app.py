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

# Sidebar Main Menu
st.sidebar.title("Menu")
main_menu = st.sidebar.selectbox(
    "Main Menu",
    ["View Data", "Customer Insights"]
)

# View Data Section
if main_menu == "View Data":
    menu = ["View Data", "Add Entry", "Update Entry", "Delete Entry", "Visualizations", "RFM Analysis", "Segmentation"]
    choice = st.sidebar.selectbox("Menu", menu)

    
    # View Data
    if choice == "View Data":
        st.subheader("View Customer Data")
         # Search filters
        custid = st.text_input("Customer ID")
        invoice_number = st.text_input("Invoice Number")
        gender = st.selectbox("Gender", ["", "Male", "Female"])
        category = st.selectbox("Category", ["", "Books", "Clothing", "Cosmetics", "Food & Beverage", "Shoes", "Souvenir", "Technology", "Toys"])
        shopping_mall = st.selectbox("Shopping Mall",["", "Cevahir AVM", "Emaar Square Mall", "Forum Istanbul", "Istinye Park", "Kanyon", "Mall of Istanbul", "Metrocity", "Metropol AVM", "Viaport Outlet", "Zorlu Center"])

        col1, col2 = st.columns(2)
        with col1:
            search = st.button("Search")
        with col2:
            reset = st.button("Reset")
        
        # Initial page load: Display all records
        if not search and not reset:
            query = "SELECT * FROM customer_data"
            cursor.execute(query)
            data = cursor.fetchall()
            df = pd.DataFrame(data)
            st.dataframe(df)
        
        if search:
            # Build the query with filters
            query = "SELECT * FROM customer_data WHERE 1=1"
            if custid:
                query += f" AND customer_id = '{custid}'"
            if invoice_number:
                query += f" AND invoice_number = '{invoice_number}'"
            if gender:
                query += f" AND gender = '{gender}'"
            if category:
                query += f" AND category = '{category}'"
            if shopping_mall:
                query += f" AND shopping_mall = '{shopping_mall}'"
        
            cursor.execute(query)
            data = cursor.fetchall()
            df = pd.DataFrame(data)
            st.dataframe(df)

        if reset:
            # Clear all input fields and show all records
            custid = ""
            invoice_number = ""
            gender = ""
            category = ""
            shopping_mall = ""
            
            query = "SELECT * FROM customer_data"
            cursor.execute(query)
            data = cursor.fetchall()
            df = pd.DataFrame(data)
            st.dataframe(df)
            

########################################################
# Customer Insights Section
if main_menu == "Customer Insights":
    st.title("Customer Insights")
    
    # Sub-menu for Customer Insights
    insight_menu = st.radio(
        "Choose a section",
        ["Top Customers", "RFM Segmentation", "Acquiring New Customers", "Product Recommendations", "Predicting Churn"]
    )

    # Top Customers Section
    if insight_menu == "Top Customers":
        st.header("Top Customers Contributing the Most Revenue")
        # Add logic for Top Customers
        # Input: Number of top customers
        num_customers = st.slider("Select number of top customers", 5, 20, 10)
        query =  """
    WITH rfm_data AS (
        SELECT
            customer_id, 
            gender, 
            age, 
          
            DATEDIFF('2024-01-01', invoice_date) AS last_date_order,
            SUM(quantity) AS total_orders,
            CAST(SUM(price * quantity ) AS DECIMAL(10, 2)) AS revenue  
        FROM 
            customer_data
        GROUP BY 
            customer_id, gender, age, invoice_date,invoice_date,quantity,price
    ),
    rfm_calc AS (
        SELECT *,
            NTILE(3) OVER (ORDER BY last_date_order) AS rfm_recency,
            NTILE(3) OVER (ORDER BY total_orders) AS rfm_frequency,
            NTILE(3) OVER (ORDER BY revenue) AS rfm_monetary
        FROM rfm_data
    )
    SELECT  customer_id, gender, age, last_date_order, total_orders, revenue,
        rfm_recency + rfm_frequency + rfm_monetary AS rfm_score
     
        
    FROM rfm_calc order by rfm_score desc  limit """ + str(num_customers) +""";
    """
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        st.dataframe(df)
        st.write("Displaying top customer insights here.")

    # RFM Segmentation Section
    if insight_menu == "RFM Segmentation":
       
         # Query to calculate segmentation
        query = """
        WITH rfm_data AS (
        SELECT
            customer_id, 
            gender, 
            age, 
          
            DATEDIFF('2024-01-01', invoice_date) AS last_date_order,
            SUM(quantity) AS total_orders,
            CAST(SUM(price * quantity ) AS DECIMAL(10, 2)) AS revenue  
        FROM 
            customer_data
        GROUP BY 
            customer_id, gender, age, invoice_date,invoice_date,quantity,price
    ),
    rfm_calc AS (
        SELECT *,
            NTILE(3) OVER (ORDER BY last_date_order) AS rfm_recency,
            NTILE(3) OVER (ORDER BY total_orders) AS rfm_frequency,
            NTILE(3) OVER (ORDER BY revenue) AS rfm_monetary
        FROM rfm_data
    )
    SELECT  customer_id, gender, age, last_date_order, total_orders, revenue, rfm_recency, rfm_frequency, rfm_monetary,
        rfm_recency + rfm_frequency + rfm_monetary AS rfm_score,
        CONCAT(rfm_recency, rfm_frequency, rfm_monetary) AS rfm,
        CASE
            WHEN CONCAT(rfm_recency, rfm_frequency, rfm_monetary) IN ('311', '312', '311') THEN 'new customers'
            WHEN CONCAT(rfm_recency, rfm_frequency, rfm_monetary) IN ('111', '121', '131', '122', '133', '113', '112', '132') THEN 'lost customers'
            WHEN CONCAT(rfm_recency, rfm_frequency, rfm_monetary) IN ('212', '313', '123', '221', '211', '232') THEN 'regular customers'
            WHEN CONCAT(rfm_recency, rfm_frequency, rfm_monetary) IN ('223', '222', '213', '322', '231', '321', '331') THEN 'loyal customers'
            WHEN CONCAT(rfm_recency, rfm_frequency, rfm_monetary) IN ('333', '332', '323', '233') THEN 'top customers'
        END AS rfm_segment
    FROM rfm_calc;
    """

        # Execute the query
        cursor.execute(query)
        data = cursor.fetchall()

        # Convert the result to a DataFrame
        df = pd.DataFrame(data, columns=[
        "customer_id", "gender", "age", 
        "last_date_order", "total_orders", "revenue", "rfm_recency", 
        "rfm_frequency", "rfm_monetary", "rfm_score", "rfm", "rfm_segment"
        ])

        # Visualization: Pie Chart for Segmentation
        st.write("### Segmentation Distribution")
        segment_counts = df["rfm_segment"].value_counts().reset_index()
        segment_counts.columns = ["Segment", "Count"]

        fig = px.pie(
            segment_counts, 
            names="Segment", 
            values="Count", 
            
        )
        st.plotly_chart(fig)
####################22:15####################
         # Dropdown for selecting a customer segment
        segment_options = ["new customers", "lost customers", "regular customers", "loyal customers", "top customers"]
        selected_segment = st.selectbox("Select a customer segment", segment_options)
        if selected_segment=="new customers":
            filter= "IN ('311', '312', '311')"
        elif selected_segment=="lost customers":
            filter="IN ('111', '121', '131', '122', '133', '113', '112', '132')"
        elif selected_segment=="regular customers":
            filter="IN ('212', '313', '123', '221', '211', '232')"
        elif selected_segment=="loyal customers":
            filter="IN ('223', '222', '213', '322', '231', '321', '331')"
        elif selected_segment=="top customers":
            filter=" IN ('333', '332', '323', '233')"
        
        
        query =  """
    WITH rfm_data AS (
        SELECT
            customer_id, 
            gender, 
            age, 
          
            DATEDIFF('2024-01-01', invoice_date) AS last_date_order,
            SUM(quantity) AS total_orders,
            CAST(SUM(price * quantity ) AS DECIMAL(10, 2)) AS revenue  
        FROM 
            customer_data
        GROUP BY 
            customer_id, gender, age, invoice_date,invoice_date,quantity,price
    ),
    rfm_calc AS (
        SELECT *,
            NTILE(3) OVER (ORDER BY last_date_order) AS rfm_recency,
            NTILE(3) OVER (ORDER BY total_orders) AS rfm_frequency,
            NTILE(3) OVER (ORDER BY revenue) AS rfm_monetary
        FROM rfm_data
    )
    SELECT  customer_id, gender, age, last_date_order, total_orders, revenue,
     
        CASE
            WHEN CONCAT(rfm_recency, rfm_frequency, rfm_monetary) IN ('311', '312', '311') THEN 'new customers'
            WHEN CONCAT(rfm_recency, rfm_frequency, rfm_monetary) IN ('111', '121', '131', '122', '133', '113', '112', '132') THEN 'lost customers'
            WHEN CONCAT(rfm_recency, rfm_frequency, rfm_monetary) IN ('212', '313', '123', '221', '211', '232') THEN 'regular customers'
            WHEN CONCAT(rfm_recency, rfm_frequency, rfm_monetary) IN ('223', '222', '213', '322', '231', '321', '331') THEN 'loyal customers'
            WHEN CONCAT(rfm_recency, rfm_frequency, rfm_monetary) IN ('333', '332', '323', '233') THEN 'top customers'
        END AS rfm_segment
    FROM rfm_calc where CONCAT(rfm_recency, rfm_frequency, rfm_monetary)  """ + filter +""";
    """
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        st.dataframe(df)
        

    # Acquiring New Customers Section
    if insight_menu == "Acquiring New Customers":
        st.header("Acquiring New Customers")
        # Add logic for acquiring new customers
        st.write("Display strategies for acquiring new customers here.")

    # Product Recommendations Section
    if insight_menu == "Product Recommendations":
        st.header("Product Recommendations")
        # Add logic for product recommendations
        st.write("Display recommended products for customers here.")

    # Predicting Churn Section
    if insight_menu == "Predicting Churn":
        st.header("Predicting Customer Churn")
        query =  """
    WITH rfm_data AS (
        SELECT
            customer_id, 
            gender, 
            age, 
          
            DATEDIFF('2024-01-01', invoice_date) AS last_date_order,
            SUM(quantity) AS total_orders,
            CAST(SUM(price * quantity ) AS DECIMAL(10, 2)) AS revenue  
        FROM 
            customer_data
        GROUP BY 
            customer_id, gender, age, invoice_date,invoice_date,quantity,price
    ),
    rfm_calc AS (
        SELECT *,
            NTILE(3) OVER (ORDER BY last_date_order) AS rfm_recency,
            NTILE(3) OVER (ORDER BY total_orders) AS rfm_frequency,
            NTILE(3) OVER (ORDER BY revenue) AS rfm_monetary
        FROM rfm_data
    )
    SELECT  customer_id, gender, age, last_date_order, total_orders, revenue,
    rfm_recency + rfm_frequency + rfm_monetary AS rfm_score
    FROM rfm_calc where CONCAT(rfm_recency, rfm_frequency, rfm_monetary)  IN ('111', '121', '131', '122', '133', '113', '112', '132')
    LIMIT 30;
    """
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        st.dataframe(df) 
        # Add logic for churn prediction
        st.write("Display churn prediction insights here.")
    



# Add Entry
elif choice == "Add Entry":
    st.subheader("Add New Customer Entry")
    with st.form("add_form"):
        invoice_number = st.text_input("Invoice Number")
        invoice_number_error = st.empty()
        
        customer_id = st.text_input("Customer ID")
        customer_id_error = st.empty()
        
        gender = st.selectbox("Gender", ["Male", "Female"])
        gender_error = st.empty()
        
        age = st.number_input("Age", min_value=1, max_value=120)
        age_error = st.empty()
        
        category = st.selectbox("Category",[
        "Books",
        "Clothing",
        "Cosmetics",
        "Food & Beverage",
        "Shoes",
        "Souvenir",
        "Technology",
        "Toys"])
        category_error = st.empty()
        
        quantity = st.number_input("Quantity", min_value=1)
        quantity_error = st.empty()
        
        price = st.number_input("Price", min_value=0.0)
        price_error = st.empty()
        
        payment_method = st.selectbox("Payment Method",[ "Cash", "Credit Card", "Debit Card"])
        payment_method_error = st.empty()
        
        invoice_date = st.date_input("Invoice Date")
        invoice_date_error = st.empty()
        
        shopping_mall = st.selectbox("Shopping Mall",[
            "Cevahir AVM",
            "Emaar Square Mall",
            "Forum Istanbul",
            "Istinye Park",
            "Kanyon",
            "Mall of Istanbul",
            "Metrocity",
            "Metropol AVM",
            "Viaport Outlet",
            "Zorlu Center", ])
        
        shopping_mall_error = st.empty()
        
        #location = st.text_input("Location")
        submitted = st.form_submit_button("Add Entry")

        if submitted:
            has_error = False
            
            if not invoice_number:
                invoice_number_error.error("Invoice Number is required.")
                has_error = True
            elif not re.match("^[a-zA-Z0-9]*$", invoice_number):
                invoice_number_error.error("Invoice Number should be alphanumeric.")
                has_error = True
            else:
                invoice_number_error.empty()
            
            if not customer_id:
                customer_id_error.error("Customer ID is required.")
                has_error = True
            elif not re.match("^[a-zA-Z0-9]*$", customer_id):
                customer_id_error.error("Customer ID should be alphanumeric.")
                has_error = True
            else:
                customer_id_error.empty()
            
            if not gender:
                gender_error.error("Gender is required.")
                has_error = True
            else:
                gender_error.empty()
            
            if not age:
                age_error.error("Age is required.")
                has_error = True
            else:
                age_error.empty()
            
            if not category:
                category_error.error("Category is required.")
                has_error = True
            else:
                category_error.empty()
            
            if not quantity:
                quantity_error.error("Quantity is required.")
                has_error = True
            else:
                quantity_error.empty()
            
            if not price:
                price_error.error("Price is required.")
                has_error = True
            else:
                price_error.empty()
            
            if not payment_method:
                payment_method_error.error("Payment Method is required.")
                has_error = True
            else:
                payment_method_error.empty()
            
            if not invoice_date:
                invoice_date_error.error("Invoice Date is required.")
                has_error = True
            elif invoice_date > datetime.date.today():
                invoice_date_error.error("Invoice Date cannot be in the future.")
                has_error = True
            else:
                invoice_date_error.empty()
            
            if not shopping_mall:
                shopping_mall_error.error("Shopping Mall is required.")
                has_error = True
            else:
                shopping_mall_error.empty()
            
            if not has_error:
                query = """
                    INSERT INTO customer_data (invoice_number, customer_id, gender, age, category, quantity, price, payment_method, invoice_date, shopping_mall)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (invoice_number, customer_id, gender, age, category, quantity, price, payment_method, invoice_date, shopping_mall)
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
            #location = st.text_input("Location", value=result["location"])
            submitted = st.form_submit_button("Update Entry")

        # Step 3: Handle Update Click
        if submitted:
            try:
                update_query = """
                    UPDATE customer_data
                    SET age = %s, category = %s
                    WHERE customer_id = %s
                """
                cursor.execute(update_query, (age, category, customer_id))
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



elif choice == "Visualizations":
    st.subheader("Data Visualizations")

    # Revenue by Category
    st.write("### Total Revenue by Category")
    query = "SELECT category, SUM(price * quantity) AS total_revenue FROM customer_data GROUP BY category;"
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["category", "total_revenue"])
    fig = px.bar(df, x="category", y="total_revenue", title="Total Revenue by Category")
    st.plotly_chart(fig)

    # Customer Age Distribution
    st.write("### Customer Age Distribution")
    query = "SELECT age FROM customer_data;"
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["age"])
    fig = px.histogram(df, x="age", nbins=10, title="Customer Age Distribution")
    st.plotly_chart(fig)

    # Sales Trends Over Time
    st.write("### Sales Trends Over Time")
    query = "SELECT invoice_date, SUM(price * quantity) AS total_sales FROM customer_data GROUP BY invoice_date ORDER BY invoice_date;"
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["invoice_date", "total_sales"])
    df["Invoice Date"] = pd.to_datetime(df["invoice_date"])
    fig = px.line(df, x="invoice_date", y="total_sales", title="Sales Trends Over Time")
    st.plotly_chart(fig)

    # Payment Method Usage
    st.write("### Payment Method Usage")
    query = "SELECT payment_method, COUNT(*) AS count FROM customer_data GROUP BY payment_method;"
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["payment_method", "count"])
    fig = px.pie(df, names="payment_method", values="count", title="Payment Method Usage")
    st.plotly_chart(fig)

    # Query to fetch spending by gender
    query = """
    SELECT 
    gender, 
    SUM(quantity) AS orders, 
    CAST(SUM(price) AS DECIMAL(10, 2)) AS revenue
    FROM 
    customer_data
    GROUP BY 
    gender
    ORDER BY 
    revenue DESC;
    """
    cursor.execute(query)
    data = cursor.fetchall()

    # Create DataFrame
    df = pd.DataFrame(data, columns=["gender", "orders", "revenue"])

    # Reshape DataFrame for grouped bar chart
    df_melted = df.melt(id_vars="gender", 
                    value_vars=["orders", "revenue"], 
                    var_name="Metric", 
                    value_name="Value")

# Debugging: Uncomment to see the DataFrame
# st.write(df_melted)

    # Create grouped bar chart
    fig = px.bar(
        df_melted, 
        x="gender", 
        y="Value", 
        color="Metric", 
        barmode="group",  # Grouped bars
        title="Spending and Orders by Gender",
        labels={"Value": "Value", "Gender": "Gender"}
    )

    # Show chart in Streamlit
    st.plotly_chart(fig)




elif choice == "RFM Analysis":
    st.subheader("RFM Analysis")

    # Query to calculate RFM metrics
    query = """
    WITH recency AS (
        SELECT customer_id, DATEDIFF('2023-03-15', MAX(invoice_date)) AS recency
        FROM customer_data
        GROUP BY customer_id
    ),
    frequency AS (
        SELECT customer_id, COUNT(*) AS frequency
        FROM customer_data
        GROUP BY customer_id
    ),
    monetary AS (
        SELECT customer_id, SUM(price * quantity) AS monetary
        FROM customer_data
        GROUP BY customer_id
    )
    SELECT 
        r.customer_id, 
        r.recency, 
        f.frequency, 
        m.monetary
    FROM 
        recency r
    JOIN 
        frequency f ON r.customer_id = f.customer_id
    JOIN 
        monetary m ON r.customer_id = m.customer_id;
    """
    
    # Execute the query
    cursor.execute(query)
    data = cursor.fetchall()

    # Create a DataFrame
    df = pd.DataFrame(data, columns=["customer_id", "recency", "frequency", "monetary"])
    st.dataframe(df)

    # Visualize RFM Segmentation
    st.write("### RFM Segmentation")

    df["monetary"] = df["monetary"].astype(float)
    
    # Add RFM scoring bins (1-5 for each)
  
# Handle identical or non-divisible bins with 'duplicates' kwarg
    try:    
        df["R_Score"] = pd.cut(df["recency"], 5, labels=[5, 4, 3, 2, 1], duplicates="drop")  # Lower Recency is better
        df["F_Score"] = pd.cut(df["frequency"], 5, labels=[1, 2, 3, 4, 5], duplicates="drop")  # Higher Frequency is better
        df["M_Score"] = pd.cut(df["monetary"], 5, labels=[1, 2, 3, 4, 5], duplicates="drop")  # Higher Monetary is better
    except ValueError:
    # Fallback: Assign default scores if bins can't be created
        df["R_Score"] = 3
        df["F_Score"] = 3
        df["M_Score"] = 3

    # Create an RFM Segment
    df["RFM_Segment"] = df["R_Score"].astype(str) + df["F_Score"].astype(str) + df["M_Score"].astype(str)

    # RFM Score
    df["RFM_Score"] = df[["R_Score", "F_Score", "M_Score"]].sum(axis=1)

    # Display the updated DataFrame
    st.write("### RFM Scored Data")
    st.dataframe(df)

    # Visualize RFM Segmentation
    st.write("### RFM Distribution")
    fig = px.scatter(
        df, 
        x="recency", 
        y="monetary", 
        size="frequency", 
        color="RFM_Score",
        title="RFM Segmentation",
        labels={"Recency": "Recency (Days)", "Monetary": "Monetary Value ($)", "Frequency": "Frequency"}
    )
    st.plotly_chart(fig)




elif choice == "Segmentation":
    st.subheader("Customer Segmentation")

    # Query to calculate segmentation
    query = """
    WITH rfm_data AS (
        SELECT
            customer_id, 
            gender, 
            age, 
          
            DATEDIFF('2024-01-01', invoice_date) AS last_date_order,
            SUM(quantity) AS total_orders,
            CAST(SUM(price * quantity ) AS DECIMAL(10, 2)) AS revenue  
        FROM 
            customer_data
        GROUP BY 
            customer_id, gender, age, invoice_date,invoice_date,quantity,price
    ),
    rfm_calc AS (
        SELECT *,
            NTILE(3) OVER (ORDER BY last_date_order) AS rfm_recency,
            NTILE(3) OVER (ORDER BY total_orders) AS rfm_frequency,
            NTILE(3) OVER (ORDER BY revenue) AS rfm_monetary
        FROM rfm_data
    )
    SELECT  customer_id, gender, age, last_date_order, total_orders, revenue, rfm_recency, rfm_frequency, rfm_monetary,
        rfm_recency + rfm_frequency + rfm_monetary AS rfm_score,
        CONCAT(rfm_recency, rfm_frequency, rfm_monetary) AS rfm,
        CASE
            WHEN CONCAT(rfm_recency, rfm_frequency, rfm_monetary) IN ('311', '312', '311') THEN 'new customers'
            WHEN CONCAT(rfm_recency, rfm_frequency, rfm_monetary) IN ('111', '121', '131', '122', '133', '113', '112', '132') THEN 'lost customers'
            WHEN CONCAT(rfm_recency, rfm_frequency, rfm_monetary) IN ('212', '313', '123', '221', '211', '232') THEN 'regular customers'
            WHEN CONCAT(rfm_recency, rfm_frequency, rfm_monetary) IN ('223', '222', '213', '322', '231', '321', '331') THEN 'loyal customers'
            WHEN CONCAT(rfm_recency, rfm_frequency, rfm_monetary) IN ('333', '332', '323', '233') THEN 'top customers'
        END AS rfm_segment
    FROM rfm_calc;
    """

    # Execute the query
    cursor.execute(query)
    data = cursor.fetchall()

    # Convert the result to a DataFrame
    df = pd.DataFrame(data, columns=[
        "customer_id", "gender", "age", 
        "last_date_order", "total_orders", "revenue", "rfm_recency", 
        "rfm_frequency", "rfm_monetary", "rfm_score", "rfm", "rfm_segment"
    ])

    # Display the DataFrame in the app
    st.write("### Segmentation Results")
    st.dataframe(df)

    # Visualization: Pie Chart for Segmentation
    st.write("### Segmentation Distribution")
    segment_counts = df["rfm_segment"].value_counts().reset_index()
    segment_counts.columns = ["Segment", "Count"]

    fig = px.pie(
        segment_counts, 
        names="Segment", 
        values="Count", 
        title="Customer Segmentation Distribution"
    )
    st.plotly_chart(fig)


# Close the database connection
conn.close()

