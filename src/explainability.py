import pandas as pd
import shap


def get_customer_explanation(
    model,
    customer_df,
    top_n=5
):

    preprocessor = (
        model.named_steps["preprocessor"]
    )

    classifier = (
        model.named_steps["classifier"]
    )

    transformed = (
        preprocessor.transform(customer_df)
    )

    if hasattr(transformed, "toarray"):
        transformed = transformed.toarray()

    feature_names = (
        preprocessor
        .get_feature_names_out()
    )

    transformed_df = pd.DataFrame(
        transformed,
        columns=feature_names
    )

    explainer = shap.TreeExplainer(
        classifier
    )

    shap_output = explainer(
        transformed_df
    )

    values = shap_output.values

    # Binary classifier handling
    if values.ndim == 3:
        customer_values = values[
            0, :, 1
        ]
    else:
        customer_values = values[0]

    result = pd.DataFrame({
        "Feature": feature_names,
        "SHAP_Value":
            customer_values
    })

    result["Importance"] = (
        result["SHAP_Value"]
        .abs()
    )

    result = result.sort_values(
        "Importance",
        ascending=False
    )

    return result.head(top_n)