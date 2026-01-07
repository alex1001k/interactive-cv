from __future__ import annotations

import re
from datetime import date, datetime
from pathlib import Path

from dash import Dash, html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
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

EDUCATION = {
    "short": "МИП • Организационное лидерство и управленческий консалтинг",
    "details": [
        "Факультет: Организационное лидерство и управленческий консалтинг",
        "НИР: «Психологические аспекты управления талантами в организации»",
        "Добавь курсы/сертификаты по желанию",
    ],
}

SKILL_HINTS = {
    "Python": "ETL/автоматизация, pandas, интеграции, Airflow, проверки качества данных, алгоритмы.",
    "SQL": "Оптимизация запросов/процедур, витрины, качество данных, MSSQL, проектирование метрик.",
    "Power BI": "DAX, модели, UX, drill-through, bookmarks, кастомные визуализации/HTML/SVG.",
    "Excel": "Power Query, модели, шаблоны, сводные, аналитические справки, автоматизация.",
}

# ВАЖНО: start_date -> пропорциональная шкала
EXPERIENCE = [
    {
        "id": "job3",
        "start_date": "2022-08-01",
        "company": "ПАО ТМК",
        "role": "Руководитель группы отчетности",
        "period": "Авг 2022 — Now",
        "start": "Авг 2022",
        "tasks": [
            "Построил систему управленческой отчётности закупок с нуля",
            "Наполнил данными из 4 разноструктурных ERP-систем базы MS SQL и SAP BW/4HANA (100M+ строк)",
            "Спроектировал и поддерживал ETL-процессы на Python с оркестрацией в Apache Airflow, сократив время обновления данных до 2 часов",
            "Создал более 30 отчетов в Power BI для 1 300 пользователей: дизайн сверстал в Figma, продумал пользовательский путь, для лучшего UX использовал кастомные визуализации HTML5, SVG-графики, закладки и drill-through детализации",
            "Создал Python-алгоритмы для автоматической проверки планов закупок (до 150 млн ₽ сокращения затрат в месяц)",
            "Оптимизировал сложные SQL-запросы и процедуры, повысив производительность на 70%",
            "Руководил командой из 3 аналитиков: планирование задач, code review SQL/Python, развитие компетенций",
        ],
        "stack": ["Python", "SQL", "MSSQL", "Power BI", "Airflow", "Figma"],
        "skills": {"Python": 9, "SQL": 8, "Power BI": 8, "Excel": 7},
        "x": 2022.8
    },
    {
        "id": "job2",
        "start_date": "2019-04-01",
        "company": "АО СУЭК",
        "role": "Главный специалист → Начальник отдела",
        "period": "Апр 2019 — Авг 2022",
        "start": "Апр 2019",
        "tasks": [
            "Формировал консолидированную отчетность на базе SAP ERP и Oracle, переносил Excel-отчеты на Power Query и Power BI",
            "Сократил время обновления отчетности с 5 дней до 1 часа, автоматизировав ручные операции в Python",
            "Контролировал KPI топ-менеджмента закупки: оборачиваемость запасов, сроки и объёмы поставок",
            "Руководил аналитической группой (3 специалиста): распределение задач, контроль сроков и качества",
        ],
        "stack": ["Excel", "SQL", "Power BI", "Python"],
        "skills": {"Excel": 10, "SQL": 5, "Python": 3, "Power BI": 3},
        "x": 2019.4
    },
    {
        "id": "job1",
        "start_date": "2016-12-01",  # исправлено
        "company": "Газпром нефть",
        "role": "Специалист",
        "period": "Дек 2016 — Апр 2019",
        "start": "Дек 2016",
        "tasks": [
            "Выполнил более 5 тыс. заявок на аккредитацию поставщиков в SRM-системе",
            "Формировал аналитические справки в Excel на базе выгрузок из SAP ERP (до 20 еженедельно)",
            "Проверил более 1,5 тыс. результатов конкурсных процедур на предмет обоснованности выбора поставщиков и предложений",
        ],
        "stack": ["Excel", "SAP ERP"],
        "skills": {"Excel": 4},
        "x": 2016.12
    },
]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "CV Dashboard"

