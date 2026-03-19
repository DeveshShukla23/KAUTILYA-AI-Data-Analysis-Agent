# ============================================================
# KAUTILYA — AI-Powered Data Analysis Agent
# Built by: Devesh Shukla
# Tech: Groq (LLaMA3) + Streamlit + Voice + Auto Analysis
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
import re
import tempfile
from groq import Groq
try:
    import speech_recognition as sr
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
from gtts import gTTS
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
import time
import threading

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="KAUTILYA — AI Data Analysis Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #e94560;
    }
    .main-header h1 {
        color: #e94560;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 0 20px rgba(233,69,96,0.5);
    }
    .main-header p {
        color: #a8b2d8;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #e94560;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .chat-message-user {
        background: linear-gradient(135deg, #0f3460, #16213e);
        border-left: 4px solid #e94560;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .chat-message-ai {
        background: linear-gradient(135deg, #1a1a2e, #0f3460);
        border-left: 4px solid #00d4ff;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .insight-box {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #00d4ff;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #e94560, #c62a47);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #c62a47, #a01f38);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# GROQ CLIENT SETUP
# ============================================================
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "df" not in st.session_state:
    st.session_state.df = None
if "data_summary" not in st.session_state:
    st.session_state.data_summary = None
if "file_name" not in st.session_state:
    st.session_state.file_name = None
# ============================================================
# VOICE FUNCTIONS
# ============================================================
def speak(text):
    """Convert text to speech and play it"""
    try:
        clean_text = re.sub(r'[#*`]', '', text)
        clean_text = clean_text[:500]
        
        tts = gTTS(text=clean_text, lang='en', slow=False)
        
        with tempfile.NamedTemporaryFile(delete=False, 
                                          suffix='.mp3') as fp:
            temp_file = fp.name
        
        tts.save(temp_file)
        
        pygame.mixer.init()
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.unlink(temp_file)
        
    except Exception as e:
        st.warning(f"Voice output error: {e}")


def listen():
    """Capture voice input and convert to text"""
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            st.info("Listening... Speak now! (Hindi or English)")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10, 
                                       phrase_time_limit=15)
            
        st.info("Processing your voice...")
        
        # Try Hindi first, then English
        try:
            text = recognizer.recognize_google(
    audio, language="en-IN"
)
        except:
            text = recognizer.recognize_google(
                audio, language="en-IN"
            )
            
        return text
        
    except sr.WaitTimeoutError:
        return "Timeout: No speech detected. Please try again."
    except sr.UnknownValueError:
        return "Could not understand audio. Please try again."
    except Exception as e:
        return f"Microphone error: {str(e)}"


# ============================================================
# DATA LOADING FUNCTIONS
# ============================================================
def load_data(file_path):
    """Load CSV or Excel file into DataFrame"""
    try:
        if file_path.endswith('.csv'):
            # Try different encodings
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    return df
                except:
                    continue
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
            return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


def get_data_summary(df):
    """Generate comprehensive data summary for AI context"""
    summary = f"""
    DATASET OVERVIEW:
    - Total Rows: {df.shape[0]}
    - Total Columns: {df.shape[1]}
    - Column Names: {list(df.columns)}
    - Data Types: {df.dtypes.to_dict()}
    
    STATISTICAL SUMMARY:
    {df.describe().to_string()}
    
    MISSING VALUES:
    {df.isnull().sum().to_dict()}
    
    SAMPLE DATA (First 3 rows):
    {df.head(3).to_string()}
    """
    return summary


# ============================================================
# AI ANALYSIS FUNCTION
# ============================================================
def ask_kautilya(question, data_summary=None):
    """Send question to Groq AI and get response"""
    
    system_prompt = """You are KAUTILYA, an expert AI Data Analysis Agent. 
    You are named after the ancient Indian strategist Chanakya (Kautilya).
    
    Your capabilities:
    - Expert data analyst with deep knowledge of statistics
    - Business intelligence specialist
    - You provide actionable insights, not just numbers
    - You explain complex findings in simple language
    - You suggest visualizations when relevant
    - You are precise, professional, and insightful
    
    When analyzing data:
    1. Always provide key findings first
    2. Explain what the numbers mean for business
    3. Highlight anomalies or interesting patterns
    4. Give actionable recommendations
    5. Keep responses clear and structured
    
    Response format:
    - Use bullet points for clarity
    - Bold important numbers
    - Keep responses concise but complete
    """
    
    if data_summary:
        user_message = f"""
        Dataset Information:
        {data_summary}
        
        User Question: {question}
        
        Please analyze and provide detailed insights.
        """
    else:
        user_message = question
    
    messages = [{"role": "user", "content": user_message}]
    
    # Add conversation history
    for msg in st.session_state.messages[-6:]:
        messages.insert(0, {
            "role": msg["role"], 
            "content": msg["content"]
        })
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    
    return response.choices[0].message.content


# ============================================================
# AUTO VISUALIZATION FUNCTION
# ============================================================
def auto_visualize(df, viz_type, x_col=None, y_col=None):
    """Generate automatic visualizations based on data"""
    fig = None
    
    try:
        if viz_type == "Distribution":
            numeric_cols = df.select_dtypes(
                include=['number']
            ).columns[:4]
            fig, axes = plt.subplots(
                1, len(numeric_cols), 
                figsize=(15, 4)
            )
            if len(numeric_cols) == 1:
                axes = [axes]
            for i, col in enumerate(numeric_cols):
                axes[i].hist(
                    df[col].dropna(), 
                    bins=30, 
                    color='#e94560',
                    edgecolor='white',
                    alpha=0.8
                )
                axes[i].set_title(f'{col}', color='white')
                axes[i].set_facecolor('#1a1a2e')
                axes[i].tick_params(colors='white')
            plt.suptitle(
                'Distribution Analysis', 
                color='white', 
                fontsize=14
            )
            fig.patch.set_facecolor('#1a1a2e')
            
        elif viz_type == "Correlation Heatmap":
            numeric_df = df.select_dtypes(include=['number'])
            if len(numeric_df.columns) > 1:
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(
                    numeric_df.corr(),
                    annot=True,
                    fmt='.2f',
                    cmap='RdYlGn',
                    ax=ax,
                    linewidths=0.5
                )
                ax.set_title(
                    'Correlation Heatmap', 
                    color='white', 
                    fontsize=14
                )
                fig.patch.set_facecolor('#1a1a2e')
                ax.set_facecolor('#1a1a2e')
                
        elif viz_type == "Top Categories":
            cat_cols = df.select_dtypes(
                include=['object']
            ).columns
            if len(cat_cols) > 0:
                col = cat_cols[0]
                top_cats = df[col].value_counts().head(10)
                fig = px.bar(
                    x=top_cats.index,
                    y=top_cats.values,
                    title=f'Top Categories — {col}',
                    color=top_cats.values,
                    color_continuous_scale='Reds'
                )
                fig.update_layout(
                    plot_bgcolor='#1a1a2e',
                    paper_bgcolor='#1a1a2e',
                    font_color='white'
                )
                
        elif viz_type == "Missing Values":
            missing = df.isnull().sum()
            missing = missing[missing > 0]
            if len(missing) > 0:
                fig = px.bar(
                    x=missing.index,
                    y=missing.values,
                    title='Missing Values per Column',
                    color=missing.values,
                    color_continuous_scale='Reds'
                )
                fig.update_layout(
                    plot_bgcolor='#1a1a2e',
                    paper_bgcolor='#1a1a2e',
                    font_color='white'
                )
            else:
                st.success("No missing values found in dataset!")
                
    except Exception as e:
        st.error(f"Visualization error: {e}")
        
    return fig
# ============================================================
# SAMPLE DATA PATHS
# ============================================================
SAMPLE_DATASETS = {
    "NIFTY50 Stock Market Data": r"C:\Users\Dell\Data_Science_Project\06_Agentic_AI\sample_data\NIFTY50_all.csv",
    "E-Commerce Order Details": r"C:\Users\Dell\Data_Science_Project\06_Agentic_AI\sample_data\Order Details.csv",
    "Superstore Sales Data": r"C:\Users\Dell\Data_Science_Project\06_Agentic_AI\sample_data\Sample - Superstore.csv"
}

# ============================================================
# MAIN UI — HEADER
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>KAUTILYA</h1>
    <p>AI-Powered Data Analysis Agent | 
    Named after Ancient Indian Strategist Chanakya</p>
    <p>Upload your data • Ask questions • Get insights • 
    Voice enabled</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## Control Panel")
    st.markdown("---")
    
    # Data Source Selection
    st.markdown("### Data Source")
    data_source = st.radio(
        "Choose data source:",
        ["Upload Your File", "Use Sample Dataset"]
    )
    
    if data_source == "Upload Your File":
        uploaded_file = st.file_uploader(
            "Upload CSV or Excel file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload any CSV or Excel file for analysis"
        )
        
        if uploaded_file is not None:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=os.path.splitext(uploaded_file.name)[1]
            ) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            df = load_data(tmp_path)
            if df is not None:
                st.session_state.df = df
                st.session_state.file_name = uploaded_file.name
                st.session_state.data_summary = get_data_summary(df)
                st.success(f"Loaded: {uploaded_file.name}")
                
    else:
        selected_dataset = st.selectbox(
            "Choose sample dataset:",
            list(SAMPLE_DATASETS.keys())
        )
        
        if st.button("Load Dataset"):
         file_path = SAMPLE_DATASETS[selected_dataset]
         df = load_data(file_path)
         if df is not None:
             st.session_state.df = df
             st.session_state.file_name = selected_dataset
             st.session_state.data_summary = get_data_summary(df)
             st.session_state.messages = []  # Chat clear!
             st.success(f"Loaded: {selected_dataset}")
             st.rerun()
    
             st.markdown("---")
    
    # Voice Settings
    st.markdown("### Voice Settings")
    voice_enabled = st.toggle("Enable Voice Output", value=True)
    
    st.markdown("---")
    
    # Quick Questions
    st.markdown("### Quick Questions")
    quick_questions = [
        "Give me a complete overview of this dataset",
        "What are the top trends in this data?",
        "Find anomalies or outliers in the data",
        "What are the key business insights?",
        "Which columns have missing values?",
        "What is the correlation between variables?"
    ]
    
    for q in quick_questions:
      if st.button(q, key=f"quick_{q[:20]}"):
        if st.session_state.df is not None:
            with st.spinner("KAUTILYA is thinking..."):
                response = ask_kautilya(
                    q,
                    st.session_state.data_summary
                )
            st.session_state.messages.append({
                "role": "user",
                "content": q
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            st.rerun()
        else:
            st.warning("Please load a dataset first!")

# ============================================================
# MAIN CONTENT AREA
# ============================================================
if st.session_state.df is not None:
    df = st.session_state.df
    
    # Dataset Metrics
    st.markdown("### Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Rows", f"{df.shape[0]:,}")
    with col2:
        st.metric("Total Columns", df.shape[1])
    with col3:
        st.metric("Missing Values", 
                  f"{df.isnull().sum().sum():,}")
    with col4:
        numeric_cols = len(df.select_dtypes(
            include=['number']
        ).columns)
        st.metric("Numeric Columns", numeric_cols)
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "Chat with KAUTILYA",
        "Auto Visualizations", 
        "Data Explorer"
    ])
    
    # --------------------------------------------------------
    # TAB 1 — CHAT
    # --------------------------------------------------------
    with tab1:
        st.markdown("### Ask KAUTILYA Anything")
        
        # Display chat history
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(message["content"])
        
        # Input Methods
        col_text, col_voice = st.columns([3, 1])
        
        with col_text:
            user_input = st.text_input(
                "Type your question here...",
                placeholder="e.g. What are the top selling products?",
                key="text_input"
            )
        
        with col_voice:
            st.markdown("<br>", unsafe_allow_html=True)
            voice_btn = st.button("Speak")

      # Handle voice input
        if voice_btn:
            with st.spinner("Listening..."):
                voice_text = listen()
            if voice_text and "error" not in voice_text.lower() and "timeout" not in voice_text.lower():
                st.success(f"You said: {voice_text}")
                with st.spinner("KAUTILYA is thinking..."):
                    response = ask_kautilya(
                        voice_text,
                        st.session_state.data_summary
                    )
                st.session_state.messages.append({
                    "role": "user",
                    "content": voice_text
                })
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
                if voice_enabled:
                    threading.Thread(
                        target=speak,
                        args=(response,),
                        daemon=True
                    ).start()
                st.rerun()
            else:
                st.error(voice_text)  
        # Handle quick questions
        if hasattr(st.session_state, 'quick_question'):
            user_input = st.session_state.quick_question
            del st.session_state.quick_question
        
        # Process input
        col_send, col_auto = st.columns(2)
        
        with col_send:
            send_btn = st.button("Ask KAUTILYA")
        
        with col_auto:
            auto_btn = st.button("Auto Analyze Dataset")
        
        if send_btn and user_input:
            with st.spinner("KAUTILYA is thinking..."):
                response = ask_kautilya(
                    user_input,
                    st.session_state.data_summary
                )
            
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response
            })
            
            if voice_enabled:
                threading.Thread(
                    target=speak, 
                    args=(response,),
                    daemon=True
                ).start()
            
            st.rerun()
        
        if auto_btn:
            auto_question = """
            Please perform a complete analysis of this dataset:
            1. Overview and key statistics
            2. Most important patterns and trends
            3. Data quality issues if any
            4. Top 5 business insights
            5. Recommendations based on the data
            """
            with st.spinner(" KAUTILYA is analyzing..."):
                response = ask_kautilya(
                    auto_question,
                    st.session_state.data_summary
                )
            
            st.session_state.messages.append({
                "role": "user",
                "content": "Perform complete auto analysis"
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            
            if voice_enabled:
                threading.Thread(
                    target=speak,
                    args=(response,),
                    daemon=True
                ).start()
            
            st.rerun()
    
    # --------------------------------------------------------
    # TAB 2 — VISUALIZATIONS
    # --------------------------------------------------------
    with tab2:
        st.markdown("### Auto Visualizations")
        
        viz_type = st.selectbox(
            "Select Visualization Type:",
            [
                "Distribution",
                "Correlation Heatmap", 
                "Top Categories",
                "Missing Values"
            ]
        )
        
        if st.button("Generate Visualization"):
            with st.spinner("Generating..."):
                fig = auto_visualize(df, viz_type)
                if fig is not None:
                    if hasattr(fig, 'data'):
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.pyplot(fig)
                        plt.close()
                else:
                    st.info("This visualization is not available for current dataset. Try another type!")
    
    # --------------------------------------------------------
    # TAB 3 — DATA EXPLORER
    # --------------------------------------------------------
    with tab3:
        st.markdown("###  Data Explorer")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("####  Dataset Preview")
            rows_to_show = st.slider(
                "Number of rows:", 5, 50, 10
            )
            st.dataframe(
                df.head(rows_to_show),
                use_container_width=True
            )
        
        with col_b:
            st.markdown("####  Statistical Summary")
            st.dataframe(
                df.describe(),
                use_container_width=True
            )
        
        st.markdown("####  Column Information")
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Data Type': df.dtypes.values,
            'Non-Null Count': df.count().values,
            'Null Count': df.isnull().sum().values,
            'Unique Values': df.nunique().values
        })
        st.dataframe(col_info, use_container_width=True)

