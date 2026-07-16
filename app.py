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
    .stApp {
        background: linear-gradient(180deg, #fff7f1 0%, #f7efe8 45%, #efe7dd 100%);
        color: #2b211c;
    }
    .block-container {
        max-width: 430px;
        padding-top: 1.1rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stSidebar"] {
        display: none;
    }
    .phone-shell {
        background: #fffaf6;
        color: #2b211c;
        border: 1px solid rgba(40, 24, 12, 0.10);
        box-shadow: 0 22px 55px rgba(80, 48, 24, 0.18);
        border-radius: 34px;
        padding: 18px 16px 22px 16px;
        margin-bottom: 18px;
    }
    .phone-shell p,
    .phone-shell span,
    .phone-shell div,
    .phone-shell label {
        color: inherit;
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
        background: linear-gradient(135deg, #2b211c 0%, #8d5b3d 100%);
        color: white;
        border-radius: 26px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .hero, .hero h1, .hero p {
        color: white !important;
    }
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
        font-size: 18px;
        font-weight: 800;
        margin: 16px 0 8px 0;
    }
    .soft-card {
        background: white;
        color: #2b211c !important;
        border: 1px solid rgba(50, 30, 15, 0.08);
        border-radius: 22px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 8px 22px rgba(80, 48, 24, 0.07);
    }
    .soft-card, .soft-card b, .soft-card span, .soft-card div {
        color: #2b211c !important;
    }
    .pill {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: #f2e2d7;
        color: #62442f;
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
    .decision-success,
    .decision-warning,
    .decision-error,
    .decision-success div,
    .decision-warning div,
    .decision-error div {
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
        color: #7b6658;
        margin-bottom: 3px;
    }
    .bottom-nav {
        display: flex;
        justify-content: space-around;
        background: #2b211c;
        border-radius: 22px;
        color: white;
        padding: 11px 7px;
        margin-top: 18px;
        font-size: 12px;
        font-weight: 700;
    }
    .bottom-nav, .bottom-nav span {
        color: white !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #efe1d6;
        padding: 5px;
        border-radius: 999px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
        padding: 8px 10px;
        font-size: 13px;
        color: #2b211c !important;
    }
    .stTabs [aria-selected="true"] {
        background: #fffaf6 !important;
        color: #2b211c !important;
    }
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] span,
    div[data-baseweb="popover"] {
        color: #2b211c !important;
    }
    input,
    textarea,
    .stTextInput input,
    .stNumberInput input {
        color: #2b211c !important;
        background: #fffaf6 !important;
    }
    .stButton > button, .stLinkButton > a {
        width: 100%;
        border-radius: 999px;
        font-weight: 800;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@dataclass
class ClothingItem:
    name: str
    category: str
    color: str
    style: str
    silhouette: str
    occasions: List[str]
    wears_90d: int
    last_worn_days: int


WARDROBE: List[ClothingItem] = [
    ClothingItem("米色短款西装外套 | Beige cropped blazer", "blazer", "beige", "business casual", "cropped", ["presentation", "office"], 1, 78),
    ClothingItem("黑色修身西装外套 | Black tailored blazer", "blazer", "black", "formal", "straight", ["interview", "presentation", "office"], 7, 9),
    ClothingItem("白色宽松衬衫 | White oversized shirt", "shirt", "white", "minimal", "oversized", ["office", "casual", "presentation"], 12, 3),
    ClothingItem("浅蓝牛仔外套 | Light blue denim jacket", "jacket", "blue", "casual", "boxy", ["casual", "travel"], 0, 122),
    ClothingItem("黑色阔腿西裤 | Black wide-leg trousers", "trousers", "black", "minimal", "wide-leg", ["office", "presentation", "dinner"], 10, 5),
    ClothingItem("奶油色针织开衫 | Cream knit cardigan", "cardigan", "cream", "soft casual", "relaxed", ["casual", "study"], 2, 46),
    ClothingItem("直筒蓝色牛仔裤 | Straight blue jeans", "jeans", "blue", "casual", "straight", ["casual", "travel", "dinner"], 8, 12),
    ClothingItem("黑色乐福鞋 | Black loafers", "shoes", "black", "business casual", "flat", ["office", "presentation", "dinner"], 15, 2),
]


PRODUCTS: Dict[str, Dict] = {
    "米色西装外套 | Beige tailored blazer": {
        "category": "blazer",
        "color": "beige",
        "style": "business casual",
        "silhouette": "straight",
        "price": 699,
        "occasions": ["presentation", "office", "dinner"],
        "material": "polyester blend",
        "image": "assets/beige_blazer.jpg",
    },
    "黑色防水风衣 | Black waterproof trench coat": {
        "category": "coat",
        "color": "black",
        "style": "commuter",
        "silhouette": "long",
        "price": 899,
        "occasions": ["office", "travel", "rainy commute"],
        "material": "water-resistant cotton blend",
        "image": "assets/black_trench_coat.jpg",
    },
    "粉色缎面连衣裙 | Pink satin mini dress": {
        "category": "dress",
        "color": "pink",
        "style": "party",
        "silhouette": "slim",
        "price": 599,
        "occasions": ["party", "dinner"],
        "material": "satin",
        "image": "assets/pink_satin_dress.jpg",
    },
    "白色经典衬衫 | White classic shirt": {
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
    "presentation": "课堂汇报 / Presentation",
    "office": "上班通勤 / Office",
    "rainy commute": "雨天通勤 / Rainy commute",
    "dinner": "晚餐约会 / Dinner",
    "travel": "旅行出行 / Travel",
}


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


def duplication_analysis(product: Dict) -> Tuple[int, List[Tuple[str, int]]]:
    matches = sorted(
        [(item.name, similarity_score(product, item)) for item in WARDROBE],
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
        return 88, "补足明确场合缺口 | Fills a clear occasion gap"
    if product_relevant and product["category"] in owned_categories:
        return 52, "可用于该场合，但不是明显缺口 | Useful, but not a clear gap"
    if product_relevant:
        return 66, "有场景相关性，仍需搭配验证 | Relevant, but needs outfit validation"
    return 28, "与当前场景关联较弱 | Weak relevance to this occasion"


def final_decision(duplication: int, dust: int, fit: int, gap: int) -> Tuple[str, str, int]:
    buy_score = int(gap * 0.35 + fit * 0.3 + (100 - duplication) * 0.2 + (100 - dust) * 0.15)
    if buy_score >= 68 and gap >= 60:
        return "建议买 · 补缺口 | Buy · Fills a gap", "success", buy_score
    if buy_score >= 48:
        return "谨慎 · 先收藏 | Cautious · Wishlist first", "warning", buy_score
    return "不建议买 · 重复/吃灰风险高 | Don't buy · High risk", "error", buy_score


def outfit_suggestions(product: Dict, target_occasion: str) -> List[Dict]:
    color = product["color"].title()
    category = product["category"]
    if category == "blazer":
        return [
            ("Look 1 · 汇报专业感", f"{color} blazer + White shirt + Black trousers + Black loafers", "Presentation / interview"),
            ("Look 2 · 轻商务休闲", f"{color} blazer + Blue jeans + Black loafers", "Casual Friday / dinner"),
        ]
    if category == "coat":
        return [
            ("Look 1 · 雨天通勤", f"{color} trench coat + White shirt + Black trousers", "Rainy commute"),
            ("Look 2 · 旅行叠穿", f"{color} trench coat + Cream cardigan + Blue jeans", "Weekend travel"),
        ]
    return [
        ("Look 1 · 衣橱混搭", f"{color} {category} + Black blazer + Black loafers", SCENE_LABELS[target_occasion]),
        ("Look 2 · 休闲替代", f"{color} {category} + Blue jeans + Cream cardigan", "Weekend casual"),
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


st.markdown('<div class="phone-shell">', unsafe_allow_html=True)
st.markdown(
    """
    <div class="status-bar">
        <span>9:41</span><span>Vera AI</span><span>●●●</span>
    </div>
    <div class="hero">
        <h1>Ask Vera<br/>Before You Buy</h1>
        <p>买前先问 Vera：重复不重复？会不会吃灰？是不是补缺口？</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_buy, tab_closet, tab_agent = st.tabs(["🛍️ Buy", "👗 Closet", "🤖 Agent"])

with tab_buy:
    st.markdown('<div class="section-title">新衣扫描 | New Item Scan</div>', unsafe_allow_html=True)
    selected_product_name = st.selectbox("选择商品 | Select item", list(PRODUCTS.keys()), label_visibility="collapsed")
    product = PRODUCTS[selected_product_name]
    uploaded_file = st.file_uploader(
        "上传商品图 | Upload product image",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed",
    )
    if uploaded_file:
        st.image(uploaded_file, caption="上传商品图 | Uploaded product image", use_container_width=True)
    else:
        st.image(product["image"], caption=selected_product_name, use_container_width=True)

    st.markdown(
        f"""
        <div class="soft-card">
            <span class="pill">{product['category']}</span>
            <span class="pill">{product['color']}</span>
            <span class="pill">{product['style']}</span>
            <span class="pill">HK${product['price']}</span>
            <div style="margin-top:8px;color:#6f5b4d;font-size:13px;">
                材质 | Material: {product['material']}<br/>
                识别方式 | Recognition: mock multimodal product intake
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">购买目标 | Buying Context</div>', unsafe_allow_html=True)
    target_occasion = st.selectbox(
        "场景 | Occasion",
        list(SCENE_LABELS.keys()),
        format_func=lambda x: SCENE_LABELS[x],
        index=0,
    )
    budget = st.slider("预算 | Budget HK$", 200, 1500, 800, 50)
    preferred_styles = st.multiselect(
        "偏好风格 | Preferred styles",
        ["minimal", "business casual", "formal", "casual", "commuter", "party", "soft casual"],
        default=["minimal", "business casual"],
    )
    preferred_colors = st.multiselect(
        "偏好颜色 | Preferred colors",
        ["black", "white", "beige", "blue", "cream", "pink"],
        default=["black", "white", "beige"],
    )

    duplication, similar_items = duplication_analysis(product)
    dust = dust_risk(product)
    fit = fit_style_score(product, preferred_styles, preferred_colors, budget)
    gap, gap_reason = occasion_gap_score(product, target_occasion)
    decision, decision_type, buy_score = final_decision(duplication, dust, fit, gap)

    st.markdown('<div class="section-title">Vera 分析 | Vera Analysis</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        metric_card("重复度 | Duplication", duplication, "越高越像已有衣物")
        metric_card("适配 | Fit Match", fit, "偏好、预算、场景")
    with col2:
        metric_card("吃灰风险 | Dust Risk", dust, "越高越可能低频使用")
        metric_card("缺口 | Gap Match", gap, gap_reason)

    st.markdown(
        f"""
        <div class="decision-{decision_type}">
            <div class="decision-title">{decision}</div>
            <div class="decision-sub">Buy Score: {buy_score}/100</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="soft-card">
            <b>为什么 | Why</b><br/>
            这件 <b>{product['color']} {product['category']}</b> 会与衣橱中部分单品对比。
            当前场景是 <b>{SCENE_LABELS[target_occasion]}</b>。Vera 判断：<b>{gap_reason}</b>。
            <br/><br/>
            Vera compares this item with Amy's wardrobe memory, predicts low-use risk,
            checks style fit, and decides whether it truly fills a wardrobe gap.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("##### 最相似已有衣物 | Similar owned items")
    for item_name, score in similar_items:
        st.markdown(
            f"""
            <div class="soft-card">
                <b>{item_name}</b><br/>
                相似度 | Similarity: {score}/100
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("##### 即时搭配 | Instant looks")
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
        st.link_button("去合作商店购买 | Go to partner store", "https://example-fashion-store.com/product/vera-demo")
    else:
        st.button("加入 Wishlist，7 天后提醒 | Wishlist & remind me", type="secondary")

with tab_closet:
    st.markdown('<div class="section-title">Amy 的数字衣橱 | Amy’s Digital Closet</div>', unsafe_allow_html=True)
    total_wears = sum(item.wears_90d for item in WARDROBE)
    low_use = sum(1 for item in WARDROBE if item.wears_90d <= 1)
    categories = len({item.category for item in WARDROBE})
    c1, c2, c3 = st.columns(3)
    c1.metric("90天穿着", total_wears)
    c2.metric("吃灰单品", low_use)
    c3.metric("品类", categories)

    wardrobe_df = pd.DataFrame([item.__dict__ for item in WARDROBE])
    wardrobe_df["occasions"] = wardrobe_df["occasions"].apply(", ".join)
    wardrobe_df = wardrobe_df.rename(
        columns={
            "name": "Item",
            "category": "Category",
            "color": "Color",
            "style": "Style",
            "silhouette": "Shape",
            "occasions": "Occasions",
            "wears_90d": "90d Wears",
            "last_worn_days": "Last Worn Days",
        }
    )
    st.dataframe(wardrobe_df, hide_index=True, use_container_width=True)

with tab_agent:
    st.markdown('<div class="section-title">Agent 工作流 | Agent Workflow</div>', unsafe_allow_html=True)
    steps = [
        ("1", "Product Intake Agent", "识别商品图片、价格、颜色、版型"),
        ("2", "Wardrobe Memory Agent", "读取 Amy 的衣橱与穿着历史"),
        ("3", "Duplication Agent", "判断是否又买了一件相似款"),
        ("4", "Dust Risk Agent", "预测是否会吃灰、低频使用"),
        ("5", "Occasion Gap Agent", "判断是否补足真实场景缺口"),
        ("6", "Decision Agent", "输出买 / 谨慎 / 不买，并解释原因"),
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

    st.markdown("##### Responsible AI Guardrails | 负责任 AI")
    st.markdown(
        """
        - 不使用羞辱性身体评价，只提供 comfort 与 fit preference 建议。
        - CPS/佣金推荐必须披露，避免利益冲突。
        - 默认 sustainable-first：先用已有衣物，只有补缺口才建议买。
        - 用户可删除衣橱照片、购买历史与偏好数据。
        """
    )

st.markdown(
    """
    <div class="bottom-nav">
        <span>🏠 Home</span><span>🛍️ Buy</span><span>👗 Closet</span><span>👤 Amy</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)
