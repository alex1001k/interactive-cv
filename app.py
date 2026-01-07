from dash import Dash, html, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


PROFILE = {
    "name": "Крюков Александр",
    "title": "BI / Python / SQL Lead",
    "location": "Москва / Удаленно",
    "email": "kryukov.av94@gmail.com",
    "telegram": "@kryukovav",
    "linkedin": "linkedin.com/in/kryukovav",
    "chat_url": "https://t.me/kryukovav",
    "about": "Я делаю аналитику как продукт: проясняю смысл, выстраиваю процессы и помогаю людям принимать решения.",
    "numbers": [
        ("Опыт", "8+ лет"),
        ("Проекты", "20+"),
        ("Роли", "Аналитик → Лид"),
        ("Фокус", "люди + результат"),
    ],
}

EXPERIENCE = [
    {
        "id": "job3",
        "x": 2025,
        "company": "ПАО ТМК",
        "role": "Руководитель группы отчетности",
        "period": "2022 — 2025",
        "start": "Авг 2022",
        "tasks": [
            "Построил систему управленческой отчётности закупок с нуля",
            "Наполнил данными из 4 разноструктурных ERP-систем базы MS SQL и SAP BW/4HANA (100M+ строк)",
            "Спроектировал и поддерживал ETL-процессы на Python с оркестрацией в Apache Airflow, сократив время обновления данных до 2 часов",
            "Создал более 30 отчетов в Power BI для 1 300 пользователей: дизайн сверстал в Figma, продумал пользовательский путь, для лучшего UX в Power BI использовал кастомные визуализации HTML5, SVG-графики, закладки и drill-through детализации",
            "Создал Python-алгоритмы, использующие статистическую базу, для автоматической проверки планов закупок, которые приносят до 150 млн ₽ сокращения затрат в месяц",
            "Оптимизировал сложные SQL-запросы и процедуры для БД, повысив их производительность на 70%",
            "Руководил командой из 3 аналитиков: планирование задач, code review по SQL/Python, развитие компетенций"
        ],
        "wins": ["Время отчётности −40%", "Меньше ручного труда за счёт автоматизации"],
        "stack": ["Python", "SQL", "MSSQL", "Superset"],
        "skills": {"Python":9, "SQL": 8, "Power BI": 8, "Excel": 7}

    },
    {
        "id": "job2",
        "x": 2022,
        "company": "АО СУЭК",
        "role": "Главный специалист -> Начальник отдела",
        "period": "2019 — 2022",
        "start": "Апр 2019",
        "tasks": ["Формировал консолидированную отчетность базе SAP ERP и Oracle. Переносил excel отчеты на Power Query и Power BI",
                   "Сократил время обновления отчетности с 5 дней до 1 часа, автоматизировав ручные операции в python;",
                    "Обеспечивал контроль исполнения ключевых показателей эффективности (KPI) топ-менеджмента закупки, включая оборачиваемость запасов, сроки и объёмы поставок",
                    "Руководил аналитической группой (3 специалиста): распределение задач, контроль сроков и качества выполнения отчетов"
        ],
        "wins": ["15+ отчётов автоматизировано", "Ошибок меньше через QC/проверки"],
        "stack": ["SQL", "Power BI", "Python"],
        "skills": {"Excel": 10, "SQL": 5, "Python": 3, "Power BI": 3}

    },
    {
        "id": "job1",
        "x": 2018,
        "company": "ПАО Газпром нефть",
        "role": "Специалист",
        "period": "2018 — 2019",
        "start": "Дек 2018",
        "tasks": ["Выполнил более 5 тыс. заявок на аккредитацию поставщиков в SRM-системе", 
                  "ПФормировал аналитические справки в excel на базе выгрузок из SAP ERP (до 20 еженедельно)",
                  "Проверил более 1,5 тыс. результатов конкурсных процедур на предмет обоснованности выбора поставщиков и предложений"],
        "wins": ["Ускорил подготовку отчётов за счёт шаблонов"],
        "stack": ["Excel", "SQL"],
        "skills": {"Excel": 4}

    },
]

SKILLS = [
    ("SQL", 9),
    ("Python", 8),
    ("BI (Superset/Power BI)", 8),
    ("Data Modeling", 7),
    ("Коммуникации", 7),
    ("Лидерство", 7),
]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "CV Dashboard"


