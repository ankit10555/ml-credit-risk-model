import joblib
from joblib import load
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
model_path='artifacts/model_data.joblib'
model_data=joblib.load(model_path)
model=model_data['model']
scalar=model_data['scalar']
features=model_data['features']
cols_to_scale=model_data['cols_to_scale']





def prepare_df(credit_utilization_ratio,delinquency_ratio,
            loan_amount,income,avg_dpd_per_delinquency,
            loan_purpose,residence_type,
            loan_tenure_months,loan_type,age,
            number_of_open_accounts):
        input_data={
                'age':age,
                'loan_tenure_months':loan_tenure_months,
                'credit_utilization_ratio':credit_utilization_ratio,
                'number_of_open_accounts':number_of_open_accounts,
                'loan_to_income':loan_amount/income if income>0 else 0,
                'delinquency_ratio':delinquency_ratio,
                'avg_dpd_per_delinquency':avg_dpd_per_delinquency,
                'residence_type_Owned':1 if residence_type=='Owned' else 0,
                'residence_type_Rented': 1 if residence_type == 'Rented' else 0,
                'loan_purpose_Education': 1 if loan_purpose=='Education' else 0,
                'loan_purpose_Home': 1 if loan_purpose == 'Home' else 0,
                'loan_purpose_Personal': 1 if loan_purpose == 'Personal' else 0,
                'loan_type_Unsecured':1 if loan_type=='Unsecured' else 0,
                # dummy column for column scaled
                'number_of_dependants':1,
                'years_at_current_address':1,
                'sanction_amount':1,
                'gst':1,
                'net_disbursement':1,
                'principal_outstanding':1,
                'bank_balance_at_application':1,
                'number_of_closed_accounts':1,
                'enquiry_count':1,
                'processing_fee':1
        }

        df=pd.DataFrame([input_data])

        df[cols_to_scale]=scalar.transform(df[cols_to_scale])
        df=df[features]
        return df

def calculate_credit_score(df,base_score=300,scale_length=600):
        probas = model.predict_proba(df)[0]
        default_probability = probas[1]
        non_default_probability = probas[0]

        credit_score=base_score+non_default_probability*scale_length
        def calculate_rating(score):
                if 300<=score <500:
                        return 'Poor'
                if 500<=score <650:
                        return 'Average'
                if 650<=score <750:
                        return 'Good'
                else:
                        return 'Excellent'
        rating=calculate_rating(credit_score)
        return default_probability.flatten()[0],int(credit_score),rating



def predict(credit_utilization_ratio,delinquency_ratio,
            loan_amount,income,avg_dpd_per_delinquency,
            loan_purpose,residence_type,
            loan_tenure_months,loan_type,age,
            number_of_open_accounts):

        input_df=prepare_df(credit_utilization_ratio,delinquency_ratio,
            loan_amount,income,avg_dpd_per_delinquency,
            loan_purpose,residence_type,
            loan_tenure_months,loan_type,age,
            number_of_open_accounts)

        probability,credit_score,rating=calculate_credit_score(input_df)

        return probability,credit_score,rating


