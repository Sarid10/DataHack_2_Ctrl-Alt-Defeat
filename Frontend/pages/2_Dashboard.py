import streamlit as st, pandas as pd, numpy as np
import random
st.title("Dashboard")

df = pd.read_csv('lawyers_final2.csv')
st.header("Experience per 100 Lawyers")
exp = [df['experience'][random.randint(1, len(df['experience']))] for i in range(100)]
st.bar_chart(exp)

st.text(f"Average Experience = {sum(exp)/len(exp)}")


st.header("Lawyers across India")
st.text('Chennai, Kolkata, Bangalore, Hyderabad, Mumbai, Delhi')

x = ['Chennai', 'Kolkata', 'Bangalore', 'Hyderabad', 'Mumbai', 'Delhi']
y = [366, 353, 336, 330, 327, 291]

st.bar_chart(y)


st.header('Lawyer Majority Locations')
mumbai_data = pd.DataFrame(
    [ [13.0853, 80.278], 
     [22.5726, 88.3639],
    [12.9716, 77.5946],
    [17.3850, 78.4867],
    [19.0170, 72.8571],
    [28.6139, 77.2090]
    ],
    columns=["lat", "lon"],
)

st.map(mumbai_data)
