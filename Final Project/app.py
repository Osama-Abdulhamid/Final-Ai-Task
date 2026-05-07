import streamlit as st
import time

# استدعاء الخوارزميات المنظمة من الملفات التانية
from backtracking_solver import solve_backtracking
from genetic_solver import solve_genetic

st.set_page_config(page_title="Bin Packing Solver", page_icon="📦", layout="wide")

st.title("📦 Bin Packing Problem Solver")
st.markdown("---")

# إعدادات الواجهة الجانبية (Sidebar)
st.sidebar.header("⚙️ إعدادات المشكلة")

bin_capacity = st.sidebar.number_input("سعة الصندوق (Bin Capacity):", min_value=1, value=8, step=1)

items_input = st.sidebar.text_area("أحجام العناصر (مفصولين بفاصلة):", "1, 2, 3, 4, 1, 2, 4, 3, 5, 3, 4, 4, 5, 1, 5, 4, 4, 6, 2, 7, 4")
items = [int(x.strip()) for x in items_input.split(",") if x.strip().isdigit()]

algorithm = st.sidebar.radio("اختر الخوارزمية:", ("Backtracking Search", "Genetic Algorithm"))

st.sidebar.markdown("---")
solve_button = st.sidebar.button("🚀 تشغيل الخوارزمية (Solve)", use_container_width=True)

if solve_button:
    if not items:
        st.error("⚠️ يرجى إدخال أحجام العناصر بشكل صحيح.")
    else:
        with st.spinner(f'جاري الحل باستخدام {algorithm}...'):
            # تشغيل الخوارزمية المطلوبة
            if algorithm == "Backtracking Search":
                best_bins, exec_time = solve_backtracking(items, bin_capacity)
            elif algorithm == "Genetic Algorithm":
                best_bins, exec_time = solve_genetic(items, bin_capacity)
            
            st.success(f"تم الحل بنجاح باستخدام {algorithm}!")
            
            # عرض الأرقام والنتائج
            col1, col2 = st.columns(2)
            col1.metric("⏱️ وقت التنفيذ", f"{exec_time:.4f} ثانية")
            col2.metric("📦 عدد الصناديق المستخدمة", f"{len(best_bins)} صندوق")
            
            st.markdown("### 📊 تفاصيل التوزيعة (Bin Configurations)")
            
            # رسم الصناديق بشكل جمالي في الواجهة
            for i, b in enumerate(best_bins):
                st.write(f"**صندوق {i+1}** (الإجمالي: {sum(b)} من أصل {bin_capacity})")
                
                # عمل Progress Bar يوضح نسبة امتلاء كل صندوق
                fill_percentage = min(sum(b) / bin_capacity, 1.0)
                st.progress(fill_percentage)
                st.write(f"العناصر: `{b}`")
                st.markdown("---")