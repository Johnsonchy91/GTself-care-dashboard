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

# Initialize data - UPDATED with new values
# Program Metrics Data
program_metrics = {
    'Registrants': {'value': 11985, 'target': 10000, 'color': '#8884d8'},
    'Contacts': {'value': 4808, 'target': None, 'color': '#82ca9d'},
    'NEW Contacts': {'value': 4808, 'target': None, 'color': '#ffc658'},
    'Completed Week 0': {'value': 3089, 'target': None, 'color': '#ff8042'}
}

# Age Demographics - UPDATED
age_data = {
    '18-25': {'value': 101, 'color': '#0088FE'},
    'Other Ages': {'value': 11884, 'color': '#00C49F'}
}

# SMS Campaign Data
sms_data = {
    'Week 1 Reminder': {'delivered': 82337, 'clicked': 7285, 'rate': 9},
    'Technical Issue': {'delivered': 82144, 'clicked': 8152, 'rate': 9.9}
}

# Website Traffic Data - UPDATED
traffic_data = {
    'Visitors': 29500,
    'Sessions': 55100,
    'Pageviews': 101200,
    'Bounce Rate': 30.3
}

# Download Data - UPDATED
stream_data = {
    'Downloads': 22186,
    'Target': 100000
}

# Social Media & Marketing Data - UPDATED as of April 25, 2025
social_data = {
    'Clicks to Site': 39000,
    'Unique Users Reached': 101900,  # Keeping this the same as no new data was provided
    'Impressions Delivered': 338000,
    'Direct Engagements': 3557,  # Sum of reactions, saves, shares, comments
    'Video Views': 70700,
    'Page Likes': 67,
    'Comments': 74,
    'Shares': 217,
    'Saves': 66,
    'Reactions': 3200
}

# Badges Data - NEW
badges_data = {
    'Week 0': 3089,
    'Week 1': 2061,
    'Week 2': 2197,
    'Total Claimed': 7347,
    'Unique Users': 4788,
    'Target': 5000
}

# Stories Data - NEW
stories_data = {
    'Submitted': 234,
    'Target': 100
}

# KPI Progress Data - UPDATED
kpi_progress = {
    'Enrollment': {'current': 11985, 'target': 10000, 'percentage': 120, 'status': 'Achieved'},
    '18-25 Enrollment': {'current': 101, 'target': 5000, 'percentage': 2, 'status': 'At Risk'},
    'Week 0 Completion': {'current': 3089, 'target': 10000, 'percentage': 31, 'status': 'Behind'},
    'Site Traffic': {'current': 29500, 'target': 250000, 'percentage': 12, 'status': 'Behind'},
    'Downloads': {'current': 22186, 'target': 100000, 'percentage': 22, 'status': 'Behind'},
    'Stories Submitted': {'current': 234, 'target': 100, 'percentage': 234, 'status': 'Achieved'}
}

# Create tabs
tab1, tab2 = st.tabs(["📊 Dashboard", "📈 Analysis & Recommendations"])

