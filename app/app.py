<<<<<<< HEAD
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)
import streamlit as st
import pandas as pd
import joblib

from datetime import date

from src.explainability import (
    get_customer_explanation
)

from src.genai import (
    generate_retention_strategy
)

@st.cache_resource
def load_model():

    return joblib.load(
        "models/best_churn_model.joblib"
    )


model = load_model()

st.set_page_config(
    page_title=
    "Customer Churn Intelligence",

    layout="wide"
)


st.title(
    "E-Commerce Customer Churn "
    "& Retention Intelligence"
)

st.write(
    "Predict customer churn, "
    "understand the reasons, "
    "and generate AI-powered "
    "retention strategies."
)

with st.form("customer_form"):

    st.subheader("Customer Profile")

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=69,
            value=43
        )

        gender = st.selectbox(
            "Gender",
            [
                "Female",
                "Male",
                "Other"
            ]
        )

        annual_income = st.number_input(
            "Annual Income (USD)",
            min_value=20014.0,
            max_value=149997.0,
            value=85000.0,
            step=1000.0
        )

        spending_score = st.slider(
            "Spending Score",
            min_value=1,
            max_value=99,
            value=49
        )

        membership = st.selectbox(
            "Membership Status",
            [
                "Bronze",
                "Silver",
                "Gold",
                "Platinum"
            ]
        )


    with col2:

        region = st.selectbox(
            "Region",
            [
                "Central",
                "East",
                "North",
                "South",
                "West"
            ]
        )

        payment_method = st.selectbox(
            "Preferred Payment Method",
            [
                "Credit Card",
                "Debit Card",
                "PayPal",
                "Cryptocurrency"
            ]
        )

        total_purchases = st.number_input(
            "Total Purchases",
            min_value=5,
            max_value=40,
            value=20
        )

        avg_purchase_value = st.number_input(
            "Average Purchase Value (USD)",
            min_value=10.07,
            max_value=499.95,
            value=251.95,
            step=10.0
        )


    st.subheader(
        "Customer Engagement & Experience"
    )

    col3, col4 = st.columns(2)

    with col3:

        satisfaction_score = st.slider(
            "Satisfaction Score",
            min_value=1.0,
            max_value=5.0,
            value=3.0,
            step=0.1
        )

        website_visits = st.number_input(
            "Website Visits Last Month",
            min_value=3,
            max_value=32,
            value=15
        )

        avg_time_per_visit = st.number_input(
            "Average Time Per Visit (Minutes)",
            min_value=0.5,
            max_value=12.68,
            value=4.99,
            step=0.1
        )


    with col4:

        support_tickets = st.number_input(
            "Support Tickets Last 6 Months",
            min_value=0,
            max_value=8,
            value=1
        )

        referred_friends = st.number_input(
            "Referred Friends",
            min_value=0,
            max_value=6,
            value=1
        )

        days_since_last_purchase = (
            st.number_input(
                "Days Since Last Purchase",
                min_value=0,
                max_value=365,
                value=183
            )
        )


    submitted = st.form_submit_button(
        "Analyze Customer"
    )

    if submitted:

        estimated_customer_value = (total_purchases * avg_purchase_value)

        engagement_score = ( website_visits * avg_time_per_visit)

        support_rate = (support_tickets/ (total_purchases + 1))

        customer_df = pd.DataFrame(
        [{
        "Age": age,

        "Gender": gender,

        "Annual_Income_USD":
            annual_income,

        "Spending_Score":
            spending_score,

        "Membership_Status":
            membership,

        "Preferred_Payment_Method":
            payment_method,

        "Region":
            region,

        "Total_Purchases":
            total_purchases,

        "Avg_Purchase_Value":
            avg_purchase_value,

        "Satisfaction_Score":
            satisfaction_score,

        "Website_Visits_Last_Month":
            website_visits,

        "Avg_Time_Per_Visit_Minutes":
            avg_time_per_visit,

        "Support_Tickets_Last_6_Months":
            support_tickets,

        "Referred_Friends":
            referred_friends,

        "Days_Since_Last_Purchase":
            days_since_last_purchase,

        "Estimated_Customer_Value":
        estimated_customer_value,

        "Engagement_Score":
            engagement_score,

        "Support_Rate":
            support_rate
        }])

        churn_probability = (
        model.predict_proba(
        customer_df
        )[0][1])

        if churn_probability >= 0.70:

         risk_level = "High"

        elif churn_probability >= 0.40:

         risk_level = "Medium"

        else:

         risk_level = "Low"

        if estimated_customer_value >= 7500:
         customer_value = "High"
        
        elif estimated_customer_value >= 3000:
         customer_value = "Medium"

        else:
         customer_value = "Low"

        retention_priority = (churn_probability * estimated_customer_value)

        col1, col2, col3, col4 = (
         st.columns(4))


        col1.metric(
         "Churn Probability",
        f"{churn_probability:.1%}")


        col2.metric(
         "Risk Level",
         risk_level)


        col3.metric(
         "Customer Value",
         customer_value)

 
        col4.metric(
        "Retention Priority",
         f"{retention_priority:,.0f}")



        shap_explanation = (
            get_customer_explanation(
            model,
            customer_df,
            top_n=5
            )
        )


        def clean_feature_name(feature_name):

    # Remove prefixes added by ColumnTransformer
         feature_name = feature_name.replace("num__", "")
         feature_name = feature_name.replace("cat__", "")

         feature_mapping={

        "Age":
            "Age",

        "Gender": "Gender",

        "Annual_Income_USD":
            "Annual Income",

        "Membership_Status":
            "Membership",

        "Spending_Score":
            "Spending Score",

        "Total_Purchases":
            "Total Purchases",

        "Avg_Purchase_Value":
            "Average Purchase Value",

        "Satisfaction_Score":
            "Satisfaction Score",

        "Website_Visits_Last_Month":
            "Website Visits Last Month",

        "Avg_Time_Per_Visit_Minutes":
            "Average Time Per Visit",

        "Support_Tickets_Last_6_Months":
            "Support Tickets",

        "Referred_Friends":
            "Referred Friends",

        "Days_Since_Last_Purchase":
            "Days Since Last Purchase",

        "Estimated_Customer_Value":
            "Estimated Customer Value",

        "Engagement_Score":
            "Engagement Score",

        "Support_Rate":
            "Support Rate",}


         if feature_name in feature_mapping:
            return feature_mapping[feature_name]

        


   
         if feature_name.startswith(
        "Gender_"):

          value = feature_name.replace(
            "Gender_",
            ""
        )

          return f"Gender: {value}"


         if feature_name.startswith(
        "Membership_Status_"):

          value = feature_name.replace(
            "Membership_Status_",
            ""
        )

         return f"Membership: {value}"


         if feature_name.startswith(
        "Preferred_Payment_Method_"):

          value = feature_name.replace(
            "Preferred_Payment_Method_",
            ""
        )

          return f"Payment Method: {value}"


         if feature_name.startswith(
        "Region_"):

          value = feature_name.replace(
            "Region_",
            ""
        )

          return f"Region: {value}"


         return feature_name.replace(
        "_",
        " ")

        shap_explanation["Feature"] = (
        shap_explanation["Feature"]
        .apply(clean_feature_name))

        shap_explanation["Impact"] = (
        shap_explanation["SHAP_Value"].apply(
        lambda x:
        "Increases Churn Risk"
        if x > 0
        else "Reduces Churn Risk"
        ))


        st.subheader(
          "Why is this customer at risk?"
        )
        st.dataframe(
              shap_explanation[
                  [
                    "Feature",
                    "SHAP_Value",
                    "Impact"
                  ]
              ],
              use_container_width=True
        )

        st.subheader(
        "AI Retention Recommendation"
        )

        try:


            retention_strategy = (
                generate_retention_strategy(
                  churn_probability=churn_probability,
                  risk_level=risk_level,
                  customer_value=customer_value,
                  shap_df=shap_explanation
                )
            )

            st.markdown(retention_strategy)

        except Exception as e:
          st.error(
            f"Groq Error: {e}"
        )

