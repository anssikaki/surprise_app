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


def build_prompt(product: str, feedback: str) -> str:
    """Create a prompt asking for an action plan.

    The wording is intentionally fixed so tests can easily verify it.
    """
    return (
        f"Generate a fun action plan to address this feedback for {product}: {feedback}. "
        "Respond in short bullet points and keep it cool and intuitive!"
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


def generate_action_plan(product: str, feedback: str) -> str:
    """Ask OpenAI to suggest an action plan based on feedback."""
    if not client:
        return "OpenAI API key not found."

    prompt = build_prompt(product, feedback)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


# Streamlit UI
st.title("Feedback Buddy")

product_name = st.text_area("Which product or service is this about?")
feedback_text = st.text_area("Share your feedback:")
if st.button("Get Action Plan"):
    if product_name.strip() and feedback_text.strip():
        logging.info("Received feedback: %s", feedback_text)
        with st.spinner("Thinking up improvements..."):
            result = generate_action_plan(product_name, feedback_text)
        st.markdown(result)
        logging.info("Plan generated")
    else:
        st.warning("Please enter the product name and your feedback.")
