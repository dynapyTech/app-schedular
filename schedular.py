import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up service account credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('dynapy_schedular.json', scope)

# Create a client instance
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open('Appointment_Schedular').worksheet('Schedule')

st.logo('assets\dynapy_logo.jpg')

st.title("Application Form")
# Create a Streamlit form
with st.form("contest_entry_form"):

    st.error("Note: *All fields are compulsary")

    col1, col2 = st.columns(2)

    with col1:
        first_name = st.text_input("First Name*")
        phone_number = st.text_input("Phone Number*")
        gender = st.text_input("Gender*")
        problem = st.text_input("Problem*")
        appointment_date = st.date_input("Appointment Date*")

    with col2:
        last_name = st.text_input("Last Name*")
        email_id = st.text_input("Email ID*")
        age = st.text_input("Age*")
        pain_index = st.slider("Rate your pain", 1,5)
        appointment_time = st.time_input("Appointment Time*")
        
    colsulted_doctor = st.text_input("Ever Consulted a Doctor Before?*")
    submit_button = st.form_submit_button("Submit your entry!")


    if submit_button:
        if not first_name or not last_name or not phone_number or not email_id or not gender or not age or not problem or not pain_index or not appointment_date or not appointment_time or not colsulted_doctor:
            st.error('Please fill out all required fields.')

        else:
            row = [first_name, last_name, phone_number,	email_id, gender, age, problem,	pain_index,	appointment_date, appointment_time,	colsulted_doctor]
            sheet.append_row(row)

            st.success("Thank you! Form has been submitted, we will contact you soon")
