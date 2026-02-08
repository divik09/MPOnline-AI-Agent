"""
MPPSC Study Dashboard
Comprehensive preparation tool with:
- Mains questions with answers
- Daily current affairs
- Mock tests with previous year papers
- Study progress tracking
"""
import streamlit as st
from datetime import datetime, date
import random

# Configure page for better viewing
st.set_page_config(
    page_title="MPPSC Study Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better visibility and larger text
st.markdown("""
<style>
    /* Larger fonts for better readability */
    .main .block-container {
        padding: 1rem 2rem;
        max-width: 100%;
    }
    
    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.5rem !important; }
    p, li { font-size: 1.1rem !important; }
    
    /* Quick action buttons - compact */
    .quick-action {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 20px;
        font-size: 0.9rem;
    }
    
    /* Daily progress - single line */
    .progress-bar {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    /* Large result cards */
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        font-size: 1.2rem;
    }
    
    /* Question cards */
    .question-card {
        background: #f8f9fa;
        border-left: 5px solid #667eea;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }
    
    /* Answer section */
    .answer-section {
        background: #e8f5e9;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Current affairs card */
    .ca-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sample Data
MAINS_QUESTIONS = {
    "GS Paper I": [
        {
            "question": "भारत में जाति व्यवस्था के विकास और इसके आधुनिक समाज पर प्रभाव की विवेचना करें। (Discuss the evolution of caste system in India and its impact on modern society.)",
            "marks": 20,
            "year": 2023,
            "answer": """
**जाति व्यवस्था का विकास (Evolution of Caste System):**

1. **वैदिक काल (Vedic Period):**
   - वर्ण व्यवस्था - ब्राह्मण, क्षत्रिय, वैश्य, शूद्र
   - कार्य आधारित विभाजन

2. **उत्तर वैदिक काल:**
   - जाति का जन्म आधारित होना
   - अंतर्जातीय विवाह पर रोक

3. **आधुनिक समाज पर प्रभाव:**
   - सामाजिक असमानता
   - राजनीतिक ध्रुवीकरण
   - आरक्षण नीति

**निष्कर्ष:** संवैधानिक प्रावधानों (अनुच्छेद 15, 17) द्वारा जाति भेदभाव समाप्त करने के प्रयास।
            """
        },
        {
            "question": "मध्य प्रदेश की जनजातीय संस्कृति और उनके विकास हेतु सरकारी प्रयासों का वर्णन करें।",
            "marks": 15,
            "year": 2022,
            "answer": """
**MP की प्रमुख जनजातियाँ:**
- भील, गोंड, कोरकू, सहरिया, बैगा

**सांस्कृतिक विशेषताएं:**
- भगोरिया हाट (भील)
- करमा नृत्य (गोंड)
- सैला नृत्य (बैगा)

**सरकारी प्रयास:**
1. ट्राइबल वेलफेयर डिपार्टमेंट
2. एकलव्य मॉडल स्कूल
3. वन अधिकार अधिनियम 2006
4. PESA Act 1996
            """
        }
    ],
    "GS Paper II": [
        {
            "question": "भारत में न्यायिक सक्रियता की अवधारणा और इसकी सीमाओं पर चर्चा करें।",
            "marks": 20,
            "year": 2023,
            "answer": """
**न्यायिक सक्रियता (Judicial Activism):**

**परिभाषा:** न्यायपालिका द्वारा कार्यपालिका और विधायिका की शक्तियों में हस्तक्षेप।

**उदाहरण:**
- विशाखा दिशानिर्देश
- पर्यावरण संरक्षण निर्णय
- PIL (जनहित याचिका)

**सीमाएं:**
1. शक्ति पृथक्करण का उल्लंघन
2. न्यायपालिका का अति भार
3. जवाबदेही का अभाव

**निष्कर्ष:** संतुलित दृष्टिकोण आवश्यक।
            """
        }
    ],
    "GS Paper III": [
        {
            "question": "मध्य प्रदेश में कृषि विपणन सुधारों और किसान कल्याण योजनाओं का मूल्यांकन करें।",
            "marks": 15,
            "year": 2022,
            "answer": """
**कृषि विपणन सुधार:**
1. e-NAM (राष्ट्रीय कृषि बाजार)
2. APMC Act संशोधन
3. किसान क्रेडिट कार्ड

**किसान कल्याण योजनाएं:**
- मुख्यमंत्री किसान कल्याण योजना
- प्रधानमंत्री फसल बीमा योजना
- सिंचाई योजनाएं

**चुनौतियां:**
- बिचौलियों की समस्या
- भंडारण सुविधाओं की कमी
            """
        }
    ]
}

CURRENT_AFFAIRS = [
    {
        "date": "08 Feb 2026",
        "topic": "राष्ट्रीय",
        "title": "केंद्रीय बजट 2026-27 की मुख्य बातें",
        "details": "वित्त मंत्री द्वारा आम बजट प्रस्तुत। कृषि क्षेत्र के लिए ₹2.5 लाख करोड़ का प्रावधान।"
    },
    {
        "date": "08 Feb 2026",
        "topic": "मध्य प्रदेश",
        "title": "MP में नई औद्योगिक नीति 2026 लागू",
        "details": "MSME क्षेत्र को प्रोत्साहन, 5 लाख नई नौकरियों का लक्ष्य।"
    },
    {
        "date": "07 Feb 2026",
        "topic": "अंतरराष्ट्रीय",
        "title": "भारत-जापान रक्षा समझौता",
        "details": "दोनों देशों के बीच द्विपक्षीय रक्षा सहयोग समझौते पर हस्ताक्षर।"
    },
    {
        "date": "07 Feb 2026",
        "topic": "विज्ञान",
        "title": "ISRO का नया उपग्रह प्रक्षेपण",
        "details": "GSLV-MkIII द्वारा संचार उपग्रह का सफल प्रक्षेपण।"
    }
]

MOCK_TEST_QUESTIONS = [
    {"q": "मध्य प्रदेश का राज्य पशु कौन सा है?", "options": ["A) बाघ", "B) बारहसिंगा", "C) हाथी", "D) शेर"], "answer": "B", "explanation": "बारहसिंगा MP का राज्य पशु है।"},
    {"q": "भोपाल के बड़े तालाब का निर्माण किसने करवाया?", "options": ["A) राजा भोज", "B) अकबर", "C) शाहजहां", "D) औरंगजेब"], "answer": "A", "explanation": "राजा भोज ने 11वीं शताब्दी में।"},
    {"q": "संविधान का अनुच्छेद 370 किससे संबंधित था?", "options": ["A) मौलिक अधिकार", "B) जम्मू-कश्मीर", "C) राष्ट्रपति", "D) संसद"], "answer": "B", "explanation": "जम्मू-कश्मीर को विशेष दर्जा।"},
    {"q": "MP में कितने संभाग हैं (2026)?", "options": ["A) 8", "B) 10", "C) 12", "D) 14"], "answer": "C", "explanation": "MP में 12 संभाग और 55 जिले हैं।"},
    {"q": "भारतीय संविधान में कितनी अनुसूचियां हैं?", "options": ["A) 8", "B) 10", "C) 12", "D) 14"], "answer": "C", "explanation": "मूल में 8, वर्तमान में 12।"},
]

# Sidebar
with st.sidebar:
    st.title("📚 MPPSC Study Hub")
    st.divider()
    
    menu = st.radio("📌 Menu", [
        "🏠 Dashboard",
        "📝 Mains Questions",
        "📰 Current Affairs",
        "🎯 Mock Test",
        "📊 Progress"
    ])
    
    st.divider()
    st.info(f"📅 Today: {date.today().strftime('%d %b %Y')}")

# Main Content
if menu == "🏠 Dashboard":
    st.title("🎓 MPPSC Preparation Dashboard")
    
    # Quick Actions - Compact single row
    st.subheader("⚡ Quick Actions")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.button("📝 Mains Q", use_container_width=True)
    with col2:
        st.button("📰 CA Today", use_container_width=True)
    with col3:
        st.button("🎯 Mock Test", use_container_width=True)
    with col4:
        st.button("📖 Syllabus", use_container_width=True)
    with col5:
        st.button("📊 Stats", use_container_width=True)
    
    # Daily Progress - Single line
    st.subheader("📈 Today's Progress")
    progress_col1, progress_col2, progress_col3, progress_col4 = st.columns(4)
    with progress_col1:
        st.metric("Questions", "15/20", "75%")
    with progress_col2:
        st.metric("CA Read", "8/10", "80%")
    with progress_col3:
        st.metric("Mock Score", "72/100", "+5")
    with progress_col4:
        st.metric("Study Hours", "4.5h", "▲ 1h")
    
    st.divider()
    
    # Featured Mains Question
    st.subheader("📝 Featured Mains Question")
    featured = random.choice(MAINS_QUESTIONS["GS Paper I"])
    with st.container():
        st.markdown(f"""
        <div class="question-card">
            <h4>📌 {featured['question']}</h4>
            <p><strong>Marks:</strong> {featured['marks']} | <strong>Year:</strong> {featured['year']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📖 View Model Answer", expanded=True):
            st.markdown(featured['answer'])
    
    # Today's Current Affairs
    st.subheader("📰 Today's Current Affairs")
    for ca in CURRENT_AFFAIRS[:2]:
        st.markdown(f"""
        <div class="ca-card">
            <strong>{ca['topic']}</strong>: {ca['title']}<br>
            <small>{ca['details']}</small>
        </div>
        """, unsafe_allow_html=True)

elif menu == "📝 Mains Questions":
    st.title("📝 MPPSC Mains Questions & Model Answers")
    
    paper = st.selectbox("Select Paper:", list(MAINS_QUESTIONS.keys()))
    
    for i, q in enumerate(MAINS_QUESTIONS[paper], 1):
        with st.expander(f"Q{i}. {q['question'][:100]}... ({q['marks']} marks)", expanded=False):
            st.markdown(f"**Full Question:** {q['question']}")
            st.markdown(f"**Marks:** {q['marks']} | **Year:** {q['year']}")
            st.divider()
            st.markdown("### 📖 Model Answer:")
            st.markdown(q['answer'])

elif menu == "📰 Current Affairs":
    st.title("📰 Daily Current Affairs")
    st.markdown(f"### 📅 {date.today().strftime('%d %B %Y')}")
    
    for ca in CURRENT_AFFAIRS:
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"**{ca['topic']}**")
            with col2:
                st.markdown(f"### {ca['title']}")
                st.markdown(ca['details'])
            st.divider()

elif menu == "🎯 Mock Test":
    st.title("🎯 Mock Test - Previous Year Questions")
    
    if 'score' not in st.session_state:
        st.session_state.score = 0
        st.session_state.answered = set()
    
    for i, q in enumerate(MOCK_TEST_QUESTIONS):
        st.markdown(f"### Q{i+1}. {q['q']}")
        answer = st.radio(f"Select answer for Q{i+1}:", q['options'], key=f"q{i}")
        
        if st.button(f"Check Answer Q{i+1}", key=f"btn{i}"):
            selected = answer[0]
            if selected == q['answer']:
                st.success(f"✅ Correct! {q['explanation']}")
            else:
                st.error(f"❌ Wrong. Correct: {q['answer']}. {q['explanation']}")
        st.divider()

elif menu == "📊 Progress":
    st.title("📊 Study Progress & Analytics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Weekly Study Hours", "32.5h", "+5.5h")
        st.metric("Questions Practiced", "245", "+48")
    with col2:
        st.metric("Mock Test Average", "68%", "+8%")
        st.metric("Current Affairs Read", "156", "+24")
    
    st.progress(0.75)
    st.caption("Overall Preparation: 75% Complete")

# Footer
st.divider()
st.caption("MPPSC Study Dashboard v1.0 | Built for serious aspirants 📚")
