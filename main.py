import streamlit as st
import requests
from converter import convert_units
from currency_api import get_exchange_rate

def set_theme(theme):
    base_style = """
    <style>
    :root {
        --primary: #1f6aa5;
        --background: #f8f9fa;
        --secondary-background: #ffffff;
        --text: #2c3e50;
        --border: #e0e0e0;
        --success: #28a745;
        --error: #dc3545;
    }
    
    [data-theme="dark"] {
        --primary: #6ab7ff;
        --background: #1a1a1a;
        --secondary-background: #262626;
        --text: #e0e0e0;
        --border: #404040;
        --success: #00c853;
        --error: #ff5252;
    }

    /* Main container styling */
    .main {
        background: var(--background) !important;
        color: var(--text) !important;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Input fields styling */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        background: var(--secondary-background) !important;
        color: var(--text) !important;
        border: 2px solid var(--primary) !important;
        border-radius: 8px !important;
        padding: 10px 15px !important;
    }

    /* Button styling */
    .stButton>button {
        background: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(var(--primary), 0.2);
    }

    /* Success/Error messages */
    .stSuccess {
        background: var(--success) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    .stError {
        background: var(--error) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    /* Card styling for conversion */
    .conversion-card {
        background: var(--secondary-background) !important;
        border-radius: 12px !important;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid var(--border);
        position: relative;
        overflow: hidden;
        transition: transform 0.3s ease;
    }

    .conversion-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, 
            transparent 25%, 
            var(--primary) 25%, 
            var(--primary) 50%, 
            transparent 50%, 
            transparent 75%, 
            var(--primary) 75%
        );
        opacity: 0.1;
        transform: rotate(30deg);
        animation: shine 4s linear infinite;
    }

    @keyframes shine {
        from { transform: translateX(-50%) rotate(30deg); }
        to { transform: translateX(50%) rotate(30deg); }
    }

    .credits {
        position: fixed;
        bottom: 20px;
        right: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 0.9rem;
        color: var(--text);
        background: var(--secondary-background);
        padding: 8px 15px;
        border-radius: 25px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid var(--border);
        animation: float 6s ease-in-out infinite;
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    </style>
    """
    
    js = f"""
    <script>
    document.documentElement.setAttribute('data-theme', '{theme.lower()}');
    </script>
    """
    
    st.markdown(base_style + js, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Unit Converter Pro",
        page_icon="🔄",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    # Theme management
    if 'theme' not in st.session_state:
        st.session_state.theme = "light"
    
    # Enhanced sidebar
    with st.sidebar:
        st.title("🎨 Settings")
        st.session_state.theme = st.radio(
            "THEME SELECTOR",
            ["Light", "Dark"],
            index=0 if st.session_state.theme == "light" else 1,
            label_visibility="collapsed"
        )
        st.markdown("---")
        st.subheader("📚 Supported Units")
        with st.expander("View All Units", expanded=True):
            st.markdown("""
            **Length:**  
            - km, mi, m, yd, ft, in  
            
            **Weight:**  
            - kg, lb, g, oz  
            
            **Temperature:**  
            - °C, °F, K  
            
            **Currency:**  
            - USD, EUR, PKR, INR, GBP
            """)
    
    set_theme(st.session_state.theme)
    
    # Main content with card effect
    with st.container():
        st.markdown("""
        <div class='main'>
            <div class="credits">✨ Crafted with ❤️ by <span style="font-weight: 800; 
            background: linear-gradient(45deg, #1f6aa5, #6ab7ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;">Fiza Nazz</span></div>
        """, unsafe_allow_html=True)
        
        st.title("📐 Ultimate Unit Converter")
        st.markdown("---")
        
        # Conversion type
        conversion_type = st.selectbox(
            "SELECT CONVERSION TYPE",
            ["Length", "Weight", "Temperature", "Currency"],
            key="conversion_type",
            label_visibility="collapsed"
        )
        
        # Value input
        value = st.number_input(
            "ENTER VALUE",
            min_value=0.0,
            format="%.4f",
            key="main_input",
            label_visibility="collapsed"
        )
        
        # Unit inputs with modern layout
        col1, col2, col3 = st.columns([3, 1, 3])
        with col1:
            if conversion_type == "Currency":
                from_unit = st.selectbox(
                    "FROM",
                    ["USD", "EUR", "PKR", "INR", "GBP"],
                    key="from_currency"
                )
            else:
                from_unit = st.text_input(
                    "FROM UNIT",
                    key="from_unit",
                    placeholder="e.g., kg, km, C",
                    label_visibility="collapsed"
                ).strip().lower()
        
        
        with col3:
            if conversion_type == "Currency":
                to_unit = st.selectbox(
                    "TO",
                    ["USD", "EUR", "PKR", "INR", "GBP"],
                    key="to_currency"
                )
            else:
                to_unit = st.text_input(
                    "TO UNIT",
                    key="to_unit",
                    placeholder="e.g., lb, mi, F",
                    label_visibility="collapsed"
                ).strip().lower()
        
        # Conversion result card
        if st.button("🚀 CONVERT NOW", use_container_width=True, type="primary"):
            with st.spinner("Converting..."):
                try:
                    result = (get_exchange_rate(from_unit, to_unit, value) 
                        if conversion_type == "Currency" 
                        else convert_units(conversion_type, value, from_unit, to_unit))
                    
                    if isinstance(result, (int, float)):
                        st.balloons()
                        st.markdown(f"""
                        <div class='conversion-card'>
                            <div style="position: relative; z-index: 2;">
                                <h3 style='color: var(--text); margin-bottom: 1rem; display: flex; 
                                    align-items: center; gap: 10px;'>
                                    <div style="background: var(--success); width: 10px; 
                                        height: 30px; border-radius: 5px;"></div>
                                    🎉 Conversion Success!
                                </h3>
                                <p style='font-size: 1.5rem; margin: 0; line-height: 1.4;'>
                                <span style="display: inline-block; min-width: 120px;">
                                {value:.4f} {from_unit.upper()}</span>
                                <span style="color: var(--text); margin: 0 10px;">→</span>
                                <span style="color: var(--primary); font-size: 2.5rem; 
                                    font-weight: 800;">{result:.4f}</span> 
                                <strong>{to_unit.upper()}</strong>
                                </p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"⚠️ {result}")
                except Exception as e:
                    st.error(f"🚨 Critical Error: {str(e)}")
                    st.toast("Please check your inputs!", icon="❌")
        
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()