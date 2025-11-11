# Updated app.py

import streamlit as st
import matplotlib.pyplot as plt

# Create separate figure instances
fig_income_obesity_duplicate = plt.figure()
fig_world_duplicate = plt.figure()

# Add your plotting code here using fig_income_obesity_duplicate and fig_world_duplicate

# Example plots (replace with your actual plotting code):

# Income vs Obesity
ax1 = fig_income_obesity_duplicate.add_subplot(111)
ax1.plot([1, 2, 3], [1, 2, 3])  # Your actual data and plotting logic

# World Plot
ax2 = fig_world_duplicate.add_subplot(111)
ax2.plot([3, 2, 1], [1, 3, 2])  # Your actual data and plotting logic

# Streamlit commands to display plots
st.pyplot(fig_income_obesity_duplicate)
st.pyplot(fig_world_duplicate)