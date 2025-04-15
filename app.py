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
    page_title="Self-Care School Dashboard",
    page_icon="🧘‍♀️",
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

# Self Care School brand colors
# Main palette based on the website
# Primary: Soft teal (#6BBFAE)
# Secondary: Light blue (#A4C3DE)
# Accent: Soft purple (#B9A6CD)
# Neutral: Soft gray (#F0F2F5)
# Text: Dark blue-gray (#334c5e)

# Add CSS for styling to match website aesthetic
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #334c5e;
        margin-bottom: 0px;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #334c5e;
        margin-top: 20px;
        margin-bottom: 10px;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .metric-card {
        background-color: #F0F2F5;
        padding: 15px;
        border-radius: 10px;
        margin: 5px;
        text-align: center;
        border: 1px solid rgba(106, 191, 174, 0.2);
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #334c5e;
    }
    .metric-label {
        font-size: 1rem;
        color: #6BBFAE;
        font-weight: 500;
    }
    .status-achieved {
        background-color: rgba(106, 191, 174, 0.2);
        color: #3b8177;
        padding: 4px 8px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .status-behind {
        background-color: rgba(164, 195, 222, 0.2);
        color: #5882a9;
        padding: 4px 8px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .status-at-risk {
        background-color: rgba(185, 166, 205, 0.2);
        color: #7e6a91;
        padding: 4px 8px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .insight-container {
        background-color: #F0F2F5;
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
        border: 1px solid rgba(106, 191, 174, 0.2);
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
        font-family: 'Helvetica Neue', sans-serif;
        color: #334c5e;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(106, 191, 174, 0.2);
        color: #334c5e;
    }
    .stButton>button {
        background-color: #6BBFAE;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #5aa99a;
    }
    div[data-testid="stForm"] {
        border: 1px solid rgba(106, 191, 174, 0.3);
        border-radius: 10px;
        padding: 20px;
        background-color: #F0F2F5;
    }
    div.row-widget.stRadio > div {
        display: flex;
        flex-direction: row;
    }
    div.row-widget.stRadio > div[role="radiogroup"] > label {
        margin-right: 15px;
        padding: 5px 10px;
        border: 1px solid rgba(106, 191, 174, 0.3);
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        border: 1px solid rgba(106, 191, 174, 0.3);
    }
    .stNumberInput>div>div>input {
        border-radius: 5px;
        border: 1px solid rgba(106, 191, 174, 0.3);
    }
    .stDateInput>div>div>input {
        border-radius: 5px;
        border: 1px solid rgba(106, 191, 174, 0.3);
    }
    .stSelectbox>div>div>div {
        border-radius: 5px;
        border: 1px solid rgba(106, 191, 174, 0.3);
    }
    footer {
        visibility: hidden;
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
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📈 Analysis & Recommendations", "✏️ Data Entry"])

with tab1:
    # Dashboard Header
    st.markdown('<p class="main-header">Self-Care School Dashboard</p>', unsafe_allow_html=True)
    st.markdown(f'Latest data as of {data["last_updated"]}')
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
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
        <div class="metric-card metric-card-green">
            <div class="metric-label">Total Contacts</div>
            <div class="metric-value">{data["program_metrics"]["Contacts"]["value"]:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card metric-card-yellow">
            <div class="metric-label">Site Visitors</div>
            <div class="metric-value">{data["traffic_data"]["Visitors"]:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
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
            color_discrete_map={'18-30': '#30BCAA', 'Other Ages': '#5E9FE0'},
            title="Age Demographics (Contacts)"
        )
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(
            font=dict(family="Helvetica Neue, sans-serif", color="#334c5e"),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div style="text-align: center;">
            <p><span style="color: #30BCAA; font-weight: bold;">18-30:</span> {data["age_data"]["18-30"]["value"]} contacts ({data["age_data"]["18-30"]["value"]/(data["age_data"]["18-30"]["value"]+data["age_data"]["Other Ages"]["value"])*100:.1f}%)</p>
            <p><span style="color: #5E9FE0; font-weight: bold;">Other Ages:</span> {data["age_data"]["Other Ages"]["value"]} contacts ({data["age_data"]["Other Ages"]["value"]/(data["age_data"]["18-30"]["value"]+data["age_data"]["Other Ages"]["value"])*100:.1f}%)</p>
            <p style="font-weight: bold; margin-top: 10px;">KPI Target: 50% ages 18-30</p>
        </div>
        """, unsafe_allow_html=True)Other Ages"]["value"])*100:.1f}%)</p>
            <p><span style="color: #5E9FE0; font-weight: bold;">Other Ages:</span> {data["age_data"]["Other Ages"]["value"]} contacts ({data["age_data"]["Other Ages"]["value"]/(data["age_data"]["18-30"]["value"]+data["age_data"]["Other Ages"]["value"])*100:.1f}%)</p>
            <p style="font-weight: bold; margin-top: 10px;">KPI Target: 50% ages 18-30</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Funnel chart
        funnel_data = [
            {'stage': 'Unique User Reach (Ads)', 'value': data["social_data"]["Unique Users Reached"], 'percent': 100},
            {'stage': 'Visitors', 'value': data["traffic_data"]["Visitors"], 'percent': data["traffic_data"]["Visitors"]/data["social_data"]["Unique Users Reached"]*100},
            {'stage': 'Registrants', 'value': data["program_metrics"]["Registrants"]["value"], 'percent': data["program_metrics"]["Registrants"]["value"]/data["traffic_data"]["Visitors"]*100},
            {'stage': 'Downloads', 'value': data["stream_data"]["Downloads"], 'percent': data["stream_data"]["Downloads"]/data["program_metrics"]["Registrants"]["value"]*100},
            {'stage': 'Week 0 Complete', 'value': data["program_metrics"]["Completed Week 0"]["value"], 'percent': data["program_metrics"]["Completed Week 0"]["value"]/data["program_metrics"]["Registrants"]["value"]*100}
        ]
        
        funnel_df = pd.DataFrame(funnel_data)
        
        colors = ['#30BCAA', '#4DAED0', '#5E9FE0', '#A57CD8', '#FF9A4D']
        
        fig = go.Figure(go.Funnel(
            y=funnel_df['stage'],
            x=funnel_df['value'],
            textposition="inside",
            textinfo="value+percent initial",
            marker={"color": colors}
        ))
        
        fig.update_layout(
            title="Program Funnel",
            margin=dict(l=20, r=20, t=60, b=20),
            height=450,
            font=dict(family="Helvetica Neue, sans-serif", color="#334c5e"),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Funnel metrics
        cols = st.columns(5)
        funnel_metrics = [
            {"label": "Unique User Reach", "value": data["social_data"]["Unique Users Reached"], "color": "#30BCAA"},
            {"label": "Visitors", "value": data["traffic_data"]["Visitors"], "color": "#4DAED0"},
            {"label": "Registrants", "value": data["program_metrics"]["Registrants"]["value"], "color": "#5E9FE0"},
            {"label": "Downloads", "value": data["stream_data"]["Downloads"], "color": "#A57CD8"},
            {"label": "Week 0 Complete", "value": data["program_metrics"]["Completed Week 0"]["value"], "color": "#FF9A4D"}
        ]
        
        for i, col in enumerate(cols):
            with col:
                metric = funnel_metrics[i]
                st.markdown(f"""
                <div class="metric-card" style="background-color: {metric['color']}25;">
                    <div class="metric-value" style="color: {metric['color']};">{metric['value']:,}</div>
                    <div class="metric-label">{metric['label']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # SMS and Social Media section
    st.markdown('<p class="sub-header">Marketing Performance</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # SMS Campaign Chart
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
            title='SMS Campaign Performance',
            labels={'value': 'Count', 'variable': 'Type'},
            color_discrete_map={'Delivered': '#30BCAA', 'Clicked': '#5E9FE0'}
        )
        
        fig.add_annotation(
            x=0, y=sms_df['Delivered'][0]*1.05,
            text=f"{data['sms_data']['Week 1 Reminder']['rate']}% click rate",
            showarrow=False
        )
        
        fig.add_annotation(
            x=1, y=sms_df['Delivered'][1]*1.05,
            text=f"{data['sms_data']['Technical Issue']['rate']}% click rate",
            showarrow=False
        )
        
        fig.update_layout(
            font=dict(family="Helvetica Neue, sans-serif", color="#334c5e"),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Social Media Marketing metrics
        st.subheader("Social Media Marketing")
        cols = st.columns(2)
        
        social_metrics = [
            {"label": "Clicks to Site", "value": data["social_data"]["Clicks to Site"], "bg": "rgba(48, 188, 170, 0.1)", "text": "#333333"},
            {"label": "Unique Users Reached", "value": data["social_data"]["Unique Users Reached"], "bg": "rgba(94, 159, 224, 0.1)", "text": "#333333"},
            {"label": "Impressions Delivered", "value": data["social_data"]["Impressions Delivered"], "bg": "rgba(165, 124, 216, 0.1)", "text": "#333333"},
            {"label": "Direct Engagements", "value": data["social_data"]["Direct Engagements"], "bg": "rgba(255, 154, 77, 0.1)", "text": "#333333"}
        ]
        
        for i, metric in enumerate(social_metrics):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="metric-card" style="background-color: {metric['bg']};">
                    <div class="metric-label" style="color: {metric['text']};">{metric['label']}</div>
                    <div class="metric-value" style="color: {metric['text']};">{metric['value']:,}</div>
                    {f"<div>{data['social_data']['Direct Engagements']/data['social_data']['Impressions Delivered']*100:.1f}% engagement rate</div>" if metric['label'] == 'Direct Engagements' else ""}
                </div>
                """, unsafe_allow_html=True)
    
    # Website Analytics
    st.markdown('<p class="sub-header">Website Analytics</p>', unsafe_allow_html=True)
    cols = st.columns(3)
    
    web_metrics = [
        {"label": "Pageviews", "value": data["traffic_data"]["Pageviews"], "bg": "rgba(48, 188, 170, 0.1)", "text": "#333333"},
        {"label": "Sessions", "value": data["traffic_data"]["Sessions"], "bg": "rgba(94, 159, 224, 0.1)", "text": "#333333"},
        {"label": "Visitors", "value": data["traffic_data"]["Visitors"], "bg": "rgba(165, 124, 216, 0.1)", "text": "#333333"}
    ]
    
    for i, col in enumerate(cols):
        with col:
            metric = web_metrics[i]
            st.markdown(f"""
            <div class="metric-card" style="background-color: {metric['bg']};">
                <div class="metric-label" style="color: {metric['text']};">{metric['label']}</div>
                <div class="metric-value" style="color: {metric['text']};">{metric['value']:,}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="margin-top: 10px;">
        <p><span style="font-weight: bold;">Pages per Session:</span> {data["traffic_data"]["Pageviews"]/data["traffic_data"]["Sessions"]:.1f}</p>
        <p><span style="font-weight: bold;">Sessions per Visitor:</span> {data["traffic_data"]["Sessions"]/data["traffic_data"]["Visitors"]:.1f}</p>
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
    
    # Priority 2
    st.markdown('<p class="sub-header">Priority 2: Completion Rate Improvement</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-container">
        <ul>
            <li><span style="font-weight: bold;">Onboarding Optimization:</span> Redesign the first-time user experience to increase immediate engagement.</li>
            <li><span style="font-weight: bold;">Milestone Recognition:</span> Implement more frequent achievement markers and digital badges.</li>
            <li><span style="font-weight: bold;">Re-engagement Campaign:</span> Launch a targeted campaign for the 5,901 registrants who haven't completed Week 0.</li>
            <li><span style="font-weight: bold;">Peer Accountability:</span> Create optional "buddy system" during registration to pair participants for mutual support.</li>
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
    
    # KPI Forecast
    st.markdown('<p class="sub-header">KPI Forecast with Recommended Actions</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-container">
        <ul>
            <li><span style="font-weight: bold;">18-30 Enrollment:</span> With dedicated youth campaigns, potential to reach 30-35% by program end (vs. 50% target).</li>
            <li><span style="font-weight: bold;">Week 0 Completion:</span> Re-engagement strategies could bring completion to 40-45% of registrants (4,200-4,700 participants).</li>
            <li><span style="font-weight: bold;">Site Traffic:</span> Optimized ad campaigns could increase visitors by 150-200% over the next 2 months.</li>
            <li><span style="font-weight: bold;">Program Completion:</span> With enhanced engagement strategies, expect 25-30% of starting registrants to complete all 10 weeks.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)R by 3-5%"},
        {"Recommendation": "College Campus Partnerships", "Timeframe": "Medium-term (1-2 months)", "Expected Impact": "High - Targeted access to 18-30 demographic"},
        {"Recommendation": "Milestone Recognition System", "Timeframe": "Medium-term (1-2 months)", "Expected Impact": "Medium - Increases sustained engagement"}
    ])
    
    st.markdown('<div class="chart-container" style="padding: 0;">', unsafe_allow_html=True)
    st.dataframe(timeline_data, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # KPI Forecast
    st.markdown('<p class="sub-header">KPI Forecast with Recommended Actions</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-container">
        <ul>
            <li><span style="font-weight: bold;">18-30 Enrollment:</span> With dedicated youth campaigns, potential to reach 30-35% by program end (vs. 50% target).</li>
            <li><span style="font-weight: bold;">Week 0 Completion:</span> Re-engagement strategies could bring completion to 40-45% of registrants (4,200-4,700 participants).</li>
            <li><span style="font-weight: bold;">Site Traffic:</span> Optimized ad campaigns could increase visitors by 150-200% over the next 2 months.</li>
            <li><span style="font-weight: bold;">Program Completion:</span> With enhanced engagement strategies, expect 25-30% of starting registrants to complete all 10 weeks.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)R by 3-5%"},
        {"Recommendation": "College Campus Partnerships", "Timeframe": "Medium-term (1-2 months)", "Expected Impact": "High - Targeted access to 18-30 demographic"},
        {"Recommendation": "Milestone Recognition System", "Timeframe": "Medium-term (1-2 months)", "Expected Impact": "Medium - Increases sustained engagement"}
    ])
    
    st.dataframe(timeline_data, use_container_width=True, hide_index=True)
    
    # KPI Forecast
    st.markdown('<p class="sub-header">KPI Forecast with Recommended Actions</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-container">
        <ul>
            <li><span style="font-weight: bold;">18-30 Enrollment:</span> With dedicated youth campaigns, potential to reach 30-35% by program end (vs. 50% target).</li>
            <li><span style="font-weight: bold;">Week 0 Completion:</span> Re-engagement strategies could bring completion to 40-45% of registrants (4,200-4,700 participants).</li>
            <li><span style="font-weight: bold;">Site Traffic:</span> Optimized ad campaigns could increase visitors by 150-200% over the next 2 months.</li>
            <li><span style="font-weight: bold;">Program Completion:</span> With enhanced engagement strategies, expect 25-30% of starting registrants to complete all 10 weeks.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab3:
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
                
                data = save_data(data)
                st.success("Program metrics updated successfully!")
        
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
                
                data = save_data(data)
                st.success("KPI targets updated successfully!")
        
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
                
                data = save_data(data)
                st.success("Traffic data updated successfully!")
        
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
        st.markdown('</div>', unsafe_allow_html=True)"]["Unique Users Reached"]
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
        st.markdown('</div>', unsafe_allow_html=True)"]["Unique Users Reached"]
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
