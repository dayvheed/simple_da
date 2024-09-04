import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
df = pd.read_excel('HomeworDATA.xlsx')

st.title('Betting Data Analysis Dashboard')

# Bet Amount Distribution Analysis
st.header('Bet Amount Distribution')
fig, ax = plt.subplots(figsize=(12, 6))
sns.histplot(df['Bet Amount per Event'], kde=True, bins=50, ax=ax)
ax.set_title('Distribution of Bet Amounts per Event')
ax.set_xlabel('Bet Amount per Event')
ax.set_ylabel('Frequency')
ax.axvline(df['Bet Amount per Event'].median(), color='r', linestyle='--', label='Median')
ax.axvline(df['Bet Amount per Event'].mean(), color='g', linestyle='--', label='Mean')
ax.legend()
st.pyplot(fig)

st.write(f"Mean Bet Amount: ${df['Bet Amount per Event'].mean():.2f}")
st.write(f"Median Bet Amount: ${df['Bet Amount per Event'].median():.2f}")
st.write(f"Standard Deviation: ${df['Bet Amount per Event'].std():.2f}")

# Sport Popularity and Profitability Analysis
st.header('Sport Popularity and Profitability')
sport_analysis = df.groupby('Sport').agg({
    'Bet ID': 'count',
    'Bet Amount per Event': 'mean',
    'Odds - Event': 'mean'
}).sort_values('Bet ID', ascending=False)

sport_analysis.columns = ['Number of Bets', 'Avg Bet Amount', 'Avg Odds']
sport_analysis['Popularity Rank'] = sport_analysis['Number of Bets'].rank(ascending=False)
sport_analysis['Potential Profitability'] = sport_analysis['Avg Bet Amount'] * (sport_analysis['Avg Odds'] - 1)

fig, ax = plt.subplots(figsize=(12, 6))
sns.scatterplot(data=sport_analysis.reset_index(), x='Popularity Rank', y='Potential Profitability', 
                size='Avg Bet Amount', hue='Sport', sizes=(20, 200), ax=ax)
ax.set_title('Sport Popularity vs Potential Profitability')
ax.set_xlabel('Popularity Rank (1 = Most Popular)')
ax.set_ylabel('Potential Profitability')
st.pyplot(fig)

st.write(sport_analysis)

# User Betting Behavior Analysis
st.header('User Betting Behavior')
user_analysis = df.groupby('User ID').agg({
    'Bet ID': 'count',
    'Bet Amount per Event': 'mean',
    'Is Multi Bet': 'mean',
    'Odds - Event': 'mean',
    'User Age': 'first'
})

user_analysis.columns = ['Number of Bets', 'Avg Bet Amount', 'Multi Bet Ratio', 'Avg Odds', 'Age']

fig, ax = plt.subplots(figsize=(12, 6))
scatter = ax.scatter(user_analysis['Age'], user_analysis['Avg Bet Amount'], 
                     c=user_analysis['Multi Bet Ratio'], s=user_analysis['Number of Bets'],
                     alpha=0.6, cmap='viridis')
plt.colorbar(scatter, label='Multi Bet Ratio')
ax.set_title('User Betting Behavior')
ax.set_xlabel('User Age')
ax.set_ylabel('Average Bet Amount')
st.pyplot(fig)

st.write("Correlation Matrix:")
st.write(user_analysis.corr())

high_value_users = user_analysis[user_analysis['Avg Bet Amount'] > user_analysis['Avg Bet Amount'].quantile(0.9)]
st.write("High-Value User Statistics:")
st.write(high_value_users.describe())
