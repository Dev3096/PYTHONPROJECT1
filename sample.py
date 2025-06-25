import pandas as pd
import matplotlib.pyplot as plt

print("Hello")

print("This is a Demo Script")

# Read the CSV file
csv_file = 'monitor_pipelines1.csv'
df = pd.read_csv(csv_file)

# Count the occurrences of each status
df['Status'] = df['Status'].fillna('Unknown')
status_counts = df['Status'].value_counts()

# Plot the status counts
plt.figure(figsize=(8, 5))
status_counts.plot(kind='bar', color='skyblue')
plt.title('Pipeline Run Status Counts')
plt.xlabel('Status')
plt.ylabel('Number of Runs')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
