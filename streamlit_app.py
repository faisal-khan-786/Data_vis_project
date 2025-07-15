import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS


st.set_page_config(
    page_title="Olist E-commerce Dashboard",
    page_icon="🛒",
    layout="wide"
)


@st.cache_data
def load_data():
    orders    = pd.read_csv("data/olist_orders_dataset.csv",
                            parse_dates=["order_purchase_timestamp",
                                         "order_delivered_customer_date",
                                         "order_estimated_delivery_date"])
    items     = pd.read_csv("data/olist_order_items_dataset.csv")
    products  = pd.read_csv("data/olist_products_dataset.csv")
    payments  = pd.read_csv("data/olist_order_payments_dataset.csv")
    customers = pd.read_csv("data/olist_customers_dataset.csv")
    translate = pd.read_csv("data/product_category_name_translation.csv")
    reviews   = pd.read_csv("data/olist_order_reviews_dataset.csv")
    return orders, items, products, payments, customers, translate, reviews

orders, items, products, payments, customers, translate, reviews = load_data()


st.sidebar.header("Filters")

min_date = orders["order_purchase_timestamp"].min().date()
max_date = orders["order_purchase_timestamp"].max().date()

date_range = st.sidebar.date_input(
    "Order date range",
    (min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

start_d, end_d = [pd.to_datetime(d) for d in date_range]
orders_filt = orders[
    orders["order_purchase_timestamp"].between(start_d, end_d)
]
order_ids = orders_filt["order_id"]

# -------- 3. KPI – repeat-customer rate ----------
uid_lookup     = customers[["customer_id", "customer_unique_id"]]
orders_uid     = orders_filt.merge(uid_lookup, on="customer_id", how="left")
orders_per_uid = orders_uid.groupby("customer_unique_id").size()
repeat_rate    = (orders_per_uid > 1).mean() * 100
st.metric("Repeat-customer rate", f"{repeat_rate:,.2f} %")

st.divider()

tabs = st.tabs([
    "Orders over Time",
    "Revenue by Category",
    "Payment Types",
    "Delivery Time by State",
    "Delay vs Review",
    "Repeat vs One-time",
    "Installments vs Value",
    "Top Sellers",
    "Cancellation Rate",
    "Word Cloud"
])


with tabs[0]:
    month_series = (
        orders_filt["order_purchase_timestamp"]
        .dt.to_period("M").astype(str)
        .value_counts()
        .sort_index()
    )
    fig = px.line(
        month_series,
        labels={"value": "Number of Orders", "index": "Month"},
        title="Monthly Order Volume"
    )
    st.plotly_chart(fig, use_container_width=True)


with tabs[1]:
    tmp = (
        items[items["order_id"].isin(order_ids)]
        .merge(products[["product_id", "product_category_name"]],
               on="product_id")
        .merge(translate, on="product_category_name", how="left")
    )
    tmp["cat"] = tmp["product_category_name_english"] \
                   .fillna(tmp["product_category_name"])
    rev_cat = (
        tmp.groupby("cat")["price"].sum()
          .sort_values(ascending=False)
          .head(15)
          .reset_index()
    )
    fig = px.bar(
        rev_cat,
        x="price",
        y="cat",
        orientation="h",
        labels={"price": "Revenue (BRL)", "cat": "Category"},
        title="Top 15 Categories by Revenue"
    )
    fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig, use_container_width=True)


with tabs[2]:
    pay_counts = payments[payments["order_id"].isin(order_ids)] \
                    ["payment_type"].value_counts()
    fig = px.pie(
        names=pay_counts.index,
        values=pay_counts.values,
        title="Payment Method Distribution"
    )
    st.plotly_chart(fig, use_container_width=False)


with tabs[3]:
    orders_filt["delivery_days"] = (
        orders_filt["order_delivered_customer_date"] -
        orders_filt["order_purchase_timestamp"]
    ).dt.days
    state_info = orders_filt.merge(
        customers[["customer_id", "customer_state"]],
        on="customer_id", how="left"
    )
    avg_delivery = (
        state_info.groupby("customer_state")["delivery_days"]
        .mean().sort_values()
    )
    fig = px.bar(
        avg_delivery,
        title="Average Delivery Time by State",
        labels={"index": "State", "value": "Mean Days"}
    )
    st.plotly_chart(fig, use_container_width=True)


with tabs[4]:
    rev_join = reviews[reviews["order_id"].isin(order_ids)][
        ["order_id", "review_score"]
    ]
    merged = orders_filt.merge(rev_join, on="order_id", how="inner")
    merged["delay_days"] = (
        merged["order_delivered_customer_date"] -
        merged["order_estimated_delivery_date"]
    ).dt.days
    fig = px.scatter(
        merged,
        x="delay_days",
        y="review_score",
        opacity=0.3,
        labels={"delay_days": "Delivery Delay (days)",
                "review_score": "Review Score"},
        title="Review Score vs Delivery Delay"
    )
    st.plotly_chart(fig, use_container_width=True)


with tabs[5]:
    repeat_cnt = (orders_per_uid > 1).sum()
    one_time   = (orders_per_uid == 1).sum()
    share_rep  = repeat_cnt / len(orders_per_uid) * 100
    fig = px.bar(
        x=["Repeat", "One-time"],
        y=[share_rep, 100-share_rep],
        labels={"x": "", "y": "Customer Share (%)"},
        title="Repeat-Customer Rate"
    )
    fig.update_yaxes(range=[0, 100])
    st.plotly_chart(fig, use_container_width=False)


with tabs[6]:
    order_totals = items[items["order_id"].isin(order_ids)] \
        .groupby("order_id")["price"].sum()
    order_install = payments[payments["order_id"].isin(order_ids)] \
        .groupby("order_id")["payment_installments"].max()
    inst_vs_total = pd.concat([order_totals, order_install], axis=1,
                              join="inner").dropna()
    inst_vs_total.columns = ["order_total", "installments"]
    fig = px.scatter(
        inst_vs_total,
        x="order_total",
        y="installments",
        opacity=0.3,
        title="Installments vs Order Value",
        labels={"order_total": "Order Value (BRL)",
                "installments": "Number of Installments"}
    )
    st.plotly_chart(fig, use_container_width=True)


with tabs[7]:
    item_rev = (
        items[items["order_id"].isin(order_ids)][["order_id", "seller_id"]]
        .merge(rev_join, on="order_id", how="inner")
    )
    top_sellers = (
        item_rev.groupby("seller_id")["review_score"].mean()
        .sort_values(ascending=False)
        .head(10).reset_index()
    )
    fig = px.bar(
        top_sellers,
        x="seller_id",
        y="review_score",
        title="Top 10 Sellers by Avg Review Score",
        labels={"seller_id": "Seller ID", "review_score": "Avg Score"}
    )
    st.plotly_chart(fig, use_container_width=True)


with tabs[8]:
    orders_filt["year_month"] = (
        orders_filt["order_purchase_timestamp"]
        .dt.to_period("M").astype(str)
    )
    total_m   = orders_filt["year_month"].value_counts().sort_index()
    canc_m    = orders_filt[
        orders_filt["order_status"] == "canceled"
    ]["year_month"].value_counts().sort_index()
    canc_rate = (canc_m / total_m * 100).reindex(total_m.index, fill_value=0)
    fig = px.line(
        canc_rate,
        labels={"index": "Month", "value": "Cancellation %"},
        title="Monthly Cancellation Rate"
    )
    st.plotly_chart(fig, use_container_width=True)


with tabs[9]:
    rev_titles = reviews[reviews["order_id"].isin(order_ids)] \
        ["review_comment_title"].dropna()
    all_text = " ".join(rev_titles)
    wc = WordCloud(
        width=800,
        height=400,
        stopwords=STOPWORDS,
        background_color="white"
    ).generate(all_text)
    fig, ax = plt.subplots(figsize=(10,4))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title("Word Cloud – Review Titles")
    st.pyplot(fig)