else:
    # --------------------------------------------------------
    # WELCOME SCREEN
    # --------------------------------------------------------
    st.markdown("""
    <div class="insight-box" style="text-align: center; 
    padding: 3rem;">
        <h2 style="color: #e94560;">
         Welcome to KAUTILYA</h2>
        <p style="color: #a8b2d8; font-size: 1.1rem;">
        Your AI-Powered Data Analysis Agent</p>
        <br>
        <p style="color: #a8b2d8;">
         Load a dataset from the sidebar to get started<br><br>
         Ask questions in text or voice<br><br>
         Get automatic visualizations<br><br>
         Explore your data with AI insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3></h3>
            <h4 style="color:#e94560">Smart Upload</h4>
            <p style="color:#a8b2d8">CSV & Excel support with auto encoding detection</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3></h3>
            <h4 style="color:#e94560">Voice Enabled</h4>
            <p style="color:#a8b2d8">Speak in Hindi or English — KAUTILYA understands</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3></h3>
            <h4 style="color:#e94560">AI Powered</h4>
            <p style="color:#a8b2d8">Groq LLaMA3 — fastest AI inference available</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3></h3>
            <h4 style="color:#e94560">Auto Insights</h4>
            <p style="color:#a8b2d8">Automatic visualizations & business insights</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #a8b2d8; padding: 1rem;">
    <p> <strong>KAUTILYA</strong> — AI Data Analysis Agent | 
    Built by <strong>Devesh Shukla</strong> | 
    Powered by <strong>Groq LLaMA3</strong></p>
</div>
""", unsafe_allow_html=True)
