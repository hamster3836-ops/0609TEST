import streamlit as st
import random
import datetime
import urllib.parse

# 1. 페이지 설정
st.set_page_config(
    page_title="오늘의 저녁",
    page_icon="🍽️",
    layout="centered"
)

# 2. 미니멀리즘 커스텀 CSS
st.markdown("""
    <style>
    .main {
        background-color: #FAFAFA;
        font-family: 'Pretendard', 'Apple SD Gothic Neo', sans-serif;
    }
    h1, h2, h3 {
        color: #333333;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
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
    .menu-box {
        padding: 30px;
        background-color: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #EEEEEE;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    .menu-title {
        font-size: 28px;
        font-weight: bold;
        color: #111111;
        margin-bottom: 10px;
    }
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

# 4. 데이터: 기분별 메뉴, 칼로리, 맞춤 운동, 조리시간, 재료, 레시피
menu_data = {
    "🔥 스트레스 팍! (매운맛)": [
        {"name": "매운 쭈꾸미 볶음", "calories": "약 350 kcal", "exercise": "스트레스 날리는 허공 펀치 30회 & 가벼운 제자리 뛰기 3분", 
         "time": "20분", "ingredients": "쭈꾸미 500g, 대파 1대, 양파 1/2개, 청양고추 2개, 고추장 2큰술, 고춧가루 3큰술, 진간장 2큰술, 다진마늘 1큰술, 매실액 1큰술, 콩나물 한 줌", 
         "recipe": "1. 쭈꾸미를 밀가루로 문질러 씻습니다.\n2. 고추장, 고춧가루, 간장, 다진마늘, 매실액으로 양념장을 만듭니다.\n3. 파와 양파를 기름에 볶다가 쭈꾸미와 양념장을 넣고 센 불에 빠르게 볶아냅니다.\n4. 데친 콩나물을 곁들이면 더욱 맛있습니다."},
        {"name": "국물 닭발", "calories": "약 400 kcal", "exercise": "매운맛 달래주는 시원한 폼롤러 전신 마사지 10분", 
         "time": "40분", "ingredients": "뼈 있는 닭발 500g, 고추장 2큰술, 고춧가루 4큰술, 청양고추 3개, 진간장 3큰술, 올리고당 2큰술, 다진마늘 2큰술, 후추 약간", 
         "recipe": "1. 닭발을 끓는 물에 한번 데쳐 잡내를 제거합니다.\n2. 고추장, 고춧가루, 청양고추, 간장, 올리고당을 섞어 매운 양념을 만듭니다.\n3. 냄비에 닭발과 양념, 물을 자작하게 붓고 푹 끓여줍니다.\n4. 주먹밥과 계란찜을 꼭 곁들여 드세요."}
    ],
    "🛌 너무 피곤해 (든든한 국물)": [
        {"name": "차돌박이 된장찌개", "calories": "약 450 kcal (밥 포함 750 kcal)", "exercise": "따뜻한 물로 샤워 후, 침대 위에서 L자 다리 휴식 10분", 
         "time": "20분", "ingredients": "차돌박이 150g, 시판 된장 3큰술, 고추장 1큰술, 애호박 1/3개, 양파 1/2개, 두부 1/2모, 쌀뜨물, 청양고추 1개", 
         "recipe": "1. 뚝배기에 차돌박이를 먼저 볶아 기름을 냅니다.\n2. 쌀뜨물을 붓고 된장과 고추장을 3:1 비율로 풉니다.\n3. 애호박, 양파, 두부, 버섯을 썰어 넣고 끓입니다.\n4. 마지막에 청양고추와 파를 썰어 넣어 칼칼함을 더합니다."},
        {"name": "뜨끈한 스지 어묵탕", "calories": "약 300 kcal", "exercise": "뭉친 어깨와 목을 부드럽게 풀어주는 앉아서 하는 요가 5분", 
         "time": "50분 (스지 삶는 시간 포함)", "ingredients": "스지(소 힘줄) 300g, 꼬치 어묵 4~5개, 무 1토막, 대파 1대, 다시마 2장, 국간장 2큰술, 쑥갓 한 줌", 
         "recipe": "1. 스지를 핏물을 빼고 푹 삶아 부드럽게 만듭니다.\n2. 무와 대파, 다시마로 맑은 육수를 냅니다.\n3. 꼬치 어묵과 삶은 스지를 육수에 넣고 국간장으로 간을 맞춥니다.\n4. 불을 끄고 쑥갓을 올려 향긋하게 마무리합니다."}
    ],
    "✨ 기분 전환이 필요해 (특별한 요리)": [
        {"name": "트러플 크림 파스타", "calories": "약 600 kcal", "exercise": "좋아하는 신나는 음악 틀어놓고 리듬 타며 방 청소하기 15분", 
         "time": "20분", "ingredients": "파스타 면 1인분, 양송이버섯 3개, 양파 1/4개, 생크림 150ml, 우유 100ml, 버터 1조각, 트러플 오일 약간, 파마산 치즈", 
         "recipe": "1. 파스타 면을 알단테로 삶아 건져냅니다.\n2. 팬에 버터를 두르고 다진 양파와 버섯을 볶습니다.\n3. 생크림과 우유를 붓고 끓이다가 면을 넣고 졸입니다.\n4. 소금, 후추로 간을 하고 마지막에 트러플 오일을 몇 방울 뿌려 풍미를 더합니다."},
        {"name": "비프 스테이크", "calories": "약 700 kcal", "exercise": "소화 촉진을 위한 선선한 밤공기 마시며 동네 산책 20분", 
         "time": "30분", "ingredients": "소고기 안심 또는 등심 200g, 올리브오일, 소금, 후추, 버터 2조각, 통마늘 5알, 로즈마리 또는 타임 1줄기", 
         "recipe": "1. 소고기를 상온에 30분 꺼내두고 소금, 후추, 올리브오일로 마리네이드합니다.\n2. 팬을 아주 뜨겁게 달군 후 고기를 올려 겉면을 튀기듯 굽습니다.\n3. 버터와 마늘, 허브를 넣고 고기에 끼얹으며 굽습니다.\n4. 고기를 꺼내 5분간 레스팅 한 후 썰어 먹습니다."}
    ],
    "🥗 가볍고 속 편하게 (건강식)": [
        {"name": "연어 아보카도 포케", "calories": "약 400 kcal", "exercise": "건강한 몸을 위한 코어 강화 플랭크 1분 x 3세트", 
         "time": "15분", "ingredients": "생연어 150g, 아보카도 1/2개, 오이 1/4개, 양파 1/4개, 현미밥 1공기, 간장 1큰술, 참기름 1작은술, 스리라차 소스 약간", 
         "recipe": "1. 생연어를 깍둑썰기하여 간장, 참기름, 스리라차 소스에 살짝 버무립니다.\n2. 현미밥을 그릇에 담고 위에 연어, 슬라이스한 아보카도, 오이, 양파를 올립니다.\n3. 김가루와 날치알, 깨를 뿌려줍니다.\n4. 취향에 따라 스리라차 마요 소스를 곁들여 비벼 먹습니다."},
        {"name": "닭가슴살 샐러드 랩", "calories": "약 350 kcal", "exercise": "가벼워진 몸으로 전신 스쿼트 15회 x 3세트", 
         "time": "10분", "ingredients": "통밀 또띠아 1장, 조리된 닭가슴살 1팩, 로메인 상추 3장, 토마토 1/2개, 머스타드 또는 그릭 요거트 2큰술", 
         "recipe": "1. 통밀 또띠아를 마른 팬에 살짝 굽습니다.\n2. 닭가슴살을 찢어 머스타드나 그릭 요거트에 버무립니다.\n3. 또띠아 위에 로메인(상추), 토마토, 닭가슴살을 올립니다.\n4. 단단하게 말아 반으로 썰어 먹습니다."}
    ],
    "☔ 비가 주룩주룩 (기름진 전과 면)": [
        {"name": "바삭한 해물파전", "calories": "약 550 kcal", "exercise": "창밖 빗소리 들으며 실내 자전거 타기 15분 (없다면 제자리 걷기)", 
         "time": "20분", "ingredients": "쪽파 한 줌, 오징어 1/2마리, 새우살 약간, 부침가루 1컵, 튀김가루 1/2컵, 얼음물 1.5컵, 달걀 1개", 
         "recipe": "1. 쪽파를 썰고 오징어, 새우 등 해물을 준비합니다.\n2. 부침가루와 튀김가루를 얼음물과 섞어 묽은 반죽을 만듭니다.\n3. 기름을 넉넉히 두른 팬에 파를 올리고 해물과 반죽을 부어 바삭하게 굽습니다.\n4. 초간장을 곁들여 막걸리와 함께 즐깁니다."},
        {"name": "시원한 바지락 칼국수", "calories": "약 500 kcal", "exercise": "누워서 하는 가벼운 자전거 타기(하늘 자전거) 동작 5분", 
         "time": "30분", "ingredients": "해감된 바지락 300g, 칼국수 면 1인분, 애호박 1/4개, 당근 약간, 멸치 다시마 육수 3컵, 국간장 1큰술, 다진마늘 1작은술", 
         "recipe": "1. 멸치와 다시마로 진한 육수를 냅니다.\n2. 육수가 끓으면 건더기를 건져내고 칼국수 면과 애호박, 당근, 바지락을 넣습니다.\n3. 바지락이 입을 벌리고 면이 익을 때까지 끓입니다.\n4. 국간장과 소금으로 간을 하고 청양고추를 송송 썰어 넣습니다."}
    ],
    "💸 월급날! 나를 위한 플렉스 (고급 요리)": [
        {"name": "버터갈릭 랍스터 구이", "calories": "약 450 kcal", "exercise": "기분 좋게 팔 벌려 뛰기(PT 체조) 20회", 
         "time": "25분", "ingredients": "랍스터 1마리, 버터 2큰술, 다진마늘 1큰술, 꿀 1작은술, 파슬리 가루, 모짜렐라 치즈 1줌", 
         "recipe": "1. 랍스터를 깨끗이 씻어 반으로 가릅니다.\n2. 녹인 버터에 다진 마늘, 파슬리, 꿀을 섞어 소스를 만듭니다.\n3. 랍스터 살 위에 소스를 듬뿍 바르고 모짜렐라 치즈를 올립니다.\n4. 180도 오븐이나 에어프라이어에서 15~20분간 노릇하게 굽습니다."},
        {"name": "양갈비 스테이크", "calories": "약 650 kcal", "exercise": "기지개 시원하게 켜고, 폼롤러로 등 근육 풀어주기 10분", 
         "time": "25분", "ingredients": "양갈비(프렌치랙) 2~3대, 올리브오일, 소금, 후추, 로즈마리, 통마늘, 가니쉬용 채소(방울토마토, 아스파라거스)", 
         "recipe": "1. 양갈비 핏물을 닦고 올리브유, 소금, 후추, 로즈마리로 10분간 밑간을 합니다.\n2. 뜨겁게 달군 팬에 양갈비를 올리고 앞뒤로 겉면을 바싹 굽습니다.\n3. 불을 줄이고 속까지 원하는 굽기로 익힌 후 5분간 레스팅합니다.\n4. 민트 젤리나 쯔란을 곁들여 먹습니다."}
    ],
    "🛋️ 다 귀찮아.. (초간단 레시피)": [
        {"name": "버터 간장계란밥", "calories": "약 480 kcal", "exercise": "오늘은 무리하지 마세요! 숨쉬기 운동 및 꿀잠 자기 😴", 
         "time": "5분", "ingredients": "따뜻한 밥 1공기, 달걀 1개, 버터 1조각, 간장 1.5큰술, 참기름 1작은술, 통깨 약간", 
         "recipe": "1. 따뜻한 밥 한 공기를 준비합니다.\n2. 계란 프라이를 반숙으로 부칩니다.\n3. 밥 위에 버터 한 조각과 계란 프라이를 올립니다.\n4. 간장 1.5큰술과 참기름을 두르고 쓱쓱 비벼 먹습니다. 김자반을 추가하면 완벽합니다."},
        {"name": "스팸 참치마요 덮밥", "calories": "약 650 kcal", "exercise": "방 안에서 물 한잔 마시며 3분만 가볍게 서성거리기", 
         "time": "10분", "ingredients": "밥 1공기, 스팸 1/4캔, 캔참치 1/2캔, 마요네즈 2큰술, 김가루 한 줌", 
         "recipe": "1. 스팸을 깍둑썰기하여 바싹 굽고, 참치는 기름을 꽉 짭니다.\n2. 그릇에 밥을 담고 스팸과 참치를 올립니다.\n3. 마요네즈를 지그재그로 뿌리고 김가루를 얹습니다.\n4. 냉장고에 남은 스크램블 에그나 양파 볶음이 있다면 더 올려줍니다."}
    ],
    "🍷 혼술 한잔 하고 싶은 밤 (안주거리)": [
        {"name": "감바스 알 아히요", "calories": "약 550 kcal", "exercise": "알코올 분해를 돕는 따뜻한 물 한잔과 목 스트레칭 3분", 
         "time": "15분", "ingredients": "새우 10~15마리, 통마늘 10알, 페페론치노 4~5개, 방울토마토 4개, 올리브오일 1컵, 소금, 후추, 바게트 빵", 
         "recipe": "1. 팬에 올리브오일을 넉넉히 붓고 편마늘과 페페론치노를 넣어 약불에서 향을 냅니다.\n2. 마늘이 노릇해지면 손질한 새우를 넣고 소금, 후추로 간을 합니다.\n3. 새우가 익으면 방울토마토와 파슬리를 넣고 가볍게 섞어줍니다.\n4. 바게트 빵을 곁들여 오일에 찍어 먹습니다."},
        {"name": "삼겹살 숙주볶음", "calories": "약 600 kcal", "exercise": "벽 짚고 서서 종아리 늘려주는 스트레칭 5분", 
         "time": "15분", "ingredients": "대패 삼겹살 200g, 숙주 1봉지(200g), 굴소스 1큰술, 간장 1큰술, 설탕 1/2작은술, 다진마늘 1큰술", 
         "recipe": "1. 대패 삼겹살이나 얇은 돼지고기를 팬에 굽습니다.\n2. 고기가 반쯤 익으면 굴소스, 간장, 설탕, 다진마늘을 넣고 볶습니다.\n3. 고기가 다 익으면 씻어둔 숙주를 듬뿍 넣고 센 불에서 빠르게 1분만 볶아냅니다.\n4. 아삭한 식감이 살아있을 때 불을 끄고 통깨를 뿌립니다."}
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
    calories = recommended["calories"]
    exercise = recommended["exercise"]
    time_taken = recommended["time"]
    ingredients = recommended["ingredients"]
    recipe_text = recommended["recipe"]
    
    # 결과 출력
    st.markdown(f"""
        <div class="menu-box">
            <div style="color: #666; font-size: 16px;">{selected_date.strftime('%Y년 %m월 %d일')}의 추천 메뉴</div>
            <div class="menu-title">{menu_name}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 칼로리 및 운동 추천 박스
    st.info(f"🔥 **예상 칼로리**: {calories}  \n🏃‍♂️ **추천 운동**: {exercise}")
    
    # 레시피 (접었다 펼칠 수 있게)
    with st.expander("👨‍🍳 직접 만들어 볼까요? (재료 및 레시피 보기)"):
        st.write(f"⏱️ **예상 조리 시간**: {time_taken}")
        st.write(f"🛒 **필요한 재료**: {ingredients}")
        st.write("---")
        st.write("📝 **조리 순서**:")
        st.write(recipe_text)
        
    # 맛집 찾기 (네이버 지도 링크 생성)
    if location:
        search_query = urllib.parse.quote(f"{location} {menu_name} 맛집")
        map_url = f"https://map.naver.com/v5/search/{search_query}"
        
        st.write("---")
        st.markdown(f"""
            <a href="{map_url}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #03C75A; color: white; padding: 15px; text-align: center; border-radius: 8px; font-weight: bold; font-size: 16px;">
                    🗺️ 네이버 지도에서 '{location} {menu_name}' 맛집 검색하기
                </div>
            </a>
        """, unsafe_allow_html=True)
    else:
        st.warning("위치를 상단에 입력하시면 근처 맛집 검색 링크를 제공해 드립니다.")
