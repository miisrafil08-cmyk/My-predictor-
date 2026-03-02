import streamlit as st
from collections import Counter

# ফাংশন: সংখ্যা থেকে প্রপার্টি বের করা
def get_properties(num):
    size = "Big" if num >= 5 else "Small"
    if num in [1, 3, 7, 9]:
        color = "🟢 Green"
    elif num in [2, 4, 6, 8]:
        color = "🔴 Red"
    else: # 0 and 5
        color = "🟣 Violet/Mix"
    return size, color

st.set_page_config(page_title="HGNICE Pattern Analyzer", layout="wide")
st.title("📊 Advanced Pattern & Color Analyzer")

# ডাটা ইনপুট
raw_data = st.text_area("অতীতের ফলাফলগুলো দিন (Space বা Comma দিয়ে আলাদা করে)", 
                        placeholder="উদাহরণ: 7 2 7 1 5 2 7 4 7 1", height=150)

target_num = st.number_input("আপনি কোন সংখ্যার পরের প্যাটার্ন দেখতে চান?", min_value=0, max_value=9, step=1)

if st.button("Analyze Deep Pattern"):
    if raw_data:
        # ডাটা প্রসেসিং
        data_list = [int(x) for x in raw_data.replace(',', ' ').split() if x.isdigit()]
        
        next_nums = []
        for i in range(len(data_list) - 1):
            if data_list[i] == target_num:
                next_nums.append(data_list[i+1])
        
        if next_nums:
            # পরিসংখ্যান তৈরি
            num_counts = Counter(next_nums)
            sizes = [get_properties(n)[0] for n in next_nums]
            colors = [get_properties(n)[1] for n in next_nums]
            
            size_counts = Counter(sizes)
            color_counts = Counter(colors)

            # রেজাল্ট দেখানো
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("🔢 Next Numbers")
                for n, f in num_counts.most_common():
                    st.write(f"সংখ্যা {n}: {f} বার")

            with col2:
                st.subheader("📏 Big/Small Status")
                for s, f in size_counts.most_common():
                    st.write(f"{s}: {f} বার")
            
            with col3:
                st.subheader("🎨 Color Status")
                for c, f in color_counts.most_common():
                    st.write(f"{c}: {f} বার")

            # প্রেডিকশন
            st.divider()
            best_num = num_counts.most_common(1)[0][0]
            p_size, p_color = get_properties(best_num)
            st.success(f"### পরবর্তী সম্ভাব্য ফলাফল: সংখ্যা {best_num} ({p_size} & {p_color})")
        else:
            st.warning("এই সংখ্যার কোনো হিস্টোরি পাওয়া যায়নি।")
    else:
        st.error("দয়া করে ডাটা ইনপুট দিন।")
