import streamlit as st
import time
import pandas as pd # هنستخدمها عشان نرسم رسومات المقارنة جوة الواجهة

# استدعاء الخوارزميات من الملفات التانية
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

# ضفنا خيار المقارنة هنا
algorithm = st.sidebar.radio("اختر وضع التشغيل:", ("Backtracking Search", "Genetic Algorithm", "مقارنة بين الاثنين (Compare Both)"))

st.sidebar.markdown("---")
solve_button = st.sidebar.button("🚀 تشغيل (Solve)", use_container_width=True)

# دالة مساعدة (Helper Function) عشان منكررش كود رسم الصناديق
def display_bins(bins, capacity):
    for i, b in enumerate(bins):
        st.write(f"**صندوق {i+1}** (الإجمالي: {sum(b)}/{capacity})")
        fill_percentage = min(sum(b) / capacity, 1.0)
        st.progress(fill_percentage)
        st.write(f"`{b}`")

# تشغيل المنطق الأساسي للواجهة
if solve_button:
    if not items:
        st.error("⚠️ يرجى إدخال أحجام العناصر بشكل صحيح.")
    else:
        with st.spinner(f'جاري الحساب...'):
            
            # === حالة المقارنة بين الاثنين ===
            if algorithm == "مقارنة بين الاثنين (Compare Both)":
                st.success("تم تشغيل الخوارزميتين بنجاح! إليك مقارنة تفصيلية:")
                
                # 1. تشغيل الخوارزميتين
                bt_bins, bt_time = solve_backtracking(items, bin_capacity)
                ga_bins, ga_time = solve_genetic(items, bin_capacity)
                
                # 2. رسم بياني سريع جوة الواجهة للمقارنة
                st.markdown("### 📊 ملخص المقارنة")
                chart_data = pd.DataFrame({
                    "الخوارزمية": ["Backtracking", "Genetic Algorithm"],
                    "وقت التنفيذ (ثانية)": [bt_time, ga_time],
                    "عدد الصناديق": [len(bt_bins), len(ga_bins)]
                }).set_index("الخوارزمية")
                
                chart_col1, chart_col2 = st.columns(2)
                with chart_col1:
                    st.markdown("**مقارنة وقت التنفيذ (أقل = أفضل)**")
                    st.bar_chart(chart_data["وقت التنفيذ (ثانية)"], color="#FF4B4B")
                with chart_col2:
                    st.markdown("**مقارنة عدد الصناديق (أقل = أفضل)**")
                    st.bar_chart(chart_data["عدد الصناديق"], color="#0068C9")
                
                st.markdown("---")
                
                # 3. عرض التوزيعة جنب بعض باستخدام الأعمدة
                col1, col2 = st.columns(2)
                
                with col1:
                    st.header("🌳 Backtracking")
                    st.metric("⏱️ الوقت", f"{bt_time:.4f} ثانية")
                    st.metric("📦 عدد الصناديق", f"{len(bt_bins)}")
                    display_bins(bt_bins, bin_capacity)
                    
                with col2:
                    st.header("🧬 Genetic Algorithm")
                    st.metric("⏱️ الوقت", f"{ga_time:.4f} ثانية")
                    st.metric("📦 عدد الصناديق", f"{len(ga_bins)}")
                    display_bins(ga_bins, bin_capacity)

            # === حالة تشغيل خوارزمية واحدة ===
            else:
                if algorithm == "Backtracking Search":
                    best_bins, exec_time = solve_backtracking(items, bin_capacity)
                elif algorithm == "Genetic Algorithm":
                    best_bins, exec_time = solve_genetic(items, bin_capacity)
                
                st.success(f"تم الحل بنجاح باستخدام {algorithm}!")
                
                col1, col2 = st.columns(2)
                col1.metric("⏱️ وقت التنفيذ", f"{exec_time:.4f} ثانية")
                col2.metric("📦 عدد الصناديق المستخدمة", f"{len(best_bins)} صندوق")
                
                st.markdown("### 📊 تفاصيل التوزيعة")
                display_bins(best_bins, bin_capacity)
