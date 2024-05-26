import streamlit as st
import pandas as pd
import openpyxl
import random
import json
from datetime import datetime, timedelta
import os

# Load tasks from the provided Excel file
file_path = 'taches.xlsx'
tasks_df = pd.read_excel(file_path)

# Debug: Display column names to check correctness


# Prepare task lists based on column names
tasks = {
    'weekly': tasks_df['Dimanche'][2:].dropna().tolist(),
    'monthly': tasks_df['1ier'][2:].dropna().tolist(),
    'bi_monthly': tasks_df['1er et 15'][2:].dropna().tolist()
}

# Function to assign tasks equally to Tom and Nuf
def assign_tasks_equally(tasks):
    random.shuffle(tasks)  # Shuffle the tasks to ensure randomness
    mid_index = len(tasks) // 2
    tom_tasks = tasks[:mid_index]
    nuf_tasks = tasks[mid_index:]
    return tom_tasks, nuf_tasks

# Generate tasks for the entire year
def generate_yearly_tasks(tasks):
    yearly_tasks = {}
    start_date = datetime(datetime.today().year, 1, 1)
    end_date = datetime(datetime.today().year, 12, 31)
    current_date = start_date

    while current_date <= end_date:
        week_key = current_date.strftime('%Y-%U')
        month_key = current_date.strftime('%Y-%m')
        bi_monthly_key = current_date.strftime('%Y-%m-%d')

        if current_date.weekday() == 6:  # Sunday
            tom_weekly, nuf_weekly = assign_tasks_equally(tasks['weekly'])
            yearly_tasks.setdefault(week_key, {}).update({'tom_weekly': tom_weekly, 'nuf_weekly': nuf_weekly})

        if current_date.day == 1:
            tom_monthly, nuf_monthly = assign_tasks_equally(tasks['monthly'])
            yearly_tasks.setdefault(month_key, {}).update({'tom_monthly': tom_monthly, 'nuf_monthly': nuf_monthly})

        if current_date.day == 1 or current_date.day == 15:
            tom_bi_monthly, nuf_bi_monthly = assign_tasks_equally(tasks['bi_monthly'])
            yearly_tasks.setdefault(bi_monthly_key, {}).update({'tom_bi_monthly': tom_bi_monthly, 'nuf_bi_monthly': nuf_bi_monthly})

        current_date += timedelta(days=1)

    return yearly_tasks

# Check if yearly tasks JSON exists, if not, generate and save it
json_file_path = 'yearly_tasks.json'
if not os.path.exists(json_file_path):
    yearly_tasks = generate_yearly_tasks(tasks)
    with open(json_file_path, 'w') as f:
        json.dump(yearly_tasks, f, indent=4)
else:
    with open(json_file_path, 'r') as f:
        yearly_tasks = json.load(f)

# Load tasks from JSON based on current date
today = datetime.today()
week_key = today.strftime('%Y-%U')
month_key = today.strftime('%Y-%m')
bi_monthly_key = today.strftime('%Y-%m-%d')



tom_tasks = []
nuf_tasks = []

if week_key in yearly_tasks and 'tom_weekly' in yearly_tasks[week_key]:
    tom_tasks.extend([('Hebdomadaires', task) for task in yearly_tasks[week_key]['tom_weekly']])
if week_key in yearly_tasks and 'nuf_weekly' in yearly_tasks[week_key]:
    nuf_tasks.extend([('Hebdomadaires', task) for task in yearly_tasks[week_key]['nuf_weekly']])

if month_key in yearly_tasks and 'tom_monthly' in yearly_tasks[month_key]:
    tom_tasks.extend([('Mensuelles', task) for task in yearly_tasks[month_key]['tom_monthly']])
if month_key in yearly_tasks and 'nuf_monthly' in yearly_tasks[month_key]:
    nuf_tasks.extend([('Mensuelles', task) for task in yearly_tasks[month_key]['nuf_monthly']])

if bi_monthly_key in yearly_tasks and 'tom_bi_monthly' in yearly_tasks[bi_monthly_key]:
    tom_tasks.extend([('Bimensuelles', task) for task in yearly_tasks[bi_monthly_key]['tom_bi_monthly']])
if bi_monthly_key in yearly_tasks and 'nuf_bi_monthly' in yearly_tasks[bi_monthly_key]:
    nuf_tasks.extend([('Bimensuelles', task) for task in yearly_tasks[bi_monthly_key]['nuf_bi_monthly']])


# Streamlit Layout
st.title("Les tâches de mimi et mimo")

col1, col2 = st.columns(2)

def display_tasks(tasks, header):
    current_category = None
    for category, task in tasks:
        if category != current_category:
            st.subheader(category)
            current_category = category
        st.write(task)

with col1:
    st.header("Tâches de mimo")
    if tom_tasks:
        display_tasks(tom_tasks, "Tâches de mimo")

with col2:
    st.header("Tâches de mimi")
    if nuf_tasks:
        display_tasks(nuf_tasks, "Tâches de mimi")
