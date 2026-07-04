# ============================================================
# Medical Insurance Cost Prediction App
# Developed by: Debdut Nandy
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
def load_model():
    return joblib.load("insurance_model.pkl")

model = load_model()

# ============================================================
# Custom CSS
# ============================================================

st.markdown("""
<style>

.main{
    background:#f8f9fa;
}

h1{
    color:#0f172a;
    text-align:center;
}

.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 0px 12px rgba(0,0,0,0.08);
}

.prediction{
    padding:25px;
    border-radius:15px;
    background:#e8f5e9;
    border-left:8px solid green;
    font-size:22px;
    font-weight:bold;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:50px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# Title
# ============================================================

st.title("🏥 Medical Insurance Cost Prediction")

st.markdown(
"""
Predict an individual's **estimated medical insurance charges**
using a trained **Random Forest Regression** model.
"""
)

st.divider()

# ============================================================
# Sidebar
# ============================================================

st.sidebar.title("About")

st.sidebar.info(
"""
Medical Insurance Cost Prediction

Machine Learning Model:
Random Forest Regressor

Enter customer information and click
Predict Insurance Cost.
"""
)

st.sidebar.success("Model Loaded Successfully")

# ============================================================
# Input Form
# ============================================================

left, right = st.columns(2)

with left:

    age = st.slider(
        "Age",
        min_value=18,
        max_value=64,
        value=30
    )

    sex = st.selectbox(
        "Gender",
        ["male", "female"]
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
        "Number of Children",
        [0,1,2,3,4,5]
    )

    smoker = st.selectbox(
        "Smoker",
        ["yes","no"]
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

    input_data = pd.DataFrame({
        "age": [age],
        "sex": [sex],
        "bmi": [bmi],
        "children": [children],
        "smoker": [smoker],
        "region": [region]
    })

    prediction = model.predict(input_data)[0]

    st.success("Prediction Completed Successfully!")

    st.markdown("## Estimated Medical Insurance Cost:")

    st.markdown(
        f"""
        <div class="prediction">
        Estimated Annual Insurance Charge<br><br>

        <span style="font-size:40px;">
        ${prediction:,.2f}
        </span>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown("### Customer Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Age", age)
        st.metric("Gender", sex.title())

    with col2:
        st.metric("BMI", round(bmi, 2))
        st.metric("Children", children)

    with col3:
        st.metric("Smoker", smoker.title())
        st.metric("Region", region.title())

    st.divider()

    st.markdown("### Interpretation")

    if smoker == "yes":
        st.warning(
            "Smoking significantly increases predicted insurance costs."
        )

    elif bmi >= 30:
        st.warning(
            "Higher BMI is associated with increased insurance costs."
        )

    else:
        st.info(
            "Based on the provided information, the predicted insurance charge is shown above."
        )

# ============================================================
# Footer
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div class='footer'>
        Developed by <b>Debdut Nandy</b><br>
        Medical Insurance Cost Prediction using Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)
