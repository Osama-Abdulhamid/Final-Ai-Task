import streamlit as st
import time
import pandas as pd # Used for comparison charts inside the UI

# Importing algorithms from other files
from backtracking_solver import solve_backtracking
from genetic_solver import solve_genetic

# Page Configuration
st.set_page_config(page_title="Bin Packing Solver", page_icon="📦", layout="wide")

st.title("📦 Bin Packing Problem Solver")
st.markdown("---")

# Sidebar Settings
st.sidebar.header("⚙️ Problem Settings")

bin_capacity = st.sidebar.number_input("Bin Capacity:", min_value=1, value=8, step=1)

items_input = st.sidebar.text_area("Item Sizes (separated by commas):", "7, 6, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1")
items = [int(x.strip()) for x in items_input.split(",") if x.strip().isdigit()]

# Algorithm Selection
algorithm = st.sidebar.radio("Select Execution Mode:", ("Backtracking Search", "Genetic Algorithm", "Compare Both"))

st.sidebar.markdown("---")
solve_button = st.sidebar.button("🚀 Solve", use_container_width=True)

# Helper Function to display bins
def display_bins(bins, capacity):
    for i, b in enumerate(bins):
        st.write(f"**Bin {i+1}** (Total: {sum(b)}/{capacity})")
        fill_percentage = min(sum(b) / capacity, 1.0)
        st.progress(fill_percentage)
        st.write(f"`{b}`")

# Main Execution Logic
if solve_button:
    if not items:
        st.error("⚠️ Please enter valid item sizes.")
    else:
        with st.spinner('Calculating...'):
            
            # === Case: Compare Both Algorithms ===
            if algorithm == "Compare Both":
                st.success("Both algorithms executed successfully! Here is a detailed comparison:")
                
                # 1. Execute both algorithms
                bt_bins, bt_time = solve_backtracking(items, bin_capacity)
                ga_bins, ga_time = solve_genetic(items, bin_capacity)
                
                # 2. Comparison Summary Chart
                st.markdown("### 📊 Comparison Summary")
                chart_data = pd.DataFrame({
                    "Algorithm": ["Backtracking", "Genetic Algorithm"],
                    "Execution Time (s)": [bt_time, ga_time],
                    "Bin Count": [len(bt_bins), len(ga_bins)]
                }).set_index("Algorithm")
                
                chart_col1, chart_col2 = st.columns(2)
                with chart_col1:
                    st.markdown("**Execution Time Comparison (Lower is Better)**")
                    st.bar_chart(chart_data["Execution Time (s)"], color="#FF4B4B")
                with chart_col2:
                    st.markdown("**Bin Count Comparison (Lower is Better)**")
                    st.bar_chart(chart_data["Bin Count"], color="#0068C9")
                
                st.markdown("---")
                
                # 3. Side-by-Side Distribution View
                col1, col2 = st.columns(2)
                
                with col1:
                    st.header("🌳 Backtracking")
                    st.metric("⏱️ Time", f"{bt_time:.4f} sec")
                    st.metric("📦 Bin Count", f"{len(bt_bins)}")
                    display_bins(bt_bins, bin_capacity)
                    
                with col2:
                    st.header("🧬 Genetic Algorithm")
                    st.metric("⏱️ Time", f"{ga_time:.4f} sec")
                    st.metric("📦 Bin Count", f"{len(ga_bins)}")
                    display_bins(ga_bins, bin_capacity)

            # === Case: Single Algorithm Execution ===
            else:
                if algorithm == "Backtracking Search":
                    best_bins, exec_time = solve_backtracking(items, bin_capacity)
                elif algorithm == "Genetic Algorithm":
                    best_bins, exec_time = solve_genetic(items, bin_capacity)
                
                st.success(f"Solved successfully using {algorithm}!")
                
                col1, col2 = st.columns(2)
                col1.metric("⏱️ Execution Time", f"{exec_time:.4f} sec")
                col2.metric("📦 Bins Used", f"{len(best_bins)} bins")
                
                st.markdown("### 📊 Distribution Details")
                display_bins(best_bins, bin_capacity)
