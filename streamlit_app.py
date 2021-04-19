# importing the libraries  
import streamlit as st
import json
from main import check_user_input,check_csv_file
import pandas as pd
import base64

def get_table_download_link(file):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    # # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href
#===========================================#
#              Streamlit Code               #
#===========================================#
desc = "This app checks if the user rating is aligned with the review."

st.title('Wrong Rating Prediction')
st.write(desc)

rating = st.number_input('Please enter the rating.',min_value=1,max_value=5,step=1)
text_input = st.text_input('Review')


if st.button('Check rating'):
    input_text,input_rating,wrong_review = check_user_input(text_input,rating)
    st.write('Review: ')
    st.write(input_text)
    st.write('Rating: ')
    st.write(input_rating)
    st.write('Mismatch between rating and review')
    st.write(wrong_review)


uploaded_file = st.file_uploader("Upload your csv file here",type="csv")
if uploaded_file is not None:
    st.text('File uploaded')
    check_csv_file(uploaded_file)
    st.text('File Saved')
    df = pd.read_csv('output.csv')

    st.markdown(get_table_download_link(df), unsafe_allow_html=True)



#streamlit run streamlit_app.py