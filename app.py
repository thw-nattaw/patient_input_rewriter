import streamlit as st
import requests

# -------- SETTINGS -------- #
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.3"

# -------- PROMPT TEMPLATES -------- #
PROMPT_TEMPLATES = {
    "Formal HPI": """You are a clinical documentation assistant trained to convert patient language into formal, physician-style notes.

Your goal is to rewrite the following raw patient statement into a clear, medically accurate HPI paragraph suitable for a physician's note.

Use complete sentences. Maintain medical neutrality and avoid speculation. Use third-person voice (e.g., "The patient reports...").

---
PATIENT INPUT:
{input_text}

---
FORMAL HPI:
""",
    "Patient Summary": """You are a patient-friendly summarizer. Rewrite the patient's input into a clear, first-person summary that could be used in a patient portal or for sharing with a healthcare team.

Keep the tone natural, respectful, and easy to understand.

---
PATIENT INPUT:
{input_text}

---
PATIENT SUMMARY:
"""
}

# -------- APP LAYOUT -------- #
st.set_page_config(page_title="Medical Note Rewriter", layout="wide")
st.title("📝 Medical Note Rewriter (Ollama)")
st.write("Transform raw patient input into structured clinical notes using your local LLM.")

# Initialize session state
if "output" not in st.session_state:
    st.session_state.output = ""
if "output1" not in st.session_state:
    st.session_state.output1 = ""
if "output2" not in st.session_state:
    st.session_state.output2 = ""
if "mode" not in st.session_state:
    st.session_state.mode = ""
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Comparison mode toggle
comparison_mode = st.toggle("🔍 Enable Comparison Mode")

if comparison_mode:
    st.markdown("Comparing: **Formal HPI** vs **Patient Summary**")
else:
    note_type = st.selectbox("Choose note format:", list(PROMPT_TEMPLATES.keys()), key="style")

# User input
user_input = st.text_area("Paste patient input:", height=150)
st.session_state.user_input = user_input  # store input for later reuse

# -------- LLM CALL -------- #
def generate_ollama_output(prompt_text):
    payload = {"model": MODEL_NAME, "prompt": prompt_text, "stream": False}
    response = requests.post(OLLAMA_ENDPOINT, json=payload)
    return response.json().get("response", "[No output received]")

# -------- REWRITE BUTTON -------- #
if st.button("Rewrite"):
    if not user_input.strip():
        st.warning("Please enter some patient text.")
    elif len(user_input.strip().split()) < 15:
        st.warning("The input is quite short. For better results, please enter at least 15 words.")
    else:
        if comparison_mode:
            st.session_state.mode = "comparison"
            prompt1 = PROMPT_TEMPLATES["Formal HPI"].format(input_text=user_input)
            prompt2 = PROMPT_TEMPLATES["Patient Summary"].format(input_text=user_input)
            st.session_state.output1 = generate_ollama_output(prompt1)
            st.session_state.output2 = generate_ollama_output(prompt2)
        else:
            st.session_state.mode = "single"
            prompt = PROMPT_TEMPLATES[note_type].format(input_text=user_input)
            st.session_state.output = generate_ollama_output(prompt)

# -------- DISPLAY OUTPUT -------- #
if st.session_state.mode == "comparison" and st.session_state.output1 and st.session_state.output2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📄 Formal HPI")
        st.text_area("Formal HPI", st.session_state.output1, height=300, label_visibility="collapsed")
        st.download_button(
            "📁 Download Formal HPI",
            st.session_state.output1,
            file_name="formal_hpi.txt",
            mime="text/plain"
        )
    with col2:
        st.subheader("🧑‍⚕️ Patient Summary")
        st.text_area("Patient Summary", st.session_state.output2, height=300, label_visibility="collapsed")
        st.download_button(
            "📁 Download Patient Summary",
            st.session_state.output2,
            file_name="patient_summary.txt",
            mime="text/plain"
        )

    # Combined file
    combined = (
        f"Patient Input:\n{st.session_state.user_input}\n\n"
        f"Formal HPI:\n{st.session_state.output1}\n\n"
        f"Patient Summary:\n{st.session_state.output2}\n"
    )
    st.download_button("📁 Download Combined Output", combined, file_name="rewritten_note.txt", mime="text/plain")

elif st.session_state.mode == "single" and st.session_state.output:
    st.subheader(f"📄 Rewritten: {note_type}")
    st.text_area(f"{note_type} Output", st.session_state.output, height=300, label_visibility="collapsed")
    st.download_button(
        f"📁 Download {note_type}",
        st.session_state.output,
        file_name=f"{note_type.lower().replace(' ', '_')}.txt",
        mime="text/plain"
    )

    # Combined file
    combined = (
        f"Patient Input:\n{st.session_state.user_input}\n\n"
        f"{note_type}:\n{st.session_state.output}\n"
    )
    st.download_button("📁 Download Combined Output", combined, file_name="rewritten_note.txt", mime="text/plain")