with tab1:
    # Dashboard Header
    st.markdown('<p class="main-header">Self-Care School Dashboard</p>', unsafe_allow_html=True)
    st.markdown('Latest data as of April 25, 2025')
    
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
            progress = min(item['percentage'], 100)
            progress_text = f"{item['current']:,} / {item['target']:,} ({item['percentage']}%)"
            
            progress_color = "#10b981" if item['status'] == 'Achieved' else "#f59e0b" if item['status'] == 'Behind' else "#ef4444"
            st.progress(progress/100)
        with col3:
            status_class = f"status-{item['status'].lower().replace(' ', '-')}"
            st.markdown(f"{progress_text} <span class='{status_class}'>{item['status']}</span>", unsafe_allow_html=True)
    
    # Key Insights - UPDATED
    st.markdown("""
    <div class="insight-container">
        <h3>Key Insights:</h3>
        <ul>
            <li style="color: #059669;"><strong>Enrollment target exceeded (120% of goal)</strong> - <span class="status-achieved">Achieved</span></li>
            <li style="color: #dc2626;"><strong>18-25 demographic severely underrepresented (2% of target)</strong> - <span class="status-at-risk">At Risk</span></li>
            <li style="color: #d97706;"><strong>Program completion rates improving but still need attention (31% of target)</strong> - <span class="status-behind">Behind</span></li>
            <li style="color: #2563eb;"><strong>Site traffic increased but still at 12% of target (29.5K vs 250K)</strong> - <span class="status-behind">Behind</span></li>
            <li style="color: #059669;"><strong>Stories submission exceeding target by 134%</strong> - <span class="status-achieved">Achieved</span></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Demographics and Funnel section
    st.markdown('<p class="sub-header">Demographics & Program Funnel</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Age Demographics Pie Chart - UPDATED
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
            color_discrete_map={'18-25': '#0088FE', 'Other Ages': '#00C49F'},
            title="Age Demographics (Registrants)"
        )
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div style="text-align: center;">
            <p><span style="color: #0088FE; font-weight: bold;">18-25:</span> {age_data['18-25']['value']} registrants ({age_data['18-25']['value']/(age_data['18-25']['value']+age_data['Other Ages']['value'])*100:.1f}%)</p>
            <p><span style="color: #00C49F; font-weight: bold;">Other Ages:</span> {age_data['Other Ages']['value']} registrants ({age_data['Other Ages']['value']/(age_data['18-25']['value']+age_data['Other Ages']['value'])*100:.1f}%)</p>
            <p style="font-weight: bold; margin-top: 10px;">KPI Target: 50% ages 18-25</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Funnel chart - UPDATED
        funnel_data = [
            {'stage': 'Impressions (Ads)', 'value': social_data['Impressions Delivered'], 'percent': 100},
            {'stage': 'Visitors', 'value': traffic_data['Visitors'], 'percent': traffic_data['Visitors']/social_data['Impressions Delivered']*100},
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
        
        # Funnel metrics - UPDATED
        cols = st.columns(5)
        funnel_metrics = [
            {"label": "Impressions", "value": social_data['Impressions Delivered'], "color": "#9333ea"},
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
    
    # New Section for Badges - NEW
    st.markdown('<p class="sub-header">Badge Progress</p>', unsafe_allow_html=True)
    
    # Badge progress bar
    badge_weeks = ['Week 0', 'Week 1', 'Week 2']
    badge_values = [badges_data['Week 0'], badges_data['Week 1'], badges_data['Week 2']]
    
    badge_fig = px.bar(
        x=badge_weeks,
        y=badge_values,
        color=badge_weeks,
        labels={'x': 'Week', 'y': 'Badges Claimed'},
        title='Badge Claims by Week (Target: 5,000 per week)'
    )
    
    badge_fig.add_shape(
        type="line",
        x0=-0.5,
        y0=5000,
        x1=2.5,
        y1=5000,
        line=dict(
            color="red",
            width=2,
            dash="dash",
        )
    )
    
    badge_fig.add_annotation(
        x=1,
        y=5300,
        text="Weekly Target: 5,000",
        showarrow=False,
        font=dict(
            color="red"
        )
    )
    
    badge_fig.update_layout(
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(badge_fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="background-color: #dbeafe;">
            <div class="metric-label">Total Badges Claimed</div>
            <div class="metric-value">{badges_data['Total Claimed']:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background-color: #dcfce7;">
            <div class="metric-label">Unique Users with Badges</div>
            <div class="metric-value">{badges_data['Unique Users']:,}</div>
            <div>{badges_data['Unique Users']/program_metrics['Registrants']['value']*100:.1f}% of registrants</div>
        </div>
        """, unsafe_allow_html=True)
    
    # SMS and Social Media section
    st.markdown('<p class="sub-header">Marketing Performance</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Social Media Metrics - UPDATED
        st.subheader("Social Media Marketing")
        cols = st.columns(2)
        
        social_metrics = [
            {"label": "Clicks to Site", "value": social_data['Clicks to Site'], "bg": "#dbeafe", "text": "#1e40af"},
            {"label": "Impressions", "value": social_data['Impressions Delivered'], "bg": "#dcfce7", "text": "#166534"},
            {"label": "Video Views", "value": social_data['Video Views'], "bg": "#f3e8ff", "text": "#6b21a8"},
            {"label": "Engagements", "value": social_data['Direct Engagements'], "bg": "#fef9c3", "text": "#854d0e"}
        ]
        
        for i, metric in enumerate(social_metrics):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="metric-card" style="background-color: {metric['bg']};">
                    <div class="metric-label" style="color: {metric['text']};">{metric['label']}</div>
                    <div class="metric-value" style="color: {metric['text']};">{metric['value']:,}</div>
                    {f"<div>{social_data['Direct Engagements']/social_data['Impressions Delivered']*100:.1f}% engagement rate</div>" if metric['label'] == 'Engagements' else ""}
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        # Detailed Social Engagement - NEW
        st.subheader("Social Engagement Breakdown")
        
        social_engagement = pd.DataFrame([
            {"Metric": "Reactions", "Value": social_data['Reactions']},
            {"Metric": "Comments", "Value": social_data['Comments']},
            {"Metric": "Shares", "Value": social_data['Shares']},
            {"Metric": "Saves", "Value": social_data['Saves']},
            {"Metric": "New Page Likes", "Value": social_data['Page Likes']}
        ])
        
        fig = px.bar(
            social_engagement,
            x="Metric",
            y="Value",
            color="Metric",
            title="Social Media Engagement Metrics"
        )
        
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Story Submissions - NEW
    st.markdown('<p class="sub-header">Story Submissions</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="background-color: #fef3c7;">
            <div class="metric-label">Stories Submitted</div>
            <div class="metric-value">{stories_data['Submitted']:,}</div>
            <div>Target: {stories_data['Target']} ({stories_data['Submitted']/stories_data['Target']*100:.0f}% achieved)</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Website Analytics - UPDATED
    st.markdown('<p class="sub-header">Website Analytics</p>', unsafe_allow_html=True)
    cols = st.columns(4)
    
    web_metrics = [
        {"label": "Pageviews", "value": traffic_data['Pageviews'], "subtext": f"{traffic_data['Pageviews']/traffic_data['Sessions']:.1f} pageviews per session", "bg": "#e0e7ff", "text": "#3730a3"},
        {"label": "Sessions", "value": traffic_data['Sessions'], "subtext": "00:01:19 per session", "bg": "#dbeafe", "text": "#1e40af"},
        {"label": "Visitors", "value": traffic_data['Visitors'], "subtext": "94.5% are new visitors", "bg": "#ccfbf1", "text": "#0f766e"},
        {"label": "Bounce Rate", "value": f"{traffic_data['Bounce Rate']}%", "subtext": f"{int(traffic_data['Visitors'] * traffic_data['Bounce Rate']/100):,} visitors bounced", "bg": "#fee2e2", "text": "#b91c1c"}
    ]
    
    for i, col in enumerate(cols):
        with col:
            metric = web_metrics[i]
            st.markdown(f"""
            <div class="metric-card" style="background-color: {metric['bg']};">
                <div class="metric-label" style="color: {metric['text']};">{metric['label']}</div>
                <div class="metric-value" style="color: {metric['text']};">{metric['value']:,}</div>
                <div>{metric['subtext']}</div>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    # Analysis & Recommendations - UPDATED with new data insights
    st.markdown('<p class="main-header">Data Analysis & Key Insights</p>', unsafe_allow_html=True)
    
    # Overall Program Performance - UPDATED
    st.markdown('<p class="sub-header">Overall Program Performance</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-container">
        <ul>
            <li><span style="font-weight: bold;">Strong Enrollment Growth:</span> With 11,985 registrants, the program has exceeded its target of 10,000 participants by 20%.</li>
            <li><span style="font-weight: bold;">Improving Completion Rate:</span> 25.8% of registrants (3,089) have completed Week 0, up from 18.7% in the previous report.</li>
            <li><span style="font-weight: bold;">Critical Age Demographics Gap:</span> Only 0.8% of registrants fall within the 18-25 age range, far below the 50% target and worse than previous metrics.</li>
            <li><span style="font-weight: bold;">Strong Story Submissions:</span> With 234 stories submitted against a target of 100, user-generated content is performing exceptionally well.</li>
            <li><span style="font-weight: bold;">Badge Engagement Challenge:</span> All badge claim weeks are below the 5,000 weekly target, with Week 0 achieving the highest at 3,089.</li>
            <li><span style="font-weight: bold;">Effective Social Engagement:</span> 70.7K video views and robust engagement metrics indicate good social media traction.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Conversion Funnel Analysis - UPDATED
    st.markdown('<p class="sub-header">Conversion Funnel Analysis</p>', unsafe_allow_html=True)
    
    funnel_analysis = pd.DataFrame([
        {"Funnel Stage": "Impressions (Ads)", "Count": 338000, "Conversion Rate": "-", "Analysis": "Strong top-of-funnel reach with ads"},
        {"Funnel Stage": "Visitors", "Count": 29500, "Conversion Rate": "8.7% of impressions", "Analysis": "Below average click-through rate from ads to site"},
        {"Funnel Stage": "Registrants", "Count": 11985, "Conversion Rate": "40.6% of visitors", "Analysis": "Excellent visitor-to-registrant conversion"},
        {"Funnel Stage": "Downloads", "Count": 22186, "Conversion Rate": "185.1% of registrants", "Analysis": "Many users downloading multiple resources"},
        {"Funnel Stage": "Week 0 Complete", "Count": 3089, "Conversion Rate": "25.8% of registrants", "Analysis": "Improving completion rate, still needs attention"}
    ])
    
    st.dataframe(funnel_analysis, use_container_width=True, hide_index=True)
    
    # Age Demographics Challenge - UPDATED
    st.markdown('<p class="sub-header">Age Demographics Challenge</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-container">
        <p>Only 101 registrants (0.8% of total) are in the 18-25 age bracket, significantly below the 50% target.</p>
        <p>This represents an even more critical gap in program KPIs than previously identified and requires immediate strategic intervention.</p>
        <p>The campaign has added 75 new members in the 18-25 demographic, showing minimal traction with this audience segment.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # New Social Media Analysis - NEW
    st.markdown('<p class="sub-header">Social Media Performance</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-container">
        <p>The social media campaign is showing strong engagement with:</p>
        <ul>
            <li>70.7K video views indicating good content consumption</li>
            <li>217 shares demonstrating content appeal and virality</li>
            <li>3.2K reactions showing positive sentiment</li>
            <li>74 comments providing opportunities for community building</li>
        </ul>
        <p>The comment engagement represents an opportunity for further community development through active response and moderation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Strategic Recommendations - UPDATED
    st.markdown('<p class="main-header">Strategic Recommendations</p>', unsafe_allow_html=True)
    
    # Priority 1 - UPDATED
    st.markdown('<p class="sub-header">Priority 1: Youth Engagement Strategy (URGENT)</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-container">
        <ul>
            <li><span style="font-weight: bold;">Youth-Specific Content Strategy:</span> Develop dedicated content streams and messaging specifically for 18-25 demographic.</li>
            <li><span style="font-weight: bold;">Platform Reallocation:</span> Immediately shift 60-70% of marketing budget to platforms with highest 18-25 demographic (TikTok, Instagram Reels).</li>
            <li><span style="font-weight: bold;">Campus Ambassador Program:</span> Launch an emergency recruitment drive targeting campus wellness centers and student organizations.</li>
            <li><span style="font-weight: bold;">Youth Focus Groups:</span> Conduct rapid research with the 101 existing 18-25 users to identify barriers and opportunities.</li>
            <li><span style="font-weight: bold;">Incentive Program:</span> Create referral bonuses specifically for bringing in 18-25 age demographic participants.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Priority 2 - UPDATED
    st.markdown('<p class="sub-header">Priority 2: Completion Rate Acceleration</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-container">
        <ul>
            <li><span style="font-weight: bold;">Badge System Enhancement:</span> Redesign badge incentive structure to improve weekly claims (currently all below 5,000 target).</li>
            <li><span style="font-weight: bold;">Community Showcase:</span> Leverage the 234 submitted stories as social proof to encourage higher completion rates.</li>
            <li><span style="font-weight: bold;">Progress Visualization:</span> Implement improved progress tracking and visualization for users.</li>
            <li><span style="font-weight: bold;">Re-engagement Campaign:</span> Target the 8,896 registrants who haven't completed Week 0 with personalized reminders.</li>
            <li><span style="font-weight: bold;">Social Accountability:</span> Create community accountability groups to improve completion rates.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Priority 3 - UPDATED
    st.markdown('<p class="sub-header">Priority 3: Social Engagement Maximization</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-container">
        <ul>
            <li><span style="font-weight: bold;">Comment Response Strategy:</span> Develop dedicated resources to respond to all 74+ comments for improved community engagement.</li>
            <li><span style="font-weight: bold;">Video Content Expansion:</span> Double down on video content given the strong 70.7K views.</li>
            <li><span style="font-weight: bold;">Shareable Content Focus:</span> Create more content optimized for sharing given the 217 shares already achieved.</li>
            <li><span style="font-weight: bold;">User Story Campaign:</span> Feature the best of the 234 submitted stories in social media campaigns.</li>
            <li><span style="font-weight: bold;">Cross-Platform Integration:</span> Ensure seamless experience between social platforms and the main program website.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Implementation Timeline - UPDATED
    st.markdown('<p class="sub-header">Implementation Timeline</p>', unsafe_allow_html=True)
    
    timeline_data = pd.DataFrame([
        {"Recommendation": "Emergency youth marketing reallocation", "Timeframe": "Immediate (48 hours)", "Expected Impact": "Critical - Direct impact on 18-25 recruitment"},
        {"Recommendation": "Badge system enhancement", "Timeframe": "Immediate (1 week)", "Expected Impact": "High - Could recover 15-25% of badge drop-offs"},
        {"Recommendation": "Comment response initiative", "Timeframe": "Immediate (72 hours)", "Expected Impact": "Medium - Builds community engagement"},
        {"Recommendation": "Youth focus groups with 101 existing 18-25 users", "Timeframe": "Short-term (1 week)", "Expected Impact": "High - Critical insights for improvement"},
        {"Recommendation": "Featured story campaign from 234 submissions", "Timeframe": "Short-term (1-2 weeks)", "Expected Impact": "Medium - Leverages existing UGC success"},
        {"Recommendation": "Campus ambassador emergency program", "Timeframe": "Short-term (2 weeks)", "Expected Impact": "High - Direct channel to target demographic"},
        {"Recommendation": "Re-engagement campaign for non-completers", "Timeframe": "Short-term (1 week)", "Expected Impact": "High - Could improve completion by 10-15%"}
    ])
    
    st.dataframe(timeline_data, use_container_width=True, hide_index=True)
    
    # KPI Forecast - UPDATED
    st.markdown('<p class="sub-header">KPI Forecast with Recommended Actions</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-container">
        <ul>
            <li><span style="font-weight: bold;">18-25 Enrollment:</span> Even with emergency measures, realistically expect to reach only 15-20% of the target by program end (vs. 50% target).</li>
            <li><span style="font-weight: bold;">Week 0 Completion:</span> With enhanced re-engagement, target 45-50% completion (5,300-6,000 participants).</li>
            <li><span style="font-weight: bold;">Badge Claims:</span> Badge system enhancement could bring weekly claims to 4,000-4,500 (vs. 5,000 target).</li>
            <li><span style="font-weight: bold;">Social Engagement:</span> Comment response initiative should increase engagement metrics by 30-40%.</li>
            <li><span style="font-weight: bold;">Story Submissions:</span> Continue to exceed targets; expect 300+ by program end.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
