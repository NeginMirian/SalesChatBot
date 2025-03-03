import pandas as pd

# URL of the dataset
DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"

def load_and_clean_data():
    """Downloads and cleans the dataset."""
    df = pd.read_excel(DATA_URL)

    # Drop missing values
    df.dropna(inplace=True)

    # Select relevant columns
    df = df[['StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']]


    df = df[df['Quantity'] > 0]

    # Reset index
    df.reset_index(drop=True, inplace=True)

    return df

if __name__ == "__main__":
    df = load_and_clean_data()
    print(df.head())  # Preview data
