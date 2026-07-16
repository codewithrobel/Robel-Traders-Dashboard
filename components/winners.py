import streamlit as st

def render_winners(df):

    if len(df) < 3:
        return

    gold, silver, bronze = df.iloc[0], df.iloc[1], df.iloc[2]

    st.subheader("🏆 Top 3 Winners")

    st.markdown(
        """
        <style>
        .winner-card {
            border-radius: 18px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(255,215,0,0.3);
            backdrop-filter: blur(10px);
            min-height: 260px;
        }
        .gold-card {
            background: linear-gradient(135deg,#3a3322,#1b1b1b);
            box-shadow: 0 0 20px rgba(255,215,0,0.25);
        }
        .silver-card {
            background: linear-gradient(135deg,#2d3548,#1b1f28);
            box-shadow: 0 0 20px rgba(192,192,192,0.20);
        }
        .bronze-card {
            background: linear-gradient(135deg,#3d2a22,#1f1a18);
            box-shadow: 0 0 20px rgba(205,127,50,0.20);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="winner-card gold-card">
            <h3>🥇 GOLD</h3>
            <p><b>{gold['ProductCode']}</b></p>
            <h2>🏆 {gold['Score']:.1f}</h2>
            <p>⭐ Rating: {gold['Rating']}</p>
            <p>📝 Reviews: {int(gold['Reviews']):,}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="winner-card silver-card">
            <h3>🥈 SILVER</h3>
            <p><b>{silver['ProductCode']}</b></p>
            <h2>🥈 {silver['Score']:.1f}</h2>
            <p>⭐ Rating: {silver['Rating']}</p>
            <p>📝 Reviews: {int(silver['Reviews']):,}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="winner-card bronze-card">
            <h3>🥉 BRONZE</h3>
            <p><b>{bronze['ProductCode']}</b></p>
            <h2>🥉 {bronze['Score']:.1f}</h2>
            <p>⭐ Rating: {bronze['Rating']}</p>
            <p>📝 Reviews: {int(bronze['Reviews']):,}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.subheader("📊 Product Rankings")

    ranking_df = df.copy()

    if 'Rank' not in ranking_df.columns:
        ranking_df.insert(0, 'Rank', range(1, len(ranking_df) + 1))

    columns_to_show = [
        col for col in [
            'Rank',
            'ProductCode',
            'Price',
            'Reviews',
            'Rating',
            'Score'
        ]
        if col in ranking_df.columns
    ]

    st.dataframe(
        ranking_df[columns_to_show],
        use_container_width=True,
        hide_index=True
    )