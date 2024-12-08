import streamlit as st
import pandas as pd
from database import connect_to_db
import plotly.express as px
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.metrics import classification_report, accuracy_score, mean_squared_error
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import datetime

# Title of the app
st.title("Customer Insights and Segmentation Dashboard")

# Connect to the database
conn = connect_to_db()
try:
    if conn.is_connected():
        cursor = conn.cursor(dictionary=True)
    else:
        raise Exception("Database connection is not active")
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()


# Preprocessing Function
def preprocess_data(data):
    # Handle missing values
    data = data.dropna()
    
    # Encode categorical variables
    le_gender = LabelEncoder()
    data['gender'] = le_gender.fit_transform(data['gender'])
    
    # Scale numeric features
    scaler = MinMaxScaler()
    data[['quantity', 'price']] = scaler.fit_transform(data[['quantity', 'price']])
    
    return data


# Sidebar Main Menu
st.sidebar.title("Menu")
main_menu = st.sidebar.selectbox(
    "Main Menu",
    ["Data Management", "Data Driven Insights"]
)

# View Data Section
if main_menu == "Data Management":
    menu = ["View Data", "Add Entry", "Update Entry", "Delete Entry", "Visualizations"]
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
        invoice_number = st.text_input("Enter Invoice Number to Update")
        if "fetch_status" not in st.session_state:
            st.session_state.fetch_status = False

        if st.button("Fetch Data"):
            try:
                if not customer_id or not invoice_number:
                    st.error("Both Customer ID and Invoice Number are required.")
                else:
                    query = "SELECT * FROM customer_data WHERE customer_id = %s AND invoice_number = %s"
                    cursor.execute(query, (customer_id, invoice_number))
                    result = cursor.fetchone()

                    if result:
                        st.session_state["result"] = result
                        st.session_state.fetch_status = True
                        st.success("Data fetched successfully!")
                    else:
                        st.session_state.fetch_status = False
                        st.error("Customer ID/Invoice Number not found.")
            except Exception as e:
                st.error(f"An error occurred: {e}")


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
        invoice_number = st.text_input("Enter Invoice Number to Delete")
        if st.button("Delete Entry"):
            try:
                if not customer_id or not invoice_number:
                    st.error("Both Customer ID and Invoice Number are required.")
                else:
                    query_check = "SELECT * FROM customer_data WHERE customer_id = %s AND invoice_number = %s"
                    cursor.execute(query_check, (customer_id, invoice_number))
                    result = cursor.fetchone()

                    if result:
                        query_delete = "DELETE FROM customer_data WHERE customer_id = %s AND invoice_number = %s"
                        cursor.execute(query_delete, (customer_id, invoice_number))
                        conn.commit()
                        st.success("Entry deleted successfully!")
                    else:
                        st.error("Customer ID or Invoice Number not found. Deletion failed.")

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")




# Additional data visualizations
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

            

