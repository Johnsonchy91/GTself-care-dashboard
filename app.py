import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# Page configuration
st.set_page_config(
    page_title="MySelfCareSchool Dashboard",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* MySelfCareSchool-inspired color scheme */
    :root {
        --primary-teal: #81c8bc;
        --soft-pink: #f49ac1;
        --warm-yellow: #ffd966;
        --soft-green: #7dc691;
        --calm-blue: #6aa5cb;
        --white: #ffffff;
        --off-white: #f9f9f9;
        --dark-text: #333333;
    }
    
    /* Global styling */
    .stApp {
        background-color: var(--white);
    }
    
    /* Header styling */
    .main-header {
        color: var(--primary-teal);
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--soft-pink);
    }
    
    /* Section styling */
    .section-header {
        color: var(--primary-teal);
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Card styling */
    .metric-card {
        background-color: var(--off-white);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-top: 4px solid var(--primary-teal);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    /* Metric value styling */
    .metric-value {
        color: var(--calm-blue);
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    /* Metric label styling */
    .metric-label {
        color: var(--dark-text);
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: var(--primary-teal);
        color: white;
        border-radius: 30px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: var(--soft-pink);
        transform: scale(1.05);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--off-white);
    }
    
    /* Radio buttons */
    .stRadio > div {
        padding: 10px;
    }
    
    .stRadio > div > label {
        background-color: var(--off-white);
        border-radius: 10px;
        padding: 10px;
        border-left: 4px solid var(--primary-teal);
        margin-bottom: 8px;
        transition: all 0.2s ease;
    }
    
    .stRadio > div > label:hover {
        background-color: var(--primary-teal);
        color: white;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: var(--off-white);
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-teal);
        color: white;
    }
    
    /* Input fields styling */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #eaeaea;
        padding: 10px;
    }
    
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: var(--soft-pink);
        box-shadow: 0 0 0 2px rgba(244,154,193,0.2);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: var(--off-white);
        border-radius: 10px;
        border-left: 4px solid var(--soft-pink);
    }
    
    /* Footer styling */
    .footer {
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid var(--off-white);
        color: var(--dark-text);
        font-size: 0.8rem;
        text-align: center;
    }
    
    /* Custom animation */
    @keyframes gently-bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    .animate-gentle {
        animation: gently-bounce 3s ease infinite;
    }
</style>
""", unsafe_allow_html=True)

# Authentication function
def check_password():
    """Returns `True` if the user had the correct password."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if st.session_state.authenticated:
        return True

    return False

# Sidebar navigation
with st.sidebar:
    st.image("https://myselfcareschool.org/wp-content/uploads/2023/04/my-self-care-school-logo-2.png", width=200)
    st.markdown("<h2 style='color: #81c8bc;'>Self-Care Dashboard</h2>", unsafe_allow_html=True)
    
    nav_option = st.radio(
        "Navigation",
        ["Overview", "Physical Health", "Mental Health", "Academic Balance", "Resources", "Data Entry"]
    )
    
    st.markdown("---")
    st.markdown("<h3 style='color: #f49ac1;'>Filters</h3>", unsafe_allow_html=True)
    
    # Example filters
    date_range = st.date_input(
        "Date Range",
        [pd.to_datetime("2023-01-01"), pd.to_datetime("today")]
    )
    
    student_type = st.multiselect(
        "Participant Type",
        ["Students", "Educators", "Parents", "Healthcare Workers"],
        default=["Students", "Educators"]
    )
    
    # Add a fun motivational quote
    st.markdown("---")
    quotes = [
        ""Self-care is how you take your power back." — Lalah Delia",
        ""Almost everything will work again if you unplug it for a few minutes, including you." — Anne Lamott",
        ""Self-care is not self-indulgence, it is self-preservation." — Audre Lorde",
        ""Rest when you're weary. Refresh and renew yourself." — Raphaelle Giordano",
        ""Taking care of yourself doesn't mean me first, it means me too." — L.R. Knost"
    ]
    
    st.markdown(f"""
    <div style='background-color: #ffd966; padding: 15px; border-radius: 10px; margin-top: 20px;'>
        <p style='font-style: italic; color: #333; text-align: center;'>{random.choice(quotes)}</p>
    </div>
    """, unsafe_allow_html=True)

# Page header
st.markdown('<div class="main-header">Self-Care Dashboard</div>', unsafe_allow_html=True)

# Add dashboard description
st.markdown("""
<div style="background-color: #f9f9f9; padding: 15px; border-radius: 15px; border-left: 5px solid #81c8bc;">
This dashboard provides insights and resources to help you maintain 
physical and mental wellbeing while balancing your responsibilities.
Take a moment for yourself today! 💖
</div>
""", unsafe_allow_html=True)

