import pandas as pd
import plotly.express as px
import plotly.io as pio

def build_bar_chart(df: pd.DataFrame, x: str, y: str, title: str = "Bar Chart") -> str:
    fig = px.bar(df, x=x, y=y, title=title)
    return pio.to_html(fig, full_html=False)

def build_pie_chart(df: pd.DataFrame, names: str, values: str, title: str = "Pie Chart") -> str:
    fig = px.pie(df, names=names, values=values, title=title)
    return pio.to_html(fig, full_html=False)

def build_dashboard(df: pd.DataFrame) -> dict:
    return {
        "bar_chart": build_bar_chart(df, x=df.columns[0], y=df.columns[1], title="Primary Distribution"),
        "pie_chart": build_pie_chart(df, names=df.columns[0], values=df.columns[1], title="Pie Breakdown")
    }