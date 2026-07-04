# ============================================================
# Medical Insurance Cost Prediction
# Developed by Debdut Nandy
# ============================================================

import streamlit as st
import pandas as pd
import joblib

# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Medical Insurance Cost Prediction",
    page_icon="🏥",
    layout="wide"
)

# ============================================================
# Load Model
# ============================================================

@st.cache_resource
def load_files():

    model = joblib.load("insurance_model (3).pkl")
    columns = joblib.load("model_columns (1).pkl")

    return model, columns

model, model_columns = load_files()

# ============================================================
# Custom CSS
# ============================================================

st.markdown("""
<style>

.main{
    background:#F5F7FA;
}

.title{
    font-size:42px;
    font-weight:bold;
    color:#1E3A8A;
}

.subtitle{
    color:gray;
    font-size:18px;
}

.prediction-box{
    background:#E8F5E9;
    padding:25px;
    border-radius:15px;
    border-left:8px solid green;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:40px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# Header
# ============================================================

st.markdown(
"""
<div class='title'>
🏥 Medical Insurance Cost Prediction
</div>

<div class='subtitle'>
Predict Annual Medical Insurance Charges using Machine Learning
</div>
""",
unsafe_allow_html=True
)

st.divider()

# ============================================================
# Sidebar
# ============================================================

st.sidebar.title("About")

st.sidebar.info(
"""
Medical Insurance Cost Prediction

Model Used:

✅ Random Forest Regressor

Enter the customer details and click Predict.
"""
)

# ============================================================
# Input Fields
# ============================================================

left, right = st.columns(2)

with left:

    age = st.slider(
        "Age",
        18,
        64,
        25
    )

    sex = st.selectbox(
        "Gender",
        [
            "male",
            "female"
        ]
    )

    bmi = st.number_input(
        "BMI",
        min_value=10.0,
        max_value=60.0,
        value=25.0,
        step=0.1
    )

with right:

    children = st.selectbox(
        "Children",
        [0,1,2,3,4,5]
    )

    smoker = st.selectbox(
        "Smoker",
        [
            "yes",
            "no"
        ]
    )

    region = st.selectbox(
        "Region",
        [
            "northeast",
            "northwest",
            "southeast",
            "southwest"
        ]
    )

st.divider()

predict = st.button(
    "Predict Insurance Cost",
    use_container_width=True
)

# ============================================================
# Prediction
# ============================================================

if predict:

    # -----------------------------------------
    # Create Input DataFrame
    # -----------------------------------------

    input_df = pd.DataFrame({

        "age":[age],
        "bmi":[bmi],
        "children":[children],

        "sex_male":[1 if sex=="male" else 0],

        "smoker_yes":[1 if smoker=="yes" else 0],

        "region_northwest":[1 if region=="northwest" else 0],
        "region_southeast":[1 if region=="southeast" else 0],
        "region_southwest":[1 if region=="southwest" else 0]

    })

    # -----------------------------------------
    # Match Training Columns
    # -----------------------------------------

    input_df = input_df.reindex(
        columns=model_columns,
        fill_value=0
    )

    # -----------------------------------------
    # Prediction
    # -----------------------------------------

    prediction = model.predict(input_df)[0]

    # -----------------------------------------
    # Result
    # -----------------------------------------

    st.success("Prediction Completed Successfully!")

    st.markdown("## 💰 Estimated Insurance Cost")

    st.markdown(
        f"""
        <div class="prediction-box">

        <h1 style="color:green;">
        ${prediction:,.2f}
        </h1>

        Estimated Annual Medical Insurance Charges

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # -----------------------------------------
    # Customer Summary
    # -----------------------------------------

    st.subheader("Customer Summary")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Age", age)
        st.metric("Gender", sex.title())

    with c2:
        st.metric("BMI", round(bmi,1))
        st.metric("Children", children)

    with c3:
        st.metric("Smoker", smoker.title())
        st.metric("Region", region.title())

    st.divider()

    # -----------------------------------------
    # Health Insights
    # -----------------------------------------

    st.subheader("Health Insights")

    if smoker == "yes":

        st.error(
            "Smoking is one of the strongest factors contributing to higher medical insurance charges."
        )

    elif bmi >= 30:

        st.warning(
            "Your BMI falls in the obese range, which may increase expected medical costs."
        )

    elif bmi >= 25:

        st.warning(
            "Your BMI is above the normal range. Maintaining a healthy BMI can help reduce long-term health risks."
        )

    else:

        st.success(
            "Your BMI is within the healthy range based on the provided information."
        )

# ============================================================
# Footer
# ============================================================

st.markdown("---")

st.markdown(
"""
<div class="footer">

Developed by <b>Debdut Nandy</b>

<br>

Medical Insurance Cost Prediction using Machine Learning

</div>
""",
unsafe_allow_html=True
)
