import streamlit as st
import cv2
import numpy as np
import easyocr
from collections import Counter

# OCR Reader Initialize
reader = easyocr.Reader(['en'])

st.title("Game History Analyzer")
st.write("আপনার স্ক্রিনশটগুলো এখানে আপলোড করুন")

uploaded_files = st.file_uploader("Upload Screenshots", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

def get_color(num):
    if num in [1, 3, 7, 9]: return "Green"
    elif num in [2, 4, 6, 8]: return "Red"
    elif num == 0: return "Red-Violet"
    elif num == 5: return "Green-Violet"
    return "Unknown"

def get_size(num):
    return "Small" if num <= 4 else "Big"

all_numbers = []

if uploaded_files:
    for file in uploaded_files:
        file_bytes = np.asarray(bytearray(file.read()), dtype=uint8)
        img = cv2.imdecode(file_bytes, 1)
        
        # OCR দিয়ে সংখ্যা বের করা (এখানে লজিকটি আপনার ইমেজ ফরম্যাট অনুযায়ী টিউন করতে হবে)
        results = reader.readtext(img)
        for (_, text, _) in results:
            if text.isdigit() and len(text) == 1:
                all_numbers.append(int(text))
    
    st.success(f"মোট {len(all_numbers)} টি সংখ্যা পাওয়া গেছে।")
    
    target_num = st.number_input("কোন সংখ্যার পরের ফলাফল দেখতে চান?", min_value=0, max_value=9, step=1)
    
    if st.button("Analyze"):
        next_results = []
        for i in range(len(all_numbers) - 1):
            if all_numbers[i] == target_num:
                next_results.append(all_numbers[i+1])
        
        if next_results:
            most_common_num = Counter(next_results).most_common(1)[0][0]
            
            st.subheader(f"সংখ্যা {target_num} এর পরের প্রেডিকশন:")
            st.write(f"**বেশি আসা সংখ্যা:** {most_common_num}")
            st.write(f"**কালার:** {get_color(most_common_num)}")
            st.write(f"**সাইজ:** {get_size(most_common_num)}")
        else:
            st.warning("এই সংখ্যাটির পরের কোনো ডাটা খুঁজে পাওয়া যায়নি।")
