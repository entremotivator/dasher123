import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from utils.auth import require_auth
from utils.gsheet_manager import get_sheets_manager
from components.data_scanner_ui import DataScannerUI

@require_auth
def main():
    # AIVACEO Header
    st.markdown("""
    <div class="aivaceo-header fade-in">
        <div class="aivaceo-logo">🚀 AIVACEO SYSTEMS</div>
        <div class="aivaceo-tagline">Advanced Intelligence & Virtual Assistant CEO Operations</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.title("📊 Comprehensive Business Intelligence Dashboard")
    st.markdown("**Real-time unified metrics across all business operations** - Powered by AIVACEO Systems")
    
    # Initialize sheets manager
    sheets_manager = get_sheets_manager()
    
    # Check for global credentials
    if not st.session_state.get("global_gsheets_creds"):
        st.error("🔑 Google Sheets credentials not found. Please upload your service account JSON in the sidebar.")
        st.info("💡 Use the sidebar to upload your service account JSON file for full functionality.")
        st.stop()
    
    # Load all data sources with progress indicator
    with st.spinner("🔄 Loading comprehensive business data from all sources..."):
        all_data = load_all_business_data(sheets_manager)
    
    # Quick Navigation Bar
    render_quick_navigation()
    
    # Main dashboard sections
    render_executive_kpis(all_data)
    
    # Tabbed detailed views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Executive Overview", 
        "💰 Financial Analytics", 
        "👥 Customer Intelligence", 
        "📈 Performance Metrics",
        "🔍 Advanced Analytics"
    ])
    
    with tab1:
        render_executive_overview(all_data)
    
    with tab2:
        render_financial_analytics(all_data)
    
    with tab3:
        render_customer_intelligence(all_data)
    
    with tab4:
        render_performance_metrics(all_data)
    
    with tab5:
        render_advanced_analytics(all_data)

def load_all_business_data(sheets_manager):
    """Load comprehensive data from all business modules"""
    data_sources = {
        'customers': {
            'sheet_id': st.session_state.get('customer_sheet_url', ''),
            'worksheet_name': st.session_state.get('customer_worksheet_name', ''),
            'key': 'customers',
            'description': 'Customer Management Data'
        },
        'pricing': {
            'sheet_id': '1WeDpcSNnfCrtx4F3bBC9osigPkzy3LXybRO6jpN7BXE',
            'worksheet_name': '',
            'key': 'pricing',
            'description': 'Service Pricing & Catalog'
        },
        'appointments': {
            'sheet_id': '1mgToY7I10uwPrdPnjAO9gosgoaEKJCf7nv-E0-1UfVQ',
            'worksheet_name': '',
            'key': 'appointments',
            'description': 'Appointment Scheduling'
        },
        'calls': {
            'sheet_id': '1LFfNwb9lRQpIosSEvV3O6zIwymUIWeG9L_k7cxw1jQs',
            'worksheet_name': '',
            'key': 'calls',
            'description': 'Call Center Operations'
        },
        'invoices': {
            'sheet_id': st.session_state.get('invoice_sheet_url', ''),
            'worksheet_name': st.session_state.get('invoice_worksheet_name', ''),
            'key': 'invoices',
            'description': 'Invoice & Billing Data'
        }
    }
    
    # Load data from multiple sheets with detailed status
    loaded_data = {}
    data_status = {}
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, (source_name, config) in enumerate(data_sources.items()):
        progress = (idx + 1) / len(data_sources)
        progress_bar.progress(progress)
        status_text.text(f"Loading {config['description']}...")
        
        if config['sheet_id']:
            try:
                df = sheets_manager.get_sheet_data(
                    sheet_id=config['sheet_id'],
                    worksheet_name=config['worksheet_name'] if config['worksheet_name'] else None,
                    use_cache=True
                )
                if df is not None and not df.empty:
                    loaded_data[source_name] = df
                    data_status[source_name] = {
                        'status': 'success',
                        'records': len(df),
                        'columns': len(df.columns),
                        'message': f"✅ Loaded {len(df):,} records"
                    }
                else:
                    loaded_data[source_name] = create_sample_data(source_name)
                    data_status[source_name] = {
                        'status': 'warning',
                        'records': len(loaded_data[source_name]),
                        'columns': len(loaded_data[source_name].columns),
                        'message': f"⚠️ Using sample data"
                    }
            except Exception as e:
                loaded_data[source_name] = create_sample_data(source_name)
                data_status[source_name] = {
                    'status': 'error',
                    'records': len(loaded_data[source_name]),
                    'columns': len(loaded_data[source_name].columns),
                    'message': f"❌ Error: {str(e)[:50]}..."
                }
        else:
            # Create sample data for demo
            loaded_data[source_name] = create_sample_data(source_name)
            data_status[source_name] = {
                'status': 'demo',
                'records': len(loaded_data[source_name]),
                'columns': len(loaded_data[source_name].columns),
                'message': f"🎯 Demo data loaded"
            }
    
    progress_bar.empty()
    status_text.empty()
    
    # Display data loading status
    st.subheader("📊 Data Source Status")
    cols = st.columns(len(data_sources))
    
    for idx, (source_name, status_info) in enumerate(data_status.items()):
        with cols[idx]:
            status_color = {
                'success': 'success',
                'warning': 'warning', 
                'error': 'error',
                'demo': 'info'
            }.get(status_info['status'], 'info')
            
            st.markdown(f"""
            <div class="metric-card scale-in">
                <div class="metric-card-icon">
                    {'✅' if status_info['status'] == 'success' else 
                     '⚠️' if status_info['status'] == 'warning' else
                     '❌' if status_info['status'] == 'error' else '🎯'}
                </div>
                <div class="metric-card-value">{status_info['records']:,}</div>
                <div class="metric-card-label">{source_name.title()}</div>
                <div class="metric-card-delta neutral">{status_info['columns']} columns</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.session_state.data_status = data_status
    return loaded_data

def create_sample_data(data_type):
    """Create enhanced sample data for demonstration"""
    current_date = datetime.now()
    
    if data_type == 'customers':
        return pd.DataFrame({
            'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson', 
                    'Diana Prince', 'Frank Castle', 'Grace Hopper', 'Henry Ford', 'Ivy League'],
            'Email': ['john@email.com', 'jane@email.com', 'bob@email.com', 'alice@email.com', 'charlie@email.com',
                     'diana@email.com', 'frank@email.com', 'grace@email.com', 'henry@email.com', 'ivy@email.com'],
            'Status': ['Active', 'Active', 'Inactive', 'Active', 'Pending', 'Active', 'Active', 'Inactive', 'Active', 'Pending'],
            'Value': [5000, 7500, 3000, 12000, 4500, 8500, 6200, 2800, 15000, 5800],
            'Date_Added': [(current_date - timedelta(days=x*10)).strftime('%Y-%m-%d') for x in range(10)],
            'Industry': ['Tech', 'Healthcare', 'Finance', 'Retail', 'Manufacturing', 'Education', 'Legal', 'Tech', 'Automotive', 'Consulting']
        })
    elif data_type == 'pricing':
        return pd.DataFrame({
            'Service': ['AI Consulting', 'System Development', 'Technical Support', 'Training & Workshops', 
                       'Security Audit', 'Data Analytics', 'Cloud Migration', 'API Integration'],
            'Price': [250, 350, 150, 200, 500, 300, 400, 275],
            'Category': ['Consulting', 'Development', 'Support', 'Education', 'Security', 'Analytics', 'Infrastructure', 'Integration'],
            'Duration': ['2 hours', '4 hours', '1 hour', '4 hours', '1 day', '3 hours', '2 days', '3 hours'],
            'Popularity': [85, 92, 78, 65, 88, 90, 75, 82]
        })
    elif data_type == 'appointments':
        return pd.DataFrame({
            'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson', 'Diana Prince'],
            'Status': ['Confirmed', 'Pending', 'Completed', 'Cancelled', 'Confirmed', 'Completed'],
            'Start Time (12hr)': ['10:00 AM', '2:00 PM', '11:00 AM', '3:00 PM', '9:00 AM', '4:00 PM'],
            'Date': [(current_date + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(6)],
            'Service': ['AI Consulting', 'System Development', 'Technical Support', 'Training & Workshops', 'Security Audit', 'Data Analytics'],
            'Duration': [120, 240, 60, 240, 480, 180]
        })
    elif data_type == 'calls':
        return pd.DataFrame({
            'customer_name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson', 'Diana Prince'],
            'call_success': ['Yes', 'Yes', 'No', 'Yes', 'Yes', 'No'],
            'call_duration_seconds': [300, 450, 120, 600, 380, 90],
            'sentiment_score': [0.8, 0.6, -0.2, 0.9, 0.7, -0.1],
            'cost': [15.50, 22.75, 6.00, 30.00, 19.00, 4.50],
            'call_date': [(current_date - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(6)],
            'call_type': ['Outbound', 'Inbound', 'Outbound', 'Inbound', 'Outbound', 'Outbound']
        })
    elif data_type == 'invoices':
        return pd.DataFrame({
            'Invoice_ID': ['INV-001', 'INV-002', 'INV-003', 'INV-004', 'INV-005'],
            'Customer': ['John Doe', 'Jane Smith', 'Alice Brown', 'Charlie Wilson', 'Diana Prince'],
            'Amount': [1250, 2100, 750, 1800, 950],
            'Status': ['Paid', 'Pending', 'Paid', 'Overdue', 'Paid'],
            'Date': [(current_date - timedelta(days=x*7)).strftime('%Y-%m-%d') for x in range(5)],
            'Due_Date': [(current_date - timedelta(days=x*7-30)).strftime('%Y-%m-%d') for x in range(5)]
        })
    else:
        return pd.DataFrame()

