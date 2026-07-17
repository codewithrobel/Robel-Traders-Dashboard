import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

from utils.data_manager import load_products, save_products
from components.hero import render_hero
from components.metrics import render_metrics
from components.winners import render_winners
from components.recommendation import render_recommendation
from database import init_db
from modules.meesho_collector import collector
from modules.screenshot_extractor import extractor

from streamlit_paste_button import paste_image_button

st.set_page_config(
    page_title="Robel Traders Dashboard",
    page_icon="📊",
    layout="wide"
)

init_db()

from styles.theme import load_theme
st.markdown(load_theme(), unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg,#0b1220,#111827,#0f172a);
    }
    .main-title {
        font-size: 58px;
        font-weight: 800;
        color: #ffffff;
        text-shadow: 0 0 25px rgba(251,191,36,0.35);
        margin-bottom: 0;
    }
    .sub-title {
        color: #fbbf24;
        font-size: 22px;
        margin-top: -10px;
        margin-bottom: 20px;
        letter-spacing: 1px;
    }
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(251,191,36,0.25);
        border-radius: 16px;
        padding: 12px;
        backdrop-filter: blur(10px);
    }
    div[data-testid="stMetric"] label {
        color: #fbbf24;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg,#050b16,#0b1220);
        border-right: 1px solid rgba(251,191,36,0.15);
    }

    div[data-testid="stMetric"] {
        box-shadow: 0 0 20px rgba(251,191,36,0.08);
    }

    h1, h2, h3 {
        color: white !important;
    }

    div[data-baseweb="tab-list"] {
        gap: 12px;
    }

    button[data-baseweb="tab"] {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 10px !important;
        padding: 10px 18px !important;
    }

    .main .block-container {
        padding-top: 2rem;
    }

    [data-testid="stSidebar"] {
        box-shadow: 0 0 30px rgba(0,0,0,0.5);
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(251,191,36,0.35);
        border-radius: 18px;
        background: rgba(17,24,39,0.75);
    }

    div[data-testid="stMetric"] * {
        color: white !important;
    }
    .hero-card {
background: linear-gradient(135deg,#111827,#0f172a);
border:1px solid rgba(251,191,36,0.25);
padding:20px;
border-radius:20px;
margin-bottom:20px;
}
.winner-card {
padding:20px;
border-radius:18px;
text-align:center;
font-weight:bold;
}
.gold-card {background:rgba(251,191,36,0.12);border:1px solid #fbbf24;}
.silver-card {background:rgba(148,163,184,0.12);border:1px solid #cbd5e1;}
.bronze-card {background:rgba(180,83,9,0.12);border:1px solid #d97706;}
.ai-card {
background:rgba(34,197,94,0.12);
border:1px solid #22c55e;
padding:20px;
border-radius:18px;
}
    </style>
    """,
    unsafe_allow_html=True,
)


logo_path = "logo.png"
csv_file = "products.csv"

if Path(logo_path).exists():
    st.sidebar.image(logo_path, width=220)
else:
    st.sidebar.warning("logo.png not found")

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📦 Product Management",
        "📈 Analytics Dashboard",
        "🔍 Research Center",
        "⚙️ Settings"
    ]
)
st.sidebar.markdown("---")
st.sidebar.success("🟢 System Online")
st.sidebar.info(
    "Manage products, analyze rankings and discover winning products using AI insights."
)

render_hero()
render_metrics()

st.divider()

if menu == "🏠 Dashboard":
    st.success("🚀 Welcome to Robel Traders Enterprise Dashboard")

    try:
        dashboard_df = load_products()

        dashboard_df["Reviews"] = pd.to_numeric(dashboard_df["Reviews"], errors="coerce").fillna(0)
        dashboard_df["Rating"] = pd.to_numeric(dashboard_df["Rating"], errors="coerce").fillna(0)

        dashboard_df["Score"] = (
            dashboard_df["Reviews"] * 0.4
            + dashboard_df["Rating"] * 1000 * 0.6
        )

        dashboard_df = dashboard_df.sort_values(
            by="Score",
            ascending=False
        ).reset_index(drop=True)

        dashboard_df["Rank"] = dashboard_df.index + 1

        render_winners(dashboard_df)

        st.divider()

        render_recommendation(dashboard_df)

    except Exception as e:
        st.info("No products available yet.")
        st.caption(f"Details: {e}")


if menu == "📦 Product Management":
    st.subheader("📂 Bulk Excel Upload")

    uploaded_file = st.file_uploader(
        "Upload Excel File (.xlsx)",
        type=["xlsx"]
    )

    if uploaded_file is not None:
        try:
            excel_df = pd.read_excel(uploaded_file)

            required_columns = ["ProductCode", "Price", "Reviews", "Rating"]

            if all(col in excel_df.columns for col in required_columns):
                try:
                    existing_df = load_products()
                    combined_df = pd.concat([existing_df, excel_df], ignore_index=True)
                    combined_df = combined_df.drop_duplicates(subset=["ProductCode"])
                except FileNotFoundError:
                    combined_df = excel_df

                save_products(combined_df)

                st.success(f"✅ {len(excel_df)} products imported successfully")
                st.toast("📂 Excel uploaded", icon="🚀")
            else:
                st.error(
                    "Excel must contain: ProductCode, Price, Reviews, Rating"
                )

        except Exception as e:
            st.error(f"Upload failed: {e}")

    st.divider()

    st.subheader("Add New Product")

    with st.form("product_form"):
        code_number = st.text_input(
            "Product Code Number",
            placeholder="470217206"
        )
        product_code = f"S-{code_number}"
        price = st.number_input("Price", min_value=0)
        reviews = st.number_input("Reviews", min_value=0, step=100)
        rating = st.number_input(
            "Rating",
            min_value=0.0,
            max_value=5.0,
            value=4.0,
            step=0.1
        )

        preview_score = (reviews * 0.4) + (rating * 1000 * 0.6)
        st.info(f"Predicted Score: {preview_score:.1f}")

        try:
            rank_df = load_products()
            rank_df["Reviews"] = pd.to_numeric(rank_df["Reviews"], errors="coerce").fillna(0)
            rank_df["Rating"] = pd.to_numeric(rank_df["Rating"], errors="coerce").fillna(0)
            rank_df["Score"] = (rank_df["Reviews"] * 0.4) + (rank_df["Rating"] * 1000 * 0.6)
            predicted_rank = (rank_df["Score"] > preview_score).sum() + 1
            st.success(f"Predicted Rank: #{predicted_rank}")
        except FileNotFoundError:
            st.success("Predicted Rank: #1")

        submitted = st.form_submit_button("Add Product")

        if submitted:
            if code_number.strip() == "":
                st.error("Please enter a product code number")
                st.stop()
            new_row = pd.DataFrame([
                {
                    "ProductCode": product_code,
                    "Price": price,
                    "Reviews": reviews,
                    "Rating": rating,
                }
            ])

            try:
                existing_df = load_products()
                if product_code in existing_df["ProductCode"].astype(str).values:
                    st.warning("Product already exists in database")
                    st.stop()
                updated_df = pd.concat([existing_df, new_row], ignore_index=True)
            except FileNotFoundError:
                updated_df = new_row

            save_products(updated_df)
            st.toast("✅ Product added successfully!", icon="🎉")
            st.balloons()


    with st.expander("🔍 Search Product"):
        st.subheader("Search Product")
        search_code = st.text_input("Enter Product Code Number to Search", placeholder="470217206")

        if search_code:
            search_product_code = str(search_code).strip()
            try:
                search_df = load_products()
                search_df["ProductCode"] = search_df["ProductCode"].astype(str)
                result = search_df[
                    (search_df["ProductCode"] == search_product_code)
                    | (search_df["ProductCode"] == f"S-{search_product_code}")
                    | (search_df["ProductCode"] == f"RT-{search_product_code}")
                ]

                if not result.empty:
                    st.success("Product Found")
                    st.dataframe(result)
                else:
                    st.warning("Product not found")
            except FileNotFoundError:
                st.error("Database file not found")

    st.divider()

    with st.expander("🗑️ Delete Product"):
        st.subheader("Delete Product")
        delete_code = st.text_input(
            "Enter Product Code Number to Delete",
            placeholder="470217206",
            key="delete_product"
        )

        if st.button("Delete Product"):
            if delete_code.strip() == "":
                st.warning("Please enter a product code number")
            else:
                delete_product_code = str(delete_code).strip()
                try:
                    import sqlite3

                    conn = sqlite3.connect("robel.db")
                    cursor = conn.cursor()

                    cursor.execute(
                        """
                        DELETE FROM products
                        WHERE ProductCode = ?
                           OR ProductCode = ?
                           OR ProductCode = ?
                        """,
                        (
                            delete_product_code,
                            f"S-{delete_product_code}",
                            f"RT-{delete_product_code}"
                        )
                    )

                    deleted_rows = cursor.rowcount

                    conn.commit()
                    conn.close()

                    if deleted_rows == 0:
                        st.warning("Product not found")
                    else:
                        st.success(f"🗑️ {delete_product_code} deleted successfully!")
                        st.toast("🗑️ Product deleted", icon="🔥")
                        st.rerun()
                except FileNotFoundError:
                    st.error("Database file not found")

    st.divider()

    with st.expander("✏️ Edit Product"):
        st.subheader("✏️ Edit Product")
        edit_code = st.text_input(
            "Enter Product Code Number to Edit",
            placeholder="470217206",
            key="edit_product"
        )

        new_price = st.number_input("New Price", min_value=0, key="edit_price")
        new_reviews = st.number_input("New Reviews", min_value=0, step=100, key="edit_reviews")
        new_rating = st.number_input(
            "New Rating",
            min_value=0.0,
            max_value=5.0,
            value=4.0,
            step=0.1,
            key="edit_rating"
        )

        if st.button("Update Product"):
            if edit_code.strip() == "":
                st.warning("Please enter a product code number")
            else:
                edit_product_code = str(edit_code).strip()
                try:
                    edit_df = load_products()

                    if (
                        edit_product_code not in edit_df["ProductCode"].astype(str).values
                        and f"S-{edit_product_code}" not in edit_df["ProductCode"].astype(str).values
                        and f"RT-{edit_product_code}" not in edit_df["ProductCode"].astype(str).values
                    ):
                        st.warning("Product not found")
                    else:
                        edit_df.loc[
                            (edit_df["ProductCode"].astype(str) == edit_product_code)
                            | (edit_df["ProductCode"].astype(str) == f"S-{edit_product_code}")
                            | (edit_df["ProductCode"].astype(str) == f"RT-{edit_product_code}"),
                            ["Price", "Reviews", "Rating"]
                        ] = [new_price, new_reviews, new_rating]

                        save_products(edit_df)
                        st.success(f"✅ {edit_product_code} updated successfully!")
                        st.toast("✏️ Product updated", icon="✅")
                        st.balloons()
                except FileNotFoundError:
                    st.error("Database file not found")


if menu == "📈 Analytics Dashboard":
    try:
        df = load_products()
    except FileNotFoundError:
        st.warning("No products available. Add products to start analysis.")
        st.stop()

    df["Reviews"] = pd.to_numeric(
        df["Reviews"].astype(str).str.replace("Reviews", "", regex=False).str.replace(",", "", regex=False).str.strip(),
        errors="coerce"
    ).fillna(0)

    df["Rating"] = pd.to_numeric(
        df["Rating"],
        errors="coerce"
    ).fillna(0)

    df["Price"] = pd.to_numeric(
        df["Price"].astype(str).str.replace("₹", "", regex=False).str.replace(",", "", regex=False).str.strip(),
        errors="coerce"
    ).fillna(0)

    df["Score"] = (df["Reviews"] * 0.4) + (df["Rating"] * 1000 * 0.6)

    df = df.sort_values(by="Score", ascending=False)
    df = df.reset_index(drop=True)
    df.insert(0, "Rank", df.index + 1)

    st.subheader("🎯 Filters")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    min_rating = filter_col1.slider(
        "Minimum Rating",
        min_value=0.0,
        max_value=5.0,
        value=0.0,
        step=0.1
    )

    min_reviews = filter_col2.number_input(
        "Minimum Reviews",
        min_value=0,
        value=0,
        step=100
    )

    max_price = int(df["Price"].max()) if len(df) > 0 else 1000

    if max_price <= 0:
        max_price = 100

    price_range = filter_col3.slider(
        "Price Range",
        min_value=0,
        max_value=max_price,
        value=(0, max_price)
    )

    filtered_df = df[
        (df["Rating"] >= min_rating)
        & (df["Reviews"] >= min_reviews)
        & (df["Price"] >= price_range[0])
        & (df["Price"] <= price_range[1])
    ]

    if len(filtered_df) > 0:
        df = filtered_df.reset_index(drop=True)
        df["Rank"] = df.index + 1

    st.divider()

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.markdown("## 🚀 Command Center")
    st.subheader("📈 Dashboard Overview")
    metric1, metric2, metric3, metric4 = st.columns(4)
    metric1.metric("Products", len(df))
    metric2.metric("Best Rating", round(df["Rating"].max(), 2))
    metric3.metric("Best Score", round(df["Score"].max(), 1))
    metric4.metric("Total Reviews", f"{int(df['Reviews'].sum()):,}")

    st.divider()

    st.download_button(
        label="📥 Download CSV",
        data=csv_data,
        file_name="robel_traders_products.csv",
        mime="text/csv"
    )

    st.subheader("Top Products")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Products", len(df))
    col2.metric("Best Score", round(df["Score"].max(), 1))
    col3.metric("Average Rating", round(df["Rating"].mean(), 2))
    st.dataframe(df, width='stretch', hide_index=True)

    render_winners(df)

    render_recommendation(df)

    # Charts and distributions
    st.subheader("📊 Top 10 Products by Score")
    fig1 = px.bar(df.head(10), x="ProductCode", y="Score", title="Top Products by Score")
    fig1.update_layout(template="plotly_dark")
    st.plotly_chart(fig1, width='stretch')

    st.subheader("⭐ Rating Distribution")
    fig2 = px.pie(df, names="ProductCode", values="Reviews", title="Reviews Distribution")
    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, width='stretch')

    st.subheader("📝 Reviews Distribution")
    fig3 = px.line(df, x="ProductCode", y="Rating", title="Rating Trend", markers=True)
    fig3.update_layout(template="plotly_dark")
    st.plotly_chart(fig3, width='stretch')

    st.divider()
    st.caption("© 2026 Robel Traders | Version 2.0 Enterprise | Developed by Priyanshu Singh")
if menu == "🔍 Research Center":
    st.header("🔍 Research Center")

    keyword = st.text_input(
        "Research Keyword",
        placeholder="women kurti"
    )

    product_limit = st.slider(
        "Products to Collect",
        min_value=10,
        max_value=100,
        value=20,
        step=10
    )

    product_url = st.text_input(
        "🔗 Product URL",
        placeholder="Paste Meesho product URL here..."
    )

    st.info("Future Meesho collection module will save data directly into robel.db")

    if st.button("🚀 Start Research"):
        if keyword.strip() == "":
            st.warning("Enter a keyword first")
        else:
            result_df = collector.collect_sample_data(keyword)

            st.success(f"Research completed for: {keyword}")
            st.write(f"Collected Products: {len(result_df)}")
            st.dataframe(result_df, width='stretch')

    paste_result = paste_image_button("📋 Paste Screenshot (Cmd+V)")

    uploaded_images = st.file_uploader(
        "📸 Upload Screenshots / Product Images",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True
    )

    if getattr(paste_result, "image_data", None) is not None:
        uploaded_images = [paste_result.image_data]

    if uploaded_images:
        st.write(f"📸 {len(uploaded_images)} image(s) selected")
        st.image(uploaded_images[0], caption="Preview", width='stretch')
    if st.button("📸 Extract Screenshot Data"):
        if not uploaded_images:
            st.warning("Upload at least one screenshot first")
        else:
            import tempfile

            all_results = []
            progress = st.progress(0)

            for idx, uploaded_image in enumerate(uploaded_images):
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                    temp_path = tmp.name

                    if hasattr(uploaded_image, 'getbuffer'):
                        tmp.write(uploaded_image.getbuffer())
                    else:
                        uploaded_image.save(temp_path)

                result_df = extractor.extract_data(temp_path)

                if result_df is not None and not result_df.empty:
                    all_results.append(result_df)

                progress.progress((idx + 1) / len(uploaded_images))

            if all_results:
                final_df = pd.concat(all_results, ignore_index=True)

                try:
                    existing_df = load_products()
                    final_df = pd.concat([existing_df, final_df], ignore_index=True)
                    final_df = final_df.drop_duplicates(subset=["ProductCode"], keep="last")
                except Exception:
                    pass

                save_products(final_df)

                st.success(f"✅ {len(all_results)} screenshot(s) processed and saved")
                st.dataframe(final_df.tail(len(all_results)), width='stretch')
                st.toast("💾 Bulk save completed", icon="✅")
            else:
                st.error("No product data could be extracted")

    st.divider()

    if st.button("🔗 Analyze Product URL"):
        if product_url.strip() == "":
            st.warning("Paste a product URL first")
        else:
            result_df = collector.collect_from_url(product_url)

            if result_df is not None and not result_df.empty:
                save_products(result_df)
                st.success(f"✅ Product URL analyzed and saved ({len(result_df)} record)")
                st.dataframe(result_df, width='stretch')
            else:
                st.error("No data was returned from the product URL")

if menu == "⚙️ Settings":
    st.header("⚙️ Settings")
    st.info("Enterprise settings panel coming soon")