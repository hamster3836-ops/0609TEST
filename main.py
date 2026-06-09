import streamlit as st
import time

# 1. 페이지 설정 (앱 이름, 아이콘, 레이아웃)
st.set_page_config(
    page_title="나의 미래 직업 찾기!",
    page_icon="🚀",
    layout="centered"
)

# 2. 학생 친화적인 커스텀 CSS 적용
st.markdown("""
    <style>
    .main {
        background-color: #F8F9FA;
    }
    h1 {
        color: #4A90E2;
        text-align: center;
        font-family: 'Apple SD Gothic Neo', sans-serif;
    }
    .job-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        border-left: 5px solid #4A90E2;
    }
    .job-title {
        color: #2C3E50;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .job-desc {
        color: #555555;
        font-size: 16px;
    }
    /* Streamlit 기본 메뉴 숨기기 (앱처럼 보이게) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. MBTI별 미래 유망 직업 데이터
mbti_data = {
    "ENFJ": {"title": "세상을 이끄는 따뜻한 리더 🌟", "jobs": [
        {"name": "🎓 에듀테크 기획자", "desc": "인공지능과 교육을 결합하여 새로운 학습 플랫폼과 코스를 기획합니다."},
        {"name": "😊 최고행복책임자 (CHO)", "desc": "기업이나 조직 내에서 구성원들의 웰빙과 멘탈 케어를 전담하는 리더입니다."}
    ]},
    "ENFP": {"title": "열정적인 아이디어 뱅크 💡", "jobs": [
        {"name": "🕶️ 메타버스 크리에이터", "desc": "가상 현실 세계에서 즐길 수 있는 공간, 게임, 아이템을 창작합니다."},
        {"name": "📈 트렌드 포어캐스터", "desc": "빅데이터와 사회 흐름을 분석하여 미래의 유행과 소비 트렌드를 예측합니다."}
    ]},
    "ENTJ": {"title": "비전을 실현하는 전략가 🎯", "jobs": [
        {"name": "🚀 테크 창업가", "desc": "혁신적인 IT 기술을 바탕으로 사회 문제를 해결하는 스타트업을 이끕니다."},
        {"name": "⚡ 신재생 에너지 전문가", "desc": "태양광, 풍력 등 친환경 에너지 시스템을 기획하고 관리합니다."}
    ]},
    "ENTP": {"title": "상상력이 풍부한 발명가 🛠️", "jobs": [
        {"name": "🤖 프롬프트 엔지니어", "desc": "AI가 최상의 결과를 낼 수 있도록 질문과 명령어를 정교하게 설계합니다."},
        {"name": "💡 혁신 전략 컨설턴트", "desc": "기업이 새로운 기술을 도입하고 혁신할 수 있도록 아이디어를 제공합니다."}
    ]},
    "ESFJ": {"title": "다정한 커뮤니티 빌더 🤝", "jobs": [
        {"name": "🌐 온라인 커뮤니티 매니저", "desc": "플랫폼 내의 유저들이 원활하게 소통할 수 있도록 환경을 조성하고 관리합니다."},
        {"name": "🩺 원격 의료 코디네이터", "desc": "환자가 비대면으로 진료를 받을 수 있도록 의료진과 환자 사이를 연결합니다."}
    ]},
    "ESFP": {"title": "에너지 넘치는 분위기 메이커 🎉", "jobs": [
        {"name": "🎬 실감형 콘텐츠(VR/AR) 디렉터", "desc": "사람들이 직접 체험하고 즐길 수 있는 가상/증강현실 콘텐츠를 연출합니다."},
        {"name": "📱 1인 미디어 창작자", "desc": "유튜브, 틱톡 등 다양한 플랫폼에서 자신만의 독창적인 콘텐츠를 기획하고 방송합니다."}
    ]},
    "ESTJ": {"title": "체계적인 시스템 관리자 📊", "jobs": [
        {"name": "📦 스마트 물류 관리자", "desc": "로봇과 AI를 활용하여 전 세계의 물류와 택배 시스템을 효율적으로 통제합니다."},
        {"name": "⚙️ 자동화 시스템 엔지니어", "desc": "공장이나 스마트 시티가 자동으로 돌아갈 수 있도록 시스템을 설계합니다."}
    ]},
    "ESTP": {"title": "도전을 즐기는 행동파 🚀", "jobs": [
        {"name": "🚁 드론 조종 및 관제사", "desc": "배송, 촬영, 인명 구조 등 다양한 목적으로 활용되는 드론을 조종하고 관리합니다."},
        {"name": "🚨 사이버 위기 대응 전문가", "desc": "해킹이나 시스템 다운 등 갑작스러운 디지털 위기 상황에 빠르게 대처합니다."}
    ]},
    "INFJ": {"title": "통찰력 있는 영감의 소유자 🔮", "jobs": [
        {"name": "⚖️ AI 윤리 전문가", "desc": "인공지능이 인간에게 해를 끼치지 않고 공정하게 판단하도록 규칙을 만듭니다."},
        {"name": "🧠 디지털 멘탈 헬스케어 기획자", "desc": "우울증, 불안 등을 치료할 수 있는 스마트폰 앱이나 VR 프로그램을 기획합니다."}
    ]},
    "INFP": {"title": "이상적인 세상을 꿈꾸는 아티스트 🎨", "jobs": [
        {"name": "🌍 ESG 컨설턴트", "desc": "환경 보호와 사회적 책임을 다하면서 기업이 성장할 수 있도록 돕습니다."},
        {"name": "👾 버추얼 캐릭터 디자이너", "desc": "가상 세계나 게임 속에서 살아 숨 쉬는 매력적인 캐릭터의 성격과 외모를 디자인합니다."}
    ]},
    "INTJ": {"title": "논리적인 미래 설계자 📐", "jobs": [
        {"name": "데이터 과학자", "desc": "엄청난 양의 데이터 속에서 숨겨진 패턴을 찾아내어 미래를 예측합니다."},
        {"name": "⚛️ 양자 컴퓨터 연구원", "desc": "현재의 슈퍼컴퓨터보다 수백만 배 빠른 미래형 양자 컴퓨터를 연구합니다."}
    ]},
    "INTP": {"title": "호기심 많은 아이디어 탐구자 🔍", "jobs": [
        {"name": "🛡️ 정보 보안 전문가", "desc": "해커들의 공격으로부터 소중한 정보와 서버를 지켜내는 사이버 경찰입니다."},
        {"name": "⛓️ 블록체인 개발자", "desc": "가상화폐, NFT 등 보안이 생명인 탈중앙화 디지털 기술을 개발합니다."}
    ]},
    "ISFJ": {"title": "섬세하고 따뜻한 수호자 🛡️", "jobs": [
        {"name": "🌱 스마트 팜 운영자", "desc": "IT 기술을 농업에 접목하여 날씨에 상관없이 친환경 작물을 기르고 관리합니다."},
        {"name": "⌚ 웨어러블 헬스케어 기획자", "desc": "스마트워치처럼 몸에 착용하여 건강을 관리해 주는 기기를 기획합니다."}
    ]},
    "ISFP": {"title": "따뜻한 감성을 지닌 예술가 🖌️", "jobs": [
        {"name": "♻️ 지속가능한 패션 디자이너", "desc": "버려지는 자원을 재활용하거나 친환경 소재를 사용하여 아름다운 옷을 만듭니다."},
        {"name": "📱 UI/UX 디자이너", "desc": "사용자들이 스마트폰 앱이나 웹사이트를 편리하고 예쁘게 사용할 수 있도록 디자인합니다."}
    ]},
    "ISTJ": {"title": "책임감 강한 원칙주의자 📋", "jobs": [
        {"name": "🚗 자율주행 차량 테스트 엔지니어", "desc": "운전자 없이 스스로 달리는 자동차가 안전하게 도로를 주행할 수 있도록 꼼꼼히 테스트합니다."},
        {"name": "☁️ 클라우드 아키텍트", "desc": "기업의 방대한 자료를 안전하게 보관하고 관리할 수 있는 가상 서버를 설계합니다."}
    ]},
    "ISTP": {"title": "논리적이고 뛰어난 손재주 🔧", "jobs": [
        {"name": "🦾 로봇 공학 기술자", "desc": "인간을 대신하여 위험한 일을 하거나 일상을 돕는 스마트 로봇을 개발하고 수리합니다."},
        {"name": "🌐 IoT(사물인터넷) 설계자", "desc": "집안의 가전제품이나 도시의 신호등을 인터넷으로 연결하여 똑똑하게 만듭니다."}
    ]}
}

# 4. 메인 UI 구성
st.title("🚀 나의 MBTI, 나의 미래 직업!")
st.write("안녕! 너의 성격 유형을 선택하면, 미래에 가장 잘 어울리는 멋진 직업을 추천해 줄게. 😎")
st.divider()

# 5. MBTI 선택 섹션 (4가지 지표를 버튼식으로 선택)
st.subheader("📌 너의 MBTI는 무엇이니?")

col1, col2, col3, col4 = st.columns(4)

with col1:
    e_i = st.radio("에너지 방향", ["E (외향)", "I (내향)"])
with col2:
    s_n = st.radio("인식 방식", ["S (감각)", "N (직관)"])
with col3:
    t_f = st.radio("판단 방식", ["T (사고)", "F (감정)"])
with col4:
    j_p = st.radio("생활 양식", ["J (판단)", "P (인식)"])

# 선택된 MBTI 문자열 조합
user_mbti = e_i[0] + s_n[0] + t_f[0] + j_p[0]

st.divider()

# 6. 결과 확인 버튼 및 애니메이션
if st.button("✨ 내 미래 직업 확인하기", use_container_width=True):
    with st.spinner("미래의 너를 만나러 가는 중... 🚀"):
        time.sleep(1.5) # 학생들의 기대감을 높이는 짧은 딜레이
        
    result = mbti_data[user_mbti]
    
    st.balloons() # 풍선 애니메이션으로 흥미 유발
    
    st.success(f"### 🎉 당신은 **{user_mbti}**! ({result['title']})")
    st.write("이런 미래 직업들은 어때요?")
    
    # 직업 카드 출력
    for job in result['jobs']:
        st.markdown(f"""
        <div class="job-card">
            <div class="job-title">{job['name']}</div>
            <div class="job-desc">{job['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
