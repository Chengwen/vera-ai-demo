from dataclasses import dataclass
from typing import Dict, List, Tuple

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Vera AI Mobile Demo",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
    <style>
    :root {
        --vera-primary: #f7a8c8;
        --vera-primary-light: #fff1f7;
        --vera-primary-mid: #ffdce9;
        --vera-primary-hover: #f9b7d1;
        --vera-primary-dark: #9f4771;
        --vera-text: #5f2643;
        --vera-body: #2b211c;
    }
    .stApp {
        background: linear-gradient(180deg, #fff7fb 0%, #fff1f7 45%, #ffeaf3 100%);
        color: var(--vera-body);
    }
    .block-container {
        max-width: 430px;
        padding-top: 1.1rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stSidebar"] { display: none; }
    .phone-shell {
        background: #fffaf6;
        color: var(--vera-body);
        border: 1px solid rgba(247, 168, 200, 0.42);
        box-shadow: 0 22px 55px rgba(247, 168, 200, 0.22);
        border-radius: 34px;
        padding: 18px 16px 22px 16px;
        margin-bottom: 18px;
    }
    [data-testid="stMarkdownContainer"],
    [data-testid="stText"],
    [data-testid="stWidgetLabel"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: #2b211c !important;
    }
    .status-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #4b3b32;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 14px;
    }
    .hero {
        background: linear-gradient(135deg, #f7a8c8 0%, #ef8bb7 55%, #d978a8 100%);
        color: white;
        border-radius: 26px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .hero, .hero h1, .hero p { color: white !important; }
    .hero h1 {
        font-size: 28px;
        line-height: 1.05;
        margin: 0 0 8px 0;
    }
    .hero p {
        margin: 0;
        opacity: 0.88;
        font-size: 14px;
    }
    .section-title {
        color: #2b211c;
        color: var(--vera-text);
        font-size: 18px;
        font-weight: 800;
        margin: 16px 0 8px 0;
    }
    .soft-card {
        background: white;
        color: #2b211c !important;
        border: 1px solid rgba(247, 168, 200, 0.30);
        border-radius: 22px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 8px 22px rgba(247, 168, 200, 0.12);
    }
    .soft-card, .soft-card b, .soft-card span, .soft-card div {
        color: #2b211c !important;
    }
    .pill {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: var(--vera-primary-light);
        color: var(--vera-primary-dark) !important;
        border: 1px solid rgba(247, 168, 200, 0.42);
        font-size: 12px;
        font-weight: 700;
        margin: 3px 4px 3px 0;
    }
    .decision-success {
        background: linear-gradient(135deg, #154d37 0%, #2f9b6b 100%);
        color: white;
        border-radius: 24px;
        padding: 18px;
        margin: 13px 0;
    }
    .decision-warning {
        background: linear-gradient(135deg, #74531b 0%, #d6942c 100%);
        color: white;
        border-radius: 24px;
        padding: 18px;
        margin: 13px 0;
    }
    .decision-error {
        background: linear-gradient(135deg, #6f2020 0%, #d45a51 100%);
        color: white;
        border-radius: 24px;
        padding: 18px;
        margin: 13px 0;
    }
    .decision-success, .decision-warning, .decision-error,
    .decision-success div, .decision-warning div, .decision-error div {
        color: white !important;
    }
    .decision-title {
        font-size: 21px;
        font-weight: 900;
        margin-bottom: 4px;
    }
    .decision-sub {
        opacity: 0.9;
        font-size: 13px;
    }
    .mini-label {
        font-size: 12px;
        color: var(--vera-primary-dark);
        margin-bottom: 3px;
    }
    .bottom-nav {
        display: flex;
        justify-content: space-around;
        background: linear-gradient(135deg, #ffdce9 0%, #f7a8c8 52%, #ef8bb7 100%);
        border-radius: 22px;
        color: #5f2643;
        padding: 11px 7px;
        margin-top: 18px;
        font-size: 12px;
        font-weight: 700;
    }
    .bottom-nav, .bottom-nav span { color: #5f2643 !important; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #fff1f7;
        padding: 5px;
        border-radius: 999px;
        border: 1px solid rgba(247, 168, 200, 0.40);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
        padding: 8px 10px;
        font-size: 13px;
        color: #9f4771 !important;
        font-weight: 800;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ffdce9 0%, #f7a8c8 52%, #ef8bb7 100%) !important;
        color: #5f2643 !important;
        box-shadow: 0 8px 18px rgba(247, 168, 200, 0.32);
    }
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span { color: #5f2643 !important; }
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] span,
    div[data-baseweb="popover"] {
        color: #2b211c !important;
    }
    div[data-baseweb="select"] > div {
        background: #fff7fb !important;
        border: 1.5px solid rgba(247, 168, 200, 0.62) !important;
        border-radius: 18px !important;
        box-shadow: 0 6px 16px rgba(247, 168, 200, 0.16);
    }
    div[data-baseweb="select"] svg {
        color: #d978a8 !important;
        fill: #d978a8 !important;
    }
    div[data-baseweb="popover"] ul,
    div[data-baseweb="menu"] {
        background: #fffaf6 !important;
        border: 1px solid rgba(247, 168, 200, 0.36) !important;
        border-radius: 16px !important;
    }
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"] *,
    ul[role="listbox"],
    ul[role="listbox"] * {
        background-color: #fffaf6 !important;
        color: #2b211c !important;
    }
    ul[role="listbox"] {
        background: #fffaf6 !important;
        border: 1px solid rgba(247, 168, 200, 0.36) !important;
        border-radius: 16px !important;
        overflow: hidden !important;
    }
    div[role="option"] {
        color: #2b211c !important;
        background: #fffaf6 !important;
    }
    li[role="option"],
    li[role="option"] *,
    div[role="option"],
    div[role="option"] * {
        background-color: #fffaf6 !important;
        color: #2b211c !important;
    }
    div[role="option"]:hover {
        background: #fff1f7 !important;
        color: #9f4771 !important;
    }
    li[role="option"]:hover,
    li[role="option"]:hover *,
    div[role="option"]:hover,
    div[role="option"]:hover * {
        background-color: #fff1f7 !important;
        color: #9f4771 !important;
    }
    div[aria-selected="true"][role="option"] {
        background: #ffdce9 !important;
        color: #5f2643 !important;
    }
    li[aria-selected="true"][role="option"],
    li[aria-selected="true"][role="option"] *,
    div[aria-selected="true"][role="option"],
    div[aria-selected="true"][role="option"] * {
        background-color: #ffdce9 !important;
        color: #5f2643 !important;
    }
    input, textarea, .stTextInput input, .stNumberInput input {
        color: #2b211c !important;
        background: #fff7fb !important;
        border-color: rgba(247, 168, 200, 0.55) !important;
    }
    div[data-testid="stFileUploader"] section {
        background: #fff7fb !important;
        border: 1.5px dashed rgba(247, 168, 200, 0.75) !important;
        border-radius: 18px !important;
    }
    div[data-testid="stFileUploader"] section * {
        color: var(--vera-text) !important;
    }
    div[data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #ffdce9 0%, #f7a8c8 52%, #ef8bb7 100%) !important;
        color: var(--vera-text) !important;
        border: none !important;
        border-radius: 999px !important;
    }
    span[data-baseweb="tag"] {
        background: #ffdce9 !important;
        color: var(--vera-text) !important;
        border: 1px solid rgba(247, 168, 200, 0.50) !important;
    }
    span[data-baseweb="tag"] * {
        color: var(--vera-text) !important;
    }
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div {
        background: #fff1f7 !important;
    }
    div[data-testid="stSlider"] div[role="slider"] {
        background: #f7a8c8 !important;
        border-color: #f7a8c8 !important;
        box-shadow: 0 4px 12px rgba(247, 168, 200, 0.45) !important;
    }
    div[data-testid="stSlider"] div[role="slider"]:focus {
        box-shadow: 0 0 0 0.2rem rgba(247, 168, 200, 0.35) !important;
    }
    div[data-testid="stSlider"] [data-testid="stTickBar"] {
        background: #ffdce9 !important;
    }
    div[data-testid="stSlider"] [style*="background: rgb(255, 75, 75)"],
    div[data-testid="stSlider"] [style*="background-color: rgb(255, 75, 75)"] {
        background: #f7a8c8 !important;
        background-color: #f7a8c8 !important;
    }
    div[data-testid="stSlider"] [style*="rgb(255, 75, 75)"] {
        color: #9f4771 !important;
        border-color: #f7a8c8 !important;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #f7a8c8 0%, #ef8bb7 100%) !important;
    }
    .stProgress > div > div > div {
        background: #fff1f7 !important;
    }
    div[data-testid="stMetric"] {
        background: #fff7fb;
        border: 1px solid rgba(247, 168, 200, 0.30);
        border-radius: 16px;
        padding: 10px;
        box-shadow: 0 6px 16px rgba(247, 168, 200, 0.10);
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(247, 168, 200, 0.35);
        border-radius: 16px;
        overflow: hidden;
    }
    .stButton > button, .stLinkButton > a {
        width: 100%;
        border-radius: 999px;
        font-weight: 800;
    }
    div[data-testid="stButton"] {
        display: flex;
        justify-content: center;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        width: 78%;
        min-height: 52px;
        background: linear-gradient(135deg, #ffdce9 0%, #f7a8c8 52%, #ef8bb7 100%) !important;
        color: #5f2643 !important;
        border: none !important;
        box-shadow: 0 12px 28px rgba(247, 168, 200, 0.36);
        font-size: 16px;
        letter-spacing: 0.2px;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #ffe5ef 0%, #f9b7d1 52%, #f09ac0 100%) !important;
        color: #5f2643 !important;
        border: none !important;
        transform: translateY(-1px);
    }
    div[data-testid="stButton"] > button[kind="secondary"],
    .stLinkButton > a {
        background: linear-gradient(135deg, #ffdce9 0%, #f7a8c8 52%, #ef8bb7 100%) !important;
        color: #5f2643 !important;
        border: none !important;
        box-shadow: 0 10px 24px rgba(247, 168, 200, 0.32);
    }
    div[data-testid="stButton"] > button[kind="secondary"]:hover,
    .stLinkButton > a:hover {
        background: linear-gradient(135deg, #ffe5ef 0%, #f9b7d1 52%, #f09ac0 100%) !important;
        color: #5f2643 !important;
        border: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@dataclass
class ClothingItem:
    name_cn: str
    name_en: str
    category: str
    color: str
    style: str
    silhouette: str
    occasions: List[str]
    wears_90d: int
    last_worn_days: int


def tr(cn: str, en: str) -> str:
    return cn if st.session_state.get("lang") == "zh" else en


def item_name(item: ClothingItem) -> str:
    return item.name_cn if st.session_state.get("lang") == "zh" else item.name_en


WARDROBE: List[ClothingItem] = [
    ClothingItem("米色短款西装外套", "Beige cropped blazer", "blazer", "beige", "business casual", "cropped", ["presentation", "office"], 1, 78),
    ClothingItem("黑色修身西装外套", "Black tailored blazer", "blazer", "black", "formal", "straight", ["interview", "presentation", "office"], 7, 9),
    ClothingItem("白色宽松衬衫", "White oversized shirt", "shirt", "white", "minimal", "oversized", ["office", "casual", "presentation"], 12, 3),
    ClothingItem("浅蓝牛仔外套", "Light blue denim jacket", "jacket", "blue", "casual", "boxy", ["casual", "travel"], 0, 122),
    ClothingItem("黑色阔腿西裤", "Black wide-leg trousers", "trousers", "black", "minimal", "wide-leg", ["office", "presentation", "dinner"], 10, 5),
    ClothingItem("奶油色针织开衫", "Cream knit cardigan", "cardigan", "cream", "soft casual", "relaxed", ["casual", "study"], 2, 46),
    ClothingItem("直筒蓝色牛仔裤", "Straight blue jeans", "jeans", "blue", "casual", "straight", ["casual", "travel", "dinner"], 8, 12),
    ClothingItem("黑色乐福鞋", "Black loafers", "shoes", "black", "business casual", "flat", ["office", "presentation", "dinner"], 15, 2),
]


PRODUCTS: Dict[str, Dict] = {
    "beige_blazer": {
        "name_cn": "米色西装外套",
        "name_en": "Beige tailored blazer",
        "category": "blazer",
        "color": "beige",
        "style": "business casual",
        "silhouette": "straight",
        "price": 699,
        "occasions": ["presentation", "office", "dinner"],
        "material": "polyester blend",
        "image": "assets/beige_blazer.jpg",
    },
    "black_trench": {
        "name_cn": "黑色防水风衣",
        "name_en": "Black waterproof trench coat",
        "category": "coat",
        "color": "black",
        "style": "commuter",
        "silhouette": "long",
        "price": 899,
        "occasions": ["office", "travel", "rainy commute"],
        "material": "water-resistant cotton blend",
        "image": "assets/black_trench_coat.jpg",
    },
    "pink_dress": {
        "name_cn": "粉色缎面连衣裙",
        "name_en": "Pink satin mini dress",
        "category": "dress",
        "color": "pink",
        "style": "party",
        "silhouette": "slim",
        "price": 599,
        "occasions": ["party", "dinner"],
        "material": "satin",
        "image": "assets/pink_satin_dress.jpg",
    },
    "white_shirt": {
        "name_cn": "白色经典衬衫",
        "name_en": "White classic shirt",
        "category": "shirt",
        "color": "white",
        "style": "minimal",
        "silhouette": "straight",
        "price": 299,
        "occasions": ["office", "presentation", "interview"],
        "material": "cotton",
        "image": "assets/white_classic_shirt.jpg",
    },
}


SCENE_GAPS = {
    "presentation": ["blazer", "shirt", "trousers", "shoes"],
    "office": ["blazer", "shirt", "trousers", "shoes", "coat"],
    "rainy commute": ["coat", "waterproof shoes", "trousers"],
    "dinner": ["dress", "blazer", "shoes"],
    "travel": ["coat", "jeans", "comfortable shoes"],
}

SCENE_LABELS = {
    "presentation": ("课堂汇报", "Presentation"),
    "office": ("上班通勤", "Office"),
    "rainy commute": ("雨天通勤", "Rainy commute"),
    "dinner": ("晚餐约会", "Dinner"),
    "travel": ("旅行出行", "Travel"),
}


def scene_label(scene: str) -> str:
    cn, en = SCENE_LABELS[scene]
    return tr(cn, en)


def product_label(product_key: str) -> str:
    product = PRODUCTS[product_key]
    return f"{tr(product['name_cn'], product['name_en'])} · HK${product['price']}"


def similarity_score(product: Dict, item: ClothingItem) -> int:
    score = 0
    if product["category"] == item.category:
        score += 42
    if product["color"] == item.color:
        score += 24
    if product["style"] == item.style:
        score += 20
    if product["silhouette"] == item.silhouette:
        score += 14
    return min(score, 100)


def duplication_analysis(product: Dict) -> Tuple[int, List[Tuple[ClothingItem, int]]]:
    matches = sorted(
        [(item, similarity_score(product, item)) for item in WARDROBE],
        key=lambda x: x[1],
        reverse=True,
    )
    top_score = matches[0][1]
    similar_count = sum(1 for _, score in matches if score >= 55)
    duplication = min(100, int(top_score * 0.7 + similar_count * 10))
    return duplication, matches[:3]


def dust_risk(product: Dict) -> int:
    same_category = [item for item in WARDROBE if item.category == product["category"]]
    same_color = [item for item in WARDROBE if item.color == product["color"]]
    reference_items = same_category + same_color
    if not reference_items:
        return 28
    avg_wears = sum(item.wears_90d for item in reference_items) / len(reference_items)
    avg_last_worn = sum(item.last_worn_days for item in reference_items) / len(reference_items)
    low_use_penalty = max(0, 55 - avg_wears * 5)
    forgotten_penalty = min(35, avg_last_worn / 3)
    return int(min(92, low_use_penalty + forgotten_penalty))


def fit_style_score(product: Dict, preferred_styles: List[str], preferred_colors: List[str], budget: int) -> int:
    score = 55
    if product["style"] in preferred_styles:
        score += 18
    if product["color"] in preferred_colors:
        score += 12
    if product["price"] <= budget:
        score += 8
    else:
        score -= 8
    return max(0, min(100, score))


def occasion_gap_score(product: Dict, target_occasion: str) -> Tuple[int, str]:
    required = SCENE_GAPS.get(target_occasion, [])
    owned_categories = {item.category for item in WARDROBE if target_occasion in item.occasions}
    product_relevant = product["category"] in required or target_occasion in product["occasions"]
    if product["category"] in required and product["category"] not in owned_categories:
        return 88, tr("补足明确场合缺口", "Fills a clear occasion gap")
    if product_relevant and product["category"] in owned_categories:
        return 52, tr("可用于该场合，但不是明显缺口", "Useful, but not a clear gap")
    if product_relevant:
        return 66, tr("有场景相关性，仍需搭配验证", "Relevant, but needs outfit validation")
    return 28, tr("与当前场景关联较弱", "Weak relevance to this occasion")


def final_decision(duplication: int, dust: int, fit: int, gap: int) -> Tuple[str, str, int]:
    buy_score = int(gap * 0.35 + fit * 0.3 + (100 - duplication) * 0.2 + (100 - dust) * 0.15)
    if buy_score >= 68 and gap >= 60:
        return tr("建议买 · 补缺口", "Buy · Fills a gap"), "success", buy_score
    if buy_score >= 48:
        return tr("谨慎 · 先收藏", "Cautious · Wishlist first"), "warning", buy_score
    return tr("不建议买 · 重复/吃灰风险高", "Don't buy · High risk"), "error", buy_score


def outfit_suggestions(product: Dict, target_occasion: str) -> List[Tuple[str, str, str]]:
    color = product["color"].title()
    category = product["category"]
    if category == "blazer":
        return [
            (tr("Look 1 · 汇报专业感", "Look 1 · Presentation Ready"), f"{color} blazer + White shirt + Black trousers + Black loafers", tr("课堂汇报 / 实习面试", "Presentation / interview")),
            (tr("Look 2 · 轻商务休闲", "Look 2 · Smart Casual"), f"{color} blazer + Blue jeans + Black loafers", tr("轻商务周五 / 晚餐", "Casual Friday / dinner")),
        ]
    if category == "coat":
        return [
            (tr("Look 1 · 雨天通勤", "Look 1 · Rainy Commute"), f"{color} trench coat + White shirt + Black trousers", tr("雨天上班或上课", "Rainy office or campus commute")),
            (tr("Look 2 · 旅行叠穿", "Look 2 · Travel Layering"), f"{color} trench coat + Cream cardigan + Blue jeans", tr("周末旅行", "Weekend travel")),
        ]
    return [
        (tr("Look 1 · 衣橱混搭", "Look 1 · Existing Wardrobe Mix"), f"{color} {category} + Black blazer + Black loafers", scene_label(target_occasion)),
        (tr("Look 2 · 休闲替代", "Look 2 · Casual Alternative"), f"{color} {category} + Blue jeans + Cream cardigan", tr("周末休闲", "Weekend casual")),
    ]


def metric_card(label: str, value: int, note: str):
    st.markdown(
        f"""
        <div class="soft-card">
            <div class="mini-label">{label}</div>
            <div style="font-size:28px;font-weight:900;color:#2b211c;">{value}/100</div>
            <div style="font-size:12px;color:#7b6658;">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(value / 100)


def language_gate():
    if "lang" in st.session_state:
        return

    st.markdown('<div class="phone-shell">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="status-bar">
            <span>9:41</span><span>Vera AI</span><span>●●●</span>
        </div>
        <div class="hero">
            <h1>Vera AI</h1>
            <p>Choose your language / 选择界面语言</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="section-title">Language / 语言</div>', unsafe_allow_html=True)
    if st.button("中文", type="primary"):
        st.session_state.lang = "zh"
        st.session_state.buy_step = "scan"
        st.rerun()
    if st.button("English", type="secondary"):
        st.session_state.lang = "en"
        st.session_state.buy_step = "scan"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


language_gate()

st.markdown('<div class="phone-shell">', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="status-bar">
        <span>9:41</span><span>Vera AI</span><span>●●●</span>
    </div>
    <div class="hero">
        <h1>{tr("买前先问 Vera", "Ask Vera<br/>Before You Buy")}</h1>
        <p>{tr("重复不重复？会不会吃灰？是不是补缺口？", "Is it duplicate? Will it be rarely worn? Does it fill a wardrobe gap?")}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

lang_switch = st.button(tr("Switch to English", "切换到中文"), type="secondary")
if lang_switch:
    st.session_state.lang = "en" if st.session_state.lang == "zh" else "zh"
    st.session_state.buy_step = "scan"
    st.rerun()

tab_buy, tab_closet, tab_agent = st.tabs([
    tr("🛍️ 购买", "🛍️ Buy"),
    tr("👗 衣橱", "👗 Closet"),
    tr("🤖 Agent", "🤖 Agent"),
])

with tab_buy:
    if "buy_step" not in st.session_state:
        st.session_state.buy_step = "scan"

    if st.session_state.buy_step == "scan":
        st.markdown(f'<div class="section-title">{tr("新衣扫描", "New Item Scan")}</div>', unsafe_allow_html=True)
        selected_product_key = st.selectbox(
            tr("选择商品", "Select item"),
            list(PRODUCTS.keys()),
            format_func=product_label,
            key="selected_product_key",
            label_visibility="collapsed",
        )
        product = PRODUCTS[selected_product_key]
        uploaded_file = st.file_uploader(
            tr("上传商品图", "Upload product image"),
            type=["png", "jpg", "jpeg"],
            key="uploaded_product_image",
            label_visibility="collapsed",
        )
        if uploaded_file:
            st.image(uploaded_file, caption=tr("上传商品图", "Uploaded product image"), use_container_width=True)
        else:
            st.image(product["image"], caption=product_label(selected_product_key), use_container_width=True)

        st.markdown(
            f"""
            <div class="soft-card">
                <span class="pill">{product['category']}</span>
                <span class="pill">{product['color']}</span>
                <span class="pill">{product['style']}</span>
                <span class="pill">HK${product['price']}</span>
                <div style="margin-top:8px;color:#6f5b4d;font-size:13px;">
                    {tr("材质", "Material")}: {product['material']}<br/>
                    {tr("识别方式：模拟多模态商品识别", "Recognition: mock multimodal product intake")}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f'<div class="section-title">{tr("购买目标", "Buying Context")}</div>', unsafe_allow_html=True)
        st.selectbox(
            tr("场景", "Occasion"),
            list(SCENE_LABELS.keys()),
            format_func=scene_label,
            index=0,
            key="target_occasion",
        )
        st.slider(tr("预算 HK$", "Budget HK$"), 200, 1500, 800, 50, key="budget")
        st.multiselect(
            tr("偏好风格", "Preferred styles"),
            ["minimal", "business casual", "formal", "casual", "commuter", "party", "soft casual"],
            default=["minimal", "business casual"],
            key="preferred_styles",
        )
        st.multiselect(
            tr("偏好颜色", "Preferred colors"),
            ["black", "white", "beige", "blue", "cream", "pink"],
            default=["black", "white", "beige"],
            key="preferred_colors",
        )

        if st.button(tr("Ask Vera · 开始买前分析", "Ask Vera · Start Analysis"), type="primary"):
            st.session_state.buy_step = "analysis"
            st.rerun()

    else:
        selected_product_key = st.session_state.get("selected_product_key", list(PRODUCTS.keys())[0])
        product = PRODUCTS[selected_product_key]
        target_occasion = st.session_state.get("target_occasion", "presentation")
        budget = st.session_state.get("budget", 800)
        preferred_styles = st.session_state.get("preferred_styles", ["minimal", "business casual"])
        preferred_colors = st.session_state.get("preferred_colors", ["black", "white", "beige"])
        uploaded_file = st.session_state.get("uploaded_product_image")

        st.markdown(f'<div class="section-title">{tr("Vera 分析", "Vera Analysis")}</div>', unsafe_allow_html=True)
        if st.button(tr("← 重新选择商品", "← Back to scan")):
            st.session_state.buy_step = "scan"
            st.rerun()

        if uploaded_file:
            st.image(uploaded_file, caption=tr("本次分析商品", "Product being analyzed"), use_container_width=True)
        else:
            st.image(product["image"], caption=product_label(selected_product_key), use_container_width=True)

        duplication, similar_items = duplication_analysis(product)
        dust = dust_risk(product)
        fit = fit_style_score(product, preferred_styles, preferred_colors, budget)
        gap, gap_reason = occasion_gap_score(product, target_occasion)
        decision, decision_type, buy_score = final_decision(duplication, dust, fit, gap)

        st.markdown(
            f"""
            <div class="soft-card">
                <b>{tr("分析对象", "Item")}</b><br/>
                {product_label(selected_product_key)}<br/>
                <span class="pill">{scene_label(target_occasion)}</span>
                <span class="pill">HK${budget}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            metric_card(tr("重复度", "Duplication"), duplication, tr("越高越像已有衣物", "Higher means more similar to owned items"))
            metric_card(tr("适配", "Fit Match"), fit, tr("偏好、预算、场景", "Preference, budget, occasion"))
        with col2:
            metric_card(tr("吃灰风险", "Dust Risk"), dust, tr("越高越可能低频使用", "Higher means more likely to be rarely worn"))
            metric_card(tr("缺口", "Gap Match"), gap, gap_reason)

        st.markdown(
            f"""
            <div class="decision-{decision_type}">
                <div class="decision-title">{decision}</div>
                <div class="decision-sub">Buy Score: {buy_score}/100</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.lang == "zh":
            why = f"这件 {product['color']} {product['category']} 会与 Amy 的衣橱记忆进行对比。当前场景是 {scene_label(target_occasion)}。Vera 判断：{gap_reason}。"
        else:
            why = f"This {product['color']} {product['category']} is compared with Amy's wardrobe memory. The target occasion is {scene_label(target_occasion)}. Vera's judgment: {gap_reason}."

        st.markdown(
            f"""
            <div class="soft-card">
                <b>{tr("为什么", "Why")}</b><br/>
                {why}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f"##### {tr('最相似已有衣物', 'Similar owned items')}")
        for item, score in similar_items:
            st.markdown(
                f"""
                <div class="soft-card">
                    <b>{item_name(item)}</b><br/>
                    {tr("相似度", "Similarity")}: {score}/100
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(f"##### {tr('即时搭配', 'Instant looks')}")
        for name, items, scene in outfit_suggestions(product, target_occasion):
            st.markdown(
                f"""
                <div class="soft-card">
                    <b>{name}</b><br/>
                    {items}<br/>
                    <span style="color:#7b6658;font-size:12px;">{scene}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if decision_type == "success":
            st.link_button(tr("去合作商店购买", "Go to partner store"), "https://example-fashion-store.com/product/vera-demo")
        else:
            st.button(tr("加入 Wishlist，7 天后提醒", "Wishlist & remind me"), type="secondary")

with tab_closet:
    st.markdown(f'<div class="section-title">{tr("Amy 的数字衣橱", "Amy’s Digital Closet")}</div>', unsafe_allow_html=True)
    total_wears = sum(item.wears_90d for item in WARDROBE)
    low_use = sum(1 for item in WARDROBE if item.wears_90d <= 1)
    categories = len({item.category for item in WARDROBE})
    c1, c2, c3 = st.columns(3)
    c1.metric(tr("90天穿着", "90d wears"), total_wears)
    c2.metric(tr("吃灰单品", "Low-use items"), low_use)
    c3.metric(tr("品类", "Categories"), categories)

    wardrobe_df = pd.DataFrame(
        [
            {
                tr("衣物", "Item"): item_name(item),
                tr("品类", "Category"): item.category,
                tr("颜色", "Color"): item.color,
                tr("风格", "Style"): item.style,
                tr("版型", "Shape"): item.silhouette,
                tr("场景", "Occasions"): ", ".join(item.occasions),
                tr("90天穿着次数", "90d Wears"): item.wears_90d,
                tr("距上次穿着天数", "Last Worn Days"): item.last_worn_days,
            }
            for item in WARDROBE
        ]
    )
    st.dataframe(wardrobe_df, hide_index=True, use_container_width=True)

with tab_agent:
    st.markdown(f'<div class="section-title">{tr("Agent 工作流", "Agent Workflow")}</div>', unsafe_allow_html=True)
    steps = [
        ("1", "Product Intake Agent", tr("识别商品图片、价格、颜色、版型", "Recognizes product image, price, color, and silhouette")),
        ("2", "Wardrobe Memory Agent", tr("读取 Amy 的衣橱与穿着历史", "Reads Amy's wardrobe and wear history")),
        ("3", "Duplication Agent", tr("判断是否又买了一件相似款", "Checks whether the item duplicates existing clothes")),
        ("4", "Dust Risk Agent", tr("预测是否会吃灰、低频使用", "Predicts whether the item will be rarely worn")),
        ("5", "Occasion Gap Agent", tr("判断是否补足真实场景缺口", "Checks whether it fills a real occasion gap")),
        ("6", "Decision Agent", tr("输出买 / 谨慎 / 不买，并解释原因", "Outputs Buy / Cautious / Don't buy with reasons")),
    ]
    for num, title, desc in steps:
        st.markdown(
            f"""
            <div class="soft-card">
                <span class="pill">{num}</span>
                <b>{title}</b><br/>
                <span style="color:#7b6658;font-size:13px;">{desc}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(f"##### {tr('负责任 AI', 'Responsible AI Guardrails')}")
    if st.session_state.lang == "zh":
        st.markdown(
            """
            - 不使用羞辱性身体评价，只提供 comfort 与 fit preference 建议。
            - CPS/佣金推荐必须披露，避免利益冲突。
            - 默认 sustainable-first：先用已有衣物，只有补缺口才建议买。
            - 用户可删除衣橱照片、购买历史与偏好数据。
            """
        )
    else:
        st.markdown(
            """
            - No body-shaming language; only comfort and fit-preference guidance.
            - CPS/affiliate incentives must be disclosed.
            - Sustainable-first by default: use existing clothes before recommending new purchases.
            - Users can delete wardrobe photos, purchase history, and preference data.
            """
        )

st.markdown(
    f"""
    <div class="bottom-nav">
        <span>🏠 {tr("首页", "Home")}</span>
        <span>🛍️ {tr("购买", "Buy")}</span>
        <span>👗 {tr("衣橱", "Closet")}</span>
        <span>👤 Amy</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)
