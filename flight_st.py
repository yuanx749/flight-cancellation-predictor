import datetime

import altair as alt
import pandas as pd
import streamlit as st

import flight

with st.sidebar.form("Sidebar"):
    prob2 = st.number_input(
        "Probabilty of small break", min_value=0.0, max_value=1.0, value=0.5
    )
    prob4 = st.number_input(
        "Probabilty of big break", min_value=0.0, max_value=1.0, value=0.2
    )
    n_weeks = st.number_input("Weeks", min_value=3, value=15)
    st.session_state.first_date = st.date_input(
        "First day", value=datetime.date(2022, 4, 1)
    )
    if st.form_submit_button(label="Run"):
        st.session_state.probs = flight.predict_prob(
            prob2, prob4, n_weeks, n_simulation=10000
        )

"""
# Flight Cancellation Predictor
Predict :airplane: cancellation probability under circuit breaker policies using Monte Carlo method.

According to the circuit breaker rules (21.4.28) on CAAC, there are mainly two kinds of break:
- Small break: 2 weeks, triggered by 5 to 9 positive cases.
- Big break: 4 weeks, triggered by 10 to 29 positive cases.
Enter your estimated probabilities of positive cases that trigger these breaks. Click `Run` to predict the cancellation for the following weeks.
"""

if "probs" in st.session_state:
    data = pd.DataFrame(
        {
            "Date": pd.date_range(
                start=st.session_state.first_date,
                periods=len(st.session_state.probs),
                freq="7D",
            ),
            "Probability": st.session_state.probs,
        }
    )
    chart = (
        alt.Chart(data)
        .mark_bar(width=400 / len(data))
        .encode(
            x="Date:T",
            y=alt.Y("Probability", scale=alt.Scale(domain=(0, 1))),
            tooltip=["Date", "Probability"],
        )
        .properties(width=500)
    )
    st.altair_chart(chart)

"""
### Notes
- The probabilities of positive cases can be estimated using history or positive rate.
- Extreme situations and other reasons for cancellation are not taken into account.
- Assume that previous weeks do not affect, e.g., long time of break or no break in the previous weeks.
"""