def timeline_fig(selected_id: str):
    xs = [e["x"] for e in EXPERIENCE]
    ys = [0] * len(EXPERIENCE)

    sel_idx = next((i for i, e in enumerate(EXPERIENCE) if e["id"] == selected_id), 0)

    # Extend to "Now"
    current_x = max(xs) + 0.9

    # Palette (match dark skills vibe + yellow accent)
    axis_color = "rgba(17,24,39,0.92)"
    yellow = "#FDE68A"
    yellow_strong = "#FBBF24"

    base_size = 10
    active_size = 16

    top_labels = [
        f"<b>{e['company']}</b><br><span style='font-size:11px'>{e['role']}</span>"
        for e in EXPERIENCE
    ]
    bottom_labels = [f"<span style='font-size:11px'>{e['start']}</span>" for e in EXPERIENCE]
    hover_text = [
        f"<b>{e['company']}</b><br>{e['role']}<br><span style='font-size:12px'>{e['period']}</span>"
        for e in EXPERIENCE
    ]

    fig = go.Figure()

    # 1) Axis line to "Now"
    fig.add_trace(
        go.Scatter(
            x=xs + [current_x],
            y=ys + [0],
            mode="lines",
            line=dict(width=3, color=axis_color),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # 2) Base clickable markers (all points)
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="markers",
            marker=dict(
                size=[base_size] * len(xs),
                color=yellow,
                line=dict(width=2, color=yellow_strong),
                opacity=0.85,
            ),
            text=hover_text,
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        )
    )

    # 3) Active marker overlay (NOT clickable, just visuals)
    fig.add_trace(
        go.Scatter(
            x=[xs[sel_idx]],
            y=[0],
            mode="markers",
            marker=dict(
                size=active_size,
                color=yellow,
                line=dict(width=4, color=yellow_strong),
                opacity=1.0,
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # 4) Glow/Pulse ring overlay (visual)
    fig.add_trace(
        go.Scatter(
            x=[xs[sel_idx]],
            y=[0],
            mode="markers",
            marker=dict(
                size=active_size + 18,
                color="rgba(0,0,0,0)",
                line=dict(width=2, color="rgba(253,230,138,0.35)"),
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # 5) Labels
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=[0.18] * len(xs),
            mode="text",
            text=top_labels,
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=[-0.18] * len(xs),
            mode="text",
            text=bottom_labels,
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[current_x],
            y=[-0.18],
            mode="text",
            text=["<span style='font-size:11px'><b>Now</b></span>"],
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.update_xaxes(visible=False, range=[min(xs) - 0.6, current_x + 0.2])
    fig.update_yaxes(visible=False, range=[-0.25, 0.25])

    fig.update_layout(
        height=120,
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",

        # smooth transitions on update (works with dcc.Graph(animate=True))
        transition=dict(duration=380, easing="cubic-in-out"),

        hoverlabel=dict(
            bgcolor=yellow,
            bordercolor=yellow_strong,
            font=dict(color="rgba(17,24,39,0.92)", size=12),
        ),
    )

    return fig




def kpi_grid():
    items = []
    for k, v in PROFILE["numbers"]:
        items.append(html.Div([html.Div(k, className="k"), html.Div(v, className="v")], className="item"))
    return html.Div(items, className="kpi")

def skills_block(skills_map: dict[str, int], prev_map: dict[str, int]):
    # сортируем по уровню (desc), затем по названию
    items = sorted(skills_map.items(), key=lambda kv: (-int(kv[1]), kv[0].lower()))

    rows = []
    for idx, (name, level) in enumerate(items):
        level = max(0, min(10, int(level)))
        prev_level = int(prev_map.get(name, 0)) if prev_map else 0

        grew = level > prev_level

        # stagger появления строк (заметно)
        row_style = {"animationDelay": f"{idx * 70}ms"}

        segs = []
        for i in range(10):
            if i < level:
                # если навык вырос — сегменты заполняются заметнее (через delay)
                if grew:
                    segs.append(html.Span(className="seg on", style={"animationDelay": f"{(idx * 70) + (i * 40)}ms"}))
                else:
                    segs.append(html.Span(className="seg on"))
            else:
                segs.append(html.Span(className="seg"))

        row_class = "row grow" if grew else "row"

        rows.append(
            html.Div(
                [
                    html.Div(name, className="name"),
                    html.Div(segs, className="battery"),
                ],
                className=row_class,
                style=row_style,
            )
        )

    # key: чтобы блок считался новым и анимация срабатывала
    key = "skills-" + "-".join([f"{k}{v}" for k, v in items])
    return html.Div(rows, className="skills", key=key)



def ul(items):
    return html.Ul([html.Li(x) for x in items])

# ---- Left: Profile hero (ref style) ----
def profile_hero():
    bg_url = "url('/assets/avatar.jpg')"  # твое фото

    return html.Div(
        className="profile-hero cardx",
        children=[
            # само фото
            html.Div(
                className="profile-media",
                style={"backgroundImage": bg_url},
            ),

            # нижняя плашка с текстом
            html.Div(
                className="profile-footer",
                children=[
                    html.Div("Крюков Александр", className="profile-name"),
                    html.Div(
                        "BI / Python / SQL • Analytics Lead",
                        className="profile-role",
                    ),
                ],
            ),
        ],
    )


# -------- Layout --------
app.layout = html.Div(
    className="page-wrap",
    children=[
        dbc.Row(
            [
                # LEFT
                dbc.Col(
                    width=4,
                    children=[
                        profile_hero(),

                        html.Div(
                            className="cardx cardx-pad",
                            style={"marginTop": "12px"},
                            children=[
                                html.Div("Обо мне в цифрах", className="section-title"),
                                kpi_grid(),
                            ],
                        ),

                        html.Div(
                            className="cardx cardx-pad",
                            style={"marginTop": "12px"},
                            children=[
                                html.Div("Обо мне", className="section-title"),
                                html.Div(PROFILE["about"]),
                                html.Div("Контакты", className="section-title", style={"marginTop": "12px"}),
                                html.Div(PROFILE["email"], className="muted"),
                                html.Div(PROFILE["telegram"], className="muted"),
                                html.Div(PROFILE["linkedin"], className="muted"),
                                html.Div("QR добавим на следующем шаге", className="muted", style={"marginTop": "12px"}),
                            ],
                        ),
                    ],
                ),

                # RIGHT
                dbc.Col(
                    width=8,
                    children=[
                        html.Div(
                            className="cardx cardx-pad",
                            children=[
                                html.Div("Карьера", className="h-title", style={"fontSize": "24px"}),
                                dcc.Graph(
                                    id="timeline",
                                    figure=timeline_fig(EXPERIENCE[0]["id"]),
                                    className="dash-graph",
                                    animate=True, 
                                    config={"displayModeBar": False, "responsive": True},
                                ),
                            ],
                        ),

                        html.Div(
                            id="job_card",
                            className="cardx cardx-pad cardx-active",  # активная карточка (и будет оставаться активной)
                            style={"marginTop": "12px"},
                            children=[
                                html.Div(id="job_title", className="h-title", style={"fontSize": "20px"}),
                                html.Div(id="job_period", className="muted"),
                                dbc.Row(
                                    [
                                        dbc.Col([
                                            html.Div("Обязанности", className="section-title"),
                                            html.Div(id="job_tasks", className="scrollbox"),
                                        ], width=7),
                                        dbc.Col([
                                            html.Div("Достижения", className="section-title"),
                                            html.Div(id="job_wins", className="scrollbox"),
                                        ], width=5),
                                    ],
                                    className="g-3",
                                ),
                                html.Div(id="job_stack", className="muted", style={"marginTop": "10px"}),
                            ],
                        ),

                        html.Div(
                            className="cardx cardx-dark cardx-pad",
                            style={"marginTop": "12px"},
                            children=[
                                html.Div("Скиллы", className="h-title", style={"fontSize": "20px"}),
                                html.Div(id="skills_container"),
                            ],
                        ),
                    ],
                ),
            ],
            className="g-3",
        ),
        dcc.Store(id="selected_job", data=EXPERIENCE[0]["id"]),
        dcc.Store(id="prev_skills", data={}),

    ],
)

# -------- Callbacks --------
@app.callback(
    Output("selected_job", "data"),
    Input("timeline", "clickData"),
    prevent_initial_call=True,
)
def on_click_timeline(clickData):
    if not clickData:
        return EXPERIENCE[0]["id"]
    pn = clickData["points"][0].get("pointNumber")
    if pn is None:
        return EXPERIENCE[0]["id"]
    pn = int(pn)
    if 0 <= pn < len(EXPERIENCE):
        return EXPERIENCE[pn]["id"]
    return EXPERIENCE[0]["id"]



@app.callback(
    Output("timeline", "figure"),
    Output("job_title", "children"),
    Output("job_period", "children"),
    Output("job_tasks", "children"),
    Output("job_wins", "children"),
    Output("job_stack", "children"),
    Output("skills_container", "children"),
    Output("prev_skills", "data"),          # ← добавили
    Input("selected_job", "data"),
    State("prev_skills", "data"),           # ← добавили
)
def render_job(job_id, prev_skills):
    job = next((e for e in EXPERIENCE if e["id"] == job_id), EXPERIENCE[0])

    fig = timeline_fig(job_id)
    title = f"{job['company']} — {job['role']}"
    period = job["period"]
    tasks = ul(job["tasks"])
    wins = ul(job["wins"])
    stack = "Стек: " + " · ".join(job["stack"])

    current_skills = job.get("skills", {}) or {}
    prev_skills = prev_skills or {}

    skills_ui = skills_block(current_skills, prev_skills)

    # сохраняем текущие как "предыдущие" для следующего переключения
    return fig, title, period, tasks, wins, stack, skills_ui, current_skills

if __name__ == "__main__":
    app.run(debug=True)
