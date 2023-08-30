import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt


def aboutit(input_data):
    if isinstance(input_data, str) and input_data.endswith('.csv'):
        # If input is a CSV file path
        df = pd.read_csv(input_data)
        file_name = os.path.basename(input_data)
    elif isinstance(input_data, pd.DataFrame):
        # If input is a DataFrame
        df = input_data
        file_name = "DataFrame"

    print(f"File Name: {file_name}")
    print(f"File Size: {os.path.getsize(input_data) / 1024:.2f} KB")
    print(f"Number of Rows: {df.shape[0]}")
    print(f"Number of Columns: {df.shape[1]}")
    print("\nColumn Names and Data Types:")
    print(df.dtypes)

    print("\nTop 5 Rows:")
    print(df.head())

    print("\nLast 5 Rows:")
    print(df.tail())

    print("\nStatistics:")
    print(df.describe())

########################################################################

def cleanit(input_data, null_strategy="average"):
    if isinstance(input_data, str) and input_data.endswith('.csv'):
        # If input is a CSV file path
        df = pd.read_csv(input_data)
        file_name = os.path.basename(input_data)
    elif isinstance(input_data, pd.DataFrame):
        # If input is a DataFrame
        df = input_data
        file_name = "DataFrame"

    print(f"Original DataFrame ({file_name}):\n")
    print(df.head())
    print(f"\nNumber of Rows: {df.shape[0]}")
    print(f"Number of Columns: {df.shape[1]}\n")

    # Replace nulls based on null_strategy
    if null_strategy == "zero":
        print("---> Replacing nulls with zeros.\n")
        df.fillna(0, inplace=True)
    elif null_strategy == "average":
        print("---> Replacing nulls with column averages.\n")
        df.fillna(df.mean(), inplace=True)
    elif null_strategy == "previous":
        print("---> Replacing nulls with previous non-null values.\n")
        df.fillna(method='ffill', inplace=True)

    print("---> Dropping duplicate rows.")
    df.drop_duplicates(inplace=True)
    print(f"     Number of Rows: {df.shape[0]}\n")

    # Drop columns with more than 50% nulls
    null_threshold = 0.5 * len(df)
    null_columns = df.columns[df.isnull().sum() > null_threshold]
    if not null_columns.empty:
        print("---> Dropping columns with more than 50% nulls:", ', '.join(null_columns))
        df.drop(null_columns, axis=1, inplace=True)
        print(f"\nNumber of Columns After Drop: {df.shape[1]}")

    print("---> Performing one-hot encoding on categorical columns.\n")
    categorical_columns = df.select_dtypes(include=['object']).columns
    df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)

    print("\nPreprocessed DataFrame:\n")
    print(df.head())
    print(f"\nNumber of Rows: {df.shape[0]}")
    print(f"Number of Columns: {df.shape[1]}")

    return df

##############################################################################

def graphit(input_data):
    if isinstance(input_data, str) and input_data.endswith('.csv'):
        # If input is a CSV file path
        df = pd.read_csv(input_data)
        file_name = os.path.basename(input_data)
    elif isinstance(input_data, pd.DataFrame):
        # If input is a DataFrame
        df = input_data
        file_name = "DataFrame"

    print(f"Graphing for {file_name}:\n")

    # Display correlation matrix
    print("Correlation Matrix:")
    corr_matrix = df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title("Correlation Matrix")
    plt.show()

    # Plot histograms for all columns
    print("\nHistograms for Columns:")
    df.hist(bins=20, figsize=(15, 12))
    plt.tight_layout()
    plt.show()

    # Pairplot for numeric columns
    print("\nPairplot for Numeric Columns:")
    sns.pairplot(df.select_dtypes(include=['number']))
    plt.show()

    # Count plot for categorical columns
    print("\nCount Plot for Categorical Columns:")
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        plt.figure(figsize=(8, 6))
        sns.countplot(data=df, x=col)
        plt.title(f"Count Plot for {col}")
        plt.xticks(rotation=45)
        plt.show()

    # Box plot for numeric columns
    print("\nBox Plot for Numeric Columns:")
    numeric_columns = df.select_dtypes(include=['number']).columns
    for col in numeric_columns:
        plt.figure(figsize=(8, 6))
        sns.boxplot(data=df, y=col)
        plt.title(f"Box Plot for {col}")
        plt.show()


