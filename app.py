import streamlit as st
import pandas as pd
import openpyxl
import random
import json
from datetime import datetime

# Load tasks from the provided Excel file
file_path = 'taches.xlsx'
tasks_df = pd.read_excel(file_path)

# Prepare task lists
tasks = {
    'weekly': tasks_df['Dimanche'][2:].dropna().tolist(),
    'monthly': tasks_df['1ier'][2:].dropna().tolist(),
    'bi_monthly': tasks_df['1er et 15'][2:].dropna().tolist()
}

# Save tasks to JSON for easy updates and management
with open('tasks.json', 'w') as f:
    json.dump(tasks, f)

# Load tasks from JSON
with open('tasks.json', 'r') as f:
    tasks = json.load(f)

# Get current date
today = datetime.today()
day = today.day
weekday = today.strftime('%A')

# Function to assign tasks equally to Tom and Nuf
def assign_tasks_equally(tasks):
    random.shuffle(tasks)  # Shuffle the tasks to ensure randomness
    mid_index = len(tasks) // 2
    tom_tasks = tasks[:mid_index]
    nuf_tasks = tasks[mid_index:]
    return tom_tasks, nuf_tasks

# Assign tasks based on frequency
tom_weekly, nuf_weekly = assign_tasks_equally(tasks['weekly']) if weekday == 'Sunday' else ([], [])
tom_monthly, nuf_monthly = assign_tasks_equally(tasks['monthly']) if day == 1 else ([], [])
tom_bi_monthly, nuf_bi_monthly = assign_tasks_equally(tasks['bi_monthly']) if day == 1 or day == 15 else ([], [])

# If no tasks are assigned, default to weekly and monthly tasks
if not (tom_weekly or nuf_weekly or tom_monthly or nuf_monthly or tom_bi_monthly or nuf_bi_monthly):
    tom_weekly, nuf_weekly = assign_tasks_equally(tasks['weekly'])
    tom_monthly, nuf_monthly = assign_tasks_equally(tasks['monthly'])
    tom_bi_monthly, nuf_bi_monthly = assign_tasks_equally(tasks['bi_monthly'])


# Streamlit Layout
st.title("Les tâches de mimi et mimo")

col1, col2 = st.columns(2)

with col1:
    st.header("Tâches de mimo")
    if tom_weekly:
        st.subheader("Hebdomadaire")
        for task in tom_weekly:
            st.write(task)
    if tom_monthly:
        st.subheader("mensuel")
        for task in tom_monthly:
            st.write(task)
    if tom_bi_monthly:
        st.subheader("le 1ier et 15ieme")
        for task in tom_bi_monthly:
            st.write(task)

with col2:
    st.header("Tâches de mimi")
    if nuf_weekly:
        st.subheader("Hebdomadaire")
        for task in nuf_weekly:
            st.write(task)
    if nuf_monthly:
        st.subheader("mensuel")
        for task in nuf_monthly:
            st.write(task)
    if nuf_bi_monthly:
        st.subheader("le 1ier et 15ieme")
        for task in nuf_bi_monthly:
            st.write(task)