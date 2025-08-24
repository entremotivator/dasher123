import streamlit as st
from pathlib import Path
import sys

# ------------------------
# Fix import paths
# ------------------------
BASE_DIR = Path(__file__).resolve().parent          # Aidash95-master4/Aidash95-master/
ROOT_DIR = BASE_DIR.parent                          # Aidash95-master4/
ORIGINAL_REPO_DIR = ROOT_DIR / "Aidash95-master"    # Aidash95-master/

# Add both local and original repo dirs to sys.path
sys.path.append(str(BASE_DIR))
sys.path.append(str(ORIGINAL_REPO_DIR))

# Now imports will work regardless of folder structure
from login_aivaceo import show_login
from sidebar_enhanced import show_sidebar
from utils.config import load_config, init_session_state


# ------------------------
# Configure Streamlit
# ------------------------
st.set_page_config(
    page_title="AIVACEO Systems - Advanced Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ------------------------
# Load custom CSS
# ------------------------
def load_css():
    """Load custom CSS for styling the app, with fallback support."""
    css_candidates = [
        BASE_DIR / "assets" / "aivaceo_style.css",
        ORIGINAL_REPO_DIR / "assets" / "aivaceo_style.css",
        BASE_DIR / "assets" / "style.css",
        ORIGINAL_REPO_DIR / "assets" / "style.css",
    ]

    for css_file in css_candidates:
        if css_file.exists():
            with open(css_file, encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            return

    st.warning("⚠️ No CSS file found — using default Streamlit styling.")


# ------------------------
# Page Router
# ------------------------
def get_page_mapping(base_dir: Path):
    """Return mapping of page labels to their script paths."""
    return {
        "Enhanced Dashboard": base_dir / "pages" / "1_Enhanced_Dashboard.py",
        "Dashboard": base_dir / "pages" / "1_Dashboard.py",
        "Calendar": base_dir / "pages" / "2_Calendar.py",
        "Invoices": base_dir / "pages" / "3_Invoices.py",
        "Customers": base_dir / "pages" / "4_Customers.py",
        "Appointments": base_dir / "pages" / "5_Appointments.py",
        "Pricing": base_dir / "pages" / "6_Pricing.py",
        "AI Chat": base_dir / "pages" / "7_Super_Chat.py",
        "Voice Calls": base_dir / "pages" / "8_AI_Caller.py",
        "Call Center": base_dir / "pages" / "9_Call_Center.py",
        "Content Management": base_dir / "pages" / "10_Content_Management_Dashboard.py",
    }


# ------------------------
# Main app logic
# ------------------------
def main():
    # Setup
    load_css()
    load_config()
    init_session_state()

    st.write("🚀 App started")

    # Check login status
    if not st.session_state.get("logged_in", False):
        st.info("🔐 Please log in to continue.")
        show_login()
        return

    # User is logged in
    st.success("✅ Logged in")
    show_sidebar()

    # Ensure a default page
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Enhanced Dashboard"

    # Resolve page
    base_dir = BASE_DIR
    page_mapping = get_page_mapping(base_dir)
    selected_page = st.session_state.get("current_page")

    st.write(f"📄 Current page: **{selected_page}**")

    if selected_page in page_mapping:
        page_path = page_mapping[selected_page]
        if page_path.exists():
            try:
                st.switch_page(str(page_path))
            except Exception as e:
                st.error(f"❌ Failed to switch page: {e}")
        else:
            st.error(f"❌ Page file not found: {page_path}")
    else:
        st.warning("⚠️ Page not found. Showing fallback dashboard.")
        st.title("🚀 AIVACEO Systems Dashboard (Fallback)")
        st.info("Use the sidebar to select a valid page.")


# ------------------------
# Entry point
# ------------------------
if __name__ == "__main__":
    main()
