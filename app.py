from dataclasses import dataclass
from typing import Dict, List, Tuple

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Vera AI | Buy Decision Agent",
    page_icon="🛍️",
    layout="wide",
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
    "米色西装外套 | Beige tailored blazer - HK$699": {
        "category": "blazer",
        "color": "beige",
        "style": "business casual",
        "silhouette": "straight",
        "price": 699,
        "occasions": ["presentation", "office", "dinner"],
        "material": "polyester blend",
        "image": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=900&q=80",
    },
    "黑色防水风衣 | Black waterproof trench coat - HK$899": {
        "category": "coat",
        "color": "black",
        "style": "commuter",
        "silhouette": "long",
        "price": 899,
        "occasions": ["office", "travel", "rainy commute"],
        "material": "water-resistant cotton blend",
        "image": "https://images.unsplash.com/photo-1548126032-079a0fb0099d?auto=format&fit=crop&w=900&q=80",
    },
    "粉色缎面连衣裙 | Pink satin mini dress - HK$599": {
        "category": "dress",
        "color": "pink",
        "style": "party",
        "silhouette": "slim",
        "price": 599,
        "occasions": ["party", "dinner"],
        "material": "satin",
        "image": "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=900&q=80",
    },
    "白色经典衬衫 | White classic shirt - HK$299": {
        "category": "shirt",
        "color": "white",
        "style": "minimal",
        "silhouette": "straight",
        "price": 299,
        "occasions": ["office", "presentation", "interview"],
        "material": "cotton",
        "image": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?auto=format&fit=crop&w=900&q=80",
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


def fit_style_score(product: Dict, user_profile: Dict) -> int:
    score = 55
    if product["style"] in user_profile["preferred_styles"]:
        score += 18
    if product["color"] in user_profile["preferred_colors"]:
        score += 12
    if product["silhouette"] in user_profile["preferred_silhouettes"]:
        score += 10
    if product["price"] <= user_profile["budget"]:
        score += 5
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
        return "谨慎 · 先加入 Wishlist | Cautious · Add to wishlist first", "warning", buy_score
    return "不建议买 · 重复/吃灰风险高 | Don't buy · High duplication/dust risk", "error", buy_score


def render_metric_card(title: str, value: int, help_text: str):
    st.metric(title, f"{value}/100", help=help_text)
    st.progress(value / 100)


def outfit_suggestions(product: Dict, target_occasion: str) -> List[Dict]:
    color = product["color"].title()
    category = product["category"]
    if category == "blazer":
        return [
            {
                "name": "Look 1 · 汇报专业感 | Presentation Ready",
                "items": f"{color} blazer + White oversized shirt + Black wide-leg trousers + Black loafers",
                "scene": "课堂汇报 / 实习面试 | Group presentation / internship interview",
            },
            {
                "name": "Look 2 · 轻商务休闲 | Smart Casual",
                "items": f"{color} blazer + Straight blue jeans + Black loafers",
                "scene": "Casual Friday / Tsim Sha Tsui dinner",
            },
        ]
    if category == "coat":
        return [
            {
                "name": "Look 1 · 雨天通勤 | Rainy Commute",
                "items": f"{color} trench coat + White shirt + Black trousers + Black loafers",
                "scene": "雨天上班 / 上课通勤 | Rainy office or campus commute",
            },
            {
                "name": "Look 2 · 旅行叠穿 | Travel Layering",
                "items": f"{color} trench coat + Cream cardigan + Straight blue jeans",
                "scene": "周末旅行 / 机场穿搭 | Weekend travel / airport outfit",
            },
        ]
    return [
        {
            "name": "Look 1 · 衣橱混搭 | Existing Wardrobe Mix",
            "items": f"{color} {category} + Black blazer + Black loafers",
            "scene": f"{SCENE_LABELS.get(target_occasion, target_occasion)}",
        },
        {
            "name": "Look 2 · 休闲替代 | Casual Alternative",
            "items": f"{color} {category} + Straight blue jeans + Cream cardigan",
            "scene": "周末休闲 | Weekend casual",
        },
    ]


st.title("🛍️ Vera AI · 买前决策 Agent | Buy Decision Agent")
st.caption(
    "把冲动消费改成：买之前先问 Vera。Turn impulse shopping into: ask Vera before buying."
)

with st.sidebar:
    st.header("用户画像 | User Profile")
    user_name = st.text_input("用户 | User", "Amy · PolyU student")
    target_occasion = st.selectbox(
        "本次购买目标场景 | Target occasion",
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
    preferred_silhouettes = st.multiselect(
        "偏好版型 | Preferred silhouettes",
        ["straight", "cropped", "oversized", "wide-leg", "relaxed", "long", "slim"],
        default=["straight", "oversized", "wide-leg"],
    )

user_profile = {
    "budget": budget,
    "preferred_styles": preferred_styles,
    "preferred_colors": preferred_colors,
    "preferred_silhouettes": preferred_silhouettes,
}

tab_buy, tab_wardrobe, tab_architecture = st.tabs(
    ["BUY 决策引擎 | Decision Engine", "用户数字衣橱 | Digital Wardrobe", "Agent 工作流 | Workflow"]
)

with tab_buy:
    left, right = st.columns([0.95, 1.35])

    with left:
        st.subheader("1. 输入：用户看中的新衣 | Input: New item")
        selected_product_name = st.selectbox("选择 demo 商品 | Select demo product", list(PRODUCTS.keys()))
        product = PRODUCTS[selected_product_name]
        uploaded_file = st.file_uploader(
            "或上传商品截图/照片（本 demo 使用模拟识别结果）| Or upload a product image (mock recognition)",
            type=["png", "jpg", "jpeg"],
        )
        product_link = st.text_input(
            "商品链接 / 电商 URL | Product link / e-commerce URL",
            "https://example-fashion-store.com/product/vera-demo",
        )

        if uploaded_file:
            st.image(uploaded_file, caption="上传商品图 | Uploaded product image", use_container_width=True)
        else:
            st.image(product["image"], caption=selected_product_name, use_container_width=True)

        st.markdown("**模拟商品识别结果 | Mock product recognition**")
        st.json(
            {
                "category": product["category"],
                "color": product["color"],
                "style": product["style"],
                "silhouette": product["silhouette"],
                "material": product["material"],
                "price_hkd": product["price"],
            }
        )

    with right:
        st.subheader("2. Vera 分析：买前先问 | Ask before buying")
        duplication, similar_items = duplication_analysis(product)
        dust = dust_risk(product)
        fit = fit_style_score(product, user_profile)
        gap, gap_reason = occasion_gap_score(product, target_occasion)
        decision, decision_type, buy_score = final_decision(duplication, dust, fit, gap)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card("重复度 | Duplication", duplication, "越高代表越像已有衣物 | Higher means more similar to owned items")
        with c2:
            render_metric_card("吃灰概率 | Dust Risk", dust, "越高代表越可能低频使用 | Higher means more likely to be rarely worn")
        with c3:
            render_metric_card("适配判断 | Fit Match", fit, "基于偏好、预算与场景知识 | Based on preference, budget, and occasion knowledge")
        with c4:
            render_metric_card("缺口匹配 | Gap Match", gap, gap_reason)

        st.divider()
        if decision_type == "success":
            st.success(f"最终结论 | Final decision: {decision} · Buy Score {buy_score}/100")
        elif decision_type == "warning":
            st.warning(f"最终结论 | Final decision: {decision} · Buy Score {buy_score}/100")
        else:
            st.error(f"最终结论 | Final decision: {decision} · Buy Score {buy_score}/100")

        st.markdown("#### Vera 的解释 | Vera's explanation")
        st.write(
            f"""
            这件 **{product['color']} {product['category']}** 与你的衣橱中部分单品存在相似性。
            当前目标场景是 **{SCENE_LABELS[target_occasion]}**，系统判断：**{gap_reason}**。

            This **{product['color']} {product['category']}** overlaps with some existing wardrobe items.
            For the target occasion **{target_occasion}**, Vera checks whether it supports real usage scenarios,
            or whether it may become another low-use item.
            """
        )

        st.markdown("#### 最相似的已有衣物 | Most similar owned items")
        similar_df = pd.DataFrame(similar_items, columns=["已有衣物 | Owned item", "相似度 | Similarity"])
        st.dataframe(similar_df, hide_index=True, use_container_width=True)

        st.markdown("#### 即时搭配建议 | Instant outfit suggestions")
        for look in outfit_suggestions(product, target_occasion):
            with st.container(border=True):
                st.markdown(f"**{look['name']}**")
                st.write(look["items"])
                st.caption(f"适用场景 | Scene: {look['scene']}")

        if decision_type == "success":
            st.link_button("跳转合作商店 | Proceed to Partner Store · CPS", product_link)
        else:
            st.button("加入 Wishlist，7 天后提醒 | Add to wishlist, remind me in 7 days", type="secondary")

with tab_wardrobe:
    st.subheader(f"{user_name} 的数字衣橱记忆 | Digital wardrobe memory")
    wardrobe_df = pd.DataFrame([item.__dict__ for item in WARDROBE])
    wardrobe_df["occasions"] = wardrobe_df["occasions"].apply(", ".join)
    wardrobe_df = wardrobe_df.rename(
        columns={
            "name": "衣物 | Item",
            "category": "品类 | Category",
            "color": "颜色 | Color",
            "style": "风格 | Style",
            "silhouette": "版型 | Silhouette",
            "occasions": "场景 | Occasions",
            "wears_90d": "90天穿着次数 | Wears in 90d",
            "last_worn_days": "距上次穿着天数 | Days since last worn",
        }
    )
    st.dataframe(wardrobe_df, use_container_width=True, hide_index=True)

    st.markdown("#### 衣橱洞察 | Wardrobe insights")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("近90天总穿着次数 | Total wears in 90d", sum(item.wears_90d for item in WARDROBE))
    with col_b:
        low_use = sum(1 for item in WARDROBE if item.wears_90d <= 1)
        st.metric("低频/吃灰单品 | Low-use items", low_use)
    with col_c:
        categories = len({item.category for item in WARDROBE})
        st.metric("覆盖品类 | Categories covered", categories)

    st.info(
        "Demo 假设这些数据来自用户上传衣橱照片、OOTD 记录、购买历史、收藏记录和手动反馈。"
        " In a real system, these signals come from wardrobe photos, OOTD logs, purchase history, wishlist data, and user feedback."
    )

with tab_architecture:
    st.subheader("Agentic AI Architecture | 智能体架构")
    st.markdown(
        """
        ```mermaid
        flowchart LR
            A[Product Intake Agent] --> B[Wardrobe Memory Agent]
            B --> C[Similarity & Duplication Agent]
            B --> D[Dust Risk Prediction Agent]
            A --> E[Fit & Style Agent]
            A --> F[Occasion Gap Agent]
            C --> G[Decision Agent]
            D --> G
            E --> G
            F --> G
            G --> H{Buy / Cautious / Don't Buy}
            H --> I[CPS Commerce Agent]
            H --> J[Sustainability Guardrail]
        ```
        """
    )

    st.markdown("#### Responsible AI Guardrails | 负责任 AI 机制")
    st.write(
        """
        - 不使用羞辱性身体评价，只提供 comfort、fit preference 与场景适配建议。No body-shaming language; only comfort and fit-preference guidance.
        - CPS/佣金推荐必须明确披露，避免利益冲突。CPS/affiliate incentives must be disclosed.
        - 默认 sustainable-first：优先使用已有衣物，只有补缺口时才建议购买。Sustainable-first by default.
        - 用户可以删除衣橱照片、购买历史和体貌偏好数据。Users can delete wardrobe photos, purchase history, and profile data.
        - 高价购买可设置冷静期，降低冲动消费。High-price purchases can trigger a cooling-off period.
        """
    )
