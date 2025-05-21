import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# تحميل البيانات
file_path = "درجات_حرارة_بمعادلات_محدثة.xlsx"
df = pd.read_excel(file_path)

# مؤشرات الأداء
total_sites = df["رقم الموقع"].nunique()
avg_diff = round(df["الفرق (°C)"].mean(), 2)
top_technique = df["نوع التقنية المستخدمة"].mode()[0]

# تهيئة التطبيق
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "داشبورد كدانة"

# الرسومات
bar_fig = px.histogram(df, x="نوع التقنية المستخدمة", color="معادلة النتيجة (انخفاض/ثبات/ارتفاع)",
                       barmode="group", text_auto=True)
bar_fig.update_layout(template="simple_white")

pie_fig = px.pie(df, names="معادلة النتيجة (انخفاض/ثبات/ارتفاع)", hole=0.5)
pie_fig.update_traces(textinfo='percent+label')
pie_fig.update_layout(template="simple_white")

line_fig = px.line(df, x="توقيت القياس", y="الفرق (°C)", color="نوع التقنية المستخدمة", markers=True)
line_fig.update_layout(template="simple_white")

# تصميم الواجهة
app.layout = dbc.Container([
    html.H2("لوحة تحكم درجات الحرارة - كدانة", className="text-center mb-4"),

    dbc.Row([
        dbc.Col(html.Div(className="card", children=[
            html.Div("عدد المواقع", className="kpi-title"),
            html.Div(f"{total_sites}", className="kpi-value"),
        ]), width=4),

        dbc.Col(html.Div(className="card", children=[
            html.Div("متوسط الفرق (°C)", className="kpi-title"),
            html.Div(f"{avg_diff}", className="kpi-value"),
        ]), width=4),

        dbc.Col(html.Div(className="card", children=[
            html.Div("أكثر تقنية استخداماً", className="kpi-title"),
            html.Div(top_technique, className="kpi-value"),
        ]), width=4),
    ]),

    dbc.Row([
        dbc.Col(html.Div(className="card", children=[
            html.H5("توزيع النتائج حسب التقنية"),
            dcc.Graph(figure=bar_fig)
        ]), width=6),

        dbc.Col(html.Div(className="card", children=[
            html.H5("نسبة توزيع النتائج"),
            dcc.Graph(figure=pie_fig)
        ]), width=6),
    ]),

    dbc.Row([
        dbc.Col(html.Div(className="card", children=[
            html.H5("تغير الفرق الحراري مع الوقت"),
            dcc.Graph(figure=line_fig)
        ]), width=12),
    ])
], fluid=True)

# تشغيل التطبيق
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

