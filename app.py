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
def assign_tasks_equally(tasks, seed):
    random.seed(seed)
    random.shuffle(tasks)  # Shuffle the tasks to ensure randomness
    mid_index = len(tasks) // 2
    tom_tasks = tasks[:mid_index]
    nuf_tasks = tasks[mid_index:]
    return tom_tasks, nuf_tasks

# Generate a seed based on the current date
seed = today.strftime('%Y%m%d')

# Assign tasks based on frequency
tom_tasks = []
nuf_tasks = []

if weekday == 'Sunday':
    tom_weekly, nuf_weekly = assign_tasks_equally(tasks['weekly'], seed)
    tom_tasks.extend(tom_weekly)
    nuf_tasks.extend(nuf_weekly)
if day == 1:
    tom_monthly, nuf_monthly = assign_tasks_equally(tasks['monthly'], seed)
    tom_tasks.extend(tom_monthly)
    nuf_tasks.extend(nuf_monthly)
if day == 1 or day == 15:
    tom_bi_monthly, nuf_bi_monthly = assign_tasks_equally(tasks['bi_monthly'], seed)
    tom_tasks.extend(tom_bi_monthly)
    nuf_tasks.extend(nuf_bi_monthly)

# If no tasks are assigned, default to weekly and monthly tasks
if not tom_tasks and not nuf_tasks:
    tom_weekly, nuf_weekly = assign_tasks_equally(tasks['weekly'], seed)
    tom_monthly, nuf_monthly = assign_tasks_equally(tasks['monthly'], seed)
    tom_bi_monthly, nuf_bi_monthly = assign_tasks_equally(tasks['bi_monthly'], seed)
    tom_tasks.extend(tom_weekly)
    tom_tasks.extend(tom_monthly)
    tom_tasks.extend(tom_bi_monthly)
    nuf_tasks.extend(nuf_weekly)
    nuf_tasks.extend(nuf_monthly)
    nuf_tasks.extend(nuf_bi_monthly)

# Streamlit Layout
st.title("Les tâches de mimi et mimo")

col1, col2 = st.columns(2)

with col1:
    st.header("Tâches de mimo")
    if tom_tasks:
        for task in tom_tasks:
            st.write(task)

with col2:
    st.header("Tâches de mimi")
    if nuf_tasks:
        for task in nuf_tasks:
            st.write(task)
