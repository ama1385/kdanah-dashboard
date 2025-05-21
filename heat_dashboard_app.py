import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import os

# تحميل البيانات
file_path = "درجات_حرارة_بمعادلات_محدثة.xlsx"
df = pd.read_excel(file_path)

# مؤشرات الأداء
total_sites = df["رقم الموقع"].nunique()
avg_diff = round(df["الفرق (°C)"].mean(), 2)
top_technique = df["نوع التقنية المستخدمة"].mode()[0]

# الرسوم البيانية
bar_fig = px.histogram(df, x="نوع التقنية المستخدمة", color="معادلة النتيجة (انخفاض/ثبات/ارتفاع)", barmode="group", text_auto=True)
bar_fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

pie_fig = px.pie(df, names="معادلة النتيجة (انخفاض/ثبات/ارتفاع)", hole=0.5)
pie_fig.update_traces(textinfo='percent+label')
pie_fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

line_fig = px.line(df, x="توقيت القياس", y="الفرق (°C)", color="نوع التقنية المستخدمة", markers=True)
line_fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

# إعداد التطبيق
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "لوحة كدانة - الحرارة"

app.layout = dbc.Container([
    html.H2("لوحة تحكم درجات الحرارة - كدانة", className="text-center text-light mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            html.Div("عدد المواقع", className="text-muted text-center"),
            html.H4(f"{total_sites}", className="text-center text-warning")
        ], body=True, className="shadow-sm"), width=12, md=4),

        dbc.Col(dbc.Card([
            html.Div("متوسط الفرق (°C)", className="text-muted text-center"),
            html.H4(f"{avg_diff}", className="text-center text-warning")
        ], body=True, className="shadow-sm"), width=12, md=4),

        dbc.Col(dbc.Card([
            html.Div("أكثر تقنية استخداماً", className="text-muted text-center"),
            html.H5(top_technique, className="text-center text-warning")
        ], body=True, className="shadow-sm"), width=12, md=4),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("توزيع النتائج حسب التقنية", className="text-light"),
            dbc.CardBody(dcc.Graph(figure=bar_fig))
        ]), width=12, md=6),

        dbc.Col(dbc.Card([
            dbc.CardHeader("نسبة توزيع النتائج", className="text-light"),
            dbc.CardBody(dcc.Graph(figure=pie_fig))
        ]), width=12, md=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("تغير الفرق الحراري مع الوقت", className="text-light"),
            dbc.CardBody(dcc.Graph(figure=line_fig))
        ]), width=12),
    ])
], fluid=True)

# تشغيل التطبيق
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
