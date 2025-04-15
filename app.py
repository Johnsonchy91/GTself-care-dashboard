import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="GirlTREK | Self-Care School Dashboard",
    page_icon="",
    layout="wide"
)

# Set the background to white
st.markdown("""
<style>
    .stApp {
        background-color: white;
    }
    div[data-testid="stHeader"] {
        background-color: white;
        display: none;
    }
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 95%;
    }
    section[data-testid="stSidebar"] {
        display: none;
    }
    div[data-testid="stToolbar"] {
        display: none;
    }
    .css-1dp5vir {
        background-color: white;
    }
    footer {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Self Care School brand colors - based on provided design samples
# Primary: Purple (#5a49a3)
# Secondary: Green (#4fb96e)
# Tertiary: Blue (#5e86d7)
# Yellow: (#f5c759)
# Light Blue: (#e6ecff)
# Light Green: (#e8f7ee)
# Light Yellow: (#fff8e0)
# Light Orange: (#fff2e8)

# Add CSS for styling to match website aesthetic
st.markdown("""
<style>
    .main-header {
        font-size: 2.25rem;
        font-weight: bold;
        color: #5a49a3;
        margin-bottom: 0.5rem;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333333;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    .metric-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        margin: 10px 5px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .metric-card-blue {
        background-color: #e6ecff;
    }
    .metric-card-green {
        background-color: #e8f7ee;
    }
    .metric-card-yellow {
        background-color: #fff8e0;
    }
    .metric-card-orange {
        background-color: #fff2e8;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #333333;
        line-height: 1.2;
        margin: 8px 0;
    }
    .metric-label {
        font-size: 1.1rem;
        color: #333333;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .metric-sublabel {
        font-size: 0.95rem;
        color: #5a49a3;
        font-weight: 500;
    }
    .metric-percentage {
        font-size: 1rem;
        color: #f5883e; /* orange */
        font-weight: 500;
    }
    .status-achieved {
        background-color: #4fb96e;
        color: white;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .status-behind {
        background-color: #f5c759;
        color: #333333;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .status-at-risk {
        background-color: #f27370;
        color: white;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .insight-container {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: #333333;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(90, 73, 163, 0.1);
        color: #5a49a3;
    }
    .stButton>button {
        background-color: #5a49a3;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #483c82;
    }
    div[data-testid="stForm"] {
        border: 1px solid rgba(90, 73, 163, 0.2);
        border-radius: 12px;
        padding: 20px;
        background-color: #FFFFFF;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    div.row-widget.stRadio > div {
        display: flex;
        flex-direction: row;
    }
    div.row-widget.stRadio > div[role="radiogroup"] > label {
        margin-right: 15px;
        padding: 5px 10px;
        border: 1px solid rgba(90, 73, 163, 0.2);
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        border: 1px solid rgba(90, 73, 163, 0.2);
    }
    .stNumberInput>div>div>input {
        border-radius: 5px;
        border: 1px solid rgba(90, 73, 163, 0.2);
    }
    .stDateInput>div>div>input {
        border-radius: 5px;
        border: 1px solid rgba(90, 73, 163, 0.2);
    }
    .stSelectbox>div>div>div {
        border-radius: 5px;
        border: 1px solid rgba(90, 73, 163, 0.2);
    }
    .progress-container {
        margin: 5px 0;
    }
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
    }
    .progress-bar {
        height: 14px;
        border-radius: 7px;
        position: relative;
        background-color: #f0f0f0;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        border-radius: 7px;
    }
    .chart-container {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 10px 0;
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    footer {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Function to load data from a file or initialize default values
def load_data():
    try:
        with open('dashboard_data.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Default data if file doesn't exist or is corrupted
        return {
            'program_metrics': {
                'Registrants': {'value': 10595, 'target': 10000, 'color': '#5a49a3'},
                'Contacts': {'value': 3938, 'target': None, 'color': '#4fb96e'},
                'NEW Contacts': {'value': 229, 'target': None, 'color': '#5e86d7'},
                'Completed Week 0': {'value': 1983, 'target': None, 'color': '#f5c759'}
            },
            'age_data': {
                '18-30': {'value': 229, 'color': '#5e86d7'},
                'Other Ages': {'value': 3709, 'color': '#4fb96e'}
            },
            'sms_data': {
                'Week 1 Reminder': {'delivered': 82337, 'clicked': 7285, 'rate': 9},
                'Technical Issue': {'delivered': 82144, 'clicked': 8152, 'rate': 9.9}
            },
            'traffic_data': {
                'Visitors': 16300,
                'Sessions': 24500,
                'Pageviews': 45500
            },
            'stream_data': {
                'Downloads': 4694,
                'Target': 10000
            },
            'social_data': {
                'Clicks to Site': 25700,
                'Unique Users Reached': 101900,
                'Impressions Delivered': 205100,
                'Direct Engagements': 2000
            },
            'kpi_progress': {
                'Enrollment': {'current': 10595, 'target': 10000, 'percentage': 106, 'status': 'Achieved'},
                '18-30 Enrollment': {'current': 229, 'target': 5000, 'percentage': 5, 'status': 'At Risk'},
                'Week 0 Completion': {'current': 1983, 'target': 10000, 'percentage': 20, 'status': 'Behind'},
                'Site Traffic': {'current': 16300, 'target': 250000, 'percentage': 7, 'status': 'Behind'}
            },
            'last_updated': datetime.now().strftime("%B %d, %Y %H:%M")
        }

# Function to save data
def save_data(data):
    data['last_updated'] = datetime.now().strftime("%B %d, %Y %H:%M")
    with open('dashboard_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    return data

# Initialize data
data = load_data()

# Create tabs
tab1, tab2 = st.tabs(["📊 Dashboard", "✏️ Data Analysis and Data Entry"])

with tab1:
    # Dashboard Header
    st.markdown('<p class="main-header">Self-Care School Dashboard</p>', unsafe_allow_html=True)
    st.markdown(f'Latest data as of {data["last_updated"]}')
    
    # Top metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card metric-card-blue">
            <div class="metric-label">Registrants</div>
            <div class="metric-value">{data["program_metrics"]["Registrants"]["value"]:,}</div>
            <div class="metric-sublabel">Target: {data["program_metrics"]["Registrants"]["target"]:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card metric-card-yellow">
            <div class="metric-label">Site Visitors</div>
            <div class="metric-value">{data["traffic_data"]["Visitors"]:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card metric-card-orange">
            <div class="metric-label">Week 0 Completed</div>
            <div class="metric-value">{data["program_metrics"]["Completed Week 0"]["value"]:,}</div>
            <div class="metric-percentage">{data["program_metrics"]["Completed Week 0"]["value"] / data["program_metrics"]["Registrants"]["value"] * 100:.1f}% of registrants</div>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI Progress & Analysis
    st.markdown('<p class="sub-header">KPI Summary & Analysis</p>', unsafe_allow_html=True)
    
    # Create progress bars
    for key, item in data["kpi_progress"].items():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.markdown(f"**{key}**")
        with col2:
            if key == 'Site Traffic':
                progress = data["traffic_data"]["Visitors"] / item["target"] * 100
                progress_text = f"{data['traffic_data']['Visitors']:,} / {item['target']:,} ({int(progress)}%)"
            else:
                progress = min(item["percentage"], 100)
                progress_text = f"{item['current']:,} / {item['target']:,} ({item['percentage']}%)"
            
            # Use HTML/CSS for better looking progress bars
            progress_color = "#4fb96e" if item["status"] == "Achieved" else "#f5c759" if item["status"] == "Behind" else "#f27370"
            
            st.markdown(f"""
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress}%; background-color: {progress_color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            status_class = f"status-{item['status'].lower().replace(' ', '-')}"
            st.markdown(f"{progress_text} <span class='{status_class}'>{item['status']}</span>", unsafe_allow_html=True)
    
    # Key Insights
    st.markdown("""
    <div class="insight-container">
        <h3>Key Insights:</h3>
        <ul>
            <li style="color: #0A8F80;"><strong>Enrollment target already exceeded (106% of goal)</strong> - <span class="status-achieved">Achieved</span></li>
            <li style="color: #6B43A9;"><strong>18-30 demographic severely underrepresented (5% of target)</strong> - <span class="status-at-risk">At Risk</span></li>
            <li style="color: #2C6DB0;"><strong>Program completion rates need improvement (20% of target)</strong> - <span class="status-behind">Behind</span></li>
            <li style="color: #2C6DB0;"><strong>Site traffic currently at 7% of target (16.3K vs 250K)</strong> - <span class="status-behind">Behind</span></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Demographics and Funnel section
    st.markdown('<p class="sub-header">Demographics & Program Funnel</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Age Demographics Pie Chart
        age_df = pd.DataFrame({
            'Age Group': list(data["age_data"].keys()),
            'Value': [item["value"] for item in data["age_data"].values()],
            'Color': [item["color"] for item in data["age_data"].values()]
        })
        
        fig = px.pie(
            age_df, 
            values='Value', 
            names='Age Group',
            color='Age Group',
            color_discrete_map={'18-30': '#5e86d7', 'Other Ages': '#4fb96e'},
            title="Age Demographics (Contacts)"
        )
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(
            font=dict(family="Helvetica Neue, Arial, sans-serif", color="#333333"),
            paper_bgcolor='white',
            plot_bgcolor='white',
            title_font=dict(size=18, color="#333333", family="Helvetica Neue, Arial, sans-serif"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        
        # Adding the summary text under the pie chart
        total_contacts = data["age_data"]["18-30"]["value"] + data["age_data"]["Other Ages"]["value"]
        pct_18_30 = data["age_data"]["18-30"]["value"] / total_contacts * 100 if total_contacts > 0 else 0
        pct_other = data["age_data"]["Other Ages"]["value"] / total_contacts * 100 if total_contacts > 0 else 0
        
        st.markdown(f"""
        <div style="text-align: center; margin-top: -20px;">
            <p><span style="color: #5e86d7; font-weight: bold;">18-30:</span> {data["age_data"]["18-30"]["value"]} contacts ({pct_18_30:.1f}%)</p>
            <p><span style="color: #4fb96e; font-weight: bold;">Other Ages:</span> {data["age_data"]["Other Ages"]["value"]} contacts ({pct_other:.1f}%)</p>
            <p style="font-weight: bold; margin-top: 10px;">KPI Target: 50% ages 18-30</p>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Funnel chart - simplified to match example
        st.markdown('<div class="chart-container" style="height: 100%; padding: 20px;">', unsafe_allow_html=True)
        st.subheader("Program Funnel")
        
        # Create an improved funnel visualization with site visitors
        funnel_data = [
            {"stage": "Unique User Reach", "value": data["social_data"]["Unique Users Reached"], "color": "#9365e0", "percentage": "100%"},
            {"stage": "Site Visitors", "value": data["traffic_data"]["Visitors"], "color": "#5e86d7", "percentage": f"{data['traffic_data']['Visitors']/data['social_data']['Unique Users Reached']*100:.1f}% of reach"},
            {"stage": "Registrants", "value": data["program_metrics"]["Registrants"]["value"], "color": "#4fb96e", "percentage": f"{data['program_metrics']['Registrants']['value']/data['traffic_data']['Visitors']*100:.1f}% of visitors"},
            {"stage": "Downloads", "value": data["stream_data"]["Downloads"], "color": "#f5c759", "percentage": f"{data['stream_data']['Downloads']/data['program_metrics']['Registrants']['value']*100:.1f}% of registrants"},
            {"stage": "Week 0 Complete", "value": data["program_metrics"]["Completed Week 0"]["value"], "color": "#f5883e", "percentage": f"{data['program_metrics']['Completed Week 0']['value']/data['program_metrics']['Registrants']['value']*100:.1f}% of registrants"}
        ]
        
        # Create funnel with gradient width based on value
        max_value = funnel_data[0]["value"]
        
        for i, item in enumerate(funnel_data):
            # Calculate width percentage based on value
            width_pct = min(100, max(30, item["value"] / max_value * 100))
            margin_left = (100 - width_pct) / 2  # Center the funnel
            
            st.markdown(f"""
            <div style="position: relative; width: 100%; margin-bottom: 5px;">
                <div style="background-color: {item['color']}; color: white; padding: 15px; border-radius: 8px; 
                     margin-left: {margin_left}%; width: {width_pct}%; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="font-size: 1.2rem; font-weight: bold;">{item["value"]:,} {item["stage"]}</div>
                    <div>{item["percentage"]}</div>
                </div>
                {f'<div style="position: absolute; top: 100%; left: 50%; transform: translateX(-50%); width: 0; height: 0; border-left: 15px solid transparent; border-right: 15px solid transparent; border-top: 15px solid {item["color"]}; z-index: 10;"></div>' if i < len(funnel_data)-1 else ''}
            </div>
            <div style="height: 15px;"></div>
            """, unsafe_allow_html=True)
        
        # Simple metrics underneath in a row
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                item = funnel_data[i]
                st.markdown(f"""
                <div style="background-color: {item['color']}15; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid {item['color']}40;">
                    <div style="font-weight: bold; color: {item['color']};">{item["value"]:,}</div>
                    <div style="font-size: 0.8rem;">{item["stage"]}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # SMS and Social Media section
    st.markdown('<p class="sub-header">Marketing Performance</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # SMS Campaign Chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("SMS Campaign Performance")
        
        sms_df = pd.DataFrame({
            'Campaign': list(data["sms_data"].keys()),
            'Delivered': [item["delivered"] for item in data["sms_data"].values()],
            'Clicked': [item["clicked"] for item in data["sms_data"].values()]
        })
        
        fig = px.bar(
            sms_df, 
            x='Campaign', 
            y=['Delivered', 'Clicked'],
            barmode='group',
            labels={'value': 'Count', 'variable': 'Type'},
            color_discrete_map={'Delivered': '#5e86d7', 'Clicked': '#4fb96e'}
        )
        
        # Add click rate annotations
        for i, campaign in enumerate(data["sms_data"].keys()):
            fig.add_annotation(
                x=i,
                y=sms_df['Delivered'][i]*1.05,
                text=f"{data['sms_data'][campaign]['rate']}% click rate",
                showarrow=False,
                font=dict(color="#333333")
            )
        
        fig.update_layout(
            font=dict(family="Helvetica Neue, Arial, sans-serif", color="#333333"),
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(l=40, r=20, t=10, b=40),
            xaxis=dict(title=None),
            yaxis=dict(title=None, gridcolor='#f0f0f0'),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Campaign metrics as text
        st.markdown(f"""
        <div style="margin-top: -20px; text-align: center;">
            <p><span style="font-weight: bold;">Week 1 Reminder:</span> {data['sms_data']['Week 1 Reminder']['rate']}% click rate</p>
            <p><span style="font-weight: bold;">Technical Issue:</span> {data['sms_data']['Technical Issue']['rate']}% click rate</p>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Social Media Marketing metrics
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Marketing Performance")
        
        # Create a 2x2 grid for the metrics
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        
        social_metrics = [
            {"label": "Clicks to Site", "value": data["social_data"]["Clicks to Site"], "bg": "#e6ecff"},
            {"label": "Unique Users", "value": data["social_data"]["Unique Users Reached"], "bg": "#e8f7ee"},
            {"label": "Impressions", "value": data["social_data"]["Impressions Delivered"], "bg": "#fff8e0"},
            {"label": "Engagements", "value": data["social_data"]["Direct Engagements"], "bg": "#fff2e8"}
        ]
        
        cols = [col1, col2, col3, col4]
        
        for i, col in enumerate(cols):
            with col:
                metric = social_metrics[i]
                st.markdown(f"""
                <div style="background-color: {metric['bg']}; padding: 15px; border-radius: 8px; text-align: center; height: 100px; display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-size: 1.5rem; font-weight: bold; color: #333333;">{metric['value']:,}</div>
                    <div style="color: #333333;">{metric['label']}</div>
                    {f"<div style='font-size: 0.8rem; margin-top: 5px;'>{data['social_data']['Direct Engagements']/data['social_data']['Impressions Delivered']*100:.1f}% engagement rate</div>" if metric['label'] == 'Engagements' else ""}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Website Analytics
    st.markdown('<p class="sub-header">Website Analytics</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    web_metrics = [
        {"label": "Pageviews", "value": data["traffic_data"]["Pageviews"], "bg": "#e6ecff"},
        {"label": "Sessions", "value": data["traffic_data"]["Sessions"], "bg": "#e8f7ee"},
        {"label": "Visitors", "value": data["traffic_data"]["Visitors"], "bg": "#fff8e0"}
    ]
    
    cols = [col1, col2, col3]
    
    for i, col in enumerate(cols):
        with col:
            metric = web_metrics[i]
            st.markdown(f"""
            <div class="metric-card" style="background-color: {metric['bg']}; margin: 5px 0;">
                <div class="metric-label">{metric['label']}</div>
                <div class="metric-value">{metric['value']:,}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="margin: 15px 0; padding: 15px; background-color: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <div><span style="font-weight: bold;">Pages per Session:</span> {data["traffic_data"]["Pageviews"]/data["traffic_data"]["Sessions"]:.1f}</div>
            <div><span style="font-weight: bold;">Sessions per Visitor:</span> {data["traffic_data"]["Sessions"]/data["traffic_data"]["Visitors"]:.1f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    # Analysis & Recommendations
    st.markdown('<p class="main-header">Data Analysis & Key Insights</p>', unsafe_allow_html=True)
    
    # Overall Program Performance
    st.markdown('<p class="sub-header">Overall Program Performance</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-container">
        <ul>
            <li><span style="font-weight: bold;">Strong Initial Recruitment:</span> With 10,595 registrants, the program has exceeded its target of 10,000 participants ahead of schedule.</li>
            <li><span style="font-weight: bold;">Concerning Drop-off Rate:</span> Only 18.7% of registrants (1,983) have completed Week 0, indicating significant early attrition.</li>
            <li><span style="font-weight: bold;">Age Demographics Gap:</span> Only 5.8% of contacts fall within the 18-30 age range, far below the 50% target.</li>
            <li><span style="font-weight: bold;">Effective Marketing Reach:</span> 101,900 unique users reached, with 16% visitor conversion (16,300 site visitors).</li>
            <li><span style="font-weight: bold;">Download Engagement:</span> 44.3% of registrants are downloading content, suggesting room for improvement in user activation.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Conversion Funnel Analysis
    st.markdown('<p class="sub-header">Conversion Funnel Analysis</p>', unsafe_allow_html=True)
    
    funnel_analysis = pd.DataFrame([
        {"Funnel Stage": "Unique User Reach (Ads)", "Count": 101900, "Conversion Rate": "-", "Analysis": "Strong top-of-funnel reach with ads"},
        {"Funnel Stage": "Visitors", "Count": 16300, "Conversion Rate": "16.0% of reach", "Analysis": "Below average click-through rate from ads to site"},
        {"Funnel Stage": "Registrants", "Count": 10595, "Conversion Rate": "65.0% of visitors", "Analysis": "Excellent visitor-to-registrant conversion"},
        {"Funnel Stage": "Downloads", "Count": 4694, "Conversion Rate": "44.3% of registrants", "Analysis": "Moderate activation rate"},
        {"Funnel Stage": "Week 0 Complete", "Count": 1983, "Conversion Rate": "18.7% of registrants", "Analysis": "Low completion rate, significant drop-off"}
    ])
    
    st.markdown('<div class="chart-container" style="padding: 0;">', unsafe_allow_html=True)
    st.dataframe(funnel_analysis, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SMS Campaign Effectiveness
    st.markdown('<p class="sub-header">SMS Campaign Effectiveness</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-container">
        <p>Both SMS campaigns are performing well with click rates of 9.0% and 9.9%, above industry average of 4-5%.</p>
        <p>The "Technical Issue Solve" message performed slightly better, suggesting users respond well to problem-solving content.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Age Demographics Challenge
    st.markdown('<p class="sub-header">Age Demographics Challenge</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-container">
        <p>Only 229 contacts (5.8% of total) are in the 18-30 age bracket, significantly below the 50% target.</p>
        <p>This represents the most critical gap in program KPIs and requires immediate strategic intervention.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Strategic Recommendations
    st.markdown('<p class="main-header">Strategic Recommendations</p>', unsafe_allow_html=True)
    
    # Priority 1
    st.markdown('<p class="sub-header">Priority 1: Youth Engagement Strategy</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-container">
        <ul>
            <li><span style="font-weight: bold;">Platform-Specific Campaigns:</span> Shift marketing budget toward platforms with higher 18-30 demographic penetration (TikTok, Instagram Reels).</li>
            <li><span style="font-weight: bold;">Youth Ambassador Program:</span> Recruit current 18-30 participants as program ambassadors with incentives for referrals.</li>
            <li><span style="font-weight: bold;">College Campus Partnerships:</span> Develop targeted partnerships with college wellness programs and student organizations.</li>
            <li><span style="font-weight: bold;">Content Adaptation:</span> Create program variations with themes and activities specifically designed to appeal to younger participants.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Priority 3
    st.markdown('<p class="sub-header">Priority 3: Marketing Funnel Optimization</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-container">
        <ul>
            <li><span style="font-weight: bold;">Ad Creative Testing:</span> Conduct A/B testing on ad creative to improve the 16% click-through rate from ads to site.</li>
            <li><span style="font-weight: bold;">Download Prompts:</span> Add strategic download prompts during registration and in follow-up communications.</li>
            <li><span style="font-weight: bold;">Content Previews:</span> Implement "preview" content on the site to demonstrate value before full download commitment.</li>
            <li><span style="font-weight: bold;">SMS Optimization:</span> Expand SMS campaign usage given the strong 9-10% click rates.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Implementation Timeline
    st.markdown('<p class="sub-header">Implementation Timeline</p>', unsafe_allow_html=True)
    
    timeline_data = pd.DataFrame([
        {"Recommendation": "Youth-targeted ad campaigns (TikTok, Instagram)", "Timeframe": "Immediate (1-2 weeks)", "Expected Impact": "High - Direct impact on 18-30 recruitment"},
        {"Recommendation": "Re-engagement SMS for incomplete registrants", "Timeframe": "Immediate (1 week)", "Expected Impact": "High - Could recover 10-20% of drop-offs"},
        {"Recommendation": "Youth Ambassador Program", "Timeframe": "Short-term (2-4 weeks)", "Expected Impact": "Medium - Builds organic growth in target demographic"},
        {"Recommendation": "Onboarding Optimization", "Timeframe": "Short-term (2-3 weeks)", "Expected Impact": "High - Could improve completion rates by 15-25%"},
        {"Recommendation": "Ad Creative A/B Testing", "Timeframe": "Short-term (2-3 weeks)", "Expected Impact": "Medium - Potential to increase CTR by 3-5%"},
        {"Recommendation": "College Campus Partnerships", "Timeframe": "Medium-term (1-2 months)", "Expected Impact": "High - Targeted access to 18-30 demographic"},
        {"Recommendation": "Milestone Recognition System", "Timeframe": "Medium-term (1-2 months)", "Expected Impact": "Medium - Increases sustained engagement"}
    ])
    
    st.markdown('<div class="chart-container" style="padding: 0;">', unsafe_allow_html=True)
    st.dataframe(timeline_data, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
with tab2:
    # Data Entry Tab
    st.markdown('<p class="main-header">Data Entry & Updates</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-container">
        <p>Use this tab to update the dashboard metrics. Select a data category to update, enter the new values, and save your changes.</p>
        <p><strong>Note:</strong> All updates will be saved to a local file and will persist between sessions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Data category selection
    data_category = st.radio(
        "Select data category to update:",
        ["Program Metrics", "KPI Targets", "Demographics", "Traffic & Website", "SMS Campaigns", "Social Media"]
    )
    
    with st.form(key=f"update_{data_category}"):
        st.markdown(f"<p class='sub-header'>Update {data_category}</p>", unsafe_allow_html=True)
        
        if data_category == "Program Metrics":
            # Program Metrics Form
            col1, col2 = st.columns(2)
            
            with col1:
                registrants = st.number_input(
                    "Total Registrants", 
                    min_value=0, 
                    value=data["program_metrics"]["Registrants"]["value"]
                )
                contacts = st.number_input(
                    "Total Contacts", 
                    min_value=0, 
                    value=data["program_metrics"]["Contacts"]["value"]
                )
            
            with col2:
                new_contacts = st.number_input(
                    "NEW Contacts", 
                    min_value=0, 
                    value=data["program_metrics"]["NEW Contacts"]["value"]
                )
                completed_week0 = st.number_input(
                    "Completed Week 0", 
                    min_value=0, 
                    value=data["program_metrics"]["Completed Week 0"]["value"]
                )
            
            submit_button = st.form_submit_button(label="Update Program Metrics")
            
            if submit_button:
                # Update the data
                data["program_metrics"]["Registrants"]["value"] = registrants
                data["program_metrics"]["Contacts"]["value"] = contacts
                data["program_metrics"]["NEW Contacts"]["value"] = new_contacts
                data["program_metrics"]["Completed Week 0"]["value"] = completed_week0
                
                # Update related KPIs
                data["kpi_progress"]["Enrollment"]["current"] = registrants
                data["kpi_progress"]["Enrollment"]["percentage"] = int(registrants / data["kpi_progress"]["Enrollment"]["target"] * 100)
                data["kpi_progress"]["Week 0 Completion"]["current"] = completed_week0
                data["kpi_progress"]["Week 0 Completion"]["percentage"] = int(completed_week0 / data["kpi_progress"]["Week 0 Completion"]["target"] * 100)
                
                # Update status
                data["kpi_progress"]["Enrollment"]["status"] = "Achieved" if data["kpi_progress"]["Enrollment"]["percentage"] >= 100 else "Behind" if data["kpi_progress"]["Enrollment"]["percentage"] >= 25 else "At Risk"
                data["kpi_progress"]["Week 0 Completion"]["status"] = "Achieved" if data["kpi_progress"]["Week 0 Completion"]["percentage"] >= 100 else "Behind" if data["kpi_progress"]["Week 0 Completion"]["percentage"] >= 25 else "At Risk"
                
        elif data_category == "KPI Targets":
            # KPI Targets Form
            col1, col2 = st.columns(2)
            
            with col1:
                enrollment_target = st.number_input(
                    "Enrollment Target", 
                    min_value=1000, 
                    value=data["kpi_progress"]["Enrollment"]["target"]
                )
                age_target = st.number_input(
                    "18-30 Enrollment Target", 
                    min_value=100, 
                    value=data["kpi_progress"]["18-30 Enrollment"]["target"]
                )
            
            with col2:
                completion_target = st.number_input(
                    "Week 0 Completion Target", 
                    min_value=1000, 
                    value=data["kpi_progress"]["Week 0 Completion"]["target"]
                )
                traffic_target = st.number_input(
                    "Site Traffic Target", 
                    min_value=10000, 
                    value=data["kpi_progress"]["Site Traffic"]["target"]
                )
            
            submit_button = st.form_submit_button(label="Update KPI Targets")
            
            if submit_button:
                # Update the data
                data["kpi_progress"]["Enrollment"]["target"] = enrollment_target
                data["kpi_progress"]["18-30 Enrollment"]["target"] = age_target
                data["kpi_progress"]["Week 0 Completion"]["target"] = completion_target
                data["kpi_progress"]["Site Traffic"]["target"] = traffic_target
                
                # Update percentages
                data["kpi_progress"]["Enrollment"]["percentage"] = int(data["kpi_progress"]["Enrollment"]["current"] / enrollment_target * 100)
                data["kpi_progress"]["18-30 Enrollment"]["percentage"] = int(data["kpi_progress"]["18-30 Enrollment"]["current"] / age_target * 100)
                data["kpi_progress"]["Week 0 Completion"]["percentage"] = int(data["kpi_progress"]["Week 0 Completion"]["current"] / completion_target * 100)
                data["kpi_progress"]["Site Traffic"]["percentage"] = int(data["traffic_data"]["Visitors"] / traffic_target * 100)
                
                # Update status
                for key in data["kpi_progress"]:
                    data["kpi_progress"][key]["status"] = "Achieved" if data["kpi_progress"][key]["percentage"] >= 100 else "Behind" if data["kpi_progress"][key]["percentage"] >= 25 else "At Risk"
                
        elif data_category == "Demographics":
            # Demographics Form
            col1, col2 = st.columns(2)
            
            total_age_contacts = data["age_data"]["18-30"]["value"] + data["age_data"]["Other Ages"]["value"]
            
            with col1:
                age_18_30 = st.number_input(
                    "18-30 Age Demographic", 
                    min_value=0, 
                    value=data["age_data"]["18-30"]["value"]
                )
            
            with col2:
                other_ages = st.number_input(
                    "Other Ages Demographic", 
                    min_value=0, 
                    value=data["age_data"]["Other Ages"]["value"]
                )
            
            submit_button = st.form_submit_button(label="Update Demographics")
            
            if submit_button:
                # Update the data
                data["age_data"]["18-30"]["value"] = age_18_30
                data["age_data"]["Other Ages"]["value"] = other_ages
                
                # Update 18-30 KPI
                data["kpi_progress"]["18-30 Enrollment"]["current"] = age_18_30
                data["kpi_progress"]["18-30 Enrollment"]["percentage"] = int(age_18_30 / data["kpi_progress"]["18-30 Enrollment"]["target"] * 100)
                data["kpi_progress"]["18-30 Enrollment"]["status"] = "Achieved" if data["kpi_progress"]["18-30 Enrollment"]["percentage"] >= 100 else "Behind" if data["kpi_progress"]["18-30 Enrollment"]["percentage"] >= 25 else "At Risk"
                
                data = save_data(data)
                st.success("Demographics updated successfully!")
        
        elif data_category == "Traffic & Website":
            # Traffic & Website Form
            col1, col2 = st.columns(2)
            
            with col1:
                visitors = st.number_input(
                    "Visitors", 
                    min_value=0, 
                    value=data["traffic_data"]["Visitors"]
                )
                sessions = st.number_input(
                    "Sessions", 
                    min_value=0, 
                    value=data["traffic_data"]["Sessions"]
                )
            
            with col2:
                pageviews = st.number_input(
                    "Pageviews", 
                    min_value=0, 
                    value=data["traffic_data"]["Pageviews"]
                )
                downloads = st.number_input(
                    "Downloads", 
                    min_value=0, 
                    value=data["stream_data"]["Downloads"]
                )
            
            submit_button = st.form_submit_button(label="Update Traffic Data")
            
            if submit_button:
                # Update the data
                data["traffic_data"]["Visitors"] = visitors
                data["traffic_data"]["Sessions"] = sessions
                data["traffic_data"]["Pageviews"] = pageviews
                data["stream_data"]["Downloads"] = downloads
                
                # Update Site Traffic KPI
                data["kpi_progress"]["Site Traffic"]["percentage"] = int(visitors / data["kpi_progress"]["Site Traffic"]["target"] * 100)
                data["kpi_progress"]["Site Traffic"]["status"] = "Achieved" if data["kpi_progress"]["Site Traffic"]["percentage"] >= 100 else "Behind" if data["kpi_progress"]["Site Traffic"]["percentage"] >= 25 else "At Risk"
                
        elif data_category == "SMS Campaigns":
            # SMS Campaigns Form
            campaign_name = st.selectbox(
                "SMS Campaign", 
                options=list(data["sms_data"].keys())
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                delivered = st.number_input(
                    "SMS Delivered", 
                    min_value=0, 
                    value=data["sms_data"][campaign_name]["delivered"]
                )
            
            with col2:
                clicked = st.number_input(
                    "SMS Clicked", 
                    min_value=0, 
                    max_value=delivered,
                    value=min(data["sms_data"][campaign_name]["clicked"], delivered)
                )
            
            # Calculate rate
            if delivered > 0:
                rate = round(clicked / delivered * 100, 1)
            else:
                rate = 0
            
            st.markdown(f"""
            <div style="margin: 10px 0; padding: 10px; background-color: #f8f9fa; border-radius: 5px; text-align: center;">
                <p style="margin: 0;"><span style="font-weight: bold;">Click Rate:</span> <span style="color: #5a49a3; font-weight: bold; font-size: 1.2rem;">{rate}%</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            submit_button = st.form_submit_button(label="Update SMS Campaign")
            
            if submit_button:
                # Update the data
                data["sms_data"][campaign_name]["delivered"] = delivered
                data["sms_data"][campaign_name]["clicked"] = clicked
                data["sms_data"][campaign_name]["rate"] = rate
                
                data = save_data(data)
                st.success(f"SMS campaign '{campaign_name}' updated successfully!")
        
        elif data_category == "Social Media":
            # Social Media Form
            col1, col2 = st.columns(2)
            
            with col1:
                clicks = st.number_input(
                    "Clicks to Site", 
                    min_value=0, 
                    value=data["social_data"]["Clicks to Site"]
                )
                users = st.number_input(
                    "Unique Users Reached", 
                    min_value=0, 
                    value=data["social_data"]["Unique Users Reached"]
                )
            
            with col2:
                impressions = st.number_input(
                    "Impressions Delivered", 
                    min_value=0, 
                    value=data["social_data"]["Impressions Delivered"]
                )
                engagements = st.number_input(
                    "Direct Engagements", 
                    min_value=0, 
                    value=data["social_data"]["Direct Engagements"]
                )
            
            submit_button = st.form_submit_button(label="Update Social Media Data")
            
            if submit_button:
                # Update the data
                data["social_data"]["Clicks to Site"] = clicks
                data["social_data"]["Unique Users Reached"] = users
                data["social_data"]["Impressions Delivered"] = impressions
                data["social_data"]["Direct Engagements"] = engagements
                
                data = save_data(data)
                st.success("Social media data updated successfully!")
    
    # Add New Campaign Section
    st.markdown('<p class="sub-header">Add New SMS Campaign</p>', unsafe_allow_html=True)
    
    with st.form(key="add_sms_campaign"):
        st.markdown('<div class="chart-container" style="padding: 15px 0;">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            new_campaign_name = st.text_input("Campaign Name")
        
        with col2:
            new_delivered = st.number_input("SMS Delivered", min_value=0, value=0)
        
        with col3:
            new_clicked = st.number_input(
                "SMS Clicked", 
                min_value=0, 
                max_value=new_delivered,
                value=0
            )
        
        # Calculate rate
        if new_delivered > 0:
            new_rate = round(new_clicked / new_delivered * 100, 1)
        else:
            new_rate = 0
        
        st.markdown(f"""
        <div style="margin: 10px 0; padding: 10px; background-color: #f8f9fa; border-radius: 5px; text-align: center;">
            <p style="margin: 0;"><span style="font-weight: bold;">Projected Click Rate:</span> <span style="color: #5a49a3; font-weight: bold; font-size: 1.2rem;">{new_rate}%</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        submit_button = st.form_submit_button(label="Add New SMS Campaign")
        
        if submit_button:
            if new_campaign_name and new_campaign_name not in data["sms_data"]:
                # Add new campaign
                data["sms_data"][new_campaign_name] = {
                    "delivered": new_delivered,
                    "clicked": new_clicked,
                    "rate": new_rate
                }
                
                data = save_data(data)
                st.success(f"New SMS campaign '{new_campaign_name}' added successfully!")
            elif not new_campaign_name:
                st.error("Please enter a campaign name.")
            else:
                st.error(f"Campaign '{new_campaign_name}' already exists. Please use a unique name.")
        st.markdown('</div>', unsafe_allow_html=True)
