import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('esg_data.csv')

# Example plots
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Bank', y='Environmental Score')
plt.title('Environmental Scores by Bank')
plt.savefig('environmental_scores.png')

plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Bank', y='Social Score')
plt.title('Social Scores by Bank')
plt.savefig('social_scores.png')

plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Bank', y='Governance Score')
plt.title('Governance Scores by Bank')
plt.savefig('governance_scores.png')
