from pypdf import PdfReader

def extract():
    try:
        reader = PdfReader('bao-cao-cuoi-ky-mi3310-he-thong-quan-ly-diem-danh-lop-hoc (2).pdf')
        with open('pdf_output.txt', 'w', encoding='utf-8') as f:
            f.write(f"Total pages: {len(reader.pages)}\n")
            # In 6 trang dau tien de lay Muc luc
            for i in range(min(6, len(reader.pages))):
                f.write(f"\n--- Page {i+1} ---\n")
                f.write(reader.pages[i].extract_text() + "\n")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    extract()
