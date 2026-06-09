import streamlit as st
import random
import datetime
import urllib.parse

# 1. 페이지 설정 (미니멀하고 세련된 느낌)
st.set_page_config(
    page_title="오늘의 저녁",
    page_icon="🍽️",
    layout="centered"
)

# 2. 미니멀리즘 커스텀 CSS
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 */
    .main {
        background-color: #FAFAFA;
        font-family: 'Pretendard', 'Apple SD Gothic Neo', sans-serif;
    }
    /* 헤더 스타일 */
    h1, h2, h3 {
        color: #333333;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    /* 응원 문구 카드 */
    .quote-box {
        padding: 30px;
        background-color: #FFFFFF;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
        text-align: center;
        margin-bottom: 30px;
        border-top: 3px solid #6c757d;
    }
    .quote-text {
        color: #555555;
        font-size: 18px;
        font-weight: 500;
        line-height: 1.6;
    }
    /* 메뉴 결과 카드 */
    .menu-box {
        padding: 30px;
        background-color: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #EEEEEE;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .menu-title {
        font-size: 28px;
        font-weight: bold;
        color: #111111;
        margin-bottom: 10px;
    }
    /* 버튼 스타일 조정 */
    .stButton>button {
        background-color: #333333;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #555555;
        color: white;
    }
    /* 불필요한 기본 UI 숨기기 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. 데이터: 응원 글귀
quotes = [
    "오늘 하루도 정말 고생 많으셨습니다. 맛있는 저녁으로 스스로를 다독여주세요.",
    "완벽하지 않아도 괜찮아요. 무사히 오늘을 마친 것만으로도 당신은 충분히 멋집니다.",
    "수많은 별 중 당신이 가장 빛나는 밤입니다. 편안한 저녁 시간 보내세요.",
    "바쁘게 달려온 오늘, 이제는 당신만의 쉼표를 찍을 시간입니다.",
    "당신의 땀방울은 절대 배신하지 않습니다. 오늘 저녁은 온전히 당신을 위해 즐기세요."
]

# 4. 데이터: 기분별 메뉴 및 레시피
menu_data = {
    "스트레스 팍! (매운맛)": [
        {"name": "🔥 매운 쭈꾸미 볶음", "recipe": "1. 쭈꾸미를 밀가루로 문질러 씻습니다.\n2. 고추장, 고춧가루, 간장, 다진마늘, 매실액으로 양념장을 만듭니다.\n3. 파와 양파를 기름에 볶다가 쭈꾸미와 양념장을 넣고 센 불에 빠르게 볶아냅니다.\n4. 콩나물을 곁들이면 더욱 맛있습니다."},
        {"name": "🔥 국물 닭발", "recipe": "1. 닭발을 끓는 물에 한번 데쳐 잡내를 제거합니다.\n2. 고추장, 고춧가루, 청양고추, 간장, 올리고당을 섞어 매운 양념을 만듭니다.\n3. 냄비에 닭발과 양념, 물을 자작하게 붓고 푹 끓여줍니다.\n4. 주먹밥과 계란찜을 꼭 곁들여 드세요."}
    ],
    "너무 피곤해 (든든한 국물)": [
        {"name": "🍲 차돌박이 된장찌개", "recipe": "1. 뚝배기에 차돌박이를 먼저 볶아 기름을 냅니다.\n2. 쌀뜨물을 붓고 된장과 고추장을 3:1 비율로 풉니다.\n3. 애호박, 양파, 두부, 버섯을 썰어 넣고 끓입니다.\n4. 마지막에 청양고추와 파를 썰어 넣어 칼칼함을 더합니다."},
        {"name": "🍲 뜨끈한 스지 어묵탕", "recipe": "1. 스지(소 힘줄)를 핏물을 빼고 푹 삶아 부드럽게 만듭니다.\n2. 무와 대파, 다시마로 맑은 육수를 냅니다.\n3. 꼬치 어묵과 삶은 스지를 육수에 넣고 국간장으로 간을 맞춥니다.\n4. 쑥갓을 올려 향긋하게 마무리합니다."}
    ],
    "기분 전환이 필요해 (특별한 요리)": [
        {"name": "🍝 트러플 크림 파스타", "recipe": "1. 파스타 면을 알단테로 삶아 건져냅니다.\n2. 팬에 버터를 두르고 다진 양파와 버섯을 볶습니다.\n3. 생크림과 우유를 붓고 끓이다가 면을 넣고 졸입니다.\n4. 소금, 후추로 간을 하고 마지막에 트러플 오일을 몇 방울 뿌려 풍미를 더합니다."},
        {"name": "🥩 비프 스테이크", "recipe": "1. 소고기(등심 또는 안심)를 상온에 30분 꺼내두고 소금, 후추, 올리브오일로 마리네이드합니다.\n2. 팬을 아주 뜨겁게 달군 후 고기를 올려 겉면을 튀기듯 굽습니다(시어링).\n3. 버터와 마늘, 타임(허브)을 넣고 고기에 끼얹으며 굽습니다.\n4. 고기를 꺼내 5분간 레스팅(휴지) 한 후 썰어 먹습니다."}
    ],
    "가볍고 속 편하게 (건강식)": [
        {"name": "🥗 연어 아보카도 포케", "recipe": "1. 생연어를 깍둑썰기하여 간장, 참기름, 스리라차 소스에 살짝 버무립니다.\n2. 현미밥을 그릇에 담고 위에 연어, 슬라이스한 아보카도, 오이, 양파를 올립니다.\n3. 김가루와 날치알, 깨를 뿌려줍니다.\n4. 취향에 따라 스리라차 마요 소스를 곁들여 비벼 먹습니다."},
        {"name": "🥙 닭가슴살 샐러드 랩", "recipe": "1. 통밀 또띠아를 마른 팬에 살짝 굽습니다.\n2. 닭가슴살을 찢어 머스타드나 그릭 요거트에 버무립니다.\n3. 또띠아 위에 로메인(상추), 토마토, 닭가슴살을 올립니다.\n4. 단단하게 말아 반으로 썰어 먹습니다."}
    ]
}

# 5. UI 구성: 상단 위로의 글귀
st.markdown(f"""
    <div class="quote-box">
        <div class="quote-text">"{random.choice(quotes)}"</div>
    </div>
""", unsafe_allow_html=True)

st.write("---")

# 6. 사용자 입력 섹션
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 날짜 선택")
    selected_date = st.date_input("언제의 저녁인가요?", datetime.date.today())

with col2:
    st.subheader("💭 오늘의 기분")
    selected_mood = st.selectbox(
        "지금 어떤 기분이신가요?",
        list(menu_data.keys())
    )

st.write("")
st.subheader("📍 나의 위치")
location = st.text_input("근처 맛집을 찾기 위해 동네 이름을 입력해 주세요. (예: 강남역, 서촌, 제주도 애월)", placeholder="동네 이름을 입력해주세요")

st.write("")

# 7. 메뉴 추천 및 결과 출력
if st.button("✨ 오늘의 저녁 메뉴 추천받기", use_container_width=True):
    # 선택한 기분에 맞는 메뉴 중 하나를 랜덤으로 선택
    recommended = random.choice(menu_data[selected_mood])
    menu_name = recommended["name"]
    recipe_text = recommended["recipe"]
    
    # 결과 출력
    st.markdown(f"""
        <div class="menu-box">
            <div style="color: #666; font-size: 16px;">{selected_date.strftime('%Y년 %m월 %d일')}의 추천 메뉴</div>
            <div class="menu-title">{menu_name}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 레시피 (접었다 펼칠 수 있게)
    with st.expander("👨‍🍳 직접 만들어 볼까요? (레시피 보기)"):
        st.write(recipe_text)
        
    # 맛집 찾기 (네이버 지도 링크 생성)
    if location:
        search_query = urllib.parse.quote(f"{location} {menu_name.split()[-1]} 맛집")
        map_url = f"https://map.naver.com/v5/search/{search_query}"
        
        st.info("👇 요리하기 지친다면? 근처 맛집을 찾아보세요!")
        st.markdown(f"""
            <a href="{map_url}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #03C75A; color: white; padding: 15px; text-align: center; border-radius: 8px; font-weight: bold; font-size: 16px;">
                    🗺️ 네이버 지도에서 '{location} {menu_name.split()[-1]}' 맛집 검색하기
                </div>
            </a>
        """, unsafe_allow_html=True)
    else:
        st.warning("위치를 입력하시면 근처 맛집 검색 링크를 제공해 드립니다.")
