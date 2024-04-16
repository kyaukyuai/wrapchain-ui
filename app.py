import os
import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from wrapchain import WrapChain

load_dotenv()

st.set_page_config(page_title="日本語 AI OCR", layout="centered")


def upload_image():
    uploaded_file = st.file_uploader(
        "画像をアップロードして下さい...", type=["jpg", "jpeg", "png"]
    )
    if uploaded_file is not None:
        return uploaded_file
    return None


def main():
    os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
    st.title("日本語 AI OCR")
    image_file = upload_image()
    if image_file:
        image_width = 300
        st.image(image_file, caption="アップロードした画像", width=image_width)

        prompt_text = """
        アップロードされる画像の日本語を読み取って下さい.わからないまたは不明な場合は正直にその旨を返答して下さい.
        """
        wc = WrapChain()
        image_bytes = image_file.read()

        with st.spinner("Processing..."):
            result = wc.document(
                image_file=image_bytes,
                prompt=prompt_text,
            )

        st.markdown(result.content)


if __name__ == "__main__":
    main()
