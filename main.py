import streamlit as st
import numpy as np
import easyocr
from collections import Counter
from PIL import Image

# ১. OCR মডেলটি একবারই লোড হবে (ক্যাশিং)
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()

st.set_page_config(page_title="Fast Predictor", layout="wide")
st.title("⚡ Ultra Fast Game Analyzer")

# ২. সেশন স্টেট (স্মৃতি) তৈরি করা
if 'extracted_numbers' not in st.session_state:
    st.session_state.extracted_numbers = []

# ফাইল আপলোডার
files = st.file_uploader("আপনার স্ক্রিনশটগুলো দিন", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

# ডাটা প্রসেস করার বাটন
if files and st.button("Extract Data from Screenshots"):
    all_nums = []
    with st.spinner('একবারই ডাটা রিড করা হচ্ছে... একটু অপেক্ষা করুন।'):
        for f in files:
            img = Image.open(f)
            img_arr = np.array(img)
            # OCR দিয়ে সংখ্যা খোঁজা
            results = reader.readtext(img_arr)
            for (_, text, _) in results:
                if text.isdigit() and len(text) == 1:
                    all_nums.append(int(text))
    
    # মেমোরিতে ডাটা সেভ করে রাখা
    st.session_state.extracted_numbers = all_nums
    st.success(f"সফলভাবে {len(all_nums)} টি সংখ্যা মেমোরিতে জমা করা হয়েছে!")

# ৩. মেমোরি থেকে ডাটা নিয়ে দ্রুত প্রেডিকশন
if st.session_state.extracted_numbers:
    st.markdown("---")
    st.write(f"বর্তমানে মেমোরিতে মোট ডাটা আছে: **{len(st.session_state.extracted_numbers)}** টি")
    
    target = st.number_input("আপনার দেখা শেষ সংখ্যাটি দিন (০-৯):", 0, 9, key="target_input")
    
    # এখানে কোনো বাটন ছাড়াই সরাসরি ফলাফল দেখাবে (Super Fast)
    res = [st.session_state.extracted_numbers[i+1] for i in range(len(st.session_state.extracted_numbers)-1) if st.session_state.extracted_numbers[i] == target]
    
    if res:
        top = Counter(res).most_common(1)[0][0]
        st.subheader(f"পরবর্তী সম্ভাব্য ফলাফল:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("সংখ্যা", top)
        with col2:
            color = "Green 🟢" if top in [1,3,7,9] else "Red 🔴" if top in [2,4,6,8] else "Violet 🟣"
            st.metric("কালার", color)
        with col3:
            size = "Small" if top <= 4 else "Big"
            st.metric("সাইজ", size)
    else:
        st.warning("এই সংখ্যার কোনো ইতিহাস ডাটাতে নেই।")

# মেমোরি ক্লিয়ার করার বাটন (যদি নতুন করে শুরু করতে চান)
if st.button("Clear Memory"):
    st.session_state.extracted_numbers = []
    st.rerun()
