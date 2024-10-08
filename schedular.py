import streamlit as st
import gspread
import re
from oauth2client.service_account import ServiceAccountCredentials
st.set_page_config(
    page_title="Dynapy",
    page_icon=":large_purple_circle:"
)
google_secrets = st.secrets.get("secrets", {})
# Set up service account credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict({
    "type": google_secrets["type"],
    "project_id": google_secrets["project_id"],
    "private_key_id": google_secrets["private_key_id"],
    "private_key": google_secrets["private_key"].replace('\\n', '\n'),
    "client_email": google_secrets["client_email"],
    "client_id": google_secrets["client_id"],
    "auth_uri": google_secrets["auth_uri"],
    "token_uri": google_secrets["token_uri"],
    "auth_provider_x509_cert_url": google_secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": google_secrets["client_x509_cert_url"]
}, scope)

# Create a client instance
client = gspread.authorize(credentials)

# Open the Google Sheet
sheet = client.open('Appointment_Schedular').worksheet('Schedule')

# st.image('assets/dynapy_logo.jpg')

st.header("Appointment Form")
# Create a Streamlit form
with st.form("contest_entry_form"):

    st.error("Note: *All fields are compulsary")

    col1, col2 = st.columns(2)

    with col1:
        first_name = st.text_input("First Name*", placeholder="First Name")
        phone_number = st.text_input("Phone Number*", max_chars=10, placeholder="Enter your phone number")
        gender = st.selectbox("Gender*", options=["Male", "Female"], placeholder="Choose an option", index=None)
        problem = st.selectbox("Symptoms or Issues*", options=["Pain", "Fracture"],placeholder="Problem you face", index=None)
        appointment_date = str(st.date_input("Appointment Date*", value="today", format="DD-MM-YYYY"))

    with col2:
        last_name = st.text_input("Last Name*")
        email_id = st.text_input("Email ID*")
        age = st.text_input("Age*")
        pain_index = st.slider("Rate your pain*", 1,5)
        appointment_time = str(st.time_input("Appointment Time*", value="now"))

    colsulted_doctor = st.selectbox("Ever Consulted a Doctor Before?*", options=["Yes", "No"])

    col11, col12, col13 = st.columns(3)

    with col12:
        submit_button = st.form_submit_button("Submit", use_container_width=True)

    # Function to validate email format
    def is_valid_email(email):
        # Simple email validation regex
        pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        return pattern.match(email)
    
    # Function to validate Phone Number
    def is_valid_phone_number(phone_number):
        # Example validation: US phone number format (xxx-xxx-xxxx)
        pattern = re.compile(r'^\d{10}$')
        return pattern.match(phone_number)

    if submit_button:
        if not first_name or not last_name or not phone_number or not email_id or not gender or not age or not problem or not pain_index or not appointment_date or not appointment_time or not colsulted_doctor:
            st.error('Please fill out all required fields.')

        else:
            if is_valid_email(email_id):
                if is_valid_phone_number(phone_number):
                    row = [first_name, last_name, phone_number,	email_id, gender, age, problem,	pain_index,	appointment_date, appointment_time,	colsulted_doctor]
                    sheet.append_row(row)
                    st.success("Thank you! Form has been submitted, we will contact you soon")
                else:
                    st.error("Invalid phone number format. Please use the format xxx-xxx-xxxx.")
            else:
                st.error("Invalid email address. Please enter a valid email address.")
