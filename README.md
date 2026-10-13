# TXRH Decision Tree App

## Files required
- `app.py`
- `requirements.txt`
- `txrh_decision_tree.pkl` (download this model from your Kaggle notebook)

Put all three files in the repository's root folder. The model file is not included in this starter ZIP; add your own saved model.

## Deploy on GitHub + Streamlit Community Cloud
1. Create a GitHub repository.
2. Upload `app.py`, `requirements.txt`, and `txrh_decision_tree.pkl`.
3. Visit https://share.streamlit.io/ and sign in with GitHub.
4. Select **Create app**, select your repository, branch, and `app.py`.
5. Deploy.

## Important model compatibility note
The app assumes your model was trained with these feature columns in this exact order:
`open`, `high`, `low`, `close`, `adjclose`, `volume`.

If your training code used other names or a different order, update `FEATURES` and the input DataFrame in `app.py` to match. Only load pickle files that you created or trust.

The app makes a directional prediction from manually entered values. It does not fetch live stock prices and is for educational use, not financial advice.
