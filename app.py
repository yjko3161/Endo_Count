import pandas as pd
import streamlit as st

st.set_page_config(page_title="내시경 앰플 계산기", layout="wide")

DEFAULT_PROCEDURES = ["M1", "M12", "FM1", "FM2", "M30"]
NUMERIC_COLUMNS = [
    "위 수면",
    "위 비수면",
    "위 공단",
    "대장 수면",
    "대장 비수면",
    "대장 공단",
    "Sig",
    "ERCP",
    "E-ESD",
    "C-ESD",
    "PEG",
]
SLEEP_RELATED = ["위 수면", "대장 수면", "Sig", "ERCP", "E-ESD", "C-ESD"]


def initialize_state():
    if "table" not in st.session_state:
        base = pd.DataFrame(
            [[proc, *([0] * len(NUMERIC_COLUMNS))] for proc in DEFAULT_PROCEDURES],
            columns=["시행과", *NUMERIC_COLUMNS],
        )
        st.session_state.table = add_sleep_totals(base)


def add_sleep_totals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["수면 총앰플"] = df[SLEEP_RELATED].sum(axis=1)
    return df


def add_new_procedure():
    new_proc = st.session_state.get("new_procedure", "").strip()
    if not new_proc:
        st.warning("추가할 시행과 이름을 입력하세요.")
        return

    if new_proc in st.session_state.table["시행과"].values:
        st.info(f"이미 존재하는 시행과입니다: {new_proc}")
        return

    new_row = pd.DataFrame([[new_proc, *([0] * len(NUMERIC_COLUMNS))]], columns=["시행과", *NUMERIC_COLUMNS])
    st.session_state.table = pd.concat([st.session_state.table, new_row], ignore_index=True)
    st.session_state.table = add_sleep_totals(st.session_state.table)
    st.session_state.new_procedure = ""


def reset_values():
    st.session_state.table.loc[:, NUMERIC_COLUMNS] = 0
    st.session_state.table = add_sleep_totals(st.session_state.table)


def format_markdown_table(df: pd.DataFrame) -> str:
    headers = [
        "시행과",
        "위 수면",
        "위 비수면",
        "위 공단",
        "대장 수면",
        "대장 비수면",
        "대장 공단",
        "Sig",
        "ERCP",
        "E-ESD",
        "C-ESD",
        "PEG",
        "수면 총앰플",
    ]
    align_row = "|:---:|" + "---:|" * (len(headers) - 1)

    lines = ["| " + " | ".join(headers) + " |", align_row]
    for _, row in df.iterrows():
        values = [row["시행과"], *[int(row[col]) for col in headers[1:]]]
        lines.append("| " + " | ".join(map(str, values)) + " |")

    return "\n".join(lines)


def build_column_config():
    config = {
        "시행과": st.column_config.Column(
            "시행과", help="시행과 이름", width="small", disabled=True
        ),
        "수면 총앰플": st.column_config.Column("수면 총앰플", disabled=True, width="small"),
    }

    number_config = st.column_config.NumberColumn(
        step=1,
        min_value=0,
        format="%d",
        help="모든 값은 0 이상의 정수로 입력",
    )

    for col in NUMERIC_COLUMNS:
        config[col] = number_config

    return config


def render_editor():
    st.subheader("시행과별 집계 입력")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.text_input(
            "새 시행과 추가",
            key="new_procedure",
            placeholder="예: FM3",
            help="추가 후 표에 행이 자동 생성됩니다.",
        )
    with col2:
        st.button("시행과 추가", on_click=add_new_procedure, use_container_width=True)

    st.button("모든 값 초기화", on_click=reset_values, type="secondary", use_container_width=True)

    column_config = build_column_config()
    edited = st.data_editor(
        st.session_state.table,
        column_config=column_config,
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
        key="editor",
    )

    numeric_only = edited.copy()
    for col in NUMERIC_COLUMNS:
        numeric_only[col] = pd.to_numeric(numeric_only[col], errors="coerce").fillna(0).astype(int)
    st.session_state.table = add_sleep_totals(numeric_only)

    total_row = {"시행과": "전체 합계(Total)"}
    for col in NUMERIC_COLUMNS + ["수면 총앰플"]:
        total_row[col] = int(st.session_state.table[col].sum())

    with st.expander("전체 합계 확인", expanded=True):
        total_df = pd.concat(
            [st.session_state.table, pd.DataFrame([total_row])], ignore_index=True
        )
        st.dataframe(total_df, hide_index=True, use_container_width=True)

    return total_df


def render_report(total_df: pd.DataFrame):
    st.subheader("보고서용 마크다운 생성")
    if st.button("마크다운 표 생성", use_container_width=True):
        md = format_markdown_table(total_df)
        st.markdown("### 복사해서 사용하세요")
        st.code(md, language="markdown")


def main():
    st.title("내시경 집계 & 앰플 계산기")
    st.caption("엑셀처럼 빠르게 입력하고, 실수 없는 합계를 자동으로 생성합니다.")
    initialize_state()
    total_df = render_editor()
    render_report(total_df)


if __name__ == "__main__":
    main()