DEFAULT_JOB = EXPERIENCE[0]["id"]


# ----------------------------
# Helpers
# ----------------------------
def parse_iso(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def to_float_year(d: date) -> float:
    start = date(d.year, 1, 1)
    end = date(d.year + 1, 1, 1)
    return d.year + (d - start).days / (end - start).days


def slug(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", s.strip()).strip("-").lower()


def find_qr_asset() -> str | None:
    for p in ["assets/qr.png", "assets/qr.jpg", "assets/qr.jpeg"]:
        if Path(p).exists():
            return "/assets/" + Path(p).name
    return None


def ul(items):
    return html.Ul([html.Li(x) for x in items])


def kpi_grid():
    items = []
    for k, v in PROFILE["numbers"]:
        items.append(html.Div([html.Div(k, className="k"), html.Div(v, className="v")], className="item"))
    return html.Div(items, className="kpi")


def profile_hero():
    bg_url = "url('/assets/avatar.jpg')"
    return html.Div(
        className="profile-hero cardx",
        children=[
            html.Div(className="profile-media", style={"backgroundImage": bg_url}),
            html.Div(
                className="profile-footer",
                children=[
                    html.Div(PROFILE["name"], className="profile-name"),
                    html.Div(PROFILE["title"], className="profile-role"),
                ],
            ),
        ],
    )


# ----------------------------
# Timeline  (НЕ ТРОГАЕМ)
# ----------------------------
def timeline_fig(selected_id: str):
    # --- SAFE extraction of x values ---
    try:
        xs = [e["x"] for e in EXPERIENCE]
    except KeyError:
        raise KeyError(
            "timeline_fig ожидает, что в EXPERIENCE у каждого элемента есть ключ 'x'. "
            "Добавь 'x' (число, например 2019.5) в каждый job."
        )

    ys = [0] * len(EXPERIENCE)
    y0 = 0.2         # базовая линия шкалы (было 0)
    y_bottom = -0.10   # нижние подписи (было -0.18)

    sel_idx = next((i for i, e in enumerate(EXPERIENCE) if e["id"] == selected_id), 0)

    # Extend to "Now"
    current_x = max(xs) + 0.9

    # Palette
    axis_color = "rgba(17,24,39,0.92)"
    yellow = "#FDE68A"
    yellow_strong = "#FBBF24"

    base_size = 10
    active_size = 16

    # Labels
    right_labels = [
        f"<b>{e['company']}</b><br><span style='font-size:11px'>{e['role']}</span>"
        for e in EXPERIENCE
    ]
    bottom_labels = [
        f"<span style='font-size:11px'>{e['start']}</span>"
        for e in EXPERIENCE
    ]

    hover_text = ["Нажмите для отображения обязанностей"] * len(EXPERIENCE)

    fig = go.Figure()

    # 1) Axis line
    fig.add_trace(
        go.Scatter(
            x=xs + [current_x],
            y=[y0] * len(xs) + [y0],
            mode="lines",
            line=dict(width=3, color=axis_color),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # 2) Clickable markers
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=[y0] * len(xs),
            mode="markers",
            marker=dict(
                size=[base_size] * len(xs),
                color=yellow,
                line=dict(width=2, color=yellow_strong),
                opacity=0.9,
            ),
            text=hover_text,
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        )
    )

    # 3) Active marker
    fig.add_trace(
        go.Scatter(
            x=[xs[sel_idx]],
            y=[y0],
            mode="markers",
            marker=dict(
                size=active_size,
                color=yellow,
                line=dict(width=4, color=yellow_strong),
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # 4) Glow ring
    fig.add_trace(
        go.Scatter(
            x=[xs[sel_idx]],
            y=[y0],
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

    # 5) Right-side labels (company + role)
    fig.add_trace(
        go.Scatter(
            x=[x + 0.08 for x in xs],   # ← сдвиг вправо от точки
            y=[y0] * len(xs),
            mode="text",
            text=right_labels,
            textposition="middle right",
            hoverinfo="skip",
            showlegend=False,
            cliponaxis=False,
        )
    )

    # 6) Bottom labels (start date)
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=[y_bottom] * len(xs),
            mode="text",
            text=bottom_labels,
            hoverinfo="skip",
            showlegend=False,
            cliponaxis=False,
        )
    )

    # 7) Now label
    fig.add_trace(
        go.Scatter(
            x=[current_x],
            y=[y_bottom],
            mode="text",
            text=["<span style='font-size:11px'><b>Now</b></span>"],
            hoverinfo="skip",
            showlegend=False,
            cliponaxis=False,
        )
    )

    fig.update_xaxes(
        visible=False,
        fixedrange=True,
    )

    fig.update_yaxes(
        visible=False,
        autorange=True,
        fixedrange=True,   # запрещаем zoom/pan
    )


    fig.update_layout(
        height=120,
        margin=dict(l=0, r=10, t=0, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        transition=dict(duration=380, easing="cubic-in-out"),
    )

    return fig



# ----------------------------
# Skills (no ghosts + tooltips)
# ----------------------------
def skills_block(job_id: str, skills_map: dict[str, int], prev_map: dict[str, int]):
    items = sorted(skills_map.items(), key=lambda kv: (-int(kv[1]), kv[0].lower()))
    rows = []
    tips = []

    for idx, (name, level) in enumerate(items):
        level = max(0, min(10, int(level)))
        prev_level = int(prev_map.get(name, 0)) if prev_map else 0
        grew = level > prev_level

        row_style = {"animationDelay": f"{idx * 90}ms"}
        row_class = "row grow" if grew else "row"

        segs = []
        for i in range(10):
            if i < level:
                if grew:
                    segs.append(html.Span(className="seg on", style={"animationDelay": f"{(idx*90) + (i*55)}ms"}))
                else:
                    segs.append(html.Span(className="seg on"))
            else:
                segs.append(html.Span(className="seg"))

        sid = slug(name)
        name_id = f"skill-name-{job_id}-{sid}"
        bar_id = f"skill-bar-{job_id}-{sid}"

        rows.append(
            html.Div(
                [
                    html.Div(name, className="name", id=name_id),
                    html.Div(segs, className="battery", id=bar_id),
                ],
                className=row_class,
                style=row_style,
            )
        )

        hint = SKILL_HINTS.get(name, "Добавь описание навыка в SKILL_HINTS.")
        tips.append(dbc.Tooltip(hint, target=name_id, placement="top", trigger="hover"))
        tips.append(dbc.Tooltip(hint, target=bar_id, placement="top", trigger="hover"))

    wrapper_key = f"skills-wrapper-{job_id}-" + "-".join([f"{slug(k)}{v}" for k, v in items])
    return html.Div([html.Div(rows, className="skills")] + tips, key=wrapper_key)


# ----------------------------
# Layout
# ----------------------------
qr_url = find_qr_asset()

timeline_card = html.Div(
    className="cardx cardx-pad timeline-card",
    children=[
        html.Div("Карьера", className="h-title", style={"fontSize": "24px"}),
        dcc.Graph(
            id="timeline",
            figure=timeline_fig(DEFAULT_JOB),
            className="dash-graph",
            animate=True,
            config={"displayModeBar": False, "responsive": True},
            style={"height": "120px"},
        ),
    ],
)

job_card = html.Div(
    id="job_card",
    className="cardx cardx-pad cardx-active job-card",
    children=[
        html.Div(id="job_title", className="h-title", style={"fontSize": "20px"}),
        html.Div(id="job_period", className="muted"),
        html.Div("Обязанности", className="section-title"),
        html.Div(id="job_tasks", className="scrollbox"),
        html.Div(id="job_stack", className="muted"),
    ],
)

edu_card = html.Div(
    className="cardx cardx-pad edu-card",
    children=[
        html.Div("Образование", className="h-title", style={"fontSize": "20px"}),
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    title=EDUCATION["short"],
                    children=html.Ul([html.Li(x) for x in EDUCATION["details"]]),
                )
            ],
            start_collapsed=True,
            flush=True,
            always_open=False,
        ),
    ],
)

skills_card = html.Div(
    className="cardx cardx-dark cardx-pad skills-card grow-last",
    children=[
        html.Div("Скиллы", className="h-title", style={"fontSize": "20px"}),
        html.Div(id="skills_container"),
    ],
)

about_card = html.Div(
    className="cardx cardx-pad about-eq",
    children=[
        html.Div("Обо мне", className="section-title"),
        kpi_grid(),
        html.Div(PROFILE["about"], className="about-text"),
    ],
)

contacts_card = html.Div(
    className="cardx cardx-pad contacts-card grow-last",
    children=[
        html.Div("Контакты", className="section-title"),
        html.Div(
            className="contacts-grid",
            children=[
                html.Div(
                    [
                        html.Div(PROFILE["email"], className="muted"),
                        html.Div(PROFILE["telegram"], className="muted"),
                        html.Div(PROFILE["linkedin"], className="muted"),
                    ]
                ),
                html.Img(src=qr_url, className="qr") if qr_url else html.Div("Добавь assets/qr.png", className="muted"),
            ],
        ),
    ],
)

app.layout = html.Div(
    className="page-wrap",
    children=[
        dbc.Row(
            [
                dbc.Col(
                    width=4,
                    children=html.Div(
                        className="col-flex",
                        children=[
                            profile_hero(),
                            about_card,
                            contacts_card,
                        ],
                    ),
                ),
                dbc.Col(
                    width=12, lg=8,
                    children=html.Div(
                        className="right-grid",
                        children=[
                            timeline_card,
                            job_card,
                            edu_card,
                            skills_card,
                        ],
                    ),
                ),
            ],
            className="g-0",
            style={"--bs-gutter-x": "12px", "--bs-gutter-y": "12px"},
        ),
        dcc.Store(id="selected_job", data=DEFAULT_JOB),
        dcc.Store(id="prev_skills", data={}),
    ],
)

# ----------------------------
# Callbacks
# ----------------------------
@app.callback(
    Output("selected_job", "data"),
    Input("timeline", "clickData"),
    prevent_initial_call=True,
)
def on_click_timeline(clickData):
    # аккуратно: если клик вне точки — просто ничего не меняем
    if not clickData or not clickData.get("points"):
        raise PreventUpdate

    pn = clickData["points"][0].get("pointNumber")
    if pn is None:
        raise PreventUpdate

    pn = int(pn)
    if 0 <= pn < len(EXPERIENCE):
        return EXPERIENCE[pn]["id"]

    raise PreventUpdate



@app.callback(
    Output("timeline", "figure"),
    Output("job_title", "children"),
    Output("job_period", "children"),
    Output("job_tasks", "children"),
    Output("job_stack", "children"),
    Output("skills_container", "children"),
    Output("prev_skills", "data"),
    Input("selected_job", "data"),
    State("prev_skills", "data"),
)
def render_job(job_id, prev_skills):
    job = next((e for e in EXPERIENCE if e["id"] == job_id), EXPERIENCE[0])

    fig = timeline_fig(job_id)
    title = f"{job['company']} — {job['role']}"
    period = job["period"]
    tasks = ul(job["tasks"])
    stack = "Стек: " + " · ".join(job["stack"])

    current_skills = job.get("skills", {}) or {}
    prev_skills = prev_skills or {}

    skills_ui = skills_block(job_id, current_skills, prev_skills) if current_skills else html.Div("—", className="muted")

    return fig, title, period, tasks, stack, skills_ui, current_skills


if __name__ == "__main__":
    app.run(debug=True)
