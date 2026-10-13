import pickle
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="TXRH Decision Tree", page_icon="📈")
st.title("TXRH Stock Direction Predictor")
st.write(
    "Enter one trading day's stock data to predict whether the next recorded "
    "closing price will increase. This is an educational model, not financial advice."
)

MODEL_PATH = Path(__file__).parent / "txrh_decision_tree.pkl"

@st.cache_resource
def load_model():
    with MODEL_PATH.open("rb") as f:
        return pickle.load(f)

if not MODEL_PATH.exists():
    st.error(
        "Model file not found. Upload txrh_decision_tree.pkl to the same "
        "GitHub repository folder as app.py."
    )
    st.stop()

model = load_model()

# These feature names/order must match the features used during training.
# If your model was trained with different columns, update this list.
FEATURES = ["open", "high", "low", "close", "adjclose", "volume"]

st.caption("Enter values using the same units and format as the training dataset.")

with st.form("stock_inputs"):
    c1, c2 = st.columns(2)
    with c1:
        open_price = st.number_input("Open", min_value=0.0, value=50.0, format="%.4f")
        high_price = st.number_input("High", min_value=0.0, value=51.0, format="%.4f")
        low_price = st.number_input("Low", min_value=0.0, value=49.0, format="%.4f")
    with c2:
        close_price = st.number_input("Close", min_value=0.0, value=50.5, format="%.4f")
        adjclose = st.number_input("Adjusted close", min_value=0.0, value=50.5, format="%.4f")
        volume = st.number_input("Volume", min_value=0, value=1000000, step=1000)
    submitted = st.form_submit_button("Predict")

if submitted:
    if high_price < low_price:
        st.error("High must be greater than or equal to Low.")
    else:
        row = pd.DataFrame([{
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "adjclose": adjclose,
            "volume": volume,
        }], columns=FEATURES)
        try:
            prediction = int(model.predict(row)[0])
            st.subheader("Predicted direction: " + ("Increase" if prediction == 1 else "No Increase"))
            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(row)[0]
                class_probabilities = dict(zip(model.classes_, probabilities))
                st.write(
                    "Model-estimated probability of increase: "
                    f"{class_probabilities.get(1, 0) * 100:.1f}%"
                )
        except Exception as exc:
            st.error(
                "Prediction failed. Confirm that FEATURES and the input column "
                f"names match your training data. Details: {exc}"
            )
        st.warning("Historical test accuracy does not guarantee future performance.")
