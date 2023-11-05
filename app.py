import streamlit as st
import pandas as pd
import joblib
import base64
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from test_preprocessing import preprocess_data


# Load the pre-trained model
loaded_model = joblib.load('trained_model.pkl')

# Function to download CSV file
def download_csv(dataframe):
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="output.csv">Download CSV File</a>'
    return href

# Streamlit app
def main():

    st.markdown(
        """
        <h1 style='text-align: center;'>FaultForecast</h1>
        """,
        unsafe_allow_html=True
    )

    # File upload
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file is not None:
        # Read the uploaded file
        data = pd.read_csv(uploaded_file)

        # Preprocess the data
        preprocessed_data = preprocess_data(data)

        # Predict using the loaded model
        y_pred = loaded_model.predict(preprocessed_data)

        # Create the output dataframe
        output = pd.DataFrame({'Customer': data['Customer'], 'y_pred': y_pred})

        # Display the output dataframe
        st.write("Prediction Results:")
        st.dataframe(output)

        # Download button
        st.markdown(download_csv(output), unsafe_allow_html=True)

if __name__ == '__main__':
    main()
