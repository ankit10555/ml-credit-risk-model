import streamlit as st
from predict_helper import predict

st.title("SRI AAM Finance: Credit Risk Model")

# Use a container to group inputs, ensuring vertical layout
with st.container():
    # Define 4 rows with 3 columns each
    row1 = st.columns(3)
    row2 = st.columns(3)
    row3 = st.columns(3)
    row4 = st.columns(3)

    # Row 1: Age, Income, Loan Amount
    with row1[0]:
        age = st.number_input('Age', min_value=18, max_value=100, value=31, step=1)
    with row1[1]:
        income = st.number_input('Income', min_value=0, value=120000)
    with row1[2]:
        loan_amount = st.number_input('Loan Amount', value=566789, min_value=0)

    # Loan to Income Ratio Display in Row 2[0]
    loan_to_income_ratio = loan_amount / income if income > 0 else 0
    with row2[0]:
        st.markdown(
            f"""
            <div style="
                background-color: #ffff99;
                padding: 20px;
                border-radius: 5px;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
                color: #211;
            ">
                Loan/Income: {loan_to_income_ratio:.2f}
            </div>
            """,
            unsafe_allow_html=True
        )

    # Add remaining inputs
    with row2[1]:
        loan_tenure_months = st.number_input('Loan Tenure (Months)', min_value=6, max_value=360, step=1, value=120)

    with row2[2]:
        number_of_open_accounts = st.number_input('Open Credit Accounts', min_value=0, step=1, value=2)

    with row3[0]:
        credit_utilization_ratio = st.number_input('Credit Utilization Ratio', min_value=0.0, max_value=1.0, step=0.01, value=0.70)

    with row3[1]:
        delinquency_ratio = st.number_input('Delinquency Ratio', min_value=0.0, max_value=1.0, step=0.01, value=0.60)

    with row3[2]:
        avg_dpd_per_delinquency = st.number_input('Avg DPD', min_value=0, max_value=365, step=1, value=7)

    with row4[0]:
        loan_purpose = st.selectbox('Loan Purpose', ['Home', 'Auto', 'Personal', 'Education'])

    with row4[1]:
        residence_type = st.selectbox('Residence Type', ['Owned', 'Mortgage', 'Rented'])

    with row4[2]:
        loan_type = st.selectbox('Loan Type', ['Secured', 'Unsecured'])

st.markdown("---")

# Submit Button and Output Section
submit_button = st.button("Calculate Risk")

if submit_button:
    probablity, credit_score, rating = predict(
        credit_utilization_ratio, delinquency_ratio,
        loan_amount, income, avg_dpd_per_delinquency,
        loan_purpose, residence_type,
        loan_tenure_months, loan_type, age,
        number_of_open_accounts
    )

    st.markdown("## 🧾 Risk Report")
    st.markdown(f"- **Default Probability**: `{probablity:.2%}`")
    st.markdown(f"- **Credit Score**: `{credit_score}`")
    st.markdown(f"- **Rating**: `{rating}`")
