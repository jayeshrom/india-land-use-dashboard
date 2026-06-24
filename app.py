import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "packages"))

from io import StringIO
from typing import List

import pandas as pd
import plotly.express as px
import streamlit as st


# Exact source: Government of India, Land Use Statistics at a Glance 2023-24,
# Table 1: Land Use Classification - All India. Units are thousand hectares.
LAND_USE_CSV = """
Year,Reporting Area,Forests,Area under non-agricultural uses,Barren and unculturable land,Permanent pastures and other grazing lands,Land under miscellaneous tree crops and groves,Culturable waste land,Fallow lands other than current fallows,Current fallows,Net area sown
1950-51,284315,40482,9357,38160,6675,19828,22943,17445,10679,118746
1951-52,287827,48889,12690,37484,8592,7881,23929,15154,13808,119400
1952-53,290787,51154,12321,37420,8634,7757,23680,13480,12899,123442
1953-54,291901,51079,13283,36379,10881,5800,22898,12750,12025,126806
1954-55,291378,50431,13784,34517,11218,5770,22805,13045,11963,127845
1955-56,291917,51343,13921,34475,11473,5885,21537,12544,11583,129156
1956-57,292179,51391,13981,33387,12186,5784,21276,11968,11358,130848
1957-58,293435,52178,14105,33232,12831,6087,20602,12620,12700,129080
1958-59,293661,51406,14300,33155,13090,6000,20175,12255,11452,131828
1959-60,297254,54021,14899,33434,13679,5818,19463,11076,11925,132939
1960-61,298458,54052,14840,35911,13966,4459,19212,11180,11639,133199
1961-62,299151,54189,14795,35921,14082,4500,18632,10478,11155,135399
1962-63,304977,60538,15111,35164,14104,4558,17908,10195,11058,136341
1963-64,305169,60692,15270,34811,14594,4378,17653,10059,11229,136483
1964-65,305252,60351,15442,34795,14743,4113,17366,9166,11156,138120
1965-66,305535,61543,15170,34327,14810,4076,16965,9262,13184,136198
1966-67,305487,63458,15357,32159,14017,4018,16671,9046,13529,137232
1967-68,306120,64217,15474,31830,13795,3969,16235,8800,11924,139876
1968-69,305885,64790,15648,31591,13316,3878,16064,9189,14096,137313
1969-70,303893,63895,15868,30290,12992,4448,15788,9594,12323,138695
1970-71,303753,63830,16478,28128,13261,4367,17500,8728,10598,140863
1971-72,304141,63771,16972,27996,12960,4284,17456,8312,12669,139721
1972-73,303992,65430,16658,25821,12707,4531,17332,9193,15176,137144
1973-74,304093,65729,16799,25217,12781,4138,17066,8655,11292,142416
1974-75,304141,65878,18377,23160,12856,3771,17032,8969,16307,137791
1975-76,304329,66699,18660,21578,12592,3630,17743,9229,12546,141652
1976-77,304680,67159,18934,21522,12532,3628,17474,9385,14570,139476
1977-78,304179,67138,19047,20219,12353,3691,17183,9567,13028,141953
1978-79,304681,67465,19201,20143,12136,3627,17292,9366,12470,142981
1979-80,304130,67501,19543,20156,12118,3527,16658,10026,15698,138903
1980-81,304159,67460,19596,19958,11989,3578,16744,9720,14826,140288
1981-82,304282,67365,19630,20092,12025,3603,16424,9658,13365,142120
1982-83,304093,67330,19865,20104,11930,3545,16332,9357,14817,140813
1983-84,304190,66599,20237,20337,12034,3628,15565,9271,13308,143211
1984-85,304310,66391,20458,20239,12000,3569,15882,9512,15358,140901
1985-86,304698,67067,20631,20090,11783,3563,15718,10051,14894,140901
1986-87,305009,66875,20879,20164,11838,3632,15548,10255,16240,139578
1987-88,304837,66936,21168,20112,11723,3509,15530,10862,20912,134085
1988-89,304826,66944,21299,19916,11525,3514,15167,10247,14323,141891
1989-90,304878,67406,21258,19699,11304,3803,15102,10273,13694,142339
1990-91,305023,67702,21220,19509,11406,3813,15000,9663,13840,142870
1991-92,304898,67866,21465,19268,11299,3761,14994,9941,14672,141632
1992-93,304846,67981,21772,19122,11096,3781,14589,9672,14188,142645
1993-94,304881,68277,22210,18694,10966,3696,14409,9834,14376,142419
1994-95,304829,68603,22556,18463,11034,3732,14262,9969,13250,142960
1995-96,304875,68817,22362,19009,11064,3481,14098,10016,13831,142197
1996-97,304622,69103,22554,17964,10880,3655,14021,10192,13323,142931
1997-98,304661,69246,23138,17461,10845,3730,13943,10078,14275,141945
1998-99,305004,69215,23346,17527,10896,3679,13899,10106,13584,142753
1999-00,305016,69164,23598,17536,10845,3725,13742,10289,15053,141063
2000-01,305195,69843,23752,17483,10662,3445,13631,10267,14777,141336
2001-02,305127,69720,23914,17414,10528,3442,13520,10513,15343,140734
2002-03,305358,69821,24119,17517,10450,3431,13651,11966,22459,131943
2003-04,305567,69968,24516,17466,10484,3381,13241,11313,14489,140708
2004-05,305587,69960,24761,17468,10452,3362,13272,10878,14792,140642
2005-06,306884,71431,24993,17331,10444,3391,13225,10696,14213,141162
2006-07,307088,71463,25445,17287,10418,3351,13274,10516,15512,139823
2007-08,307232,71529,25882,17020,10362,3400,13044,10333,14646,141016
2008-09,307408,71543,26211,16851,10344,3343,12735,10290,14192,141899
2009-10,307408,71555,26158,17177,10340,3214,12945,10838,16009,139173
2010-11,307224,71593,26422,16990,10303,3200,12643,10325,14379,141370
2011-12,307134,71618,26355,16980,10264,3160,12636,10669,14660,140792
2012-13,307232,71590,26549,16833,10211,3181,12642,11040,15439,139746
2013-14,307538,71848,26958,16706,10215,3186,12386,10698,14304,141238
2014-15,307523,72071,27146,16839,10199,3103,12553,11093,15075,139445
2015-16,307493,72137,27270,16502,10214,3092,12284,11310,15711,138974
2016-17,308058,72295,28042,16507,10291,3125,12211,11288,15298,139000
2017-18,307509,72334,27557,16510,10291,3169,12250,11640,14988,138770
2018-19,307528,72295,27589,16693,10328,3155,12162,11654,15214,138439
2019-20,306542,71751,27777,16542,10480,3134,11945,11242,13770,139901
2020-21,306982,71980,27726,16684,10327,3012,11905,10818,12986,141544
2021-22,306486,72000,27578,16515,10281,3013,11920,10917,13255,141007
2022-23,306650,72021,27845,16554,10248,2992,11659,11128,13498,140705
2023-24,306934,72021,28549,16589,10210,2948,11586,11163,14907,138992
""".strip()

