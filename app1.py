#Load Data
#Problemstatement: In the US market, do smaller loan amounts correlate with specific business activities and is there a gender that tend to get more loans?
#Importing packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import math
from sklearn.linear_model import LinearRegression
import streamlit as st

# Read the CSV file from Google Drive
af = pd.read_csv("kiva_loans.csv")
# Here, im making an initial check of the dataset
af.head()

#Data Cleaning
#Data Cheaning: Out of the total rows in the dataset, 1611 rows have no information for the borrower_gender field. This is crucial that we clean those cells, because we will need to use borrower_genders, to answer our problem statement
print(af.isna().sum())
af = af.dropna(subset=['borrower_genders']) #Dropper rækker med intet indhold
#Here i check again, and see that borrower_genders is now 0. Great.
print(af.isna().sum())

# After i found out that the variable "borrower_gender" had more then 2 collums with genders in them, we had to drop all other genders than the top two.
top_genders = af['borrower_genders'].value_counts().nlargest(2).index
af = af[af['borrower_genders'].isin(top_genders)]
print(af['borrower_genders'].unique())

#First, i group the contries, with the loan amount, and then sunms it up. This was done, because the currecny was different, from country to country, which means i could not compare it overall, unless i calculatted the same currency.
# Then i created a new variable, that has the top 10 countries, and sorted the values descending, and only took the top 10.
country_loans = af.groupby('country')['loan_amount'].sum()
top_10_countries = country_loans.sort_values(ascending=False).head(10)
print(top_10_countries)
af_usa = af[af['country'] == 'United States']

#Visualisering
# Check for outliers
plt.figure(figsize=(10, 6))
sns.boxplot(data=af_usa, y='loan_amount')
plt.show()

# To get an overview of the variables
af_usa.info()
# First i create a new variabl. Here i do a simple value count
activity_counts = af_usa['activity'].value_counts()

# Take the top 10
top_activities = activity_counts.head(10)
top_activities.plot(kind='bar')
plt.xlabel('Activity')
plt.ylabel('Count')
plt.title('Top 10 Loan Activities')
plt.show()

# NOw to answer my problem statement, i take the data UNDER q1, if we look at the boxplot.
# This represents the lower 25% of loan amounts, as shown in the boxplot
minimum = af_usa['loan_amount'].min()
q1 = af_usa['loan_amount'].quantile(0.25)
# This now filters the data to be BETWEEN minimum and q1
af_filtered_usa = af_usa[(af_usa['loan_amount'] >= minimum) & (af_usa['loan_amount'] <= q1)]

# To show
plt.figure(figsize=(10, 6))
sns.boxplot(data=af_filtered_usa, y='loan_amount')
plt.show()
# To gain an understanding of the variance/Std. deviation they are printet here.
mean_loan_usa = af_usa['funded_amount'].mean()
median_loan_usa = af_usa['funded_amount'].median()
std_loan_usa = af_usa['funded_amount'].std()
variance_loan_usa = af_usa['funded_amount'].var()

mean_loan_usa_under_q1 = af_filtered_usa['funded_amount'].mean()
median_loan_usa_under_q1 = af_filtered_usa['funded_amount'].median()
std_loan_usa_under_q1 = af_filtered_usa['funded_amount'].std()
variance_loan_usa_under_q1 = af_filtered_usa['funded_amount'].var()

print("Mean:", mean_loan_usa)
print("Median:", median_loan_usa)
print("Std. Deviation:", std_loan_usa)
print("Variance:", variance_loan_usa)

print("Mean:", mean_loan_usa_under_q1)
print("Median:", median_loan_usa_under_q1)
print("Std. Deviation:", std_loan_usa_under_q1)
print("Variance:", variance_loan_usa_under_q1)

# Now that we have the data for the smaller loans, we first make a simple plot for the counts of each loan.
activity_counts_underq1 = af_filtered_usa['activity'].value_counts()
top_activities_under_q1 = activity_counts_underq1.head(10)
top_activities_under_q1.plot(kind='bar')
plt.xlabel('Activity')
plt.ylabel('Count')
plt.title('Top 10 Loan Activities')
plt.show()
# To get a deeper understanding of the data compared to all loans, we make a pandas dataframe, with all loans and loans under q1
comparison_df = pd.DataFrame({'all_loans': top_activities, 'loans_under_q1': top_activities_under_q1})
# Find the precentage of smaller loans and sort them
comparison_df['percentage_small_loans'] = (comparison_df['loans_under_q1'] / comparison_df['all_loans']) * 100
comparison_df_sorted = comparison_df.sort_values(by='percentage_small_loans', ascending=False)
print(comparison_df_sorted)



# Plotting it
comparison_df_sorted['percentage_small_loans'].plot(kind='bar')
plt.title('Percentage of Small Loans (Q1) by Sector')
plt.xlabel('Activity')
plt.ylabel('Percentage of Small Loans')
plt.show()
print(af_usa['borrower_genders'].unique())
# To answer the last part of the problem formulation i make a boxplot with the loan amount distrubiton by gender
sns.boxplot(x='borrower_genders', y='loan_amount', data=af_usa)
plt.xlabel('Gender')
plt.ylabel('loan_amount')
plt.title('Loan Amount Distribution by Gender')
plt.show()
#Conclussion
#Smaller loans are more common in the Cosmetics Sales, Entertainment, and Clothing sectors, while sectors like Agriculture tend to get larger loans.

#The median loan amounts are similar for both genders, but male borrowers have a wider IQR. This can show that they receive slightly larger loans withitn the q1-q3