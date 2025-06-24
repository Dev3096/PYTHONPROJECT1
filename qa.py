import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('EDW-1138.csv')

# Count the number of PASS and FAIL in the 'Result' column
result_counts = df['Result'].value_counts()

# Plot the results
plt.figure(figsize=(6,4))
result_counts[['PASS', 'FAIL']].plot(kind='bar', color=['green', 'red'])
plt.title('Total Number of Passed and Failed Test Cases')
plt.xlabel('Result')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

