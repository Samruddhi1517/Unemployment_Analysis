import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Unemployment Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)


st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #F5F5DC, #E8DCC4);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #DCC7AA, #CBB89D);
}

section[data-testid="stSidebar"] * {
    color: #4E3D2A !important;
}

/* Upload Box */
[data-testid="stFileUploader"] {
    background: #F8F1E7;
    border: 2px dashed #8B7355;
    border-radius: 15px;
    padding: 15px;
}

/* Metric Cards */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #DCC7AA, #CBB89D);
    border-radius: 15px;
    padding: 15px;
    color: #4E3D2A;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
}

/* Headers */
h1 {
    color: white !important;
}

h2, h3 {
    color: #8B7355 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #CBB89D, #DCC7AA);
    color: #4E3D2A;
    border: none;
    border-radius: 10px;
    font-weight: bold;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #BFA88A, #D6C2A8);
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] {
    background-color: white;
    border-radius: 10px;
}

/* DataFrame */
[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
}

/* Text */
p, li, label {
    color: #5C4B37 !important;
}

/* Divider */
hr {
    border-color: #CBB89D;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div style='
padding:30px;
border-radius:20px;
background:linear-gradient(90deg,#CBB89D,#DCC7AA,#F5F5DC);
text-align:center;
color:#4E3D2A;
box-shadow:0px 6px 20px rgba(0,0,0,0.15);'>

<h1 style="color:#4E3D2A;">📊 Unemployment Analysis Dashboard</h1>

<p style='font-size:18px;color:#5C4B37;'>
Analyze unemployment trends, investigate COVID-19 impact,
identify seasonal patterns, and generate policy insights.
</p>

</div>
""", unsafe_allow_html=True)


st.sidebar.markdown(
    "<h2 style='color:#FFD700;'>⚙ Dashboard Controls</h2>",
    unsafe_allow_html=True
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Unemployment Dataset",
    type=["csv"]
)


if uploaded_file is None:

    st.info("⬅ Upload your unemployment dataset to begin analysis.")

    st.markdown("""
    ### Project Features

    ✅ Data Cleaning

    ✅ Exploratory Data Analysis (EDA)

    ✅ Interactive Visualizations

    ✅ COVID-19 Impact Analysis

    ✅ Seasonal Trend Analysis

    ✅ State-wise Comparison

    ✅ Correlation Analysis

    ✅ Policy Recommendations
    """)


else:

    df = pd.read_csv(uploaded_file)

    # Remove duplicates
    duplicates_before = df.duplicated().sum()
    df = df.drop_duplicates()

    st.success("Dataset Loaded Successfully!")

    
    date_col = None

    for col in df.columns:
        if "date" in col.lower():
            date_col = col
            df[date_col] = pd.to_datetime(df[date_col])
            break

  
    st.header("📂 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", int(df.isnull().sum().sum()))
    col4.metric("Duplicates Removed", int(duplicates_before))

    st.dataframe(df.head(), use_container_width=True)

    st.divider()

  
    numeric_cols = df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    if len(numeric_cols) == 0:
        st.error("No numerical columns available.")
        st.stop()

    unemployment_col = st.sidebar.selectbox(
        "Select Unemployment Rate Column",
        numeric_cols
    )

    
    st.header("📈 Key Statistics")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Average Rate",
        f"{df[unemployment_col].mean():.2f}%"
    )

    c2.metric(
        "Highest Rate",
        f"{df[unemployment_col].max():.2f}%"
    )

    c3.metric(
        "Lowest Rate",
        f"{df[unemployment_col].min():.2f}%"
    )

    st.divider()

  
    st.header("📊 Distribution Analysis")

    fig = px.histogram(
        df,
        x=unemployment_col,
        nbins=30,
        title=f"Distribution of {unemployment_col}"
    )

    st.plotly_chart(fig, use_container_width=True)


    st.header("📦 Outlier Detection")

    fig = px.box(
        df,
        y=unemployment_col,
        title=f"Boxplot of {unemployment_col}"
    )

    st.plotly_chart(fig, use_container_width=True)

  
    if date_col:

        st.header("📈 Unemployment Trend Over Time")

        trend = (
            df.groupby(date_col)[unemployment_col]
            .mean()
            .reset_index()
        )

        fig = px.line(
            trend,
            x=date_col,
            y=unemployment_col,
            markers=True,
            title="Average Unemployment Trend"
        )

        st.plotly_chart(fig, use_container_width=True)

      
        st.header("🦠 COVID-19 Impact Analysis")

        pre_covid = df[df[date_col] < "2020-03-01"]
        post_covid = df[df[date_col] >= "2020-03-01"]

        pre_avg = pre_covid[unemployment_col].mean()
        post_avg = post_covid[unemployment_col].mean()

        a, b = st.columns(2)

        a.metric(
            "Pre-COVID Average",
            f"{pre_avg:.2f}%"
        )

        b.metric(
            "Post-COVID Average",
            f"{post_avg:.2f}%"
        )

        covid_df = pd.DataFrame({
            "Period": ["Pre-COVID", "Post-COVID"],
            "Rate": [pre_avg, post_avg]
        })

        fig = px.bar(
            covid_df,
            x="Period",
            y="Rate",
            color="Period",
            title="COVID-19 Impact on Unemployment"
        )

        st.plotly_chart(fig, use_container_width=True)

     
        st.header("📅 Seasonal Trend Analysis")

        df["Month"] = df[date_col].dt.month_name()

        month_order = [
            "January","February","March","April",
            "May","June","July","August",
            "September","October","November","December"
        ]

        monthly = (
            df.groupby("Month")[unemployment_col]
            .mean()
            .reset_index()
        )

        monthly["Month"] = pd.Categorical(
            monthly["Month"],
            categories=month_order,
            ordered=True
        )

        monthly = monthly.sort_values("Month")

        fig = px.bar(
            monthly,
            x="Month",
            y=unemployment_col,
            color=unemployment_col,
            title="Monthly Unemployment Pattern"
        )

        st.plotly_chart(fig, use_container_width=True)

 
    region_cols = [
        col for col in df.columns
        if "region" in col.lower()
        or "state" in col.lower()
    ]

    if region_cols:

        region_col = region_cols[0]

        st.header("🏙 Top Regions by Unemployment")

        region_df = (
            df.groupby(region_col)[unemployment_col]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig = px.bar(
            region_df,
            x=region_col,
            y=unemployment_col,
            color=unemployment_col,
            title="Top 10 Regions with Highest Unemployment"
        )

        st.plotly_chart(fig, use_container_width=True)

    if len(numeric_cols) > 1:

        st.header("🔥 Correlation Heatmap")

        corr = df[numeric_cols].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="Blues"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.header("📋 Key Insights & Recommendations")

    st.success("""
• Unemployment trends can be monitored over time using historical data.

• COVID-19 significantly affected employment levels in many regions.

• Some states consistently show higher unemployment rates.

• Seasonal fluctuations suggest that employment opportunities vary throughout the year.

• Governments can use these insights to create targeted job programs and economic policies.

• Investment in skill development and regional employment initiatives can help reduce unemployment.
""")

   