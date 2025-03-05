import streamlit as st
import requests

def get_exchange_rate(from_currency, to_currency, amount):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "rates" in data and to_currency in data["rates"]:
            return amount * data["rates"][to_currency]
        else:
            return "Conversion Error: Invalid currency code."
    except requests.exceptions.RequestException as e:
        return f"API Error: {str(e)}"

def load_custom_css(theme):
    css = f"""
    <style>
    body {{
        background-color: {'#1a1a1a' if theme == 'Dark' else '#f8f9fa'};
        color: {'#e0e0e0' if theme == 'Dark' else '#2c3e50'};
    }}

    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {{
        background: {'#262626' if theme == 'Dark' else '#ffffff'};
        color: {'#e0e0e0' if theme == 'Dark' else '#2c3e50'};
        border: 2px solid {'#6ab7ff' if theme == 'Dark' else '#1f6aa5'};
    }}

    .stButton>button {{
        background: {'#6ab7ff' if theme == 'Dark' else '#1f6aa5'};
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }}

    .conversion-result {{
        background: {'#262626' if theme == 'Dark' else '#ffffff'};
        border: 1px solid {'#404040' if theme == 'Dark' else '#e0e0e0'};
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        color: {'#e0e0e0' if theme == 'Dark' else '#2c3e50'};
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Unit Converter Pro", page_icon="🔄", layout="centered")

    if 'theme' not in st.session_state:
        st.session_state.theme = "Light"

    with st.sidebar:
        st.title("🎨 Settings")
        st.session_state.theme = st.radio(
            "THEME SELECTOR", ["Light", "Dark"],
            index=0 if st.session_state.theme == "Light" else 1
        )

        st.markdown("---")
        st.subheader("📚 Supported Units")
        with st.expander("View All Units", expanded=True):
            st.markdown("""
            *Length:* km, mi, m, yd, ft, in  
            *Weight:* kg, lb, g, oz  
            *Temperature:* °C, °F, K  
            *Currency:* USD, EUR, PKR, INR, GBP
            """)

    load_custom_css(st.session_state.theme)

    st.title("📐 Ultimate Unit Converter")
    st.markdown("---")

    conversion_type = st.selectbox("SELECT CONVERSION TYPE", ["Currency"], index=0)
    value = st.number_input("ENTER VALUE", min_value=0.0, format="%.4f")

    col1, col2, col3 = st.columns([3, 1, 3])

    with col1:
        from_unit = st.selectbox("FROM", ["USD", "EUR", "PKR", "INR", "GBP"], key="from_currency")

    with col3:
        to_unit = st.selectbox("TO", ["USD", "EUR", "PKR", "INR", "GBP"], key="to_currency")

    if st.button("🚀 CONVERT NOW", use_container_width=True):
        with st.spinner("Converting..."):
            result = get_exchange_rate(from_unit, to_unit, value)

            if isinstance(result, (float, int)):
                st.balloons()
                st.markdown(f"""
                <div class="conversion-result">
                    <h3>🎉 Conversion Successful!</h3>
                    <p><strong>{value:.4f} {from_unit}</strong> = <strong>{result:.4f} {to_unit}</strong></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(result)

if __name__ == "_main_":
    main()