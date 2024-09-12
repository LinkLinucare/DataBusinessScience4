import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data function
@st.cache_data
def load_data():
    return pd.read_csv("kiva_loans.csv")

# Load the dataset
af = load_data()

# Page navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Loan Activities", "Gender Distribution"])

# Shared introduction section
st.title('US Loan Data Analysis')
st.subheader("Exploring loans by business activities and gender")

# Show the first few rows of the dataset
st.write("Dataset preview:")
st.write(af.head())

# Shared data cleaning step
af = af.dropna(subset=['borrower_genders'])  # Clean missing borrower_gender rows
top_genders = af['borrower_genders'].value_counts().nlargest(2).index
af = af[af['borrower_genders'].isin(top_genders)]  # Keep only the top 2 genders

af_usa = af[af['country'] == 'United States']  # Filter for USA data

# Loan Activities Page
if page == "Loan Activities":
    st.header("Loan Activities Analysis")
    
    # Plot loan amount boxplot
    st.subheader("Loan Amount Distribution in the USA")
    fig, ax = plt.subplots()
    sns.boxplot(data=af_usa, y='loan_amount', ax=ax)
    st.pyplot(fig)

    # Loan activities count
    st.subheader("Top 10 Loan Activities in the USA")
    activity_counts = af_usa['activity'].value_counts().head(10)
    st.bar_chart(activity_counts)

    # Filter data for loans under Q1 (lower 25%)
    st.subheader("Loans Under Q1 (Lower 25%)")
    minimum = af_usa['loan_amount'].min()
    q1 = af_usa['loan_amount'].quantile(0.25)
    af_filtered_usa = af_usa[(af_usa['loan_amount'] >= minimum) & (af_usa['loan_amount'] <= q1)]

    # Plot loan amount distribution for smaller loans
    fig, ax = plt.subplots()
    sns.boxplot(data=af_filtered_usa, y='loan_amount', ax=ax)
    st.pyplot(fig)

    # Top loan activities for smaller loans
    activity_counts_underq1 = af_filtered_usa['activity'].value_counts()
    top_activities_under_q1 = activity_counts_underq1.head(10)
    st.subheader("Top 10 Loan Activities for Small Loans (Under Q1)")
    st.bar_chart(top_activities_under_q1)

    # Comparison of loan activities
    comparison_df = pd.DataFrame({'all_loans': activity_counts, 'loans_under_q1': top_activities_under_q1})
    comparison_df['percentage_small_loans'] = (comparison_df['loans_under_q1'] / comparison_df['all_loans']) * 100
    comparison_df_sorted = comparison_df.sort_values(by='percentage_small_loans', ascending=False)

    st.subheader("Percentage of Small Loans (Q1) by Sector")
    st.bar_chart(comparison_df_sorted['percentage_small_loans'])

# Gender Distribution Page
elif page == "Gender Distribution":
    st.header("Gender Distribution Analysis")
    
# Because it is a new statement, i write the variables again
    minimum = af_usa['loan_amount'].min()
    q1 = af_usa['loan_amount'].quantile(0.25)
    af_filtered_usa = af_usa[(af_usa['loan_amount'] >= minimum) & (af_usa['loan_amount'] <= q1)]

    # Gender distribution boxplot
    st.subheader("Loan Amount Distribution by Gender")
    fig, ax = plt.subplots()
    sns.boxplot(x='borrower_genders', y='loan_amount', data=af_usa, ax=ax)
    st.pyplot(fig)

    # Gender distribution summary statistics
    st.subheader("Summary Statistics for All Loans and Loans Under Q1")
    
    mean_loan_usa = af_usa['loan_amount'].mean()
    median_loan_usa = af_usa['loan_amount'].median()
    std_loan_usa = af_usa['loan_amount'].std()
    variance_loan_usa = af_usa['loan_amount'].var()

    mean_loan_usa_under_q1 = af_filtered_usa['loan_amount'].mean()
    median_loan_usa_under_q1 = af_filtered_usa['loan_amount'].median()
    std_loan_usa_under_q1 = af_filtered_usa['loan_amount'].std()
    variance_loan_usa_under_q1 = af_filtered_usa['loan_amount'].var()

    st.write("All loans statistics:")
    st.write(f"Mean: {mean_loan_usa}")
    st.write(f"Median: {median_loan_usa}")
    st.write(f"Standard Deviation: {std_loan_usa}")
    st.write(f"Variance: {variance_loan_usa}")

    st.write("Loans under Q1 statistics:")
    st.write(f"Mean: {mean_loan_usa_under_q1}")
    st.write(f"Median: {median_loan_usa_under_q1}")
    st.write(f"Standard Deviation: {std_loan_usa_under_q1}")
    st.write(f"Variance: {variance_loan_usa_under_q1}")