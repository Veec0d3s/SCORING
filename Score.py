# credit_scoring_app_v2.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Credit Scoring System", layout="wide")
st.title("AI Credit Scoring System")

# Step 1: Upload Dataset
file = st.file_uploader("Upload CSV or Excel file", type=['csv', 'xls', 'xlsx'])
if file:
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        st.success("Dataset loaded successfully!")
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    # Check required columns
    required_columns = ['Name', 'Character', 'Capacity', 'Collateral', 'Condition', 'Capital', 'Income', 'CollateralValue']
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        st.error(f"Missing required columns: {missing_cols}")
        st.stop()

    # Step 2: Select Person
    name = st.selectbox("Select a person", df['Name'].unique())
    person_data = df[df['Name'] == name].iloc[0]

    # Step 3: Calculate 5 Cs Scores
    scores = {
        "Character": person_data['Character'],
        "Capacity": person_data['Capacity'],
        "Collateral": person_data['Collateral'],
        "Condition": person_data['Condition'],
        "Capital": person_data['Capital']
    }
    total_score = sum(scores.values())  # Max 50

    st.subheader(f"Credit Score for {name}: {total_score}/50")

    # Step 4: Determine Suggested Loan Amount Based on Score
    income = person_data['Income']
    collateral_value = person_data['CollateralValue']

    # Scale loan amount based on credit score
    # Credit score 0-50, we normalize to 0.2x - 1x max possible
    score_ratio = total_score / 50
    min_ratio = 0.2  # even lowest scorer gets 20% of max possible
    effective_ratio = min_ratio + (score_ratio * (1 - min_ratio))
    
    recommended_loan = min(income * 0.5, collateral_value * 0.7) * effective_ratio
    st.write(f"Suggested Loan Amount: ${recommended_loan:,.2f}")

    # Step 5: Visualize Scores
    st.subheader("5 Cs Credit Score Breakdown")
    fig, ax = plt.subplots()
    ax.bar(scores.keys(), scores.values(), color='mediumorchid')
    ax.set_ylim(0, 10)
    ax.set_ylabel("Score (1-10)")
    ax.set_title("Credit Score Components")
    st.pyplot(fig)
