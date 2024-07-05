import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = 'C:/Users/gabri/Downloads/Downloads/Research Team/gravity-spy-comments-processed06-May-2021 11.05.csv'
data = pd.read_csv(file_path)

# Convert 'comment_created_at' to datetime format
data['comment_created_at'] = pd.to_datetime(data['comment_created_at'])

# Filter comments related to Q-values
q_value_comments = data[data['comment_body'].str.contains('Q-value|q-value|Q value|q value', case=False)]

# Create a new column for year and month, now that 'comment_created_at' is in datetime format
q_value_comments['year_month'] = q_value_comments['comment_created_at'].dt.to_period('M')

# Group by the new 'year_month' column to count comments per month
comments_per_month = q_value_comments.groupby('year_month').size()

# Plotting
plt.figure(figsize=(14, 7))
comments_per_month.plot(kind='bar', color='skyblue')
plt.title('Comments Related to Q-values Over Time')
plt.xlabel('Year-Month')
plt.ylabel('Number of Comments')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--')

plt.show()
