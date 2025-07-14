import streamlit as st
import pandas as pd
import plotly.express as px
import os
import json

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Product Feedback Dashboard")

# --- Custom CSS for styling ---
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
    }
    .stMetric {
        background-color: #262730;
        border-radius: 10px;
        padding: 15px;
    }
    .st-emotion-cache-1r6slb0 {
        background-color: #262730;
        border-radius: 10px;
        padding: 20px;
    }
    h1, h2, h3 {
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)


# --- App Title ---
st.title("Product Feedback Analysis Dashboard")

# --- Load Data and Summaries ---
csv_file_path = 'final_comprehensive_report.csv'
summaries_file_path = 'dashboard_summaries.json'

# Load AI-generated summaries from the JSON file
summaries = {}
if os.path.exists(summaries_file_path):
    with open(summaries_file_path, 'r') as f:
        summaries = json.load(f)

# Load the main report data from the CSV file
if os.path.exists(csv_file_path):
    df = pd.read_csv(csv_file_path)
    
    # --- Top Row Layout ---
    col1, col2, col3 = st.columns([2, 1, 2])

    # --- Column 1: Text Boxes with AI-Generated Summaries (Read More/Less Style) ---
    with col1:
        # Function to create a "Read More/Less" section for a summary
        def create_summary_expander(title, summary_key):
            st.subheader(title)
            summary_text = summaries.get(summary_key, "AI summary not generated. Please run the main analysis notebook.")
            
            # Initialize session state for each expander
            if f'{summary_key}_expanded' not in st.session_state:
                st.session_state[f'{summary_key}_expanded'] = False

            # Check the state and display content accordingly
            if st.session_state[f'{summary_key}_expanded']:
                # If expanded, show full text and a "Read Less" button
                st.write(summary_text)
                if st.button("Read Less", key=f'less_{summary_key}'):
                    st.session_state[f'{summary_key}_expanded'] = False
                    st.rerun()
            else:
                # If collapsed, show truncated text and a "Read More" button
                st.write(f"{summary_text[:150]}...")
                if st.button("Read More", key=f'more_{summary_key}'):
                    st.session_state[f'{summary_key}_expanded'] = True
                    st.rerun()

        create_summary_expander("Low-Hanging Fruits", "low_hanging_fruits")
        create_summary_expander("Nice-to-Have", "nice_to_have")
        create_summary_expander("No Business Impact", "no_business_impact")

    # --- Column 2: Key Metrics ---
    with col2:
        category_counts = df['category'].value_counts()
        struggle_count = category_counts.get('Struggle / Confusion', 0)
        feature_request_count = category_counts.get('Feature Request', 0)
        negative_feedback_count = category_counts.get('Negative Feedback', 0)
        positive_feedback_count = category_counts.get('Positive Feedback', 0)
        
        st.metric(label="Struggle/Confusion", value=struggle_count)
        st.metric(label="Feature Requests", value=feature_request_count)
        st.metric(label="Negative Feedback", value=negative_feedback_count)
        st.metric(label="Positive Feedback", value=positive_feedback_count)

    # --- Column 3: Pie Chart ---
    with col3:
        st.subheader("Comments by Category")
        pie_data = category_counts.reset_index()
        pie_data.columns = ['category', 'count']
        
        fig = px.pie(
            pie_data, 
            names='category', 
            values='count', 
            hole=.3,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig.update_layout(
            legend_title_text='Categories',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --- Bottom Row Layout ---
    st.header("Top Feedback Items")
    col_a, col_b, col_c = st.columns(3)

    # Function to display top items for a category
    def display_top_feedback(column, category_name):
        with column:
            st.subheader(f"Top {category_name}")
            category_df = df[df['category'] == category_name]
            if not category_df.empty:
                # MODIFIED: Changed back to st.info to get the blue background, 
                # but kept enumerate to ensure correct 1, 2, 3 numbering.
                for i, row in enumerate(category_df.head(3).itertuples()):
                    st.info(f"{i+1}. {row.user_problem}")
            else:
                st.write(f"No feedback found for '{category_name}'.")

    # Display top items in each column
    display_top_feedback(col_a, "Feature Request")
    display_top_feedback(col_b, "Struggle / Confusion")
    display_top_feedback(col_c, "Negative Feedback")

else:
    st.warning(f"The report file '{csv_file_path}' was not found.")
    st.info("Please run the main analysis notebook (`analyzer.ipynb`) first to generate both the report and summary files.")
