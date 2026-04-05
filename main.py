import streamlit as st
import numpy as np
import easyocr
from collections import Counter
from PIL import Image

# ১. OCR মডেল লোড করা (একবারই হবে)
@st.cache_resource
def load_ocr_model():
    return easyocr.Reader(['en'])

reader = load_ocr_model()

st.set_page_config(page_title="Fast Predictor", layout="wide")
st.title("⚡ Game History Predictor")

# ২. মেমোরি বা সেশন স্টেট সেটআপ
if 'data_list' not in st.session_state:
    st.session_state.data_list = []

# ৩. ফাইল আপলোডার অংশ
uploaded_files = st.file_uploader("২০-৩০টি স্ক্রিনশট আপলোড করুন", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if uploaded_files:
    if st.button("Extract Data (একবার ক্লিক করুন)"):
        temp_list = []
        with st.spinner('ছবি থেকে সংখ্যা পড়া হচ্ছে...'):
            for f in uploaded_files:
                img = Image.open(f)
                img_arr = np.array(img)
                results = reader.readtext(img_arr)
                for (_, text, _) in results:
                    if text.isdigit() and len(text) == 1:
                        temp_list.append(int(text))
        
        st.session_state.data_list = temp_list
        st.success(f"সফলভাবে {len(temp_list)} টি সংখ্যা পাওয়া গেছে!")

st.markdown("---")

# ৪. ইনপুট এবং প্রেডিকশন অংশ (এটি সব সময় দেখা যাবে)
st.subheader("প্রেডিকশন চেক করুন")
target = st.number_input("বর্তমানে আসা শেষ সংখ্যাটি লিখুন (0-9):", min_value=0, max_value=9, step=1, value=0)

if st.session_state.data_list:
    # হিস্ট্রি থেকে পরের সংখ্যাগুলো খুঁজে বের করা
    all_data = st.session_state.data_list
    predictions = [all_data[i+1] for i in range(len(all_data)-1) if all_data[i] == target]
    
    if predictions:
        most_common = Counter(predictions).most_common(1)[0][0]
        
        # ফলাফল দেখানো
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("সম্ভাব্য সংখ্যা", most_common)
        with c2:
            color = "Green 🟢" if most_common in [1,3,7,9] else "Red 🔴" if most_common in [2,4,6,8] else "Violet 🟣"
            st.metric("কালার", color)
        with c3:
            size = "Small" if most_common <= 4 else "Big"
            st.metric("সাইজ", size)
    else:
        st.info("আপনার আপলোড করা হিস্ট্রিতে এই সংখ্যার পরে কোনো ডাটা নেই।")
else:
    st.warning("আগে স্ক্রিনশট আপলোড করে 'Extract Data' বাটনে ক্লিক করুন।")

# ডাটা ক্লিয়ার করার অপশন
if st.sidebar.button("Clear All Data"):
    st.session_state.data_list = []
    st.rerun()