CATEGORIES = [
    "Forests",
    "Area under non-agricultural uses",
    "Barren and unculturable land",
    "Permanent pastures and other grazing lands",
    "Land under miscellaneous tree crops and groves",
    "Culturable waste land",
    "Fallow lands other than current fallows",
    "Current fallows",
    "Net area sown",
]

COLOR_MAP = {
    "Forests": "#2f855a",
    "Area under non-agricultural uses": "#2563eb",
    "Barren and unculturable land": "#8b5e34",
    "Permanent pastures and other grazing lands": "#84cc16",
    "Land under miscellaneous tree crops and groves": "#16a34a",
    "Culturable waste land": "#d97706",
    "Fallow lands other than current fallows": "#f59e0b",
    "Current fallows": "#ef4444",
    "Net area sown": "#0f766e",
}


@st.cache_data
def load_data() -> pd.DataFrame:
    """Read the hardcoded CSV and coerce any non-numeric tokens safely."""
    df = pd.read_csv(StringIO(LAND_USE_CSV), dtype=str)
    df["Year Start"] = df["Year"].str.slice(0, 4).astype(int)
    for column in ["Reporting Area", *CATEGORIES]:
        cleaned = df[column].str.replace(r"[^0-9.\-]", "", regex=True)
        df[column] = pd.to_numeric(cleaned, errors="coerce")
    df["Total Cultivated Land"] = df["Current fallows"] + df["Net area sown"]
    df["Total Uncultivated Land"] = df[[cat for cat in CATEGORIES if cat not in {"Current fallows", "Net area sown"}]].sum(axis=1)
    return df.sort_values("Year Start").reset_index(drop=True)


