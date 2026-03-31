import streamlit as st
import re
import os
import json
from pdf_parser import extract_text_and_images
from llm_extractor import extract_structured_data
from report_generator import generate_report

st.title("AI DDR Generator")

inspection = st.file_uploader("Upload Inspection PDF")
thermal = st.file_uploader("Upload Thermal PDF")

if inspection and thermal:
    with open("inspection.pdf", "wb") as f:
        f.write(inspection.read())

    with open("thermal.pdf", "wb") as f:
        f.write(thermal.read())

    st.write("Processing...")

    try:
        text1, images1 = extract_text_and_images("inspection.pdf", "img1")
        text2, images2 = extract_text_and_images("thermal.pdf", "img2")

        merged_json = extract_structured_data(text1, text2)

        # Check if data extraction failed due to quota or other API errors
        if not merged_json or "Error" in merged_json:
            st.error("❌ **Data Extraction Failed**\n\nThe LLM failed to extract data. Check the terminal for API errors.")
            st.stop()
        
        # Prepare image metadata
        image_metadata = "Image Extracted Paths:\n"
        image_metadata += "\n".join([f"Inspection: {img}" for img in images1]) + "\n"
        image_metadata += "\n".join([f"Thermal: {img}" for img in images2]) + "\n"

        # Also provide the text context if images contain page mappings in the future,
        # but the prompt handles finding [IMAGE_REF: img1/pageX_imgY.png] directly
        # Wait, the prompt says "Image metadata extracted from reports (with page mapping)"
        # Note: images1 and images2 look like 'img1/page0_img0.png'
        # So providing the paths implicitly provides page numbers.
        
        report = generate_report(json.dumps(merged_json, indent=2), image_metadata)
        
        # Check if report generation failed
        if report.startswith("Error:"):
            st.error(f"❌ **Report Generation Failed**\n\n{report}")
            st.stop()

        st.subheader("DDR Report")
        
        # Parse out [RENDER_IMAGE: path] and display images inline
        parts = re.split(r'\[RENDER_IMAGE:\s*(.*?)\]', report)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part.strip():
                    st.markdown(part)
            else:
                image_path = part.strip()
                if os.path.exists(image_path):
                    st.image(image_path)
                else:
                    st.warning(f"Image not found: {image_path}")
    except Exception as e:
        st.error(f"❌ **Error**: {str(e)}")