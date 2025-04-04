import pdfplumber
from PIL import Image
import pytesseract

# Ensure Tesseract is correctly set up
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# File paths
input_pdf_path = r"C:\Users\yashe\OneDrive\Desktop\DraCor\Dharmveer-Bharati-Andhayug.pdf"
output_txt_path = r"C:\Users\yashe\OneDrive\Desktop\DraCor\output.txt"

def extract_text_from_pdf(pdf_path, output_txt_path):
    text = ""
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            print(f"Processing page {i+1}/{len(pdf.pages)}...")

            try:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
                else:
                    # Convert page to image
                    img = page.to_image(resolution=300).original
                    img = img.convert("L")  # Convert to grayscale
                    img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)  # Upscale

                    # Save image for debugging (optional)
                    debug_image_path = f"C:\\Users\\yashe\\OneDrive\\Desktop\\DraCor\\debug_page_{i+1}.png"
                    img.save(debug_image_path)
                    print(f"Saved debug image: {debug_image_path}")

                    # OCR with better settings
                    extracted_text = pytesseract.image_to_string(img, lang="hin+eng", config="--psm 6")
                    text += extracted_text + "\n"
            
            except Exception as e:
                print(f"⚠️ Error processing page {i+1}: {e}")

    # Save extracted text as UTF-8
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"✅ Hindi text extraction complete! Output saved at: {output_txt_path}")

# Run the function
extract_text_from_pdf(input_pdf_path, output_txt_path)