########################################################
# Data Driven Insights Section
if main_menu == "Data Driven Insights":
    st.title("Data Driven Insights")
    
    # Sub-menu for Customer Insights
    questions_menu = st.radio(
        "Choose a section",
        ["Top Customers", "RFM Segmentation", "Sales Analysis: Age Group","Customer Segmentation"]
    )

    # Top Customers Section
    if questions_menu == "Top Customers":
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
          
            DATEDIFF('2023-12-31', invoice_date) AS last_date_order,
            SUM(quantity) AS total_orders,
            CAST(SUM(price * quantity ) AS DECIMAL(10, 2)) AS revenue  
        FROM 
            customer_data
        GROUP BY 
            customer_id, gender, age
    ),
    rfm_calc AS (
        SELECT *,
             NTILE(5) OVER (ORDER BY last_date_order) AS rfm_recency,
            NTILE(5) OVER (ORDER BY total_orders) AS rfm_frequency,
            NTILE(5) OVER (ORDER BY revenue) AS rfm_monetary
        FROM rfm_data
    )
    SELECT  customer_id, gender, age, last_date_order, total_orders, revenue,
    rfm_recency , rfm_frequency , rfm_monetary ,
        rfm_recency + rfm_frequency + rfm_monetary AS rfm_score
     
        
    FROM rfm_calc order by rfm_score desc  limit """ + str(num_customers) +""";
    """
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["customer_id", "total_orders", "revenue", "last_date_order", "rfm_score"])
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        features = ["total_orders", "revenue", "last_date_order", "rfm_score"]
        scaled_data = scaler.fit_transform(df[features])
        from sklearn.cluster import KMeans

        # User selects the number of clusters
        num_clusters = st.slider("Select the number of clusters", 2, 10, 3)

        # Apply K-Means
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        df["Cluster"] = kmeans.fit_predict(scaled_data)

        #     Display results
        st.write(f"Customer Segments with {num_clusters} Clusters:")
        df = df.drop(columns=["last_date_order"])
        st.dataframe(df)

        import plotly.express as px

        fig = px.scatter(df, x="total_orders", y="revenue", color="Cluster", 
                 title="Customer Segments by Revenue and Orders",
                 hover_data=["customer_id"])
        st.plotly_chart(fig)

    # RFM Segmentation Section
    if questions_menu == "RFM Segmentation":
       
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
                 
        ################ Decision tree #####################33
        st.header("RFM Segmentation Analysis (Decision Tree Classifier)")

        # Fetches RFM data from the database
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
                customer_id, gender, age, invoice_date, invoice_date, quantity, price
        ),
        rfm_calc AS (
            SELECT *,
                NTILE(3) OVER (ORDER BY last_date_order) AS rfm_recency,
                NTILE(3) OVER (ORDER BY total_orders) AS rfm_frequency,
                NTILE(3) OVER (ORDER BY revenue) AS rfm_monetary
            FROM rfm_data
        )
        SELECT  
            customer_id, gender, age, last_date_order, total_orders, revenue, 
            rfm_recency, rfm_frequency, rfm_monetary,
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
        
        cursor.execute(query)
        result = cursor.fetchall()

        # Converting query result into a DataFrame
        rfm_df = pd.DataFrame(result, columns=["customer_id", "gender", "age", "last_date_order", 
                                            "total_orders", "revenue", "rfm_recency", 
                                            "rfm_frequency", "rfm_monetary", "rfm_score", 
                                            "rfm", "rfm_segment"])

        # Prepare the data for Decision Tree Classification
        features = ["total_orders", "revenue", "rfm_recency", "rfm_frequency", "rfm_monetary"]
        X = rfm_df[features]
        y = rfm_df["rfm_segment"]

        # Encode categorical target variable
        from sklearn.preprocessing import LabelEncoder
        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)

        # Split the data into training and testing sets
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

        # Train the Decision Tree Classifier
        from sklearn.tree import DecisionTreeClassifier
        clf = DecisionTreeClassifier(random_state=42, max_depth=5)
        clf.fit(X_train, y_train)

        # Predict and evaluate
        y_pred = clf.predict(X_test)

        # Calculate accuracy
        from sklearn.metrics import accuracy_score
        accuracy = accuracy_score(y_test, y_pred)
        st.subheader(f"Model Accuracy: {accuracy:.2f}")

        # Allow the user to input features for prediction
        st.subheader("Predict Customer Segment")
        user_input = {
            "total_orders": st.number_input("Enter Total Orders", value=10, step=1),
            "revenue": st.number_input("Enter Revenue", value=5000.0, step=100.0),
            "rfm_recency": st.number_input("Enter RFM Recency ", value=2, step=1),
            "rfm_frequency": st.number_input("Enter RFM Frequency ", value=2, step=1),
            "rfm_monetary": st.number_input("Enter RFM Monetary ", value=2, step=1),
        }

        # Convert user input into a DataFrame
        user_df = pd.DataFrame([user_input])

        # Predict the segment for the input
        predicted_segment = clf.predict(user_df)
        segment_label = label_encoder.inverse_transform(predicted_segment)[0]

        st.subheader(f"Predicted Segment: {segment_label}")

        # Visualize feature importance
        st.subheader("Feature Importance")
        importance = clf.feature_importances_
        feature_importance_df = pd.DataFrame({"Feature": features, "Importance": importance})
        feature_importance_df = feature_importance_df.sort_values(by="Importance", ascending=False)
        st.bar_chart(feature_importance_df.set_index("Feature"))

        # Dropdown for selecting a customer segment
        st.header("Check customers based on their segments")
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
    SELECT  customer_id, gender, age,  total_orders, revenue,
    rfm_recency + rfm_frequency + rfm_monetary as rfm_score,
     
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

    # Sales Analysis Section
    if questions_menu == "Sales Analysis: Age Group":
        st.header("How do age groups influence the quantity of products purchased and their preferred product categories?")

        # Fetch data from the database
        query = "SELECT * FROM customer_data"
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data)

        # Preprocess data for clustering
        df = preprocess_data(df)

        # Perform Clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        df['age_group'] = kmeans.fit_predict(df[['age']])

        # Analyze the age ranges for each cluster
        cluster_ranges = (
            df.groupby('age_group')['age']
            .agg(['min', 'max', 'mean'])
            .reset_index()
        )
        st.write("### Age Group Ranges:")
        st.dataframe(cluster_ranges)

        # Map cluster labels to meaningful age groups (adjust based on cluster_ranges)
        age_group_labels = {
            0: "Young Adults (18-30)",
            1: "Middle-Aged (31-50)",
            2: "Seniors (51+)"
        }
        df['age_group_label'] = df['age_group'].map(age_group_labels)

        # Summarize total products purchased by labeled age groups
        age_group_summary = df.groupby('age_group_label')['quantity'].sum().reset_index()

        # Update bar chart to use labeled groups
        st.write("### Total Products Purchased by Age Group:")
        fig = px.bar(
            age_group_summary,
            x='age_group_label',
            y='quantity',
            title="Total Products Purchased by Age Group",
            labels={'age_group_label': 'Age Group', 'quantity': 'Total Products'}
        )
        st.plotly_chart(fig)

        # Identify the most purchased product category for each age group
        category_summary = (
            df.groupby(['age_group_label', 'category'])['quantity']
            .sum()
            .reset_index()
        )
        most_purchased_categories = (
            category_summary.loc[
                category_summary.groupby('age_group_label')['quantity'].idxmax()
            ]
        )

        st.write("### Most Purchased Product Category by Age Group")
        st.dataframe(most_purchased_categories[['age_group_label', 'category', 'quantity']])

     # Customer Segmentation Section
    if questions_menu == "Customer Segmentation":
        st.header("What customer behaviors (age, gender, price sensitivity, and quantity purchased) predict product category preferences?")

        # Fetch data from the database
        query = "SELECT * FROM customer_data"
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data)

        # Preprocess data for classification
        df = preprocess_data(df)
        features = ['gender', 'age', 'quantity', 'price']
        X = df[features]
        y = df['category']  # Target is the product category

        # Train/Test Split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train Decision Tree Classifier
        clf = DecisionTreeClassifier(random_state=42)
        clf.fit(X_train, y_train)

        # Model Evaluation
        y_pred = clf.predict(X_test)

        # User Input for Classification
        st.write("### Enter Customer Information for Prediction:")
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.number_input("Age", min_value=10, step=1)
        quantity = st.number_input("Quantity Purchased", min_value=1, step=1)
        price = st.number_input("Price of Product", min_value=1.0, step=0.1)

        # Encode Gender Input
        gender_encoded = 0 if gender == "Male" else 1

        # Prediction
        if st.button("Classify Customer"):
            prediction = clf.predict([[gender_encoded, age, quantity, price]])
            st.write(f"The customer is classified under the '{prediction[0]}' category.")

    
# Closing the database connection
conn.close()

