import os
import streamlit as st
from openai import OpenAI


def build_prompt(company_name: str, future_year: int, details: str) -> str:
    """Return an example prompt for the OpenAI model."""
    return (
        f"Write a press release from the year {future_year} about {company_name}. "
        f"Include the following details if relevant: {details}."
    )


def read_log_file(path: str = "app.log", max_lines: int = 200) -> str:
    """Return the last ``max_lines`` lines from the log file."""
    if not os.path.exists(path):
        return "Log file does not exist."
    with open(path, "r") as fh:
        lines = fh.readlines()
    return "".join(lines[-max_lines:])


def main() -> None:
    """Minimal placeholder Streamlit app."""
    api_key = st.secrets.get("openai", {}).get("api_key") or os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key) if api_key else None

    st.title("Placeholder App")
    st.write("Configure OpenAI API key via `.streamlit/secrets.toml`:")
    st.code('[openai]\napi_key = "YOUR_API_KEY"', language="toml")
    st.write("OpenAI client configured:", bool(client))


if __name__ == "__main__":  # pragma: no cover - entry point
    main()
