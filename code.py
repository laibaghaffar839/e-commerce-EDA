#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Converted from Jupyter Notebook: notebook.ipynb
Conversion Date: 2025-09-19T03:00:51.063Z
"""

# ## Student Name: Laiba Shahzadi  
# ## Roll No: FA23-BST-036  
# ## Section: BST-B  

# #### Load the Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# #### Load the Dataset
st.title("Upload and View E-commerce Dataset")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file)
    

    # # EDA Analysis
    st.subheader("Expolatory Data Analysis")
    st.write(df.shape)
    st.write(df.info())
    st.write(df.isnull().sum())

    # ### Convert 'order_date' to datetime format
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['order_year'] = df['order_date'].dt.year
    df['order_month'] = df['order_date'].dt.month
    df['date'] = df['order_date'].dt.day
    df['order_weekday'] = df['order_date'].dt.day_name()
    df['order_time'] = df['order_date'].dt.time
    df['total_price'] = df['price'] * df['quantity']
    st.dataframe(df.head())

    # ## Visualization
    daily_sales = df.groupby('date')['total_price'].sum().reset_index()
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=daily_sales, x='date', y='total_price', marker='o',
                 color='seagreen', markerfacecolor='black', markeredgecolor='blue')
    plt.title("Daily Sales Trend")
    plt.xlabel("Date")
    plt.ylabel("Total Sales (Revenue)")
    st.pyplot(plt.gcf())

    df_sum = df.groupby("category", as_index=False)["total_price"].sum()
    plt.figure(figsize=(8, 6))
    sns.barplot(data=df_sum, x="category", y="total_price", hue="category",
                palette="Blues", legend=False, errorbar=None)
    plt.xlabel("Category")
    plt.ylabel("Total Price")
    plt.title("Total Price by Category")
    st.pyplot(plt.gcf())

    region_payment = df.groupby(['region', 'payment_method'])['total_price'].sum().reset_index()
    pivot_table = region_payment.pivot(index='region', columns='payment_method', values='total_price')
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, annot=True, fmt=".0f", cmap="YlGnBu")
    plt.title("Sales Heatmap: Region vs Payment Method")
    st.pyplot(plt.gcf())

    category_summary = df.groupby('category').agg({
        'quantity': 'sum',
        'discount': 'mean'
    }).reset_index()
    fig, ax1 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=category_summary, x='category', y='quantity', ax=ax1, color='steelblue')
    ax1.set_ylabel("Total Quantity Sold", color="blue")
    ax1.set_xlabel("Product Category")
    ax2 = ax1.twinx()
    sns.lineplot(data=category_summary, x='category', y='discount',
                 ax=ax2, color="red", marker="o")
    ax2.set_ylabel("Average Discount", color="red")
    plt.title("Quantity Sold vs Average Discount per Category")
    st.pyplot(fig)

    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='category', y='total_price', hue='category',
                palette="Blues", legend=False)
    plt.title("Boxplot of Total Sales by Category")
    plt.xlabel("Product Category")
    plt.ylabel("Total Sales (Revenue)")
    st.pyplot(plt.gcf())

    sales_summary = df.groupby(['category', 'order_month'])['total_price'].sum().reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(data=sales_summary, x='category', y='total_price',
                hue='order_month', palette="Set2")
    plt.title("Total Sales by Category and Month")
    plt.xlabel("Product Category")
    plt.ylabel("Total Sales (Revenue)")
    plt.legend(title="Month")
    st.pyplot(plt.gcf())

    payment_summary = df.groupby('payment_method')['total_price'].sum()
    plt.figure(figsize=(6, 6))
    plt.pie(payment_summary, labels=payment_summary.index,
            autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set2"))
    plt.title("Sales Share by Payment Method")
    st.pyplot(plt.gcf())

    g = sns.catplot(data=df, x="category", y="discount",
                    hue="region", kind="bar", palette="Reds",
                    height=5, aspect=2, errorbar=None)
    g.set_axis_labels("Category", "Average Discount")
    g.fig.suptitle("Average Discount by Category and Region", y=1.02)
    st.pyplot(g.fig)

    sales_summary = df.groupby(['order_weekday', 'order_month'])['total_price'].sum().reset_index()
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                     'Friday', 'Saturday', 'Sunday']
    sales_summary['order_weekday'] = pd.Categorical(
        sales_summary['order_weekday'], categories=weekday_order, ordered=True)
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=sales_summary, x='order_weekday', y='total_price',
                 hue='order_month', marker='o',
                 markeredgecolor='black', markerfacecolor='red')
    plt.title("Sales Trend Across Weekdays by Month")
    plt.xlabel("Weekday")
    plt.ylabel("Total Sales (Revenue)")
    plt.legend(title="Month")
    st.pyplot(plt.gcf())

    df_sum = df.groupby(["region", "category"], as_index=False)["quantity"].sum()
    g = sns.catplot(data=df_sum, x='category', y='quantity',
                    hue='category', col='region', kind='bar',
                    palette='Blues', col_wrap=2, height=5, aspect=1)
    g.fig.subplots_adjust(top=0.8)
    g.fig.suptitle('Quantity by Category and Region')
    st.pyplot(g.fig)

else:
    st.warning("Please upload a CSV file to continue.")
