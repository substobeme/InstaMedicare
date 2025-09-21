import streamlit as st
import requests
import sqlite3

st.set_page_config(page_title="InstaMediHelp", layout="wide")

# -------------------- Sidebar Login --------------------
st.sidebar.title("InstaMediHelp")
mode = st.sidebar.selectbox("Mode", ["Customer Mode", "Admin Mode"])
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login_button = st.sidebar.button("Login")

creds = {"customer": "123", "admin": "234"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.mode = None

if login_button:
    if (mode == "Customer Mode" and password == creds["customer"]) or \
       (mode == "Admin Mode" and password == creds["admin"]):
        st.session_state.logged_in = True
        st.session_state.mode = mode
    else:
        st.sidebar.error("Invalid username or password")

# -------------------- After Login --------------------
if st.session_state.logged_in:
    st.success(f"Logged in as **{st.session_state.mode}**")
    mode = st.session_state.mode

    # -------------------- Customer Mode --------------------
    if mode == "Customer Mode":
        st.header("Patient Information")
        with st.form(key="recommendation_form"):
            col1, col2 = st.columns(2)
            with col1:
                rec_id = st.text_input("Receipt ID")
                name = st.text_input("Name")
                age = st.number_input("Age", min_value=0, max_value=120, step=1)
            with col2:
                top_k = st.number_input("Number of drug recommendations", min_value=1, max_value=5, value=3, step=1)
            
            review_input = st.text_area("Describe your symptoms or condition")
            submit_btn = st.form_submit_button("Get Recommendations")
        
        if submit_btn:
            if not all([rec_id.strip(), name.strip(), review_input.strip()]):
                st.warning("Please fill in all required fields.")
            else:
                payload = {
                    "rec_id": rec_id,
                    "name": name,
                    "age": age,
                    "review": review_input,
                    "top_k": top_k
                }
                try:
                    response = requests.post("http://localhost:8000/recommend/", json=payload)
                    data = response.json()
                    st.markdown("### Recommended Drugs")
                    for drug, _ in data["predictions"]:
                        st.success(f"{drug}")
                except Exception as e:
                    st.error(f"Error contacting backend: {e}")

    # -------------------- Admin Mode --------------------
    elif mode == "Admin Mode":
        st.header("All Recommendations Log")
        conn = sqlite3.connect("logs.db")
        c = conn.cursor()
        c.execute("""
            SELECT rec_id, name, age, problem, recommended_drugs, timestamp 
            FROM recommendations ORDER BY timestamp DESC
        """)
        rows = c.fetchall()
        conn.close()
        
        if rows:
            for row in rows:
                st.markdown(f"#### Receipt ID: {row[0]}")
                st.markdown(f"**Name:** {row[1]}  |  **Age:** {row[2]}")
                st.markdown(f"**Problem:** {row[3]}")
                st.markdown(f"**Recommended Drugs:** {row[4]}")
                st.markdown(f"**Timestamp:** {row[5]}")
                st.markdown("---")
        else:
            st.info("No recommendations logged yet.")

