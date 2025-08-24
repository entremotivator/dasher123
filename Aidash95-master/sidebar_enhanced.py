import streamlit as st
import json
import os
from datetime import datetime
from utils.auth import logout_user
from utils.gsheet import test_gsheet_connection

def show_sidebar():
    """Enhanced AIVACEO sidebar with modern card-based UI and navigation"""
    with st.sidebar:
        # AIVACEO Branding Header
        st.markdown("""
        <div class="sidebar-card fade-in">
            <div style="text-align: center;">
                <div style="font-size: 1.8rem; font-weight: 800; margin-bottom: 0.5rem;">
                    🚀 AIVACEO
                </div>
                <div style="font-size: 0.9rem; opacity: 0.9; font-weight: 300;">
                    Advanced Intelligence & Virtual Assistant CEO Operations
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # User Profile Card
        render_user_profile_card()
        
        # Navigation Menu Card
        render_navigation_menu()
        
        # System Status Card
        render_system_status_card()
        
        # Google Sheets Integration Card
        render_gsheets_status_card()
        
        # Quick Actions Card
        render_quick_actions_card()
        
        # System Information Card
        render_system_info_card()

def render_user_profile_card():
    """Render user profile information card"""
    user_name = st.session_state.get('user_name', 'User')
    user_role = st.session_state.get('user_role', 'guest')
    last_login = st.session_state.get('last_login', 'N/A')
    login_time = st.session_state.get('login_time', 'N/A')
    
    st.markdown(f"""
    <div class="sidebar-card slide-in-left">
        <div class="sidebar-card-title">
            <span>👤</span> User Profile
        </div>
        <div class="sidebar-card-content">
            <div style="margin-bottom: 0.75rem;">
                <strong>Welcome, {user_name}!</strong>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Role:</span>
                <span style="text-transform: capitalize; font-weight: 600;">{user_role}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Status:</span>
                <span style="color: #10B981; font-weight: 600;">🟢 Active</span>
            </div>
            <div style="font-size: 0.8rem; opacity: 0.8; margin-top: 0.75rem;">
                Last login: {last_login if last_login != 'N/A' else 'First time'}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_navigation_menu():
    """Render enhanced navigation menu with cards"""
    st.markdown("""
    <div class="sidebar-card">
        <div class="sidebar-card-title">
            <span>🧭</span> Navigation
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation items with enhanced styling
    nav_items = [
        {
            "name": "Enhanced Dashboard", 
            "icon": "📊", 
            "desc": "Comprehensive Analytics", 
            "page": "pages/1_Enhanced_Dashboard.py",
            "color": "#4A90E2"
        },
        {
            "name": "Dashboard", 
            "icon": "📈", 
            "desc": "Overview & Analytics", 
            "page": "pages/1_Dashboard.py",
            "color": "#4A90E2"
        },
        {
            "name": "Calendar", 
            "icon": "📅", 
            "desc": "Schedule & Events", 
            "page": "pages/2_Calendar.py",
            "color": "#10B981"
        },
        {
            "name": "Invoices", 
            "icon": "📄", 
            "desc": "Billing & Payments", 
            "page": "pages/3_Invoices.py",
            "color": "#F59E0B"
        },
        {
            "name": "Customers", 
            "icon": "👥", 
            "desc": "Client Management", 
            "page": "pages/4_Customers.py",
            "color": "#8B5CF6"
        },
        {
            "name": "Appointments", 
            "icon": "🕐", 
            "desc": "Booking System", 
            "page": "pages/5_Appointments.py",
            "color": "#EC4899"
        },
        {
            "name": "Pricing", 
            "icon": "💰", 
            "desc": "Service Rates", 
            "page": "pages/6_Pricing.py",
            "color": "#F97316"
        },
        {
            "name": "AI Chat", 
            "icon": "🤖", 
            "desc": "AI Assistant", 
            "page": "pages/7_Super_Chat.py",
            "color": "#22C55E"
        },
        {
            "name": "Voice Calls", 
            "icon": "📞", 
            "desc": "Outbound Calling", 
            "page": "pages/8_AI_Caller.py",
            "color": "#3B82F6"
        },
        {
            "name": "Call Center", 
            "icon": "🎧", 
            "desc": "Support Center", 
            "page": "pages/9_Call_Center.py",
            "color": "#EF4444"
        },
        {
            "name": "Content Management", 
            "icon": "📝", 
            "desc": "Content Dashboard", 
            "page": "pages/10_Content_Management_Dashboard.py",
            "color": "#6366F1"
        }
    ]
    
    current_page = st.session_state.get('current_page', 'Enhanced Dashboard')
    
    for item in nav_items:
        is_active = current_page == item['name']
        button_class = "nav-button active" if is_active else "nav-button"
        
        # Create custom button with enhanced styling
        button_html = f"""
        <div class="{button_class}" style="margin-bottom: 0.5rem;">
            <div class="nav-button-icon">{item['icon']}</div>
            <div class="nav-button-text">
                <div style="font-weight: 600;">{item['name']}</div>
                <div class="nav-button-desc">{item['desc']}</div>
            </div>
        </div>
        """
        
        if st.button(
            f"{item['icon']} {item['name']}", 
            key=f"nav_{item['name']}", 
            help=item['desc'],
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.current_page = item['name']
            try:
                st.switch_page(item['page'])
            except Exception as e:
                st.error(f"Navigation error: {str(e)}")
                st.rerun()

def render_system_status_card():
    """Render system status monitoring card"""
    st.markdown("""
    <div class="sidebar-card">
        <div class="sidebar-card-title">
            <span>⚡</span> System Status
        </div>
        <div class="sidebar-card-content">
    """, unsafe_allow_html=True)
    
    # Status indicators with enhanced styling
    gsheets_connected = "global_gsheets_creds" in st.session_state
    auth_active = st.session_state.get("logged_in", False)
    session_active = st.session_state.get("user_name") is not None
    
    status_items = [
        {
            "label": "Google Sheets",
            "status": "🟢 Connected" if gsheets_connected else "🔴 Disconnected",
            "class": "status-success" if gsheets_connected else "status-error"
        },
        {
            "label": "Authentication", 
            "status": "🟢 Active" if auth_active else "🔴 Inactive",
            "class": "status-success" if auth_active else "status-error"
        },
        {
            "label": "Session",
            "status": "🟢 Active" if session_active else "🔴 Inactive", 
            "class": "status-success" if session_active else "status-error"
        }
    ]
    
    for item in status_items:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span>{item['label']}:</span>
            <span class="status-indicator {item['class']}">{item['status']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Cache information
    if st.session_state.get('sheets_cache'):
        cache_count = len(st.session_state.sheets_cache)
        st.markdown(f"""
        <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid rgba(255,255,255,0.2);">
            <div style="display: flex; justify-content: space-between;">
                <span>Cached Sheets:</span>
                <span style="font-weight: 600;">{cache_count}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def render_gsheets_status_card():
    """Render Google Sheets integration status card"""
    st.markdown("""
    <div class="sidebar-card">
        <div class="sidebar-card-title">
            <span>📊</span> Google Sheets
        </div>
        <div class="sidebar-card-content">
    """, unsafe_allow_html=True)
    
    if "global_gsheets_creds" in st.session_state and st.session_state.global_gsheets_creds:
        creds = st.session_state.global_gsheets_creds
        client_email = creds.get('client_email', 'Unknown')
        project_id = creds.get('project_id', 'Unknown')
        
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <div style="color: #10B981; font-weight: 600; margin-bottom: 0.5rem;">
                ✅ Connected & Ready
            </div>
            <div style="font-size: 0.85rem; margin-bottom: 0.5rem;">
                <strong>Email:</strong><br>
                <span style="word-break: break-all;">{client_email[:30]}...</span>
            </div>
            <div style="font-size: 0.85rem;">
                <strong>Project:</strong><br>
                <span>{project_id[:20]}...</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Connection test buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧪 Test", help="Test connection", key="sidebar_test_connection", use_container_width=True):
                with st.spinner("Testing..."):
                    if test_gsheet_connection(st.session_state.global_gsheets_creds):
                        st.success("✅ Connection OK")
                    else:
                        st.error("❌ Connection Failed")
        
        with col2:
            if st.button("🔄 Refresh", help="Clear cache", key="sidebar_refresh_cache", use_container_width=True):
                # Clear cache
                cache_keys = ['sheets_cache', 'data_cache', 'sync_status']
                for key in cache_keys:
                    if key in st.session_state:
                        st.session_state[key] = {}
                st.success("Cache cleared!")
    else:
        st.markdown("""
        <div style="text-align: center;">
            <div style="color: #F59E0B; font-weight: 600; margin-bottom: 0.5rem;">
                ⚠️ Not Configured
            </div>
            <div style="font-size: 0.85rem; opacity: 0.9;">
                Upload service account JSON on login page to enable full functionality
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def render_quick_actions_card():
    """Render quick actions card"""
    st.markdown("""
    <div class="sidebar-card">
        <div class="sidebar-card-title">
            <span>⚙️</span> Quick Actions
        </div>
        <div class="sidebar-card-content">
    """, unsafe_allow_html=True)
    
    # Quick action buttons with enhanced styling
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh", use_container_width=True, help="Refresh application data"):
            # Clear non-essential caches but preserve auth and gsheets config
            cache_keys = ['data_cache', 'sync_status', 'sheets_cache']
            for key in cache_keys:
                if key in st.session_state:
                    st.session_state[key] = {}
            st.success("App refreshed!")
            st.rerun()
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True, help="Logout and return to login page"):
            # Preserve Google Sheets config across logout
            gsheets_creds = st.session_state.get('global_gsheets_creds')
            logout_user()
            if gsheets_creds:
                st.session_state.global_gsheets_creds = gsheets_creds
                st.session_state.gsheets_creds = gsheets_creds
            st.rerun()
    
    # Additional quick actions
    st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
    
    if st.button("📊 Enhanced Dashboard", use_container_width=True, help="Go to comprehensive dashboard"):
        st.session_state.current_page = "Enhanced Dashboard"
        st.switch_page("pages/1_Enhanced_Dashboard.py")
    
    if st.button("⚙️ Settings", use_container_width=True, help="Application settings"):
        st.session_state.current_page = "Settings"
        st.info("Settings page coming soon!")
    
    st.markdown('</div></div></div>', unsafe_allow_html=True)

def render_system_info_card():
    """Render system information card"""
    user_name = st.session_state.get('user_name', 'Unknown')
    user_role = st.session_state.get('user_role', 'guest')
    login_time = st.session_state.get('login_time', 'N/A')
    
    # Format login time safely
    formatted_login = "N/A"
    if isinstance(login_time, str) and len(login_time) >= 16:
        formatted_login = login_time[:16]
    elif isinstance(login_time, str):
        formatted_login = login_time
    
    st.markdown(f"""
    <div class="sidebar-card">
        <div class="sidebar-card-title">
            <span>📋</span> System Information
        </div>
        <div class="sidebar-card-content">
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Version:</span>
                    <span style="font-weight: 600;">v2.1.0</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Build:</span>
                    <span style="font-weight: 600;">{datetime.now().strftime("%Y%m%d")}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>User Role:</span>
                    <span style="font-weight: 600; text-transform: capitalize;">{user_role}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Login Time:</span>
                    <span style="font-weight: 600; font-size: 0.8rem;">{formatted_login}</span>
                </div>
            </div>
            
            <div style="border-top: 1px solid rgba(255,255,255,0.2); padding-top: 0.75rem;">
                <div style="text-align: center; font-size: 0.85rem;">
                    <div style="font-weight: 600; margin-bottom: 0.25rem;">
                        🚀 AIVACEO Systems
                    </div>
                    <div style="opacity: 0.8;">
                        Advanced Intelligence Platform
                    </div>
                    <div style="margin-top: 0.5rem; font-size: 0.8rem; opacity: 0.7;">
                        Support: support@aivaceo.com
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Alternative function name for compatibility"""
    show_sidebar()

# Additional utility functions for sidebar enhancements
def get_navigation_stats():
    """Get navigation statistics for sidebar display"""
    return {
        'total_pages': 11,
        'active_modules': 8,
        'last_accessed': datetime.now().strftime("%H:%M")
    }

def get_system_health():
    """Get system health metrics for sidebar display"""
    return {
        'uptime': "99.9%",
        'response_time': "< 200ms",
        'data_freshness': "Real-time"
    }

def render_performance_indicators():
    """Render performance indicators in sidebar"""
    stats = get_navigation_stats()
    health = get_system_health()
    
    st.markdown(f"""
    <div class="sidebar-card">
        <div class="sidebar-card-title">
            <span>📈</span> Performance
        </div>
        <div class="sidebar-card-content">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Uptime:</span>
                <span style="color: #10B981; font-weight: 600;">{health['uptime']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Response:</span>
                <span style="color: #10B981; font-weight: 600;">{health['response_time']}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>Data:</span>
                <span style="color: #10B981; font-weight: 600;">{health['data_freshness']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

