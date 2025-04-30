    # Self-Care School Podcast Analytics - NEW SECTION
    st.markdown('<p class="sub-header">Self-Care School Podcast Analytics</p>', unsafe_allow_html=True)
    
    # Add container
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Summary metrics
    st.markdown('<h3 style="font-size: 1.2rem; color: #4338ca; margin-bottom: 16px; font-weight: 600; text-align: center;">Podcast Performance Overview</h3>', unsafe_allow_html=True)
    
    # Top metrics row
    cols = st.columns(3)
    
    podcast_summary = [
        {"icon": "🎧", "label": "Total Plays", "value": podcast_data['Total Plays'], "bg": "linear-gradient(135deg, #e0e7ff 0%, #a5b4fc 100%)", "text": "#4338ca"},
        {"icon": "🎙️", "label": "Total Episodes", "value": podcast_data['Total Episodes'], "bg": "linear-gradient(135deg, #dbeafe 0%, #93c5fd 100%)", "text": "#1e40af"},
        {"icon": "📈", "label": "Average Plays Per Episode", "value": podcast_data['Average Plays'], "bg": "linear-gradient(135deg, #f3e8ff 0%, #d8b4fe 100%)", "text": "#7e22ce"}
    ]
    
    for i, col in enumerate(cols):
        with col:
            metric = podcast_summary[i]
            st.markdown(f"""
            <div class="metric-card" style="background: {metric['bg']};">
                <div style="font-size: 2rem; margin-bottom: 4px;">{metric['icon']}</div>
                <div class="metric-label" style="color: {metric['text']};">{metric['label']}</div>
                <div class="metric-value" style="color: {metric['text']};">{metric['value']:,}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Weekly Plays Chart
    st.markdown('<h3 style="font-size: 1.2rem; color: #4338ca; margin: 20px 0 16px 0; font-weight: 600;">Episode Plays by Week</h3>', unsafe_allow_html=True)
    
    weekly_data = pd.DataFrame({
        'Week': list(podcast_data['Weekly Plays'].keys()),
        'Plays': list(podcast_data['Weekly Plays'].values())
    })
    
    # Set colors for weekly bars
    week_colors = {
        'Week 0': '#8b5cf6',
        'Week 1': '#a78bfa',
        'Week 2': '#10b981',
        'Week 3': '#f59e0b'
    }
    
    # Create weekly plays bar chart
    weekly_fig = go.Figure()
    
    for i, row in weekly_data.iterrows():
        weekly_fig.add_trace(go.Bar(
            x=[row['Week']],
            y=[row['Plays']],
            name=row['Week'],
            marker_color=week_colors[row['Week']],
            text=[f"{row['Plays']:,}"],
            textposition='auto',
            hovertemplate=f"<b>{row['Week']}</b><br>Total Plays: %{{y:,}}"
        ))
    
    weekly_fig.update_layout(
        title="Total Plays by Week",
        title_font_size=16,
        title_x=0.5,
        showlegend=False,
        height=350,
        margin=dict(l=20, r=20, t=60, b=20),
        bargap=0.4,
        yaxis_title="Number of Plays"
    )
    
    st.plotly_chart(weekly_fig, use_container_width=True)
    
    # Top episodes within each week
    st.markdown('<h3 style="font-size: 1.2rem; color: #4338ca; margin: 20px 0 16px 0; font-weight: 600;">Individual Episode Performance</h3>', unsafe_allow_html=True)
    
    # Create tabs for each week
    week_tabs = st.tabs(["Week 0", "Week 1", "Week 2", "Week 3"])
    
    for week_idx, week_tab in enumerate(week_tabs):
        week_name = f"Week {week_idx}"
        
        with week_tab:
            # Filter episodes for this week
            week_episodes = [ep for ep in podcast_data['Episodes'] if ep['week'] == week_idx]
            week_episodes.sort(key=lambda x: x['day'])
            
            # Create week-specific bar chart
            ep_fig = go.Figure()
            
            for ep in week_episodes:
                ep_fig.add_trace(go.Bar(
                    y=[f"Day {ep['day']}: {ep['title']}"],
                    x=[ep['plays']],
                    orientation='h',
                    marker_color=ep['color'],
                    text=[f"{ep['plays']:,}"],
                    textposition='auto',
                    hovertemplate=f"<b>Day {ep['day']}: {ep['title']}</b><br>Plays: %{{x:,}}"
                ))
            
            ep_fig.update_layout(
                title=f"{week_name} Episode Performance",
                title_font_size=16,
                title_x=0.5,
                showlegend=False,
                height=350,
                margin=dict(l=20, r=20, t=60, b=20),
                bargap=0.2,
                xaxis_title="Number of Plays",
                xaxis=dict(
                    title="Plays",
                    titlefont=dict(size=14),
                ),
                yaxis=dict(
                    title="",
                    titlefont=dict(size=14),
                    autorange="reversed"  # This puts the highest value at the top
                )
            )
            
            st.plotly_chart(ep_fig, use_container_width=True)
            
            # Add weekly insights
            total_week_plays = sum(ep['plays'] for ep in week_episodes)
            avg_week_plays = int(total_week_plays / len(week_episodes))
            most_played = max(week_episodes, key=lambda x: x['plays'])
            
            st.markdown(f"""
            <div style="display: flex; gap: 16px; margin-top: 10px;">
                <div style="flex: 1; background: {week_colors[week_name]}20; padding: 12px; border-radius: 8px; text-align: center; border-left: 3px solid {week_colors[week_name]};">
                    <div style="font-weight: 600; color: {week_colors[week_name]};">Total Plays</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: {week_colors[week_name]};">{total_week_plays:,}</div>
                </div>
                <div style="flex: 1; background: {week_colors[week_name]}20; padding: 12px; border-radius: 8px; text-align: center; border-left: 3px solid {week_colors[week_name]};">
                    <div style="font-weight: 600; color: {week_colors[week_name]};">Average Per Episode</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: {week_colors[week_name]};">{avg_week_plays:,}</div>
                </div>
                <div style="flex: 2; background: {week_colors[week_name]}20; padding: 12px; border-radius: 8px; text-align: center; border-left: 3px solid {week_colors[week_name]};">
                    <div style="font-weight: 600; color: {week_colors[week_name]};">Most Popular Episode</div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: {week_colors[week_name]};">Day {most_played['day']}: {most_played['title']}</div>
                    <div style="font-size: 0.9rem; color: {week_colors[week_name]};">{most_played['plays']:,} plays</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Key insights for podcast data
    st.markdown("""
    <div class="insight-container">
        <h3 style="margin-top: 0; color: #4338ca; font-size: 1.2rem; margin-bottom: 12px;">Key Podcast Insights:</h3>
        <ul style="list-style-type: none; padding-left: 0;">
            <li style="margin-bottom: 10px; display: flex; align-items: center;"><span style="background-color: #8b5cf6; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></span> <strong>Week 0 (Orientation)</strong> has the highest total plays at 6,957, showing strong initial engagement</li>
            <li style="margin-bottom: 10px; display: flex; align-items: center;"><span style="background-color: #a78bfa; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></span> <strong>Day 1 episodes</strong> consistently have the highest plays within each week</li>
            <li style="margin-bottom: 10px; display: flex; align-items: center;"><span style="background-color: #f59e0b; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></span> <strong>Week 3</strong> shows a significant drop in plays (1,190) compared to previous weeks</li>
            <li style="margin-bottom: 10px; display: flex; align-items: center;"><span style="background-color: #10b981; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></span> Average plays gradually decrease each week, indicating an opportunity for re-engagement strategies</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Close container
    st.markdown('</div>', unsafe_allow_html=True)    # Black History Bootcamp Analytics - NEW SECTION
    st.markdown('<p class="sub-header">Black History Bootcamp Analytics</p>', unsafe_allow_html=True)
    
    # Add container
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Summary metrics
    st.markdown('<h3 style="font-size: 1.2rem; color: #4338ca; margin-bottom: 16px; font-weight: 600; text-align: center;">Podcast Performance Overview</h3>', unsafe_allow_html=True)
    
    # Top metrics row
    cols = st.columns(3)
    
    bootcamp_summary = [
        {"icon": "🎧", "label": "Total Plays", "value": bootcamp_data['Total Plays'], "bg": "linear-gradient(135deg, #e0e7ff 0%, #a5b4fc 100%)", "text": "#4338ca"},
        {"icon": "🎙️", "label": "Total Episodes", "value": bootcamp_data['Total Episodes'], "bg": "linear-gradient(135deg, #dbeafe 0%, #93c5fd 100%)", "text": "#1e40af"},
        {"icon": "📈", "label": "Average Plays Per Episode", "value": bootcamp_data['Average Plays'], "bg": "linear-gradient(135deg, #f3e8ff 0%, #d8b4fe 100%)", "text": "#7e22ce"}
    ]
    
    for i, col in enumerate(cols):
        with col:
            metric = bootcamp_summary[i]
            st.markdown(f"""
            <div class="metric-card" style="background: {metric['bg']};">
                <div style="font-size: 2rem; margin-bottom: 4px;">{metric['icon']}</div>
                <div class="metric-label" style="color: {metric['text']};">{metric['label']}</div>
                <div class="metric-value" style="color: {metric['text']};">{metric['value']:,}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Series comparison
    st.markdown('<h3 style="font-size: 1.2rem; color: #4338ca; margin: 20px 0 16px 0; font-weight: 600;">Series Comparison</h3>', unsafe_allow_html=True)
    
    series_df = pd.DataFrame(bootcamp_data['Series Data'])
    
    # Create series comparison chart
    series_fig = go.Figure()
    
    # Add bars
    for i, row in series_df.iterrows():
        series_fig.add_trace(go.Bar(
            x=[row['name']],
            y=[row['plays']],
            name=row['name'],
            marker_color=row['color'],
            text=[f"{row['plays']:,}"],
            textposition='auto',
            hovertemplate=f"<b>{row['name']}</b><br>Total Plays: %{{y:,}}<br>Episodes: {row['episodes']}<br>Avg: {row['avg']:,} per episode"
        ))
    
    series_fig.update_layout(
        title="Plays by Series",
        title_font_size=16,
        title_x=0.5,
        showlegend=False,
        height=350,
        margin=dict(l=20, r=20, t=60, b=20),
        bargap=0.4,
        yaxis_title="Total Plays"
    )
    
    st.plotly_chart(series_fig, use_container_width=True)
    
    # Top Episodes Bar Chart
    st.markdown('<h3 style="font-size: 1.2rem; color: #4338ca; margin: 20px 0 16px 0; font-weight: 600;">Top 10 Episodes by Plays</h3>', unsafe_allow_html=True)
    
    top_episodes_df = pd.DataFrame(bootcamp_data['Top Episodes'])
    
    episode_fig = go.Figure()
    
    # Add horizontal bars for better readability of episode titles
    for i, row in top_episodes_df.iterrows():
        episode_fig.add_trace(go.Bar(
            y=[row['title']],
            x=[row['plays']],
            orientation='h',
            marker_color=row['color'],
            text=[f"{row['plays']:,}"],
            textposition='auto',
            hovertemplate=f"<b>{row['title']}</b><br>Plays: %{{x:,}}"
        ))
    
    episode_fig.update_layout(
        title="Top Episodes by Number of Plays",
        title_font_size=16,
        title_x=0.5,
        showlegend=False,
        height=500,
        margin=dict(l=20, r=20, t=60, b=20),
        bargap=0.2,
        xaxis_title="Plays",
        xaxis=dict(
            title="Number of Plays",
            titlefont=dict(size=14),
        ),
        yaxis=dict(
            title="",
            titlefont=dict(size=14),
            autorange="reversed"  # This puts the highest value at the top
        )
    )
    
    st.plotly_chart(episode_fig, use_container_width=True)
    
    # Key insights for bootcamp data
    st.markdown("""
    <div class="insight-container">
        <h3 style="margin-top: 0; color: #4338ca; font-size: 1.2rem; margin-bottom: 12px;">Key Insights:</h3>
        <ul style="list-style-type: none; padding-left: 0;">
            <li style="margin-bottom: 10px; display: flex; align-items: center;"><span style="background-color: #8b5cf6; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></span> <strong>Original Black History Bootcamp</strong> episodes have the highest average plays (7,849 per episode)</li>
            <li style="margin-bottom: 10px; display: flex; align-items: center;"><span style="background-color: #3b82f6; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></span> <strong>Day 1 | Audre Lorde</strong> is the most played episode with 22,816 plays</li>
            <li style="margin-bottom: 10px; display: flex; align-items: center;"><span style="background-color: #10b981; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></span> <strong>First week episodes</strong> consistently receive the highest play counts, showing strong initial engagement</li>
            <li style="margin-bottom: 10px; display: flex; align-items: center;"><span style="background-color: #f59e0b; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></span> The <strong>Resistance Series</strong> performs well with 5,341 average plays per episode</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Close container
    st.markdown('</div>', unsafe_allow_html=True)import streamlit as st
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

# Add CSS for styling - Enhanced for responsiveness and cleaner design
st.markdown("""
<style>
    /* Global styles */
    .main-header {
        font-size: calc(1.8rem + 0.6vw);
        font-weight: 700;
        color: #3730a3;
        margin-bottom: 8px;
        padding-left: 0.5rem;
    }
    .sub-header {
        font-size: calc(1.2rem + 0.3vw);
        font-weight: 600;
        color: #4338ca;
        margin-top: 24px;
        margin-bottom: 12px;
        padding-left: 0.5rem;
        border-left: 4px solid #4338ca;
    }
    
    /* Card styles */
    .metric-card {
        background-color: #f9fafb;
        padding: 16px;
        border-radius: 12px;
        margin: 8px 0;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: calc(1.5rem + 0.5vw);
        font-weight: 700;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 1rem;
        color: #4b5563;
        margin-bottom: 4px;
    }
    
    /* Status indicators */
    .status-achieved {
        background-color: #d1fae5;
        color: #065f46;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 8px;
    }
    .status-behind {
        background-color: #fef3c7;
        color: #92400e;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 8px;
    }
    .status-at-risk {
        background-color: #fee2e2;
        color: #b91c1c;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 8px;
    }
    
    /* Container styles */
    .insight-container {
        background-color: #f9fafb;
        padding: 20px;
        border-radius: 12px;
        margin-top: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-left: 4px solid #6366f1;
    }
    .insight-container ul {
        padding-left: 20px;
        margin-bottom: 0;
    }
    .insight-container li {
        margin-bottom: 8px;
    }
    
    /* Tab styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: #f9fafb;
        padding: 8px 16px;
        border-radius: 8px 8px 0 0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px 8px 0 0;
        gap: 1px;
        padding: 10px 16px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e0e7ff;
        color: #4338ca;
        font-weight: 600;
    }
    
    /* Progress bar styles */
    .stProgress > div > div {
        background-color: #e0e7ff;
    }
    .stProgress {
        height: 10px;
    }
    
    /* Chart container */
    .chart-container {
        background-color: white;
        padding: 16px;
        border-radius: 12px;
        margin: 12px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .metric-card {
            padding: 12px 8px;
        }
        .metric-value {
            font-size: calc(1.2rem + 0.3vw);
        }
        .metric-label {
            font-size: 0.85rem;
        }
        .insight-container {
            padding: 12px;
        }
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
    # Dashboard Header - Improved with container and date badge
    st.markdown('<div style="background-color: #f9fafb; padding: 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
    st.markdown('<p class="main-header">Self-Care School Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<div style="display: flex; align-items: center; margin-bottom: 10px;"><div style="background-color: #e0e7ff; padding: 6px 12px; border-radius: 16px; font-size: 0.9rem; color: #4338ca; font-weight: 500;">Latest data as of April 25, 2025</div></div>', unsafe_allow_html=True)
    
    # Divider
    st.markdown('<hr style="margin: 0; border: none; border-top: 1px solid #e5e7eb;">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Top metrics - Enhanced card design
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);">
            <div class="metric-label">Registrants</div>
            <div class="metric-value">{:,}</div>
            <div style="color: #4338ca; font-weight: 500;">Target: {:,}</div>
        </div>
        """.format(program_metrics['Registrants']['value'], program_metrics['Registrants']['target']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);">
            <div class="metric-label">Visitors</div>
            <div class="metric-value">{:,}</div>
            <div style="color: #92400e; font-weight: 500;">94.5% are new visitors</div>
        </div>
        """.format(traffic_data['Visitors']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #ffedd5 0%, #fed7aa 100%);">
            <div class="metric-label">Total Badges Claimed</div>
            <div class="metric-value">{:,}</div>
            <div style="color: #9a3412; font-weight: 500;">{:.1f}% of weekly target</div>
        </div>
        """.format(badges_data['Total Claimed'], 
                  badges_data['Total Claimed'] / (3 * badges_data['Target']) * 100), 
                  unsafe_allow_html=True)
    
    # KPI Progress & Analysis - Enhanced with better progress bars and layout
    st.markdown('<p class="sub-header">KPI Progress & Analysis</p>', unsafe_allow_html=True)
    
    # Add container
    st.markdown('<div class="chart-container" style="padding: 20px;">', unsafe_allow_html=True)
    
    # Calculate average weekly badges
    avg_weekly_badges = (badges_data['Week 0'] + badges_data['Week 1'] + badges_data['Week 2']) / 3
    
    # Updated KPI Progress Data with new Average Weekly Badges metric
    kpi_progress = {
        'Enrollment': {'current': 11985, 'target': 10000, 'percentage': 120, 'status': 'Achieved', 'color': '#10b981'},
        '18-25 Enrollment': {'current': 101, 'target': 5000, 'percentage': 2, 'status': 'At Risk', 'color': '#ef4444'},
        'Average Weekly Badges': {'current': avg_weekly_badges, 'target': 5000, 'percentage': int(avg_weekly_badges/5000*100), 'status': 'Behind', 'color': '#f59e0b'},
        'Site Traffic': {'current': 29500, 'target': 250000, 'percentage': 12, 'status': 'Behind', 'color': '#f59e0b'},
        'Downloads': {'current': 22186, 'target': 100000, 'percentage': 22, 'status': 'Behind', 'color': '#f59e0b'},
        'Stories Submitted': {'current': 234, 'target': 100, 'percentage': 234, 'status': 'Achieved', 'color': '#10b981'}
    }
    
    # Create progress bars with enhanced styling
    for key, item in kpi_progress.items():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.markdown(f'<div style="font-weight: 600; padding: 8px 0;">{key}</div>', unsafe_allow_html=True)
        with col2:
            progress = min(item['percentage'], 100)
            
            # Custom progress bar styling based on status
            progress_color = item['color']
            st.markdown(f"""
            <div style="background-color: #f3f4f6; border-radius: 8px; height: 12px; margin-top: 12px;">
                <div style="background-color: {progress_color}; width: {progress}%; height: 12px; border-radius: 8px;"></div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            status_class = f"status-{item['status'].lower().replace(' ', '-')}"
            progress_text = f"{int(item['current']):,} / {item['target']:,}"
            st.markdown(f'<div style="padding: 8px 0; text-align: right;">{progress_text} <span class="{status_class}">{item["status"]}</span></div>', unsafe_allow_html=True)
    
    # Close container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Key Insights - Enhanced styling
    st.markdown("""
    <div class="insight-container">
        <h3 style="margin-top: 0; color: #4338ca; font-size: 1.2rem; margin-bottom: 12px;">Key Insights:</h3>
        <ul style="list-style-type: none; padding-left: 0;">
            <li style="margin-bottom: 10px; display: flex; align-items: center;"><span style="background-color: #d1fae5; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></span> <strong style="color: #059669;">Enrollment target exceeded (120% of goal)</strong> - <span class="status-achieved">Achieved</span></li>
            <li style="margin-bottom: 10px; display: flex; align-items: center;"><span style="background-color: #fee2e2; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></span> <strong style="color: #dc2626;">18-25 demographic severely underrepresented (2% of target)</strong> - <span class="status-at-risk">At Risk</span></li>
            <li style="margin-bottom: 10px; display: flex; align-items: center;"><span style="background-color: #fef3c7; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></span> <strong style="color: #d97706;">Average weekly badge claims at 49% of target</strong> - <span class="status-behind">Behind</span></li>
            <li style="margin-bottom: 10px; display: flex; align-items: center;"><span style="background-color: #fef3c7; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></span> <strong style="color: #2563eb;">Site traffic increased but still at 12% of target (29.5K vs 250K)</strong> - <span class="status-behind">Behind</span></li>
            <li style="margin-bottom: 10px; display: flex; align-items: center;"><span style="background-color: #d1fae5; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></span> <strong style="color: #059669;">Stories submission exceeding target by 134%</strong> - <span class="status-achieved">Achieved</span></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Demographics and Funnel section - Now stacked instead of side by side
    st.markdown('<p class="sub-header">Demographics & Program Funnel</p>', unsafe_allow_html=True)
    
    # Age Demographics Pie Chart - Enhanced with container
    st.markdown('<p class="sub-header">Age Demographics</p>', unsafe_allow_html=True)
    
    # Add chart container
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
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
    fig.update_layout(
        height=400,
        title_font_size=16,
        title_x=0.5,
        margin=dict(t=60, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 10px;">
        <p><span style="color: #0088FE; font-weight: bold;">18-25:</span> {age_data['18-25']['value']} registrants ({age_data['18-25']['value']/(age_data['18-25']['value']+age_data['Other Ages']['value'])*100:.1f}%)</p>
        <p><span style="color: #00C49F; font-weight: bold;">Other Ages:</span> {age_data['Other Ages']['value']} registrants ({age_data['Other Ages']['value']/(age_data['18-25']['value']+age_data['Other Ages']['value'])*100:.1f}%)</p>
        <p style="font-weight: bold; margin-top: 10px;">KPI Target: 50% ages 18-25</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Close chart container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Program Funnel - Enhanced with container
    st.markdown('<p class="sub-header">Program Funnel</p>', unsafe_allow_html=True)
    
    # Add chart container
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
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
        title="Program Conversion Flow",
        title_font_size=16,
        title_x=0.5,
        margin=dict(l=20, r=20, t=60, b=20),
        height=450
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Funnel metrics - Enhanced with better cards
    cols = st.columns(5)
    funnel_metrics = [
        {"label": "Impressions", "value": social_data['Impressions Delivered'], "color": "#9333ea", "bg": "#f3e8ff"},
        {"label": "Visitors", "value": traffic_data['Visitors'], "color": "#3b82f6", "bg": "#dbeafe"},
        {"label": "Registrants", "value": program_metrics['Registrants']['value'], "color": "#4f46e5", "bg": "#e0e7ff"},
        {"label": "Downloads", "value": stream_data['Downloads'], "color": "#10b981", "bg": "#dcfce7"},
        {"label": "Week 0 Complete", "value": program_metrics['Completed Week 0']['value'], "color": "#f59e0b", "bg": "#fef3c7"}
    ]
    
    for i, col in enumerate(cols):
        with col:
            metric = funnel_metrics[i]
            st.markdown(f"""
            <div class="metric-card" style="background-color: {metric['bg']}; border-left: 4px solid {metric['color']};">
                <div class="metric-value" style="color: {metric['color']};">{metric['value']:,}</div>
                <div class="metric-label" style="color: {metric['color']};">{metric['label']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Close chart container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # New Section for Badges - Enhanced with container and better styling
    st.markdown('<p class="sub-header">Badge Progress</p>', unsafe_allow_html=True)
    
    # Add container
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Badge progress bar
    badge_weeks = ['Week 0', 'Week 1', 'Week 2']
    badge_values = [badges_data['Week 0'], badges_data['Week 1'], badges_data['Week 2']]
    badge_colors = ['#4f46e5', '#3b82f6', '#60a5fa']
    
    badge_fig = go.Figure()
    
    # Add bars
    for i, (week, value) in enumerate(zip(badge_weeks, badge_values)):
        badge_fig.add_trace(go.Bar(
            x=[week], 
            y=[value],
            name=week,
            marker_color=badge_colors[i],
            text=[f"{value:,}"],
            textposition='auto',
        ))
    
    # Add target line
    badge_fig.add_shape(
        type="line",
        x0=-0.5,
        y0=5000,
        x1=2.5,
        y1=5000,
        line=dict(
            color="#ef4444",
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
            color="#ef4444",
            size=12
        )
    )
    
    badge_fig.update_layout(
        title="Badge Claims by Week",
        title_font_size=16,
        title_x=0.5,
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(
            title="",
            tickfont=dict(size=14),
        ),
        yaxis=dict(
            title="Number of Badges",
            titlefont=dict(size=14),
        ),
    )
    
    st.plotly_chart(badge_fig, use_container_width=True)
    
    # Badge metrics with enhanced cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border-left: 4px solid #3b82f6;">
            <div class="metric-label">Total Badges Claimed</div>
            <div class="metric-value" style="color: #1e40af;">{badges_data['Total Claimed']:,}</div>
            <div style="font-weight: 500; color: #1e40af;">{badges_data['Total Claimed']/(3*badges_data['Target'])*100:.1f}% of three-week target</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); border-left: 4px solid #10b981;">
            <div class="metric-label">Unique Users with Badges</div>
            <div class="metric-value" style="color: #047857;">{badges_data['Unique Users']:,}</div>
            <div style="font-weight: 500; color: #047857;">{badges_data['Unique Users']/program_metrics['Registrants']['value']*100:.1f}% of registrants</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Close container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Social Media section - Enhanced with better styling and containers
    st.markdown('<p class="sub-header">Marketing Performance</p>', unsafe_allow_html=True)
    
    # Add container
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Social Media Metrics - UPDATED with better styling
    st.markdown('<h3 style="font-size: 1.2rem; color: #4338ca; margin-bottom: 16px; font-weight: 600;">Social Media Marketing</h3>', unsafe_allow_html=True)
    cols = st.columns(4)
    
    social_metrics = [
        {"label": "Clicks to Site", "value": social_data['Clicks to Site'], "bg": "linear-gradient(135deg, #dbeafe 0%, #93c5fd 100%)", "text": "#1e40af", "icon": "🔗"},
        {"label": "Impressions", "value": social_data['Impressions Delivered'], "bg": "linear-gradient(135deg, #dcfce7 0%, #86efac 100%)", "text": "#166534", "icon": "👁️"},
        {"label": "Video Views", "value": social_data['Video Views'], "bg": "linear-gradient(135deg, #f3e8ff 0%, #d8b4fe 100%)", "text": "#6b21a8", "icon": "📺"},
        {"label": "Engagements", "value": social_data['Direct Engagements'], "bg": "linear-gradient(135deg, #fef9c3 0%, #fde047 100%)", "text": "#854d0e", "icon": "👍"}
    ]
    
    for i, col in enumerate(cols):
        with col:
            metric = social_metrics[i]
            st.markdown(f"""
            <div class="metric-card" style="background: {metric['bg']};">
                <div style="font-size: 1.5rem; margin-bottom: 4px;">{metric['icon']}</div>
                <div class="metric-label" style="color: {metric['text']};">{metric['label']}</div>
                <div class="metric-value" style="color: {metric['text']};">{metric['value']:,}</div>
                {f"<div style='color: {metric['text']}; font-weight: 500;'>{social_data['Direct Engagements']/social_data['Impressions Delivered']*100:.1f}% engagement rate</div>" if metric['label'] == 'Engagements' else ""}
            </div>
            """, unsafe_allow_html=True)
    
    # Close container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add container for engagement breakdown
    st.markdown('<div class="chart-container" style="margin-top: 16px;">', unsafe_allow_html=True)
    
    # Detailed Social Engagement - Enhanced styling
    st.markdown('<h3 style="font-size: 1.2rem; color: #4338ca; margin-bottom: 16px; font-weight: 600;">Social Engagement Breakdown</h3>', unsafe_allow_html=True)
    
    social_engagement = pd.DataFrame([
        {"Metric": "Reactions", "Value": social_data['Reactions'], "Color": "#3b82f6"},
        {"Metric": "Comments", "Value": social_data['Comments'], "Color": "#8b5cf6"},
        {"Metric": "Shares", "Value": social_data['Shares'], "Color": "#10b981"},
        {"Metric": "Saves", "Value": social_data['Saves'], "Color": "#f59e0b"},
        {"Metric": "New Page Likes", "Value": social_data['Page Likes'], "Color": "#ef4444"}
    ])
    
    fig = go.Figure()
    
    # Add bars with custom colors
    for i, row in social_engagement.iterrows():
        fig.add_trace(go.Bar(
            x=[row['Metric']],
            y=[row['Value']],
            name=row['Metric'],
            marker_color=row['Color'],
            text=[f"{row['Value']:,}"],
            textposition='auto',
        ))
    
    fig.update_layout(
        title="Social Media Engagement by Type",
        title_font_size=16,
        title_x=0.5,
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(
            title="",
            tickfont=dict(size=14),
        ),
        yaxis=dict(
            title="Count",
            titlefont=dict(size=14),
        ),
        bargap=0.4,
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add engagement metrics in small cards
    cols = st.columns(5)
    
    engagement_metrics = [
        {"icon": "❤️", "label": "Reactions", "value": social_data['Reactions'], "color": "#3b82f6"},
        {"icon": "💬", "label": "Comments", "value": social_data['Comments'], "color": "#8b5cf6"},
        {"icon": "🔄", "label": "Shares", "value": social_data['Shares'], "color": "#10b981"},
        {"icon": "🔖", "label": "Saves", "value": social_data['Saves'], "color": "#f59e0b"},
        {"icon": "👍", "label": "Page Likes", "value": social_data['Page Likes'], "color": "#ef4444"},
    ]
    
    for i, col in enumerate(cols):
        with col:
            metric = engagement_metrics[i]
            st.markdown(f"""
            <div style="text-align: center; padding: 8px; background-color: #f9fafb; border-radius: 8px; border-bottom: 3px solid {metric['color']};">
                <div style="font-size: 1.2rem; margin-bottom: 4px;">{metric['icon']}</div>
                <div style="font-weight: 600; color: {metric['color']};">{metric['value']:,}</div>
                <div style="font-size: 0.8rem; color: #6b7280;">{metric['label']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Close container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Story Submissions - Enhanced with container and better styling
    st.markdown('<p class="sub-header">Story Submissions</p>', unsafe_allow_html=True)
    
    # Add container
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Create a centered column that takes 60% of the width
    _, col, _ = st.columns([1, 3, 1])
    
    with col:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); text-align: center; padding: 24px; border-left: 4px solid #f59e0b;">
            <div class="metric-label" style="font-size: 1.2rem; margin-bottom: 8px;">Stories Submitted</div>
            <div class="metric-value" style="font-size: 3rem; color: #92400e;">{stories_data['Submitted']:,}</div>
            <div style="font-weight: 500; color: #92400e; margin-top: 8px;">
                <span style="display: inline-block; background-color: #fde68a; border: 2px solid #f59e0b; border-radius: 9999px; padding: 6px 16px;">
                    Target: {stories_data['Target']} 
                    <span style="color: #059669; font-weight: 600; margin-left: 8px;">({stories_data['Submitted']/stories_data['Target']*100:.0f}% achieved)</span>
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Close container
    st.markdown('</div>', unsafe_allow_html=True)
    
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
                <div class="metric-value" style="color: {metric['text']};"> {metric['value']} </div>
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