=======
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)
import streamlit as st
import pandas as pd
import joblib

from datetime import date

from src.explainability import (
    get_customer_explanation
)

from src.genai import (
    generate_retention_strategy
)

@st.cache_resource
def load_model():

    return joblib.load(
        "models/best_churn_model.joblib"
    )


model = load_model()

st.set_page_config(
    page_title=
    "Customer Churn Intelligence",

    layout="wide"
)


st.title(
    "E-Commerce Customer Churn "
    "& Retention Intelligence"
)

st.write(
    "Predict customer churn, "
    "understand the reasons, "
    "and generate AI-powered "
    "retention strategies."
)

with st.form("customer_form"):

    st.subheader("Customer Profile")

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=69,
            value=43
        )

        gender = st.selectbox(
            "Gender",
            [
                "Female",
                "Male",
                "Other"
            ]
        )

        annual_income = st.number_input(
            "Annual Income (USD)",
            min_value=20014.0,
            max_value=149997.0,
            value=85000.0,
            step=1000.0
        )

        spending_score = st.slider(
            "Spending Score",
            min_value=1,
            max_value=99,
            value=49
        )

        membership = st.selectbox(
            "Membership Status",
            [
                "Bronze",
                "Silver",
                "Gold",
                "Platinum"
            ]
        )


    with col2:

        region = st.selectbox(
            "Region",
            [
                "Central",
                "East",
                "North",
                "South",
                "West"
            ]
        )

        payment_method = st.selectbox(
            "Preferred Payment Method",
            [
                "Credit Card",
                "Debit Card",
                "PayPal",
                "Cryptocurrency"
            ]
        )

        total_purchases = st.number_input(
            "Total Purchases",
            min_value=5,
            max_value=40,
            value=20
        )

        avg_purchase_value = st.number_input(
            "Average Purchase Value (USD)",
            min_value=10.07,
            max_value=499.95,
            value=251.95,
            step=10.0
        )


    st.subheader(
        "Customer Engagement & Experience"
    )

    col3, col4 = st.columns(2)

    with col3:

        satisfaction_score = st.slider(
            "Satisfaction Score",
            min_value=1.0,
            max_value=5.0,
            value=3.0,
            step=0.1
        )

        website_visits = st.number_input(
            "Website Visits Last Month",
            min_value=3,
            max_value=32,
            value=15
        )

        avg_time_per_visit = st.number_input(
            "Average Time Per Visit (Minutes)",
            min_value=0.5,
            max_value=12.68,
            value=4.99,
            step=0.1
        )


    with col4:

        support_tickets = st.number_input(
            "Support Tickets Last 6 Months",
            min_value=0,
            max_value=8,
            value=1
        )

        referred_friends = st.number_input(
            "Referred Friends",
            min_value=0,
            max_value=6,
            value=1
        )

        days_since_last_purchase = (
            st.number_input(
                "Days Since Last Purchase",
                min_value=0,
                max_value=365,
                value=183
            )
        )


    submitted = st.form_submit_button(
        "Analyze Customer"
    )

    if submitted:

        estimated_customer_value = (total_purchases * avg_purchase_value)

        engagement_score = ( website_visits * avg_time_per_visit)

        support_rate = (support_tickets/ (total_purchases + 1))

        customer_df = pd.DataFrame(
        [{
        "Age": age,

        "Gender": gender,

        "Annual_Income_USD":
            annual_income,

        "Spending_Score":
            spending_score,

        "Membership_Status":
            membership,

        "Preferred_Payment_Method":
            payment_method,

        "Region":
            region,

        "Total_Purchases":
            total_purchases,

        "Avg_Purchase_Value":
            avg_purchase_value,

        "Satisfaction_Score":
            satisfaction_score,

        "Website_Visits_Last_Month":
            website_visits,

        "Avg_Time_Per_Visit_Minutes":
            avg_time_per_visit,

        "Support_Tickets_Last_6_Months":
            support_tickets,

        "Referred_Friends":
            referred_friends,

        "Days_Since_Last_Purchase":
            days_since_last_purchase,

        "Estimated_Customer_Value":
        estimated_customer_value,

        "Engagement_Score":
            engagement_score,

        "Support_Rate":
            support_rate
        }])

        churn_probability = (
        model.predict_proba(
        customer_df
        )[0][1])

        if churn_probability >= 0.70:

         risk_level = "High"

        elif churn_probability >= 0.40:

         risk_level = "Medium"

        else:

         risk_level = "Low"

        if estimated_customer_value >= 7500:
         customer_value = "High"
        
        elif estimated_customer_value >= 3000:
         customer_value = "Medium"

        else:
         customer_value = "Low"

        retention_priority = (churn_probability * estimated_customer_value)

        col1, col2, col3, col4 = (
         st.columns(4))


        col1.metric(
         "Churn Probability",
        f"{churn_probability:.1%}")


        col2.metric(
         "Risk Level",
         risk_level)


        col3.metric(
         "Customer Value",
         customer_value)

 
        col4.metric(
        "Retention Priority",
         f"{retention_priority:,.0f}")



        shap_explanation = (
            get_customer_explanation(
            model,
            customer_df,
            top_n=5
            )
        )


        def clean_feature_name(feature_name):

    # Remove prefixes added by ColumnTransformer
         feature_name = feature_name.replace("num__", "")
         feature_name = feature_name.replace("cat__", "")

         feature_mapping={

        "Age":
            "Age",

        "Gender": "Gender",

        "Annual_Income_USD":
            "Annual Income",

        "Membership_Status":
            "Membership",

        "Spending_Score":
            "Spending Score",

        "Total_Purchases":
            "Total Purchases",

        "Avg_Purchase_Value":
            "Average Purchase Value",

        "Satisfaction_Score":
            "Satisfaction Score",

        "Website_Visits_Last_Month":
            "Website Visits Last Month",

        "Avg_Time_Per_Visit_Minutes":
            "Average Time Per Visit",

        "Support_Tickets_Last_6_Months":
            "Support Tickets",

        "Referred_Friends":
            "Referred Friends",

        "Days_Since_Last_Purchase":
            "Days Since Last Purchase",

        "Estimated_Customer_Value":
            "Estimated Customer Value",

        "Engagement_Score":
            "Engagement Score",

        "Support_Rate":
            "Support Rate",}


         if feature_name in feature_mapping:
            return feature_mapping[feature_name]

        


   
         if feature_name.startswith(
        "Gender_"):

          value = feature_name.replace(
            "Gender_",
            ""
        )

          return f"Gender: {value}"


         if feature_name.startswith(
        "Membership_Status_"):

          value = feature_name.replace(
            "Membership_Status_",
            ""
        )

         return f"Membership: {value}"


         if feature_name.startswith(
        "Preferred_Payment_Method_"):

          value = feature_name.replace(
            "Preferred_Payment_Method_",
            ""
        )

          return f"Payment Method: {value}"


         if feature_name.startswith(
        "Region_"):

          value = feature_name.replace(
            "Region_",
            ""
        )

          return f"Region: {value}"


         return feature_name.replace(
        "_",
        " ")

        shap_explanation["Feature"] = (
        shap_explanation["Feature"]
        .apply(clean_feature_name))

        shap_explanation["Impact"] = (
        shap_explanation["SHAP_Value"].apply(
        lambda x:
        "Increases Churn Risk"
        if x > 0
        else "Reduces Churn Risk"
        ))


        st.subheader(
          "Why is this customer at risk?"
        )
        st.dataframe(
              shap_explanation[
                  [
                    "Feature",
                    "SHAP_Value",
                    "Impact"
                  ]
              ],
              use_container_width=True
        )

        st.subheader(
        "AI Retention Recommendation"
        )

        try:


            retention_strategy = (
                generate_retention_strategy(
                  churn_probability=churn_probability,
                  risk_level=risk_level,
                  customer_value=customer_value,
                  shap_df=shap_explanation
                )
            )

            st.markdown(retention_strategy)

        except Exception as e:
          st.error(
            f"Groq Error: {e}"
        )

>>>>>>> 31405d7 (Fix Streamlit import path)