# Generate sample data (in a real application, this would be loaded from a database)
@st.cache_data
def load_data():
    # Example data for trend chart
    trend_data = {
        'Month': pd.date_range(start='2023-01-01', periods=12, freq='M'),
        'Physical Activity': [68, 71, 73, 78, 82, 79, 75, 72, 74, 77, 80, 83],
        'Mental Wellbeing': [75, 73, 72, 77, 80, 82, 84, 81, 79, 78, 81, 83],
        'Academic Balance': [65, 62, 58, 55, 63, 70, 72, 68, 64, 61, 67, 72]
    }
    
    trend_df = pd.DataFrame(trend_data)
    
    # Example data for resources
    resources = ['Counseling', 'Recreation Center', 'Tutoring', 'Nutrition', 'Study Groups']
    values = [30, 25, 20, 15, 10]
    
    # Example data for satisfaction
    satisfaction_data = {
        'Resource': ['Counseling', 'Recreation Center', 'Tutoring', 'Nutrition', 'Study Groups'],
        'Satisfaction': [85, 90, 75, 80, 70]
    }
    
    sat_df = pd.DataFrame(satisfaction_data)
    
    return trend_df, resources, values, sat_df

trend_df, resources, values, sat_df = load_data()

# Create tabs for main content areas
if nav_option == "Overview":
    # Overview metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">78%</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">People reporting adequate sleep</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">65%</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Using self-care resources</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">3.2h</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Avg. daily physical activity</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">82%</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Positive mental health outcomes</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Trend chart example
    st.markdown('<div class="section-header">Wellness Trends</div>', unsafe_allow_html=True)
    
    # Using Plotly for better interactivity
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=trend_df['Month'], y=trend_df['Physical Activity'],
        mode='lines+markers', name='Physical Activity',
        line=dict(color='#81c8bc', width=3),
        marker=dict(size=10, symbol='circle')
    ))
    
    fig.add_trace(go.Scatter(
        x=trend_df['Month'], y=trend_df['Mental Wellbeing'],
        mode='lines+markers', name='Mental Wellbeing',
        line=dict(color='#f49ac1', width=3),
        marker=dict(size=10, symbol='diamond')
    ))
    
    fig.add_trace(go.Scatter(
        x=trend_df['Month'], y=trend_df['Academic Balance'],
        mode='lines+markers', name='Academic Balance',
        line=dict(color='#ffd966', width=3),
        marker=dict(size=10, symbol='square') 
    ))
    
    fig.update_layout(
        title='Wellness Metrics Over Time',
        xaxis_title='Month',
        yaxis_title='Score (%)',
        legend_title='Metrics',
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        font=dict(family="Poppins, sans-serif"),
        title_font=dict(size=24, color='#81c8bc'),
        legend_font=dict(size=12),
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add additional visualization section
    st.markdown('<div class="section-header">Resource Utilization</div>', unsafe_allow_html=True)
    
    # Two charts side by side
    col1, col2 = st.columns(2)
    
    with col1:
        # Example data for pie chart
        pie_fig = px.pie(
            names=resources, 
            values=values,
            title='Self-Care Resource Utilization',
            color_discrete_sequence=['#81c8bc', '#f49ac1', '#ffd966', '#7dc691', '#6aa5cb'],
            hole=0.4
        )
        
        pie_fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
            margin=dict(l=20, r=20, t=40, b=20),
            title_font=dict(size=20, color='#81c8bc'),
            font=dict(family="Poppins, sans-serif"),
        )
        
        pie_fig.update_traces(
            textinfo='percent+label',
            marker=dict(line=dict(color='#ffffff', width=2))
        )
        
        st.plotly_chart(pie_fig, use_container_width=True)
    
    with col2:
        # Example data for bar chart        
        bar_fig = px.bar(
            sat_df,
            x='Resource',
            y='Satisfaction',
            title='Resource Satisfaction Ratings',
            color='Satisfaction',
            color_continuous_scale=['#f49ac1', '#81c8bc'],
            text='Satisfaction'
        )
        
        bar_fig.update_layout(
            xaxis_title='Resource',
            yaxis_title='Satisfaction Score (%)',
            yaxis_range=[0, 100],
            margin=dict(l=20, r=20, t=40, b=20),
            title_font=dict(size=20, color='#81c8bc'),
            font=dict(family="Poppins, sans-serif"),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        bar_fig.update_traces(
            texttemplate='%{text}%', 
            textposition='outside',
            marker_line_color='white',
            marker_line_width=2,
            opacity=0.8
        )
        
        st.plotly_chart(bar_fig, use_container_width=True)

# Additional pages would be implemented in similar fashion
elif nav_option == "Physical Health":
    st.markdown('<div class="section-header">Physical Health Metrics</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
        <p>Physical self-care involves activities that improve physical health and wellbeing.
        This includes adequate sleep, nutrition, exercise, and preventative healthcare.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample content for this section
    tabs = st.tabs(["Exercise", "Sleep", "Nutrition", "Resources"])
    
    with tabs[0]:
        st.subheader("Physical Activity Recommendations")
        st.write("Regular physical activity is essential for maintaining physical and mental health.")
        
        # Sample exercise metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Recommended Daily Exercise", "30 min", "moderate intensity")
        with col2:
            st.metric("Community Average", "27 min", "-3 min")
        
        # Sample chart
        activity_data = {
            'Activity': ['Walking', 'Running', 'Yoga', 'Swimming', 'Cycling', 'Strength Training'],
            'Minutes per Week': [150, 60, 90, 45, 80, 70],
            'Calories Burned': [400, 500, 300, 450, 480, 350]
        }
        
        activity_df = pd.DataFrame(activity_data)
        
        activity_fig = px.bar(
            activity_df,
            x='Activity',
            y='Minutes per Week',
            color='Calories Burned',
            color_continuous_scale=['#f49ac1', '#81c8bc'],
            title='Popular Physical Activities'
        )
        
        activity_fig.update_layout(
            xaxis_title='Activity Type',
            yaxis_title='Average Minutes per Week',
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(activity_fig, use_container_width=True)
    
    with tabs[1]:
        st.subheader("Sleep Health")
        st.write("Quality sleep is fundamental to overall wellbeing and self-care.")
        
        # Sleep recommendations
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div style="background-color: #81c8bc20; padding: 15px; border-radius: 10px; height: 150px; text-align: center;">
                <h3 style="color: #81c8bc;">7-9 Hours</h3>
                <p>Recommended sleep for adults</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: #f49ac120; padding: 15px; border-radius: 10px; height: 150px; text-align: center;">
                <h3 style="color: #f49ac1;">6.8 Hours</h3>
                <p>Community average sleep time</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div style="background-color: #ffd96620; padding: 15px; border-radius: 10px; height: 150px; text-align: center;">
                <h3 style="color: #ffd966;">30 Minutes</h3>
                <p>Average time to fall asleep</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Sleep tips
        st.subheader("Tips for Better Sleep")
        
        sleep_tips = [
            "Maintain a consistent sleep schedule",
            "Create a restful environment (dark, quiet, cool)",
            "Limit screen time before bed",
            "Avoid caffeine and large meals before sleeping",
            "Practice relaxation techniques before bedtime"
        ]
        
        for i, tip in enumerate(sleep_tips):
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="background-color: #81c8bc; color: white; border-radius: 50%; width: 25px; height: 25px; 
                            display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                    {i+1}
                </div>
                <div>{tip}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[2]:
        st.subheader("Nutrition")
        st.write("Proper nutrition is a cornerstone of physical self-care.")
        
        # Nutrition guidance
        st.image("https://www.myplate.gov/sites/default/files/styles/medium/public/2020-11/myplate-graphics-fruits-vegetables.png", 
                 caption="Sample balanced plate illustration")
        
        st.subheader("Hydration Tracking")
        
        # Sample hydration data
        hydration_data = {
            'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            'Water (oz)': [64, 72, 68, 56, 80, 76, 70]
        }
        
        hydration_df = pd.DataFrame(hydration_data)
        
        hydration_fig = px.line(
            hydration_df,
            x='Day', 
            y='Water (oz)',
            markers=True,
            line_shape='spline',
            title='Weekly Hydration Tracking',
            color_discrete_sequence=['#6aa5cb']
        )
        
        hydration_fig.update_layout(
            xaxis_title='Day of Week',
            yaxis_title='Water Intake (oz)',
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        hydration_fig.add_shape(
            type="line",
            x0=0, y0=64, x1=6, y1=64,
            line=dict(color="#f49ac1", width=2, dash="dash"),
            name="Recommended"
        )
        
        hydration_fig.add_annotation(
            x=0.5, y=64,
            text="Recommended daily intake (64 oz)",
            showarrow=False,
            yshift=10,
            font=dict(color="#f49ac1")
        )
        
        st.plotly_chart(hydration_fig, use_container_width=True)
    
    with tabs[3]:
        st.subheader("Physical Health Resources")
        
        # Resource cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="border: 1px solid #e1e1e1; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
                <h4 style="color: #81c8bc;">30-Day Wellness Challenge</h4>
                <p>Join our community challenge to build healthy physical habits.</p>
                <a href="#" style="color: #81c8bc; text-decoration: none; font-weight: bold;">Learn More →</a>
            </div>
            
            <div style="border: 1px solid #e1e1e1; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
                <h4 style="color: #81c8bc;">Beginner Workout Guides</h4>
                <p>Simple, effective workouts you can do at home with minimal equipment.</p>
                <a href="#" style="color: #81c8bc; text-decoration: none; font-weight: bold;">Learn More →</a>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div style="border: 1px solid #e1e1e1; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
                <h4 style="color: #81c8bc;">Nutrition Planning Tools</h4>
                <p>Resources to help you plan balanced, nutritious meals.</p>
                <a href="#" style="color: #81c8bc; text-decoration: none; font-weight: bold;">Learn More →</a>
            </div>
            
            <div style="border: 1px solid #e1e1e1; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
                <h4 style="color: #81c8bc;">Sleep Improvement Course</h4>
                <p>A 4-week program to develop healthier sleep habits.</p>
                <a href="#" style="color: #81c8bc; text-decoration: none; font-weight: bold;">Learn More →</a>
            </div>
            """, unsafe_allow_html=True)
