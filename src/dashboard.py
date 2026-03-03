import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# Ensure repo root is on sys.path so `import src.*` works no matter
# where Streamlit is launched from.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.agent import WaterIntakeAgent
from src.database import get_intake_history, log_intake

if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False

#welcome section
if not st.session_state.tracker_started:
    st.title("Welcome to the AI Water Intake Tracker")
    st.markdown("""
    Track your daily water intake and get personalized hydration recommendations.
    log in your intake, get smart feedback and stay hydrated.""")

    if st.button("Start Tracking"):
        st.session_state.tracker_started = True
        st.experimental_rerun()

else:
    st.title("Water Intake Tracker Dashboard")
    user_id = st.text_input("Enter your user ID", value="user_123")
    intake_ml = st.number_input("Enter your water intake in ml", value=0, min_value=0, step=100)

    if st.sidebar.button("Submit"):
        if user_id and intake_ml:
            log_intake(user_id, intake_ml)
            st.success(f"Water intake of {intake_ml} ml logged successfully for user {user_id}.")

            agent = WaterIntakeAgent()
            feedback = agent.analyze_intake(intake_ml)
            st.info(f"Hydration Analysis: {feedback}")

    st.markdown("---")

    st.header("Water Intake History")

    if user_id:
        history = get_intake_history(user_id)
        if history:
            dates= [datetime.strptime(d[1], '%Y-%m-%d').strftime('%Y-%m-%d') for d in history]
            intakes= [d[0] for d in history]

            df = pd.DataFrame({"Date": dates, "Intake (ml)": intakes})
            st.dataframe(df)
            st.line_chart(df.set_index("Date")["Intake (ml)"])
        else:
            st.warning("No water intake data found. Please log your intake first")