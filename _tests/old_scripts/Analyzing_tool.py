import pandas as pd

# Load the data
file_path = 'C:/Users/gabri/Downloads/Downloads/Research Team/gravity-spy-comments-processed06-May-2021 11.05.csv'
data = pd.read_csv(file_path)

# Explicitly print the first few rows of the dataframe to understand its structure
print(data.head())

data.head()

import matplotlib.pyplot as plt


# Convert 'comment_created_at' to datetime format
data['comment_created_at'] = pd.to_datetime(data['comment_created_at'])

# Resample to get the number of comments per day
comments_per_day = data.set_index('comment_created_at').resample('D').size()

# Plotting
plt.figure(figsize=(12, 6))
comments_per_day.plot()
plt.title('Number of Comments Per Day')
plt.xlabel('Date')
plt.ylabel('Number of Comments')
plt.grid(True)
plt.show()

