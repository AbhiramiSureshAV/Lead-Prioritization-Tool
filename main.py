import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import random
import numpy as np
from scraper import enrich_leads, calculate_acquisition_fit_score

# Enable caching to improve performance
@st.cache_data
def load_sample_data():
    """Cache sample data loading"""
    return pd.read_csv("sample_leads.csv")

def enrich_lead_data(company_name, domain):
    """Lead enrichment without caching to avoid display issues"""
    enriched_data = enrich_leads(company_name, domain)
    score = calculate_acquisition_fit_score(enriched_data)
    enriched_data['acquisition_score'] = score
    return enriched_data

# Page configuration
st.set_page_config(
    page_title="🎯 SaaSquatch AI Lead Prioritizer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced professional styling with animations
st.markdown("""
<style>
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes countUp {
        from { opacity: 0; transform: scale(0.8); }
        to { opacity: 1; transform: scale(1); }
    }
    
    .main {
        background: linear-gradient(135deg, #0f1419 0%, #1a202c 100%);
        color: white;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 25%, #2d1b3d 50%, #1a202c 75%, #0f1419 100%);
    }
    
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        text-align: center;
        color: white;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 1rem;
    }
    
    .hero-badge {
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.2rem;
        backdrop-filter: blur(10px);
    }
    
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
        cursor: pointer;
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 8px 25px rgba(72, 187, 120, 0.3);
        border-color: rgba(72, 187, 120, 0.5);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #48bb78;
        margin-bottom: 0.3rem;
        animation: countUp 1s ease-out 0.3s both;
    }
    
    .metric-value:hover {
        animation: pulse 1s infinite;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(72, 187, 120, 0.4);
    }
    
    .css-1d391kg {
        background: linear-gradient(180deg, #0a0e1a 0%, #1a1f2e 50%, #2d1b3d 100%);
        border-right: 1px solid rgba(72, 187, 120, 0.2);
    }
    
    .filter-chip {
        display: inline-block;
        background: rgba(72, 187, 120, 0.2);
        color: #48bb78;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        border: 1px solid rgba(72, 187, 120, 0.4);
        animation: fadeInUp 0.4s ease-out;
    }
    
    .lead-card {
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .lead-card:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    
    .score-badge {
        animation: pulse 2s infinite;
        transition: all 0.3s ease;
    }
    
    .score-badge:hover {
        transform: scale(1.1);
        animation: none;
    }
</style>
""", unsafe_allow_html=True)

def create_hero():
    """Create clean hero section"""
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">🎯 SaaSquatch AI Lead Prioritizer</div>
        <div class="hero-subtitle">Transform leads into acquisition-ready targets with AI intelligence</div>
        <div>
            <span class="hero-badge">🤖 AI-Powered</span>
            <span class="hero-badge">📊 Smart Analytics</span>
            <span class="hero-badge">🚀 ETA Focused</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_metrics(df):
    if df is None or df.empty:
        return
    
    # Calculate metrics
    score_col = 'acquisition_score' if 'acquisition_score' in df.columns else 'acquisition_fit_score'
    avg_score = df[score_col].mean() if score_col in df.columns else 0
    high_priority = len(df[df[score_col] >= 80]) if score_col in df.columns else 0
    total_leads = len(df)
    top_industry = df['industry'].value_counts().index[0] if 'industry' in df.columns and not df['industry'].value_counts().empty else "N/A"
    
    st.markdown(
        f"""
        <div class="metrics-container">
            <div class="metric-card">
                <div class="metric-value">{avg_score:.1f}</div>
                <div class="metric-label">Avg Score</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{high_priority}</div>
                <div class="metric-label">High Priority</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{total_leads}</div>
                <div class="metric-label">Total Leads</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{top_industry}</div>
                <div class="metric-label">Top Industry</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    """Main application"""
    create_hero()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎛️ Control Panel")
        st.markdown("---")
        
        # Sample data option
        if st.button("📁 Load Sample Data", type="primary", use_container_width=True):
            sample_data = load_sample_data()
            st.session_state.leads_df = sample_data
            st.rerun()
        
        # File upload
        uploaded_file = st.file_uploader(
            "📤 Upload Your CSV File", 
            type=['csv'],
            help="Upload a CSV with columns: company_name, domain (optional)"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                required_cols = ['company_name']
                if all(col in df.columns for col in required_cols):
                    st.session_state.leads_df = df
                    st.rerun()
                else:
                    st.error(f"❌ CSV must contain: {', '.join(required_cols)}")
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
        
        # Enhanced Filters with chips
        if 'leads_df' in st.session_state and 'acquisition_score' in st.session_state.leads_df.columns:
            st.markdown("---")
            st.markdown("### 🔍 Smart Filters")
            
            # Quick preset buttons vertically
            st.markdown("**Quick Filters:**")
            if st.button("🔥 High Priority", use_container_width=True):
                st.session_state.min_score = 80
            if st.button("🏢 SaaS Only", use_container_width=True):
                if 'industry' in st.session_state.leads_df.columns:
                    st.session_state.selected_industries = ['SaaS/Tech']
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.min_score = 30
                if 'industry' in st.session_state.leads_df.columns:
                    st.session_state.selected_industries = list(st.session_state.leads_df['industry'].unique())
            
            min_score = st.slider("🎯 Min Score", 0, 100, st.session_state.get('min_score', 70), 5)
            
            if 'industry' in st.session_state.leads_df.columns:
                industries = st.session_state.leads_df['industry'].unique()
                selected_industries = st.multiselect("🏢 Industry", industries, default=st.session_state.get('selected_industries', industries))
            else:
                selected_industries = []
            
            st.session_state.min_score = min_score
            st.session_state.selected_industries = selected_industries

    # Main content area
    if 'leads_df' not in st.session_state:
        st.markdown("""
        <div style="text-align: center; padding: 3rem 2rem; background: rgba(26, 32, 44, 0.9); border-radius: 20px; margin: 2rem 0; border: 2px solid rgba(72, 187, 120, 0.3);">
            <div style="font-size: 4rem; margin-bottom: 1.5rem;">🎯</div>
            <h1 style="color: white; font-size: 2.5rem; margin-bottom: 1rem; font-weight: 800;">Acquisition Intelligence Engine</h1>
            <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; line-height: 1.6; margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto;">
                Transform raw company lists into <strong style="color: #48bb78;">strategic acquisition targets</strong> using proprietary AI scoring algorithms designed for <strong style="color: #667eea;">ETA investments</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: rgba(72, 187, 120, 0.1); padding: 2rem; border-radius: 15px; border: 1px solid rgba(72, 187, 120, 0.3); text-align: center; margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🧠</div>
                <div style="color: #48bb78; font-weight: 700; margin-bottom: 0.8rem;">Neural Scoring</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">6-factor acquisition readiness algorithm</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: rgba(102, 126, 234, 0.1); padding: 2rem; border-radius: 15px; border: 1px solid rgba(102, 126, 234, 0.3); text-align: center; margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">⚡</div>
                <div style="color: #667eea; font-weight: 700; margin-bottom: 0.8rem;">Lightning Enrichment</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Instant contact discovery & validation</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: rgba(118, 75, 162, 0.1); padding: 2rem; border-radius: 15px; border: 1px solid rgba(118, 75, 162, 0.3); text-align: center; margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🎯</div>
                <div style="color: #764ba2; font-weight: 700; margin-bottom: 0.8rem;">ETA Precision</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Built for acquisition targeting</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-top: 2rem; padding: 1.5rem; background: rgba(72, 187, 120, 0.1); border-radius: 12px; border: 1px solid rgba(72, 187, 120, 0.4); text-align: center;">
            <div style="color: #48bb78; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;">🚀 Ready to Transform Your Deal Flow?</div>
            <div style="color: rgba(255,255,255,0.9);">Upload your company list or explore our sample dataset</div>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        # Process leads if not already processed
        if 'acquisition_score' not in st.session_state.leads_df.columns:
            st.markdown("### 🚀 Processing Leads")
            
            progress_bar = st.progress(0)
            
            enriched_leads = []
            total_leads = len(st.session_state.leads_df)
            
            for i, row in st.session_state.leads_df.iterrows():
                progress = (i + 1) / total_leads
                progress_bar.progress(progress)
                
                enriched_data = enrich_lead_data(row['company_name'], row.get('domain', ''))
                enriched_leads.append(enriched_data)
            
            st.session_state.leads_df = pd.DataFrame(enriched_leads)
            
            progress_bar.progress(1.0)
            st.success("✅ Processing complete!")
            time.sleep(1)
            st.rerun()
        
        # Apply filters
        filtered_df = st.session_state.leads_df.copy()
        
        if 'acquisition_score' in filtered_df.columns:
            min_score = st.session_state.get('min_score', 70)
            selected_industries = st.session_state.get('selected_industries', [])
            
            filtered_df = filtered_df[filtered_df['acquisition_score'] >= min_score]
            
            if selected_industries and 'industry' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['industry'].isin(selected_industries)]
        
        # Show metrics
        create_metrics(filtered_df)
        
        # Top leads display
        if 'acquisition_score' in st.session_state.leads_df.columns:
            st.markdown("### 🏆 Top Acquisition-Ready Leads")
            
            if len(filtered_df) == 0:
                st.warning(f"⚠️ No leads match your criteria (Score ≥ {st.session_state.get('min_score', 70)}). Try lowering the minimum score.")
            else:
                top_leads = filtered_df.nlargest(5, 'acquisition_score')
                
                for i, (_, lead) in enumerate(top_leads.iterrows(), 1):
                    score = lead.get('acquisition_score', 0)
                    score_emoji = "🔥" if score >= 80 else "⚡" if score >= 60 else "📊"
                    score_color = "#48bb78" if score >= 80 else "#ed8936" if score >= 60 else "#e53e3e"
                    
                    # Create a card container for each lead
                    with st.container():
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, rgba(26, 32, 44, 0.9) 0%, rgba(45, 55, 72, 0.8) 100%); 
                                    padding: 1.5rem; border-radius: 15px; border-left: 5px solid {score_color}; 
                                    box-shadow: 0 4px 15px rgba(0,0,0,0.3); margin-bottom: 1.5rem; 
                                    border: 1px solid rgba(72, 187, 120, 0.2);">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <h3 style="color: white; margin: 0; font-size: 1.3rem; font-weight: 700;">#{i} {lead['company_name']}</h3>
                                    <p style="color: rgba(255,255,255,0.8); margin: 0.3rem 0 0 0; font-size: 1rem;">🏢 {lead.get('industry', 'N/A')}</p>
                                </div>
                                <div style="background: {score_color}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold; font-size: 1.1rem;">
                                    {score_emoji} {score:.1f}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                        with st.expander("View Details", expanded=False):
                            col1, col2, col3 = st.columns(3)
                        
                        with col1:
                                st.markdown(f"**Industry:** {lead.get('industry', 'N/A')}")
                                st.markdown(f"**Revenue:** {lead.get('revenue_range', 'N/A')}")
                        
                        with col2:
                                st.markdown(f"**Email:** {lead.get('email', 'N/A')}")
                                st.markdown(f"**Phone:** {lead.get('phone', 'N/A')}")
                        
                        with col3:
                                st.markdown(f"**Location:** {lead.get('location', 'N/A')}")
                                st.markdown(f"**Size:** {lead.get('company_size', 'N/A')}")
        
        # Enhanced Export section
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(26, 32, 44, 0.9) 0%, rgba(45, 55, 72, 0.8) 100%); padding: 2rem; border-radius: 15px; border: 2px solid rgba(72, 187, 120, 0.3); margin: 2rem 0; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; right: 0; width: 100px; height: 100px; background: radial-gradient(circle, rgba(72, 187, 120, 0.1) 0%, transparent 70%); border-radius: 50%;"></div>
            <h3 style="color: #48bb78; margin-bottom: 1rem; font-size: 1.5rem;">📤 Export Intelligence Report</h3>
            <p style="color: rgba(255,255,255,0.9); margin-bottom: 1.5rem; font-size: 1.1rem;">Download your AI-prioritized leads with comprehensive scoring and enriched data</p>
            <div style="display: flex; gap: 1rem; align-items: center; margin-bottom: 1rem;">
                <span style="background: rgba(72, 187, 120, 0.2); color: #48bb78; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.9rem;">📊 CSV Format</span>
                <span style="background: rgba(102, 126, 234, 0.2); color: #667eea; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.9rem;">🔄 Real-time Data</span>
                <span style="background: rgba(237, 137, 54, 0.2); color: #ed8936; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.9rem;">🎯 CRM Ready</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💾 Download Prioritized Leads", type="primary", use_container_width=True):
            display_columns = [
                'company_name', 'acquisition_score', 'industry', 'revenue_range',
                'email', 'phone', 'linkedin', 'domain', 'location', 'company_size'
            ]
            
            available_columns = [col for col in display_columns if col in filtered_df.columns]
            display_df = filtered_df[available_columns] if len(filtered_df) > 0 else st.session_state.leads_df[available_columns]
            
            if 'acquisition_score' in display_df.columns:
                display_df = display_df.sort_values('acquisition_score', ascending=False)
            
            csv = display_df.to_csv(index=False)
            timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
            filename = f"ai_prioritized_leads_{timestamp}.csv"
            
            st.download_button(
                label=f"📥 Download {len(display_df)} Prioritized Leads",
                data=csv,
                file_name=filename,
                mime="text/csv",
                use_container_width=True
            )
            
            avg_score = display_df['acquisition_score'].mean() if 'acquisition_score' in display_df.columns else 0
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(72, 187, 120, 0.2) 0%, rgba(56, 161, 105, 0.2) 100%); padding: 1rem; border-radius: 10px; border: 1px solid rgba(72, 187, 120, 0.4); margin-top: 1rem; animation: fadeInUp 0.5s ease-out;">
                <div style="color: #48bb78; font-weight: 700; margin-bottom: 0.5rem;">🎯 Export Preview</div>
                <div style="color: rgba(255,255,255,0.9); display: flex; justify-content: space-between; align-items: center;">
                    <span>{len(display_df)} prioritized leads ready</span>
                    <span style="background: rgba(72, 187, 120, 0.3); padding: 0.2rem 0.6rem; border-radius: 10px; font-weight: 600;">Avg Score: {avg_score:.1f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # How It Works section at the end
        st.markdown("---")
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(72, 187, 120, 0.15) 0%, rgba(102, 126, 234, 0.15) 100%); padding: 2rem; border-radius: 15px; border: 2px solid rgba(72, 187, 120, 0.3); margin: 2rem 0;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2 style="color: #48bb78; font-size: 2rem; margin-bottom: 0.5rem;">🧠 AI Scoring Algorithm</h2>
                <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">Our proprietary 6-factor acquisition readiness engine</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: rgba(72, 187, 120, 0.2); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(72, 187, 120, 0.4); margin-bottom: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">💰</div>
                <div style="color: #48bb78; font-weight: 700; font-size: 1.2rem; margin-bottom: 0.5rem;">Revenue (30%)</div>
                <div style="color: rgba(255,255,255,0.9); line-height: 1.5;">Financial health assessment</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: rgba(102, 126, 234, 0.2); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(102, 126, 234, 0.4);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏢</div>
                <div style="color: #667eea; font-weight: 700; font-size: 1.2rem; margin-bottom: 0.5rem;">Industry (20%)</div>
                <div style="color: rgba(255,255,255,0.9); line-height: 1.5;">Market compatibility</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: rgba(118, 75, 162, 0.2); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(118, 75, 162, 0.4); margin-bottom: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📈</div>
                <div style="color: #764ba2; font-weight: 700; font-size: 1.2rem; margin-bottom: 0.5rem;">Growth (20%)</div>
                <div style="color: rgba(255,255,255,0.9); line-height: 1.5;">Expansion signals</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: rgba(237, 137, 54, 0.2); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(237, 137, 54, 0.4);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📧</div>
                <div style="color: #ed8936; font-weight: 700; font-size: 1.2rem; margin-bottom: 0.5rem;">Contact (10%)</div>
                <div style="color: rgba(255,255,255,0.9); line-height: 1.5;">Verified information</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: rgba(56, 178, 172, 0.2); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(56, 178, 172, 0.4); margin-bottom: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">👥</div>
                <div style="color: #38b2ac; font-weight: 700; font-size: 1.2rem; margin-bottom: 0.5rem;">Size (10%)</div>
                <div style="color: rgba(255,255,255,0.9); line-height: 1.5;">Company scale</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: rgba(245, 101, 101, 0.2); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(245, 101, 101, 0.4);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📍</div>
                <div style="color: #f56565; font-weight: 700; font-size: 1.2rem; margin-bottom: 0.5rem;">Location (10%)</div>
                <div style="color: rgba(255,255,255,0.9); line-height: 1.5;">Geographic advantage</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(26, 32, 44, 0.8); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(72, 187, 120, 0.3); margin: 2rem 0; text-align: center;">
            <h3 style="color: #48bb78; margin-bottom: 1rem;">Score Guide</h3>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1rem;">
                <div style="padding: 1rem; background: rgba(72, 187, 120, 0.1); border-radius: 8px; min-width: 150px;">
                    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🔥</div>
                    <div style="color: #48bb78; font-weight: 700;">80-100</div>
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">High Priority</div>
                </div>
                <div style="padding: 1rem; background: rgba(237, 137, 54, 0.1); border-radius: 8px; min-width: 150px;">
                    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">⚡</div>
                    <div style="color: #ed8936; font-weight: 700;">60-79</div>
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Medium Priority</div>
                </div>
                <div style="padding: 1rem; background: rgba(229, 62, 62, 0.1); border-radius: 8px; min-width: 150px;">
                    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📊</div>
                    <div style="color: #e53e3e; font-weight: 700;">Below 60</div>
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Needs Review</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()