import os
import streamlit as st

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def get_groq_client():

    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = os.getenv("GROQ_API_KEY")

    return Groq(
        api_key=api_key
    )


def generate_retention_strategy( 
    churn_probability, 
    risk_level, 
    customer_value, 
    shap_df 
): 

    churn_probability = float(churn_probability)

    client = get_groq_client()

   

    try:
        model_name = st.secrets["GROQ_MODEL"]
    except Exception:
        model_name = os.getenv("GROQ_MODEL")

        
    driver_lines = []

    for _, row in shap_df.iterrows():

        direction = (
            "increases churn risk"
            if row["SHAP_Value"] > 0
            else "reduces churn risk"
        )

        driver_lines.append(
            f"- {row['Feature']}: "
            f"{direction}"
        )

    driver_text = "\n".join(
        driver_lines
    )

    prompt = f"""
You are an e-commerce customer
retention analyst.

A machine learning model has already
generated the following prediction.

Churn Probability:
{churn_probability:.1%}

Risk Level:
{risk_level}

Estimated Customer Value:
{customer_value}

SHAP explanation of the ML prediction:

{driver_text}

Your job is NOT to predict churn again.

Based only on the information above:

1. Explain the major churn reasons
   in simple business language.

2. Recommend exactly 3 practical
   retention actions.

3. Give a retention priority:
   Low, Medium, or High.
   
For the retention actions, ALWAYS return a complete Markdown table.

The table MUST contain exactly these 3 columns:
| Action | Recommended Strategy | Business Rationale |

Provide exactly 3 retention actions.

IMPORTANT:
- Every row MUST contain content in all 3 columns.
- Never leave any table cell empty.
- Keep each cell concise.
- Ensure every Markdown row has exactly 3 columns.
- Do not create additional columns.

Keep the response concise.

Do not invent customer information.
"""

    response = (
        client.chat.completions.create(
            model=model_name,

            messages=[
                {
                    "role": "system",
                    "content":
                    "You are an expert "
                    "customer retention analyst."
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3
        )
    )

    return (response.choices[0].message.content)