def render_quick_navigation():
    """Render quick navigation bar"""
    st.markdown("### ⚡ Quick Navigation")
    
    nav_items = [
        {"name": "Customers", "icon": "👥", "page": "pages/4_Customers.py", "color": "#4A90E2"},
        {"name": "Calendar", "icon": "📅", "page": "pages/2_Calendar.py", "color": "#10B981"},
        {"name": "Invoices", "icon": "📄", "page": "pages/3_Invoices.py", "color": "#F59E0B"},
        {"name": "Pricing", "icon": "💰", "page": "pages/6_Pricing.py", "color": "#8B5CF6"},
        {"name": "AI Chat", "icon": "🤖", "page": "pages/7_Super_Chat.py", "color": "#EC4899"},
        {"name": "Call Center", "icon": "📞", "page": "pages/9_Call_Center.py", "color": "#F97316"}
    ]
    
    cols = st.columns(len(nav_items))
    
    for idx, item in enumerate(nav_items):
        with cols[idx]:
            if st.button(f"{item['icon']} {item['name']}", key=f"nav_{item['name']}", use_container_width=True):
                st.switch_page(item['page'])

def render_executive_kpis(all_data):
    """Render executive KPI overview"""
    st.markdown("### 📊 Executive KPI Overview")
    
    # Calculate comprehensive KPIs
    customers_df = all_data.get('customers', pd.DataFrame())
    pricing_df = all_data.get('pricing', pd.DataFrame())
    appointments_df = all_data.get('appointments', pd.DataFrame())
    calls_df = all_data.get('calls', pd.DataFrame())
    invoices_df = all_data.get('invoices', pd.DataFrame())
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        # Total Revenue
        total_revenue = 0
        if not customers_df.empty and 'Value' in customers_df.columns:
            total_revenue += pd.to_numeric(customers_df['Value'], errors='coerce').sum()
        if not invoices_df.empty and 'Amount' in invoices_df.columns:
            total_revenue += pd.to_numeric(invoices_df['Amount'], errors='coerce').sum()
        
        st.markdown(f"""
        <div class="metric-card fade-in">
            <div class="metric-card-icon">💰</div>
            <div class="metric-card-value">${total_revenue:,.0f}</div>
            <div class="metric-card-label">Total Revenue</div>
            <div class="metric-card-delta positive">+12.5% vs last month</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Active Customers
        active_customers = 0
        if not customers_df.empty and 'Status' in customers_df.columns:
            active_customers = len(customers_df[customers_df['Status'] == 'Active'])
        
        st.markdown(f"""
        <div class="metric-card fade-in">
            <div class="metric-card-icon">👥</div>
            <div class="metric-card-value">{active_customers}</div>
            <div class="metric-card-label">Active Customers</div>
            <div class="metric-card-delta positive">+{len(customers_df) - active_customers} pending</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Confirmed Appointments
        confirmed_appointments = 0
        if not appointments_df.empty and 'Status' in appointments_df.columns:
            confirmed_appointments = len(appointments_df[appointments_df['Status'] == 'Confirmed'])
        
        st.markdown(f"""
        <div class="metric-card fade-in">
            <div class="metric-card-icon">📅</div>
            <div class="metric-card-value">{confirmed_appointments}</div>
            <div class="metric-card-label">Confirmed Appointments</div>
            <div class="metric-card-delta neutral">{len(appointments_df)} total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Call Success Rate
        success_rate = 0
        if not calls_df.empty and 'call_success' in calls_df.columns:
            total_calls = len(calls_df)
            successful_calls = len(calls_df[calls_df['call_success'] == 'Yes'])
            success_rate = (successful_calls / total_calls * 100) if total_calls > 0 else 0
        
        st.markdown(f"""
        <div class="metric-card fade-in">
            <div class="metric-card-icon">📞</div>
            <div class="metric-card-value">{success_rate:.1f}%</div>
            <div class="metric-card-label">Call Success Rate</div>
            <div class="metric-card-delta positive">{len(calls_df)} total calls</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        # Average Service Price
        avg_price = 0
        if not pricing_df.empty and 'Price' in pricing_df.columns:
            avg_price = pd.to_numeric(pricing_df['Price'], errors='coerce').mean()
        
        st.markdown(f"""
        <div class="metric-card fade-in">
            <div class="metric-card-icon">🛍️</div>
            <div class="metric-card-value">${avg_price:.0f}</div>
            <div class="metric-card-label">Avg Service Price</div>
            <div class="metric-card-delta neutral">{len(pricing_df)} services</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        # Outstanding Invoices
        outstanding = 0
        if not invoices_df.empty and 'Status' in invoices_df.columns:
            outstanding_invoices = invoices_df[invoices_df['Status'].isin(['Pending', 'Overdue'])]
            if not outstanding_invoices.empty and 'Amount' in outstanding_invoices.columns:
                outstanding = pd.to_numeric(outstanding_invoices['Amount'], errors='coerce').sum()
        
        st.markdown(f"""
        <div class="metric-card fade-in">
            <div class="metric-card-icon">📋</div>
            <div class="metric-card-value">${outstanding:,.0f}</div>
            <div class="metric-card-label">Outstanding</div>
            <div class="metric-card-delta warning">{len(invoices_df[invoices_df['Status'] == 'Overdue']) if not invoices_df.empty else 0} overdue</div>
        </div>
        """, unsafe_allow_html=True)

def render_executive_overview(all_data):
    """Render executive overview with comprehensive charts"""
    st.subheader("📊 Executive Business Overview")
    
    customers_df = all_data.get('customers', pd.DataFrame())
    appointments_df = all_data.get('appointments', pd.DataFrame())
    calls_df = all_data.get('calls', pd.DataFrame())
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Customer Status Distribution
        if not customers_df.empty and 'Status' in customers_df.columns:
            status_counts = customers_df['Status'].value_counts()
            fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Customer Status Distribution",
                color_discrete_sequence=['#4A90E2', '#10B981', '#F59E0B', '#EF4444']
            )
            fig.update_layout(
                font=dict(size=12),
                showlegend=True,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No customer status data available")
    
    with col2:
        # Appointment Status Trends
        if not appointments_df.empty and 'Status' in appointments_df.columns:
            status_counts = appointments_df['Status'].value_counts()
            fig = px.bar(
                x=status_counts.index,
                y=status_counts.values,
                title="Appointment Status Overview",
                color=status_counts.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                xaxis_title="Status",
                yaxis_title="Count",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No appointment data available")
    
    # Recent Activity Timeline
    st.subheader("🕐 Recent Business Activity Timeline")
    
    activities = []
    
    # Collect activities from all sources
    if not customers_df.empty and 'Date_Added' in customers_df.columns:
        for _, customer in customers_df.head(5).iterrows():
            activities.append({
                'date': customer.get('Date_Added', ''),
                'activity': f"New customer: {customer.get('Name', 'Unknown')}",
                'type': 'Customer',
                'icon': '👥',
                'value': customer.get('Value', 0)
            })
    
    if not appointments_df.empty and 'Date' in appointments_df.columns:
        for _, appointment in appointments_df.head(5).iterrows():
            activities.append({
                'date': appointment.get('Date', ''),
                'activity': f"Appointment: {appointment.get('Name', 'Unknown')} - {appointment.get('Status', 'Unknown')}",
                'type': 'Appointment',
                'icon': '📅',
                'value': 0
            })
    
    # Sort activities by date
    activities.sort(key=lambda x: x['date'], reverse=True)
    
    # Display activities in a timeline format
    for activity in activities[:10]:
        col1, col2, col3 = st.columns([1, 6, 2])
        with col1:
            st.markdown(f"**{activity['icon']}**")
        with col2:
            st.markdown(f"**{activity['date']}** - {activity['activity']}")
        with col3:
            if activity['value'] > 0:
                st.markdown(f"*${activity['value']:,.0f}*")

def render_financial_analytics(all_data):
    """Render comprehensive financial analytics"""
    st.subheader("💰 Financial Analytics & Insights")
    
    customers_df = all_data.get('customers', pd.DataFrame())
    pricing_df = all_data.get('pricing', pd.DataFrame())
    invoices_df = all_data.get('invoices', pd.DataFrame())
    calls_df = all_data.get('calls', pd.DataFrame())
    
    # Financial KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Total Customer Value
        customer_value = 0
        if not customers_df.empty and 'Value' in customers_df.columns:
            customer_value = pd.to_numeric(customers_df['Value'], errors='coerce').sum()
        st.metric("💎 Customer Portfolio", f"${customer_value:,.2f}")
    
    with col2:
        # Invoice Revenue
        invoice_revenue = 0
        if not invoices_df.empty and 'Amount' in invoices_df.columns:
            paid_invoices = invoices_df[invoices_df['Status'] == 'Paid']
            if not paid_invoices.empty:
                invoice_revenue = pd.to_numeric(paid_invoices['Amount'], errors='coerce').sum()
        st.metric("📄 Invoice Revenue", f"${invoice_revenue:,.2f}")
    
    with col3:
        # Service Portfolio Value
        service_value = 0
        if not pricing_df.empty and 'Price' in pricing_df.columns:
            service_value = pd.to_numeric(pricing_df['Price'], errors='coerce').sum()
        st.metric("🛍️ Service Portfolio", f"${service_value:,.2f}")
    
    with col4:
        # Call Center Costs
        call_costs = 0
        if not calls_df.empty and 'cost' in calls_df.columns:
            call_costs = pd.to_numeric(calls_df['cost'], errors='coerce').sum()
        st.metric("📞 Call Center Costs", f"${call_costs:,.2f}")
    
    # Financial Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by Source
        revenue_sources = {
            'Customer Value': customer_value,
            'Invoice Revenue': invoice_revenue,
            'Service Portfolio': service_value
        }
        
        fig = px.bar(
            x=list(revenue_sources.keys()),
            y=list(revenue_sources.values()),
            title="Revenue by Source",
            color=list(revenue_sources.values()),
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            xaxis_title="Revenue Source",
            yaxis_title="Amount ($)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Customer Value Distribution
        if not customers_df.empty and 'Value' in customers_df.columns:
            customer_values = pd.to_numeric(customers_df['Value'], errors='coerce').dropna()
            fig = px.histogram(
                x=customer_values,
                nbins=15,
                title="Customer Value Distribution",
                color_discrete_sequence=['#4A90E2']
            )
            fig.update_layout(
                xaxis_title="Customer Value ($)",
                yaxis_title="Count",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No customer value data available")

def render_customer_intelligence(all_data):
    """Render customer intelligence and insights"""
    st.subheader("👥 Customer Intelligence & Insights")
    
    customers_df = all_data.get('customers', pd.DataFrame())
    appointments_df = all_data.get('appointments', pd.DataFrame())
    calls_df = all_data.get('calls', pd.DataFrame())
    
    if customers_df.empty:
        st.warning("No customer data available for analysis")
        return
    
    # Customer Analytics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Customer Segmentation by Value
        if 'Value' in customers_df.columns:
            customer_values = pd.to_numeric(customers_df['Value'], errors='coerce').dropna()
            high_value = len(customer_values[customer_values > customer_values.quantile(0.8)])
            medium_value = len(customer_values[(customer_values >= customer_values.quantile(0.4)) & 
                                             (customer_values <= customer_values.quantile(0.8))])
            low_value = len(customer_values[customer_values < customer_values.quantile(0.4)])
            
            segments = ['High Value', 'Medium Value', 'Low Value']
            counts = [high_value, medium_value, low_value]
            
            fig = px.pie(
                values=counts,
                names=segments,
                title="Customer Value Segmentation",
                color_discrete_sequence=['#10B981', '#F59E0B', '#EF4444']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Industry Distribution
        if 'Industry' in customers_df.columns:
            industry_counts = customers_df['Industry'].value_counts()
            fig = px.bar(
                x=industry_counts.values,
                y=industry_counts.index,
                orientation='h',
                title="Customers by Industry",
                color_discrete_sequence=['#4A90E2']
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No industry data available")
    
    with col3:
        # Customer Status Trends
        if 'Status' in customers_df.columns:
            status_counts = customers_df['Status'].value_counts()
            fig = px.donut(
                values=status_counts.values,
                names=status_counts.index,
                title="Customer Status Overview",
                color_discrete_sequence=['#10B981', '#F59E0B', '#EF4444']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Customer Insights
    st.subheader("💡 Customer Intelligence Insights")
    
    insights = []
    
    if not customers_df.empty:
        total_customers = len(customers_df)
        if 'Status' in customers_df.columns:
            active_customers = len(customers_df[customers_df['Status'] == 'Active'])
            retention_rate = (active_customers / total_customers * 100) if total_customers > 0 else 0
            insights.append(f"📊 Customer retention rate: {retention_rate:.1f}% ({active_customers}/{total_customers})")
        
        if 'Value' in customers_df.columns:
            customer_values = pd.to_numeric(customers_df['Value'], errors='coerce').dropna()
            if len(customer_values) > 0:
                avg_value = customer_values.mean()
                top_customer_value = customer_values.max()
                insights.append(f"💰 Average customer value: ${avg_value:,.2f}")
                insights.append(f"🏆 Highest value customer: ${top_customer_value:,.2f}")
    
    for insight in insights:
        st.info(insight)

def render_performance_metrics(all_data):
    """Render comprehensive performance metrics"""
    st.subheader("📈 Performance Metrics & Analytics")
    
    calls_df = all_data.get('calls', pd.DataFrame())
    appointments_df = all_data.get('appointments', pd.DataFrame())
    pricing_df = all_data.get('pricing', pd.DataFrame())
    
    # Performance KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Call Performance
        if not calls_df.empty and 'call_success' in calls_df.columns:
            success_rate = len(calls_df[calls_df['call_success'] == 'Yes']) / len(calls_df) * 100
            st.metric("📞 Call Success Rate", f"{success_rate:.1f}%")
        else:
            st.metric("📞 Call Success Rate", "No data")
    
    with col2:
        # Appointment Efficiency
        if not appointments_df.empty and 'Status' in appointments_df.columns:
            confirmed_rate = len(appointments_df[appointments_df['Status'] == 'Confirmed']) / len(appointments_df) * 100
            st.metric("📅 Confirmation Rate", f"{confirmed_rate:.1f}%")
        else:
            st.metric("📅 Confirmation Rate", "No data")
    
    with col3:
        # Service Popularity
        if not pricing_df.empty and 'Popularity' in pricing_df.columns:
            avg_popularity = pd.to_numeric(pricing_df['Popularity'], errors='coerce').mean()
            st.metric("🛍️ Avg Service Rating", f"{avg_popularity:.1f}/100")
        else:
            st.metric("🛍️ Avg Service Rating", "No data")
    
    with col4:
        # Customer Sentiment
        if not calls_df.empty and 'sentiment_score' in calls_df.columns:
            avg_sentiment = pd.to_numeric(calls_df['sentiment_score'], errors='coerce').mean()
            st.metric("😊 Avg Sentiment", f"{avg_sentiment:.2f}")
        else:
            st.metric("😊 Avg Sentiment", "No data")
    
    # Performance Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Call Duration Analysis
        if not calls_df.empty and 'call_duration_seconds' in calls_df.columns:
            durations = pd.to_numeric(calls_df['call_duration_seconds'], errors='coerce').dropna()
            duration_minutes = durations / 60
            
            fig = px.histogram(
                x=duration_minutes,
                nbins=15,
                title="Call Duration Distribution (Minutes)",
                color_discrete_sequence=['#4A90E2']
            )
            fig.update_layout(
                xaxis_title="Duration (Minutes)",
                yaxis_title="Count",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No call duration data available")
    
    with col2:
        # Service Performance
        if not pricing_df.empty and 'Popularity' in pricing_df.columns and 'Service' in pricing_df.columns:
            fig = px.bar(
                pricing_df,
                x='Service',
                y='Popularity',
                title="Service Popularity Ratings",
                color='Popularity',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(
                xaxis_title="Service",
                yaxis_title="Popularity Score",
                height=400
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No service popularity data available")

def render_advanced_analytics(all_data):
    """Render advanced analytics and data scanner"""
    st.subheader("🔍 Advanced Analytics & Data Intelligence")
    
    # Data Scanner Integration
    st.markdown("#### 📊 Comprehensive Data Analysis")
    
    available_data = {k: v for k, v in all_data.items() if not v.empty}
    
    if available_data:
        selected_source = st.selectbox(
            "Select data source for advanced analysis",
            list(available_data.keys()),
            format_func=lambda x: f"{x.title()} ({len(available_data[x])} records)"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Launch Advanced Scanner", type="primary", use_container_width=True):
                st.session_state.scanner_data = available_data[selected_source]
                st.session_state.show_scanner = True
        
        with col2:
            if st.button("📊 Generate Report", use_container_width=True):
                st.info("Report generation feature coming soon!")
        
        # Show scanner if requested
        if st.session_state.get('show_scanner', False) and 'scanner_data' in st.session_state:
            st.markdown("---")
            st.subheader(f"🔍 Advanced Data Scanner - {selected_source.title()}")
            
            try:
                scanner_ui = DataScannerUI(st.session_state.scanner_data)
                scanner_ui.render_main_interface()
            except Exception as e:
                st.error(f"Scanner error: {str(e)}")
            
            if st.button("❌ Close Scanner"):
                st.session_state.show_scanner = False
                if 'scanner_data' in st.session_state:
                    del st.session_state.scanner_data
                st.rerun()
    else:
        st.warning("No data sources available for advanced analysis")
    
    # System Health Dashboard
    st.markdown("#### 🔧 System Health & Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Data Quality Score
        total_records = sum(len(df) for df in all_data.values() if not df.empty)
        data_sources_active = len([df for df in all_data.values() if not df.empty])
        quality_score = (data_sources_active / 5) * 100
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-icon">📊</div>
            <div class="metric-card-value">{quality_score:.0f}%</div>
            <div class="metric-card-label">Data Quality Score</div>
            <div class="metric-card-delta neutral">{total_records:,} total records</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # System Status
        if st.session_state.get("global_gsheets_creds"):
            status = "🟢 Connected"
            status_class = "positive"
        else:
            status = "🔴 Disconnected"
            status_class = "negative"
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-icon">🔗</div>
            <div class="metric-card-value">{data_sources_active}/5</div>
            <div class="metric-card-label">Data Sources</div>
            <div class="metric-card-delta {status_class}">{status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Cache Status
        cache_info = get_sheets_manager().get_cache_info() if st.session_state.get("global_gsheets_creds") else {'cached_sheets': 0}
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-icon">📦</div>
            <div class="metric-card-value">{cache_info.get('cached_sheets', 0)}</div>
            <div class="metric-card-label">Cached Sheets</div>
            <div class="metric-card-delta neutral">Ready for analysis</div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

