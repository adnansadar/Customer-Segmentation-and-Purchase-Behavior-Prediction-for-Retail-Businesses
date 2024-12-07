# Customer-Segmentation-and-Purchase-Behavior-Prediction-for-Retail-Businesses

## Team Number 29

| Name                           | UB Number |
| ------------------------------ | --------- |
| Adnan Shahid Sadar             | 50592332  |
| Rachana Ramesh                 | 50596083  |
| Mohammed Abdul Aftab Muddassir | 50604245  |
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
├── pdf/
│   ├── 50592332_phase2.pdf
│   ├── 50604245_phase2.pdf
│   ├── 50596083_phase2.pdf
│   ├── 50610164_phase2.pdf
├── app/
│   ├── streamlit_app.py
│   ├── database.py
│   ├── requirements.txt
└── README.md
```

## Questions and Code Locations

### Adnan Shahid Sadar(50592332)

- **Question 1:** How do age and gender affect customer preferences for different product categories?
- **Question 2:** Do customers in different locations (shopping malls) show distinct purchasing behaviors?
- **Code 1 Location:** `src/50592332_phase2.ipynb`
- **Analysis 1 Location:** `refer to src/50592332_phase2.ipynb or pdf/50592332_phase2.pdf`
- **Code 2 Location:** `src/50592332_phase2.ipynb`
- **Analysis 2 Location:** `refer to src/50592332_phase2.ipynb or pdf/50592332_phase2.pdf`

### Rachana Ramesh

- **Question:** How can we predict customer purchase behavior?
- **Code Location:** `src/rachana_purchase_prediction.ipynb`
- **Analysis Location:** `src/rachana_purchase_prediction.ipynb`

### Mohammed Abdul Aftab Muddassir

- **Question 1:** Which product categories are generating the highest sales, indicating a need for potential adjustments in stocking strategies?
- **Question 2:** How do the revenue trends across different quarters in 2021 and 2022 compare, and how can quarterly performance of past years be helpful to plan for the future of business?
- **Code Location:** `src/50604245_phase2.ipynb`
- **Analysis Location:** `src/50604245_phase2.ipynb or 50604245_phase2.pdf`

### Brunda Venkatesh

- **Question:** How do external factors affect customer purchasing decisions?
- **Code Location:** `src/brunda_external_factors.ipynb`
- **Analysis Location:** `src/brunda_external_factors.ipynb`

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
