import streamlit as st
import json
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards
import re

# Set page config
st.set_page_config(page_title="Experiment Plan Generator", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
    <style>
    .stMetricValue, .stMetricLabel {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.4);
    }
    .stMetric {
        background-color: rgba(28, 131, 225, 0.1) !important;
        border: 1px solid #1C83E1 !important;
        padding: 10px !important;
        border-radius: 5px !important;
        margin-bottom: 10px !important;
    }
    .stMetricValue { font-size: 2rem !important; }
    .stMetricLabel { font-size: 1rem !important; }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #FFFFFF !important; }
    .stButton>button {
        background-color: #1C83E1;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
    }
    .stButton>button:hover { background-color: #0F5A9E; }
    .feedback-button {
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        border: none;
        color: white;
        font-weight: bold;
        cursor: pointer;
        margin-right: 0.5rem;
    }
    .thumbs-up { background-color: #28a745; }
    .thumbs-down { background-color: #dc3545; }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    with open('experiment_data.json', 'r') as file:
        return json.load(file)

# Custom metric display
def custom_metric(label, value):
    st.markdown(f"""
    <div class="stMetric">
        <div class="stMetricLabel">{label}</div>
        <div class="stMetricValue">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# Simulated data export function
def export_data():
    st.success("Data exported to laboratory information management system (LIMS). 📊🧬 (Simulated action)")

def clean_and_format_steps(steps):
    cleaned_steps = []
    for step in steps:
        # Remove leading/trailing whitespace
        step = step.strip()
        # Remove leading numbers and dots
        step = re.sub(r'^\d+\.?\s*', '', step)
        if step:  # Check if step is not empty after cleaning
            cleaned_steps.append(step)
    return cleaned_steps

def display_numbered_steps(title, content):
    st.subheader(title)
    if isinstance(content, str):
        # Split the string into individual steps
        steps = content.split('.')
    else:
        steps = content

    cleaned_steps = clean_and_format_steps(steps)
    for index, step in enumerate(cleaned_steps, 1):
        st.markdown(f"{index}. {step}")

# Feedback mechanism
def feedback_buttons(key):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 Reproducible", key=f"thumbs_up_{key}", help="Mark this protocol as reproducible"):
            st.success("Feedback recorded. This protocol will be flagged as reproducible.")
    with col2:
        if st.button("👎 Needs Improvement", key=f"thumbs_down_{key}", help="Suggest improvements for this protocol"):
            st.error("Feedback recorded. We'll review this protocol for potential improvements.")

# Main application
def main():
    colored_header(
        label="Experiment Planner",
        description="Temperature-dependent enzyme activity analysis",
        color_name="blue-70"
    )
    
    data = load_data()

    # Data export button
    if st.button("Export Data to LIMS / ELN 💾"):
        export_data()
    
    # Optimized protocols
    st.header("Optimized Experimental Protocols")
    best_experiments = data['best_experiments']
    for i, experiment in enumerate(best_experiments, 1):
        with st.expander(f"Protocol {i}: Temperature {experiment.get('temperature', 'N/A')}°C", expanded=i == 1):
            st.subheader(f"Optimization Score: {experiment['score']:.2f}")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                display_numbered_steps("Materials and Equipment", experiment['content']['equipment_setup'])
                
                display_numbered_steps("Experimental Procedure", experiment['content']['procedure'])
                
                st.subheader("Research Goal")
                st.info(experiment['content']['objective'])
                
                st.subheader("Data Collection")
                st.markdown(experiment['content']['observations'])
                
                st.subheader("Expected Outcomes")
                st.success(experiment['content']['results'])
            
            with col2:
                st.subheader("Protocol Analysis")
                st.markdown(experiment['reflection']['overall_assessment'])
                
                st.markdown("**Strengths:**")
                for strength in experiment['reflection']['strengths']:
                    st.markdown(f"- {strength}")
                
                st.markdown("**Potential Improvements:**")
                for suggestion in experiment['reflection']['suggestions']:
                    st.markdown(f"- {suggestion}")
                
                st.markdown("**Limitations:**")
                for weakness in experiment['reflection']['weaknesses']:
                    st.markdown(f"- {weakness}")
            
            feedback_buttons(f"protocol_{i}")
    
    # Alternative protocols
    st.header("Alternative Experimental Approaches")
    variants = data['generated_variants']
    for i, variant in enumerate(variants, 1):
        with st.expander(f"Alternative Protocol {i}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Materials and Equipment")
                st.markdown(variant['content']['equipment_setup'])
                
                st.subheader("Research Goal")
                st.info(variant['content']['objective'])
                
                st.subheader("Experimental Procedure")
                procedure = variant['content']['procedure']
                if isinstance(procedure, list):
                    for step in procedure:
                        st.markdown(f"- {step}")
                elif isinstance(procedure, str):
                    steps = procedure.split('\n')
                    for step in steps:
                        if step.strip():
                            st.markdown(f"- {step.strip()}")
                
                st.subheader("Data Collection")
                st.markdown(variant['content']['observations'])
                
                st.subheader("Expected Outcomes")
                st.success(variant['content']['results'])
            
            with col2:
                st.subheader("Protocol Evaluation")
                for criterion, score in variant['evaluation'].items():
                    custom_metric(criterion, f"{score:.1f}")
                
                st.subheader("Analysis")
                st.markdown(variant['reflection']['overall_assessment'])
                
                st.markdown("**Strengths:**")
                for strength in variant['reflection']['strengths']:
                    st.markdown(f"- {strength}")
                
                st.markdown("**Potential Improvements:**")
                for suggestion in variant['reflection']['suggestions']:
                    st.markdown(f"- {suggestion}")
                
                st.markdown("**Limitations:**")
                for weakness in variant['reflection']['weaknesses']:
                    st.markdown(f"- {weakness}")
            
            feedback_buttons(f"alternative_{i}")
    
    # Experimental metrics
    st.header("Experimental Metrics Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        custom_metric("Total Protocols", len(variants) + len(best_experiments))
    with col2:
        avg_objective = sum(v['evaluation']['Clear Objective'] for v in variants) / len(variants)
        custom_metric("Avg. Research Objective Clarity", f"{avg_objective:.2f}")
    with col3:
        avg_safety = sum(v['evaluation']['Safety Considerations'] for v in variants) / len(variants)
        custom_metric("Avg. Safety Score", f"{avg_safety:.2f}")

if __name__ == "__main__":
    main()