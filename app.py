import streamlit as st
import json
from core import SportsIntelAnalyzer

# Set page layout
st.set_page_config(page_title="Sports Intelligence Pipeline", page_icon="⚽", layout="wide")

st.title("⚽ Sports & News Intelligence Pipeline")
st.markdown("Analyze sports commentary and news using **spaCy** (NER) and **Hugging Face** (Sentiment).")

# Cache the NLP model so it only loads once across app refreshes
@st.cache_resource
def load_engine():
    return SportsIntelAnalyzer()

with st.spinner("Initializing AI Models..."):
    analyzer = load_engine()

# Create two tabs: Real-time Analyzer and Batch File Viewer
tab1, tab2 = st.tabs(["⚡ Real-time Analysis", "📁 Saved Report Dashboard"])

with tab1:
    st.subheader("Analyze Custom Text")
    user_text = st.text_area(
        "Enter sports commentary or news snippet:",
        value="Real Madrid played a fantastic match against Rayo Vallecano today, absolutely brilliant!",
        height=100
    )
    
    if st.button("Run Intelligence Pipeline", type="primary"):
        if user_text.strip():
            result = analyzer.analyze(user_text)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.metric(
                    label="Overall Sentiment",
                    value=result['sentiment']['label'],
                    delta=f"{result['sentiment']['confidence']:.2%} Confidence"
                )
            
            with col2:
                st.write("**Extracted Entities**")
                if result['entities']:
                    st.dataframe(result['entities'], use_container_width=True)
                else:
                    st.info("No specific entities detected.")
        else:
            st.warning("Please enter some text to analyze.")

with tab2:
    st.subheader("Batch Report Summary")
    try:
        with open("summary.json", "r") as f:
            summary = json.load(f)
        
        st.dataframe(summary, use_container_width=True)
        
        # Show simple counts
        total_entities = len(summary)
        pos_entities = sum(1 for e in summary if "Positive" in e['trend'])
        st.caption(f"Tracking **{total_entities}** entities across saved reports ({pos_entities} trending positive).")
        
    except FileNotFoundError:
        st.warning("No `summary.json` file found. Run `aggregate.py` first to generate batch reports.")