import streamlit as st
import time
import os
import sys

st.set_page_config(
    page_title="TrueCheck: AI Fact Verification",
    page_icon="🔍",
    layout="centered"
)

if not os.path.exists("./chroma_db"):
    st.warning("⚠️ Vector Database not found. Building it for the first time... (This takes ~10s)")
    try:
        import build_db
        build_db.build_database()
        st.success("✅ Database built successfully! Reloading...")
        time.sleep(1.5)
        st.rerun()
    except Exception as e:
        st.error(f"❌ Failed to build database: {e}")
        st.stop()
# ---------------------------------------------

# Import Modules 
from src.extractor import ClaimExtractor
from src.retrieval_engine import FactRetriever
from src.verifier_llm import FactChecker

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .reportview-container {
        background: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Modules
@st.cache_resource
def load_modules():
    return ClaimExtractor(), FactRetriever(), FactChecker()

try:
    nlp_tool, rag_engine, llm_verifier = load_modules()
except Exception as e:
    st.error(f"Error loading modules: {e}")
    st.stop()

st.title("🔍 TrueCheck: AI Fact Verification")
st.markdown("### Powered by RAG & LLM Agents")
st.caption("Submit a claim to verify it against the Official Indian Government Knowledge Base.")

# Input Section
query = st.text_area(
    "Enter a statement to verify:", 
    placeholder="e.g., The government announced free electricity for all farmers starting July 2025.",
    height=100
)

col1, col2 = st.columns([1, 2])

with col1:
    verify_btn = st.button("🚀 Verify Claim", type="primary")

if verify_btn:
    if not query.strip():
        st.warning("Please enter a valid claim.")
    else:
        with st.spinner("🕵️ Extracting Entities & Retrieving Evidence..."):
            # Start Timer
            start_time = time.time()
            
            # 1. NLP Analysis
            analysis = nlp_tool.extract_metadata(query)
            
            # 2. Retrieve Facts & SCORES
            # Returns tuple: (list_of_facts, list_of_distances)
            evidence, distances = rag_engine.retrieve(query, k=3)
            
            # Safety check if no distances returned
            best_score = distances[0] if distances else 2.0
            
            
            THRESHOLD = 0.5

            if best_score > THRESHOLD:
                result = {
                    "verdict": "🤷‍♂️ Unverifiable (Vague/No Data)",
                    "reasoning": f"No relevant facts found in the database. The closest match had a low relevance score ({round(best_score, 2)}).",
                    "evidence": []
                }
            else:
                # 3. LLM Verification (Only if relevant facts exist)
                result = llm_verifier.verify_claim(query, evidence)
            
            end_time = time.time()
            latency = round(end_time - start_time, 2)

            # --- Display Results ---
            st.divider()
            
            verdict = result.get("verdict", "Unverifiable")
            if "True" in verdict:
                st.success(f"## {verdict}")
            elif "False" in verdict:
                st.error(f"## {verdict}")
            else:
                st.warning(f"## {verdict}")

            # Reasoning
            st.markdown(f"**Reasoning:** {result.get('reasoning')}")
            
            # Evidence Section
            if result.get("evidence"):
                st.subheader("📚 Verified Evidence Source")
                for i, fact in enumerate(result.get("evidence", [])):
                    st.info(f"{i+1}. {fact}")
            else:
                st.info("No trusted evidence found matching this claim.")

            m1, m2, m3 = st.columns(3)
            m1.metric("Processing Time", f"{latency}s")
            m1.metric("Evidence Retrieved", f"{len(evidence)} docs")
            m1.metric("Relevance Score", f"{round(best_score, 2)} (Lower is better)")

            st.write("---")
            st.markdown("**Was this analysis helpful?**")
            c1, c2, c3 = st.columns([1,1,4])
            with c1: 
                if st.button("👍 Yes"):
                    st.toast("Thanks for your feedback!", icon="🎉")
            with c2: 
                if st.button("👎 No"):
                    st.toast("We'll try to improve.", icon="🔧")

            # --- Developer Debug View ---
            with st.expander("🛠️ Developer Logs (Pipeline State)"):
                st.json({
                    "extracted_keywords": analysis.get('keywords', []),
                    "extracted_entities": analysis.get('entities', []),
                    "vector_distances": distances,
                    "threshold_used": THRESHOLD,
                    "raw_llm_response": result
                })
