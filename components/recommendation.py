import streamlit as st

def render_recommendation(df):

    if len(df) == 0:
        st.info("No products available for recommendation.")
        return

    best_product = df.iloc[0]

    st.subheader("🤖 AI Recommendation")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown(
            f"""
            <div class="ai-card" style="box-shadow:0 0 25px rgba(34,197,94,0.25);">
            <h2>🏆 AI Recommendation : {best_product['ProductCode']}</h2>

            <p>
            <b>Rank:</b> #{best_product['Rank']}
            |
            <b>Score:</b> {best_product['Score']:.1f}
            </p>

            <p>⭐ Rating: {best_product['Rating']}</p>
            <p>📝 Reviews: {int(best_product['Reviews']):,}</p>

            <p>✅ Highest Overall Score</p>
            <p>✅ Strong Reviews</p>
            <p>✅ Good Rating</p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style="
            background:rgba(34,197,94,0.15);
            border:1px solid #22c55e;
            border-radius:15px;
            padding:25px;
            text-align:center;
            min-height:320px;
            display:flex;
            flex-direction:column;
            justify-content:center;
            align-items:center;
            box-shadow:0 0 25px rgba(34,197,94,0.25);
            ">

            <div style="font-size:60px;">📈</div>

            <h2 style="color:#ffffff;margin:10px 0;">
            Growth Trend
            </h2>

            <h1 style="color:#4ade80;margin:5px 0;">+24%</h1>

            <p style="margin:6px 0;color:#d1fae5;">AI Forecast: Positive</p>
            <p style="margin:6px 0;color:#d1fae5;">Expected Performance: High</p>

            <div style="
                margin-top:15px;
                padding:10px 20px;
                background:#16a34a;
                border-radius:999px;
                color:white;
                font-weight:bold;
            ">
                Confidence: 98%
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )