import pandas as pd
import sqlite3



def extract_data(file_path, password):
    return pd.read_excel(file_path, password=password)

def transform_data(data_a, data_b):
    # differentiating the regions data
    data_a['region'] = 'A'
    data_b['region'] = 'B'
    
    # modify the data 
    data_a['total_sales'] = data_a['QuantityOrdered'] * data_a['ItemPrice']
    data_b['total_sales'] = data_b['QuantityOrdered'] * data_b['ItemPrice']
    
   
    combined_data = pd.concat([data_a, data_b])   #combining data
    
    remove_duplicates = combined_data.drop_duplicates(subset='OrderId')  #removing duplicates
    
    return remove_duplicates


def load_data_to_db(data, db_name='sales_data.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Creating the table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_data (
            OrderId INTEGER PRIMARY KEY,
            OrderItemId INTEGER,
            QuantityOrdered INTEGER,
            ItemPrice REAL,
            PromotionDiscount REAL,
            total_sales REAL,
            region TEXT
        )
    ''')
    
    # Insert data into the table
    data.to_sql('sales')
    data.to_sql('sales_data', conn, if_exists='replace', index=False)
    
    conn.commit()
    conn.close()

def validate_data(db_name='sales_data.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # a.Count the total number of records.
    cursor.execute('SELECT COUNT(*) FROM sales_data')
    total_records = cursor.fetchone()[0]
    print(f'Total number of records: {total_records}')
    
    # b.Find the total sales amount by region.
    cursor.execute('SELECT region, SUM(total_sales) FROM sales_data GROUP BY region')
    total_sales_by_region = cursor.fetchall()
    print(f'Total sales amount by region: {total_sales_by_region}')
    
    # c.Find the average sales amount per transaction.
    cursor.execute('SELECT AVG(total_sales) FROM sales_data')
    avg_sales_per_transaction = cursor.fetchone()[0]
    print(f'Average sales amount per transaction: {avg_sales_per_transaction}')
    
    # d.Ensure there are no duplicate id values.
    cursor.execute('SELECT OrderId, COUNT(*) FROM sales_data GROUP BY OrderId HAVING COUNT(*) > 1')
    duplicate_ids = cursor.fetchall()
    print(f'Duplicate OrderIds: {duplicate_ids}')
    
    conn.close()


data_a = extract_data('order_region_a.xlsx', 'order_region_a')
data_b = extract_data('order_region_b.xlsx', 'order_region_b')
transformed_data = transform_data(data_a, data_b)
load_data_to_db(transformed_data)
validate_data()