def metric_card(title: str, value: float, suffix: str = " thousand ha") -> str:
    """Return compact Power BI-style KPI card markup."""
    return f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value:,.0f}</div>
        <div class="kpi-subtitle">{suffix}</div>
    </div>
    """


def apply_theme() -> None:
    st.set_page_config(page_title="India Land Use Dashboard", layout="wide")
    st.markdown(
        """
        <style>
        .main .block-container {padding-top: 1.2rem; padding-bottom: 1.5rem;}
        h1, h2, h3, .stMarkdown {color: #172033;}
        [data-testid="stSidebar"] {background: #f3f6fa;}
        [data-testid="stSidebar"] * {
            color: #172033 !important;
            opacity: 1 !important;
        }
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span {
            color: #172033 !important;
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #172033 !important;
        }
        [data-testid="stSidebar"] [data-baseweb="checkbox"] svg {
            color: #ffffff !important;
            fill: #ffffff !important;
        }
        [data-testid="stSidebar"] [data-baseweb="checkbox"] > div:first-child {
            background-color: #1f4e79 !important;
            border-color: #1f4e79 !important;
        }
        [data-testid="stSidebar"] [data-baseweb="slider"] div {
            color: #172033 !important;
        }
        .report-header {
            margin: 0 0 1.35rem 0;
            padding: 0.25rem 0 0.15rem 0;
            border-left: 6px solid #00a6d6;
            padding-left: 1rem;
        }
        .dashboard-title {
            font-size: 2.15rem;
            font-weight: 850;
            color: #25c7f7;
            line-height: 1.1;
            margin-bottom: 0.35rem;
            letter-spacing: 0;
            text-shadow: 0 0 18px rgba(37, 199, 247, 0.22);
        }
        .dashboard-subtitle {
            font-size: 1rem;
            color: #b9e9f8;
            margin-bottom: 0.45rem;
            font-weight: 500;
        }
        .dashboard-context {
            display: inline-flex;
            gap: 0.55rem;
            align-items: center;
            color: #7dd3fc;
            font-size: 0.82rem;
            font-weight: 700;
            text-transform: uppercase;
        }
        .dashboard-context span {
            background: rgba(0, 166, 214, 0.14);
            border: 1px solid rgba(125, 211, 252, 0.28);
            border-radius: 999px;
            padding: 0.22rem 0.55rem;
        }
        .kpi-card {
            background: #ffffff;
            border: 1px solid #d9e2ec;
            border-left: 5px solid #1f4e79;
            border-radius: 8px;
            padding: 1rem 1.1rem;
            box-shadow: 0 2px 8px rgba(23, 32, 51, 0.07);
        }
        .kpi-title {font-size: 0.78rem; color: #526070; font-weight: 700; text-transform: uppercase;}
        .kpi-value {font-size: 1.9rem; color: #172033; font-weight: 800; line-height: 1.2;}
        .kpi-subtitle {font-size: 0.78rem; color: #6b7280;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def line_chart(df: pd.DataFrame, selected_categories: List[str]):
    long_df = df.melt(
        id_vars=["Year", "Year Start"],
        value_vars=selected_categories,
        var_name="Nine-Fold Classification",
        value_name="Area (thousand hectares)",
    )
    fig = px.line(
        long_df,
        x="Year",
        y="Area (thousand hectares)",
        color="Nine-Fold Classification",
        markers=True,
        color_discrete_map=COLOR_MAP,
        labels={"Year": "Agricultural Year", "Area (thousand hectares)": "Area (thousand hectares)"},
        hover_data={"Year Start": False, "Area (thousand hectares)": ":,.0f"},
    )
    fig.update_layout(legend_title_text="Nine-Fold Classification", hovermode="x unified", height=470)
    fig.update_xaxes(tickangle=-45)
    return fig


def donut_chart(row: pd.Series):
    donut_df = pd.DataFrame({"Category": CATEGORIES, "Area": [row[col] for col in CATEGORIES]})
    fig = px.pie(
        donut_df,
        names="Category",
        values="Area",
        hole=0.58,
        color="Category",
        color_discrete_map=COLOR_MAP,
        labels={"Area": "Area (thousand hectares)", "Category": "Nine-Fold Classification"},
    )
    fig.update_traces(textposition="inside", textinfo="percent", hovertemplate="%{label}<br>%{value:,.0f} thousand ha<br>%{percent}<extra></extra>")
    fig.update_layout(legend_title_text="Nine-Fold Classification", height=440)
    return fig


def stacked_decade_chart(df: pd.DataFrame, max_year_start: int):
    decade_df = df[(df["Year Start"] % 10 == 0) | (df["Year Start"] == max_year_start)].copy()
    decade_df = decade_df.drop_duplicates(subset=["Year Start"], keep="last")
    plot_df = decade_df.melt(
        id_vars=["Year", "Year Start"],
        value_vars=["Total Uncultivated Land", "Total Cultivated Land"],
        var_name="Land Group",
        value_name="Area (thousand hectares)",
    )
    fig = px.bar(
        plot_df,
        x="Year",
        y="Area (thousand hectares)",
        color="Land Group",
        barmode="stack",
        color_discrete_map={"Total Cultivated Land": "#0f766e", "Total Uncultivated Land": "#64748b"},
        labels={"Year": "Agricultural Year", "Area (thousand hectares)": "Area (thousand hectares)", "Land Group": "Land Group"},
        hover_data={"Year Start": False, "Area (thousand hectares)": ":,.0f"},
    )
    fig.update_layout(legend_title_text="Derived Land Group", height=440)
    return fig


def main() -> None:
    apply_theme()
    df = load_data()

    st.sidebar.header("Report Controls")
    min_year, max_year = int(df["Year Start"].min()), int(df["Year Start"].max())
    year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year), 1)
    selected_categories = [cat for cat in CATEGORIES if st.sidebar.checkbox(cat, value=True)]

    filtered = df[df["Year Start"].between(*year_range)].copy()
    current = filtered.loc[filtered["Year Start"].idxmax()]
    base = df.loc[df["Year Start"].idxmin()]

    st.markdown(
        f"""
        <div class="report-header">
            <div class="dashboard-title">India Land Use Dashboard</div>
            <div class="dashboard-subtitle">Nine-Fold Land Use Classification | {filtered["Year"].iloc[0]} to {current["Year"]}</div>
            <div class="dashboard-context">
                <span>All India</span>
                <span>Thousand hectares</span>
                <span>Historical land records</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.markdown(metric_card("Current Net Sown Area", current["Net area sown"]), unsafe_allow_html=True)
    kpi2.markdown(metric_card("Current Forest Cover", current["Forests"]), unsafe_allow_html=True)
    urban_change = current["Area under non-agricultural uses"] - base["Area under non-agricultural uses"]
    kpi3.markdown(metric_card("Urban / Non-Agri Change Since 1950", urban_change), unsafe_allow_html=True)

    st.subheader("Main Historical Trends")
    if selected_categories:
        st.plotly_chart(line_chart(filtered, selected_categories), use_container_width=True)
    else:
        st.warning("Select at least one land category in the sidebar to display the trend chart.")

    left, right = st.columns(2)
    with left:
        st.subheader(f"Nine-Fold Share in {current['Year']}")
        st.plotly_chart(donut_chart(current), use_container_width=True)
    with right:
        st.subheader("Cultivated vs Uncultivated Land by Decade")
        st.plotly_chart(stacked_decade_chart(filtered, int(current["Year Start"])), use_container_width=True)


if __name__ == "__main__":
    main()
