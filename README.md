# Customer Insights and Segmentation Dashboard

### This streamlit web-app is deployed on [this url](https://customer-insight-engine.streamlit.app/)

The **Customer Insights and Segmentation Dashboard** is an interactive Streamlit app designed to help retail businesses derive actionable insights from customer data. At its core, the app features **RFM Segmentation**, a powerful framework to categorize customers and enhance business intelligence.

## RFM Segmentation Highlights

### What It Does
Categorizes customers based on three key metrics:
- **Recency**: How recently a customer made a purchase.
- **Frequency**: How often a customer makes purchases.
- **Monetary Value**: How much revenue a customer generates.

### Actionable Insights
Identifies customer segments like:
- **Top Customers**: High-value, loyal customers.
- **New Customers**: Recently acquired customers.
- **Lost Customers**: Customers who need re-engagement.
- **Regular Customers**: Steady, consistent buyers.
- **Loyal Customers**: Highly frequent and valuable customers.

### Business Intelligence
- **Resource Allocation**: Helps allocate marketing resources effectively.
- **Re-engagement Strategies**: Guides re-engagement strategies for lost customers.
- **Upselling and Retention**: Pinpoints high-potential customer segments for upselling and retention.
- **Strategic Improvements**: Highlights gaps in customer retention to improve business strategy.



## Team Number 29

| Name                           | UB Number |
| ------------------------------ | --------- |
| Adnan Shahid Sadar             | 50592332  |
| Mohammed Abdul Aftab Muddassir | 50604245  |
| Rachana Ramesh                 | 50596083  |
| Brunda Venkatesh               | 50610164  |

## Folder Structure

```
├── datasets/
│   ├── customer_shopping_data.csv
│   ├── df_encoded.csv
│   ├── customer_shopping_data_processed.csv
│   └── processed_data.csv
├── exp/
│   ├── 50592332_phase2.ipynb
│   ├── 50596083_phase2.ipynb
│   ├── 50604245_phase2.ipynb
│   |── 50610164_phase2.ipynb
│   |── phase1.ipynb
├── app/
│   ├── streamlit_app.py
│   ├── database.py
│   ├── requirements.txt
└── README.md
└── app_short_video.mp4
└── project_report.pdf
```

## Questions and Code Locations

### Adnan Shahid Sadar(50592332)

- **Question 1:** How do age groups influence the quantity of products purchased and their preferred product categories?
- **Code 1 Location:** `app/streamlit_app.py line 704`
- **Analysis 1 Location:** `refer to project_report.pdf`
- **Question 2:** What customer behaviours (age, gender, price sensitivity, and quantity purchased) predict product category preferences?
- **Code 2 Location:** `app/streamlit_app.py line 767`
- **Analysis 2 Location:** `refer to project_report.pdf`

### Mohammed Abdul Aftab Muddassir

- **Question 1:** Who are the top customers contributing the most revenue?
- **Code Location:** `app/streamlit_app.py line 420`
- **Analysis 1 Location:** `refer to project_report.pdf`
- **Question 2:** How many customers fall into each RFM segment, and what is their behaviour?
- **Code Location:** `app/streamlit_app.py line 484`
- **Analysis 2 Location:** `refer to project_report.pdf`

## Instructions to Build and Run the App

### Prerequisites

1. **Python**: Ensure you have Python 3.7 or higher installed. You can download it from [python.org](https://www.python.org/downloads/).
2. **Git**: Ensure you have Git installed. You can download it from [git-scm.com](https://git-scm.com/downloads).

### Instructions

1. **Clone the Repository**:
   Open a terminal and clone the repository using Git:

   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**:
   Install the required Python packages using `pip`:

   ```sh
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the `app` directory with the following content:

   ```env
   DB_HOST=YOUR_HOSTNAME
   DB_USER=YOUR_USERNAME
   DB_PASSWORD=YOUR_PW
   DB_NAME=YOUR_DBNAME
   DB_PORT=YOUR_PORTNO
   ```

4. **Run the Streamlit App**:
   Navigate to the `app` directory and run the Streamlit app:

   ```sh
   cd app
   streamlit run streamlit_app.py
   ```

5. **Additional Notes**:
   - **Database Setup**: Ensure that your MySQL database is running and accessible with the credentials provided in the `.env` file.
