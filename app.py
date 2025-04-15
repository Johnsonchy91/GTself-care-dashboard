import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="Self-Care School Dashboard",
    page_icon="🏃‍♀️",
    layout="wide"
)

# Add CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #3730a3;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #4338ca;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .metric-card {
        background-color: #f3f4f6;
        padding: 15px;
        border-radius: 10px;
        margin: 5px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 1rem;
        color: #4b5563;
    }
    .status-achieved {
        background-color: #d1fae5;
        color: #065f46;
        padding: 4px 8px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .status-behind {
        background-color: #fef3c7;
        color: #92400e;
        padding: 4px 8px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .status-at-risk {
        background-color: #fee2e2;
        color: #b91c1c;
        padding: 4px 8px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .insight-container {
        background-color: #f9fafb;
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
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
    }
    .stTabs [aria-selected="true"] {
        background-color: #e0e7ff;
        color: #4338ca;
    }
</style>
""", unsafe_allow_html=True)

# Initialize data
# Program Metrics Data
program_metrics = {
    'Registrants': {'value': 10595, 'target': 10000, 'color': '#8884d8'},
    'Contacts': {'value': 3938, 'target': None, 'color': '#82ca9d'},
    'NEW Contacts': {'value': 229, 'target': None, 'color': '#ffc658'},
    'Completed Week 0': {'value': 1983, 'target': None, 'color': '#ff8042'}
}

# Age Demographics
age_data = {
    '18-30': {'value': 229, 'color': '#0088FE'},
    'Other Ages': {'value': 3709, 'color': '#00C49F'}
}

# SMS Campaign Data
sms_data = {
    'Week 1 Reminder': {'delivered': 82337, 'clicked': 7285, 'rate': 9},
    'Technical Issue': {'delivered': 82144, 'clicked': 8152, 'rate': 9.9}
}

# Website Traffic Data
traffic_data = {
    'Visitors': 16300,
    'Sessions': 24500,
    'Pageviews': 45500
}

# Download Data
stream_data = {
    'Downloads': 4694,
    'Target': 10000
}

# Social Media & Marketing Data
social_data = {
    'Clicks to Site': 25700,
    'Unique Users Reached': 101900,
    'Impressions Delivered': 205100,
    'Direct Engagements': 2000
}

# KPI Progress Data
kpi_progress = {
    'Enrollment': {'current': 10595, 'target': 10000, 'percentage': 106, 'status': 'Achieved'},
    '18-30 Enrollment': {'current': 229, 'target': 5000, 'percentage': 5, 'status': 'At Risk'},
    'Week 0 Completion': {'current': 1983, 'target': 10000, 'percentage': 20, 'status': 'Behind'},
    'Site Traffic': {'current': 16300, 'target': 250000, 'percentage': 7, 'status': 'Behind'}
}

# Create tabs
tab1, tab2 = st.tabs(["📊 Dashboard", "📈 Analysis & Recommendations"])

with tab1:
    # Dashboard Header
    st.markdown('<p class="main-header">Self-Care School Dashboard</p>', unsafe_allow_html=True)
    st.markdown('Latest data as of April 15, 2025')
    
    # Top metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card" style="background-color: #e0e7ff;">
            <div class="metric-label">Registrants</div>
            <div class="metric-value">{:,}</div>
            <div>Target: {:,}</div>
        </div>
        """.format(program_metrics['Registrants']['value'], program_metrics['Registrants']['target']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card" style="background-color: #fef3c7;">
            <div class="metric-label">Visitors</div>
            <div class="metric-value">{:,}</div>
        </div>
        """.format(traffic_data['Visitors']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card" style="background-color: #ffedd5;">
            <div class="metric-label">Week 0 Completed</div>
            <div class="metric-value">{:,}</div>
            <div>{:.1f}% of registrants</div>
        </div>
        """.format(program_metrics['Completed Week 0']['value'], 
                  program_metrics['Completed Week 0']['value'] / program_metrics['Registrants']['value'] * 100), 
                  unsafe_allow_html=True)
    
    # KPI Progress & Analysis
    st.markdown('<p class="sub-header">KPI Progress & Analysis</p>', unsafe_allow_html=True)
    
    # Create progress bars
    for key, item in kpi_progress.items():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.markdown(f"**{key}**")
        with col2:
            if key == 'Site Traffic':
                progress = traffic_data['Visitors'] / item['target'] * 100
                progress_text = f"{traffic_data['Visitors']:,} / {item['target']:,} ({int(progress)}%)"
            else:
                progress = min(item['percentage'], 100)
                progress_text = f"{item['current']:,} / {item['target']:,} ({item['percentage']}%)"
            
            progress_color = "#10b981" if item['status'] == 'Achieved' else "#f59e0b" if item['status'] == 'Behind' else "#ef4444"
            st.progress(progress/100)
        with col3:
            status_class = f"status-{item['status'].lower().replace(' ', '-')}"
            st.markdown(f"{progress_text} <span class='{status_class}'>{item['status']}</span>", unsafe_allow_html=True)
    
    # Key Insights
    st.markdown("""
    <div class="insight-container">
        <h3>Key Insights:</h3>
        <ul>
            <li style="color: #059669;"><strong>Enrollment target already exceeded (106% of goal)</strong> - <span class="status-achieved">Achieved</span></li>
            <li style="color: #dc2626;"><strong>18-30 demographic severely underrepresented (5% of target)</strong> - <span class="status-at-risk">At Risk</span></li>
            <li style="color: #d97706;"><strong>Program completion rates need improvement (20% of target)</strong> - <span class="status-behind">Behind</span></li>
            <li style="color: #2563eb;"><strong>Site traffic currently at 7% of target (16.3K vs 250K)</strong> - <span class="status-behind">Behind</span></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Demographics and Funnel section
    st.markdown('<p class="sub-header">Demographics & Program Funnel</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Age Demographics Pie Chart
        age_df = pd.DataFrame({
            'Age Group': list(age_data.keys()),
            'Value': [item['value'] for item in age_data.values()],
            'Color': [item['color'] for item in age_data.values()]
        })
        
        fig = px.pie(
            age_df, 
            values='Value', 
            names='Age Group',
            color='Age Group',
            color_discrete_map={'18-30': '#0088FE', 'Other Ages': '#00C49F'},
            title="Age Demographics (Contacts)"
        )
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div style="text-align: center;">
            <p><span style="color: #0088FE; font-weight: bold;">18-30:</span> {age_data['18-30']['value']} contacts ({age_data['18-30']['value']/(age_data['18-30']['value']+age_data['Other Ages']['value'])*100:.1f}%)</p>
            <p><span style="color: #00C49F; font-weight: bold;">Other Ages:</span> {age_data['Other Ages']['value']} contacts ({age_data['Other Ages']['value']/(age_data['18-30']['value']+age_data['Other Ages']['value'])*100:.1f}%)</p>
            <p style="font-weight: bold; margin-top: 10px;">KPI Target: 50% ages 18-30</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Funnel chart
        funnel_data = [
            {'stage': 'Unique User Reach (Ads)', 'value': social_data['Unique Users Reached'], 'percent': 100},
            {'stage': 'Visitors', 'value': traffic_data['Visitors'], 'percent': traffic_data['Visitors']/social_data['Unique Users Reached']*100},
            {'stage': 'Registrants', 'value': program_metrics['Registrants']['value'], 'percent': program_metrics['Registrants']['value']/traffic_data['Visitors']*100},
            {'stage': 'Downloads', 'value': stream_data['Downloads'], 'percent': stream_data['Downloads']/program_metrics['Registrants']['value']*100},
            {'stage': 'Week 0 Complete', 'value': program_metrics['Completed Week 0']['value'], 'percent': program_metrics['Completed Week 0']['value']/program_metrics['Registrants']['value']*100}
        ]
        
        funnel_df = pd.DataFrame(funnel_data)
        
        colors = ['#9333ea', '#3b82f6', '#4f46e5', '#10b981', '#f59e0b']
        
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
            height=450
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Funnel metrics
        cols = st.columns(5)
        funnel_metrics = [
            {"label": "Unique User Reach", "value": social_data['Unique Users Reached'], "color": "#9333ea"},
            {"label": "Visitors", "value": traffic_data['Visitors'], "color": "#3b82f6"},
            {"label": "Registrants", "value": program_metrics['Registrants']['value'], "color": "#4f46e5"},
            {"label": "Downloads", "value": stream_data['Downloads'], "color": "#10b981"},
            {"label": "Week 0 Complete", "value": program_metrics['Completed Week 0']['value'], "color": "#f59e0b"}
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
            'Campaign': list(sms_data.keys()),
            'Delivered': [item['delivered'] for item in sms_data.values()],
            'Clicked': [item['clicked'] for item in sms_data.values()]
        })
        
        fig = px.bar(
            sms_df, 
            x='Campaign', 
            y=['Delivered', 'Clicked'],
            barmode='group',
            title='SMS Campaign Performance',
            labels={'value': 'Count', 'variable': 'Type'},
            color_discrete_map={'Delivered': '#8884d8', 'Clicked': '#82ca9d'}
        )
        
        fig.add_annotation(
            x=0, y=sms_df['Delivered'][0]*1.05,
            text=f"{sms_data['Week 1 Reminder']['rate']}% click rate",
            showarrow=False
        )
        
        fig.add_annotation(
            x=1, y=sms_df['Delivered'][1]*1.05,
            text=f"{sms_data['Technical Issue']['rate']}% click rate",
            showarrow=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Social Media Marketing metrics
        st.subheader("Social Media Marketing")
        cols = st.columns(2)
        
        social_metrics = [
            {"label": "Clicks to Site", "value": social_data['Clicks to Site'], "bg": "#dbeafe", "text": "#1e40af"},
            {"label": "Unique Users Reached", "value": social_data['Unique Users Reached'], "bg": "#dcfce7", "text": "#166534"},
            {"label": "Impressions Delivered", "value": social_data['Impressions Delivered'], "bg": "#f3e8ff", "text": "#6b21a8"},
            {"label": "Direct Engagements", "value": social_data['Direct Engagements'], "bg": "#fef9c3", "text": "#854d0e"}
        ]
        
        for i, metric in enumerate(social_metrics):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="metric-card" style="background-color: {metric['bg']};">
                    <div class="metric-label" style="color: {metric['text']};">{metric['label']}</div>
                    <div class="metric-value" style="color: {metric['text']};">{metric['value']:,}</div>
                    {f"<div>{social_data['Direct Engagements']/social_data['Impressions Delivered']*100:.1f}% engagement rate</div>" if metric['label'] == 'Direct Engagements' else ""}
                </div>
                """, unsafe_allow_html=True)
    
    # Website Analytics
    st.markdown('<p class="sub-header">Website Analytics</p>', unsafe_allow_html=True)
    cols = st.columns(3)
    
    web_metrics = [
        {"label": "Pageviews", "value": traffic_data['Pageviews'], "bg": "#e0e7ff", "text": "#3730a3"},
        {"label": "Sessions", "value": traffic_data['Sessions'], "bg": "#dbeafe", "text": "#1e40af"},
        {"label": "Visitors", "value": traffic_data['Visitors'], "bg": "#ccfbf1", "text": "#0f766e"}
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
        <p><span style="font-weight: bold;">Pages per Session:</span> {traffic_data['Pageviews']/traffic_data['Sessions']:.1f}</p>
        <p><span style="font-weight: bold;">Sessions per Visitor:</span> {traffic_data['Sessions']/traffic_data['Visitors']:.1f}</p>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    # Analysis & Recommendations
    st.markdown('<p class="main-header">Data Analysis & Key Insights</p>', unsafe_allow_html=True)
    
    # Overall Program Performance
    st.markdown('<p class="sub-header">Overall Program Performance</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-container">
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
    
    st.dataframe(funnel_analysis, use_container_width=True, hide_index=True)
    
    # SMS Campaign Effectiveness
    st.markdown('<p class="sub-header">SMS Campaign Effectiveness</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-container">
        <p>Both SMS campaigns are performing well with click rates of 9.0% and 9.9%, above industry average of 4-5%.</p>
        <p>The "Technical Issue Solve" message performed slightly better, suggesting users respond well to problem-solving content.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Age Demographics Challenge
    st.markdown('<p class="sub-header">Age Demographics Challenge</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-container">
        <p>Only 229 contacts (5.8% of total) are in the 18-30 age bracket, significantly below the 50% target.</p>
        <p>This represents the most critical gap in program KPIs and requires immediate strategic intervention.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Strategic Recommendations
    st.markdown('<p class="main-header">Strategic Recommendations</p>', unsafe_allow_html=True)
    
    # Priority 1
    st.markdown('<p class="sub-header">Priority 1: Youth Engagement Strategy</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-container">
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
    <div class="insight-container">
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
    <div class="insight-container">
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
