import fitz
import os

def extract_text_and_images(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    text = ""
    images = []

    os.makedirs(output_folder, exist_ok=True)

    for page_num, page in enumerate(doc):
        text += f"\n--- PAGE {page_num} ---\n"
        text += page.get_text()

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            image_path = f"{output_folder}/page{page_num}_img{img_index}.png"
            with open(image_path, "wb") as f:
                f.write(image_bytes)

            images.append(image_path)
            text += f"\n[IMAGE_REF: {image_path}]\n"

    return text, images