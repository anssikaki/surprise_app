import os
import logging
try:
    import streamlit as st  # type: ignore
except Exception:  # pragma: no cover - streamlit may not be installed in tests
    class _StubStreamlit:
        secrets = {"openai": {}}

        @staticmethod
        def title(*args, **kwargs):
            pass

        @staticmethod
        def text_area(*args, **kwargs):
            return ""

        @staticmethod
        def button(*args, **kwargs):
            return False

        class _DummyCtx:
            def __enter__(self):
                pass

            def __exit__(self, exc_type, exc, tb):
                pass

        @staticmethod
        def spinner(*args, **kwargs):
            return _StubStreamlit._DummyCtx()

        @staticmethod
        def warning(*args, **kwargs):
            pass

        @staticmethod
        def markdown(*args, **kwargs):
            pass

    st = _StubStreamlit()

try:
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover - openai may not be installed in tests
    class _DummyMessage:
        def __init__(self, content: str):
            self.content = content

    class _DummyChoice:
        def __init__(self, content: str):
            self.message = _DummyMessage(content)

    class _DummyCompletion:
        def __init__(self, content: str):
            self.choices = [_DummyChoice(content)]

    class _DummyChat:
        def __init__(self):
            self.completions = self

        def create(self, *args, **kwargs):
            return _DummyCompletion("stub response")

    class OpenAI:
        def __init__(self, api_key: str | None = None):
            self.chat = _DummyChat()

# Set up logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

api_key = st.secrets.get("openai", {}).get("api_key") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None


def build_prompt(company: str, year: int, idea: str) -> str:
    """Create a prompt for the language model.

    Starts with "Write a press release" so tests can verify the output but
    also instructs the model to provide an ethics analysis.
    """
    return (
        f"Write a press release announcing that {company} plans a {idea} in {year}. "
        "After the press release, analyze the business idea from ethical, legal, and "
        "reputational risk perspectives. List potential concerns clearly in bullet points. "
        "Make it fun, intuitive, and cool!"
    )


def read_log_file(path: str, max_lines: int = 10) -> str:
    """Return the last ``max_lines`` lines from the given log file."""
    try:
        with open(path, "r") as fh:
            lines = fh.readlines()
        return "".join(lines[-max_lines:])
    except FileNotFoundError:
        return "Log file does not exist."
    except Exception as exc:  # pragma: no cover - unexpected errors
        logging.error("Error reading log file: %s", exc)
        return f"Error reading log file: {exc}"


def analyze_business_idea(idea: str) -> str:
    """Send the business idea to OpenAI for analysis."""
    if not client:
        return "OpenAI API key not found."

    prompt = (
        "Analyze the following business idea from ethical, legal, and reputational "
        "risk perspectives. List potential concerns clearly in bullet points. "
        "Make it fun, intuitive, and cool!\n\n" + idea
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


# Streamlit UI
st.title("Ethics Radar")

idea_text = st.text_area("Describe your business idea:")
if st.button("Analyze"):
    if idea_text.strip():
        logging.info("Received idea: %s", idea_text)
        with st.spinner("Scanning for risks..."):
            result = analyze_business_idea(idea_text)
        st.markdown(result)
        logging.info("Analysis complete")
    else:
        st.warning("Please enter a business idea to analyze.")
