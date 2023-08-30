# Vizedax: Instant EDA, Cleaning and Data Visualization for CSV Data
Author: Shreyas Madhav A V (avshreyasmadhav@gmail.com)

Vizedax is a powerful Python library designed to make exploratory data analysis (EDA) a breeze. With just a few lines of code, you can perform comprehensive EDA on your clean CSV datasets and create stunning visualizations of all attributes. Say goodbye to the hassle of manually inspecting and plotting data – Vizedax has got you covered!

## aboutit() Function
The aboutit() function reads a CSV file and displays the following information about the dataset:

#### Name of the file
#### Size of the file
#### Number of rows and columns
#### Column names and their data types
#### Top 5 rows
#### Last 5 rows
#### Summary statistics 

```python
from Vizedax import datagod

#For a CSV
datagod.aboutit("example.csv") 

#For a Dataframe
datagod.aboutit(df)

```


## cleanit() Function
The cleanit() function takes a DataFrame or a CSV file as its argument. It performs the following cleaning tasks:

#### Replaces null values based on the provided argument (zero, average, previous reading; default is average of the column).
#### Deletes duplicate rows.
#### Drops columns with more than 50% null values.
#### Detects categorical columns and performs one-hot encoding.

```python
from vizedax import datagod

#For a CSV
# null strategy can be on of {average ,null ,previous}
datagod.cleanit("example.csv", null_strategy) 

#For a Dataframe
datagod.cleanit(df,null_strategy)

```

## graphit() Function
The graphit() function reads a CSV file and generates exploratory data analysis visualizations:

#### Correlation matrix
#### Various graphs for all columns of the dataset

```python
from vizedax import datagod

#For a CSV
# null strategy can be on of {average ,null ,previous}
datagod.graphit("example.csv") 

#For a Dataframe
datagod.graphit(df)

```
