import dask.dataframe as dd

# Load the data with an appropriate partition size
partition_size = "100MB"  # Adjust as needed
df = dd.read_csv("C:/pythontest/src/5m Sales Records.csv", blocksize=partition_size)

# Perform computations on the Dask DataFrame
result = df.groupby("Order Date").sum().compute()

print(result)