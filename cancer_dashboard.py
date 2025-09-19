import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Load the CSV file
# -------------------------------
df = pd.read_csv("cancer data for MOOC 1.csv")

# Clean column names
df.columns = df.columns.str.strip().str.replace(" ", "_")

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.title("Filters")
gender_map = {0: "Female", 1: "Male"}
df['Gender_Label'] = df['gender'].map(gender_map)

selected_gender = st.sidebar.selectbox(
    "Select Gender", ["All"] + list(gender_map.values()))
age_min, age_max = int(df['age'].min()), int(df['age'].max())
selected_age = st.sidebar.slider(
    "Select Age Range", age_min, age_max, (age_min, age_max))

filtered_df = df.copy()
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df['Gender_Label'] == selected_gender]
filtered_df = filtered_df[(filtered_df['age'] >= selected_age[0]) & (
    filtered_df['age'] <= selected_age[1])]

# -------------------------------
# Dashboard Title
# -------------------------------
st.title("🧬 Cancer Risk Dashboard")
st.markdown("Exploring lifestyle and demographic factors from MOOC dataset")

# -------------------------------
# Summary Metrics
# -------------------------------
total_patients = len(filtered_df)
cancer_cases = filtered_df['cancer'].sum()
prevalence = (cancer_cases / total_patients) * 100 if total_patients > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Patients", f"{total_patients}")
col2.metric("Cancer Cases", f"{cancer_cases}")
col3.metric("Prevalence (%)", f"{prevalence:.1f}")

# -------------------------------
# Cancer Prevalence by Gender
# -------------------------------
st.subheader("📊 Cancer Prevalence by Gender")
gender_cancer = filtered_df.groupby(
    'Gender_Label')['cancer'].mean().reset_index()
gender_cancer['Prevalence (%)'] = gender_cancer['cancer'] * 100
fig1 = px.bar(gender_cancer, x='Gender_Label',
              y='Prevalence (%)', color='Gender_Label')
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# BMI Distribution
# -------------------------------
st.subheader("⚖️ BMI Distribution")
fig2 = px.histogram(filtered_df, x='bmi', nbins=20, color='Gender_Label')
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# Lifestyle Factors
# -------------------------------
st.subheader("🚬 Smoking Frequency")
fig3 = px.histogram(filtered_df, x='smoking',
                    color='Gender_Label', barmode='group')
st.plotly_chart(fig3, use_container_width=True)

st.subheader("🏃 Exercise Level")
fig4 = px.histogram(filtered_df, x='exercise',
                    color='Gender_Label', barmode='group')
st.plotly_chart(fig4, use_container_width=True)

st.subheader("🍎 Fruit & Vegetable Intake")
fig5 = px.box(filtered_df, x='Gender_Label', y='fruit',
              points='all', title="Fruit Servings")
fig6 = px.box(filtered_df, x='Gender_Label', y='veg',
              points='all', title="Vegetable Servings")
st.plotly_chart(fig5, use_container_width=True)
st.plotly_chart(fig6, use_container_width=True)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption(
    "Dashboard built by Irene • Powered by Streamlit • Data: cancer data for MOOC 1.csv")
