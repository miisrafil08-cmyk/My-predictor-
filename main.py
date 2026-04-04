import streamlit as st
import cv2
import numpy as np
import easyocr
from collections import Counter

# OCR Setup
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

st.set_page_config(page_title="Result Analyzer", layout="wide")
st.title("📊 Game History Analyzer & Predictor")

uploaded_files = st.file_uploader("আপনার গেম হিস্ট্রির স্ক্রিনশটগুলো এখানে আপলোড করুন (২০-৩০টি)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

def get_color(num):
    if num in [1, 3, 7, 9]: return "Green 🟢"
    elif num in [2, 4, 6, 8]: return "Red 🔴"
    elif num == 0: return "Red-Violet 🔴🟣"
    elif num == 5: return "Green-Violet 🟢🟣"
    return "Unknown"

def get_size(num):
    return "Small" if num <= 4 else "Big"

all_numbers = []

if uploaded_files:
    with st.spinner('স্ক্রিনশট থেকে ডাটা সংগ্রহ করা হচ্ছে... ধৈর্য ধরুন।'):
        for file in uploaded_files:
            file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, 1)
            results = reader.readtext(img)
            for (_, text, _) in results:
                if text.isdigit() and len(text) == 1:
                    all_numbers.append(int(text))
    
    st.success(f"সফলভাবে {len(all_numbers)} টি ডাটা পাওয়া গেছে!")
    
    target_num = st.number_input("বর্তমানে আসা শেষ সংখ্যাটি লিখুন (০-৯):", min_value=0, max_value=9, step=1)
    
    if st.button("প্রেডিকশন দেখুন"):
        next_results = []
        for i in range(len(all_numbers) - 1):
            if all_numbers[i] == target_num:
                next_results.append(all_numbers[i+1])
        
        if next_results:
            most_common_num = Counter(next_results).most_common(1)[0][0]
            st.markdown("---")
            st.subheader(f"পরবর্তী সম্ভাব্য ফলাফল:")
            c1, c2, c3 = st.columns(3)
            with c1: st.metric("সংখ্যা", most_common_num)
            with c2: st.metric("কালার", get_color(most_common_num))
            with c3: st.metric("সাইজ", get_size(most_common_num))
        else:
            st.error("দুঃখিত, এই সংখ্যার পরের কোনো ইতিহাস ডাটাতে পাওয়া যায়নি। আরও স্ক্রিনশট দিন।")
