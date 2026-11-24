
import streamlit as st
from PIL import Image
from utils.ocr_engine import load_ocr_model, extract_text

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="ScanGenius AI",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero {
    text-align: center;
    padding: 25px;
    border-radius: 15px;
    background: linear-gradient(135deg, #16213e, #0f3460);
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 42px;
}

.hero p {
    color: #d1d5db;
    font-size: 17px;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    font-weight: bold;
    height: 45px;
}

.result-box {
    background-color: #1c2333;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #344054;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HEADER
# -----------------------------------

st.markdown("""
<div class="hero">
    <h1>📝 ScanGenius AI</h1>
    <p>AI-Powered Handwritten Text Recognition</p>
    <p>Transform handwritten notes into digital text instantly.</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:
    st.title("⚙️ ScanGenius AI")

    st.markdown("---")

    st.subheader("About")

    st.write(
        "ScanGenius AI uses Microsoft's "
        "TrOCR handwritten recognition model "
        "to extract text from handwritten images."
    )

    st.markdown("---")

    st.subheader("Features")

    st.write("📤 Image Upload")
    st.write("🤖 AI Handwriting Recognition")
    st.write("✏️ Editable Text")
    st.write("📋 Copy Text")
    st.write("⬇️ Download Text")

    st.markdown("---")

    st.caption("Powered by Hugging Face TrOCR")

# -----------------------------------
# MODEL LOADING
# -----------------------------------

@st.cache_resource
def get_model():
    return load_ocr_model()


try:
    with st.spinner("🤖 Loading AI model... Please wait"):
        processor, model, device = get_model()

    st.success(f"AI Model Ready | Device: {device.upper()}")

except Exception as error:
    st.error(f"Unable to load AI model: {error}")
    st.stop()

# -----------------------------------
# IMAGE UPLOAD SECTION
# -----------------------------------

st.subheader("📤 Upload Your Handwriting")

uploaded_file = st.file_uploader(
    "Choose a handwritten image",
    type=["png", "jpg", "jpeg"],
    help="Upload a clear image of handwritten text."
)

# -----------------------------------
# IMAGE PREVIEW
# -----------------------------------

if uploaded_file is not None:

    try:
        image = Image.open(uploaded_file).convert("RGB")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🖼️ Uploaded Image")

            st.image(
                image,
                use_container_width=True
            )

            st.caption(
                f"Image Size: {image.width} × {image.height}"
            )

        with col2:
            st.subheader("🔍 Recognition")

            st.write(
                "Your handwritten image is ready "
                "for AI text recognition."
            )

            if st.button(
                "🚀 Extract Handwritten Text",
                use_container_width=True
            ):

                try:
                    with st.spinner(
                        "AI is recognizing handwriting..."
                    ):

                        result = extract_text(
                            image,
                            processor,
                            model,
                            device
                        )

                    st.session_state["extracted_text"] = result

                    st.success("Text extraction completed!")

                except Exception as error:
                    st.error(
                        f"Text extraction failed: {error}"
                    )

    except Exception as error:
        st.error(f"Invalid image file: {error}")

# -----------------------------------
# EXTRACTED TEXT SECTION
# -----------------------------------

if "extracted_text" in st.session_state:

    st.markdown("---")

    st.subheader("📄 Extracted Text")

    extracted_text = st.text_area(
        "Review and edit your extracted text:",
        value=st.session_state["extracted_text"],
        height=220,
        key="editable_text"
    )

    st.session_state["extracted_text"] = extracted_text

    # Statistics

    words = len(extracted_text.split())
    characters = len(extracted_text)

    col1, col2, col3 = st.columns(3)

    col1.metric("📝 Words", words)
    col2.metric("🔤 Characters", characters)
    col3.metric("📊 Status", "Completed")

    # Download

    st.download_button(
        label="⬇️ Download Extracted Text",
        data=extracted_text,
        file_name="scangenius_extracted_text.txt",
        mime="text/plain",
        use_container_width=True
    )

    # Copy

    st.code(extracted_text, language="text")

    st.caption(
        "Use the code block's copy icon to copy your extracted text."
    )

    # Clear

    if st.button("🗑️ Clear Results"):

        del st.session_state["extracted_text"]

        if "editable_text" in st.session_state:
            del st.session_state["editable_text"]

        st.rerun()

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.markdown(
    "<center>Built with ❤️ using Python, Streamlit "
    "and Hugging Face TrOCR</center>",
    unsafe_allow_html=True
)
