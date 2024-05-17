import streamlit as st
from streamlit_option_menu import option_menu
import pymongo
import plotly.express as px
import pandas as pd 
import os
from PIL import Image
# import warnings
import matplotlib.pyplot as plt


# warnings.filterwarnings('ignore')

# streamlit creation

# Setting page configuration
st.set_page_config(page_title="AirBnb-Analysis", layout="wide", page_icon=":bar_chart:")
st.title(":bar_chart:   AirBnb-Analysis")
st.header("AirBnb-Analysis - Data Visualization and Exploration", divider='rainbow')
st.sidebar.header(":wave: :violet[Hello! Welcome to the Visualization dashboard]")

conn = pymongo.MongoClient("mongodb+srv://anto4848:hannah4848@test.8pdvcqm.mongodb.net/?retryWrites=true&w=majority&appName=test")

db=conn["sample_airbnb"]
col=db["listingsAndReviews"]

df = pd.read_csv("D:\DS\Projects\project 4 - Airbnb\Airbnb_data_final.csv")

SELECT = option_menu(None, ["Home", "Overview", 'Explore'], 
    icons=['house', "list-task", 'gear'], 
    default_index=0, orientation="horizontal")


if SELECT=="Home":
    st.markdown("## :blue[Overview] : To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")
    st.markdown("## :blue[Technologies used] : Python, Pandas, Plotly, Streamlit, MongoDB")
    st.markdown("## :blue[Domain] : Travel Industry, Property Management and Tourism")

elif SELECT=="Overview":
    # GETTING USER INPUTS
        country = st.multiselect(label='Select a Country', options=sorted(
            df.Country.unique()), placeholder="Select Country")
        prop = st.multiselect(label='Select Property_type', options=sorted(
            df.Property_type.unique()), placeholder="Select Property_type")
        room = st.multiselect(label='Select Room_type', options=sorted(
            df.Room_type.unique()), placeholder="Select Room_type")
        price = st.slider('Select Price', df.Price.min(),df.Price.max(), (df.Price.min(), df.Price.max()))

    # CONVERTING THE USER INPUT INTO QUERY
        query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'

    # CREATING COLUMNS
        col1, col2 = st.columns(2, gap='medium')
        with col1:
            # TOP 10 PROPERTY TYPES BAR CHART
            df1 = df.query(query).groupby(["Property_type"]).size().reset_index(
                name="listings").sort_values(by='listings', ascending=False)[:10]
            fig = px.bar(df1,
                         title='Top 10 Property Types',
                         x='listings',
                         y='Property_type',
                         orientation='h',
                         color='Property_type',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)

            # TOP 10 HOSTS BAR CHART
            df2 = df.query(query).groupby(["Name"]).size().reset_index(
                name="listings").sort_values(by='listings', ascending=False)[:10]
            fig = px.bar(df2,
                         title='Top 10 Hosts with Highest number of Listings',
                         x='listings',
                         y='Name',
                         orientation='h',
                         color='Name',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            
            with col2:
            # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
                df1 = df.query(query).groupby(
                    ["Room_type"]).size().reset_index(name="counts")
                fig = px.pie(df1,
                            title='Total Listings in each Room_types',
                            names='Room_type',
                            values='counts',
                            color_discrete_sequence=px.colors.sequential.Rainbow
                            )
                fig.update_traces(textposition='outside', textinfo='value+label')
                st.plotly_chart(fig, use_container_width=True)

            # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
                country_df = df.query(query).groupby(['Country'], as_index=False)['Name'].count().rename(columns={'Name': 'total_Listings'})
                fig = px.choropleth(country_df,
                                    title='Total Listings in each Country',
                                    locations='Country',
                                    locationmode='country names',
                                    color='total_Listings',
                                    color_continuous_scale=px.colors.sequential.Plasma
                                    )
                st.plotly_chart(fig, use_container_width=True)
    
        # # GETTING USER INPUTS
        # country = st.multiselect(label='Select a country',
        #                         options=sorted(df.Country.unique()), placeholder="Select country")
        # prop = st.multiselect(label='Select property_type', options=sorted(
        #     df.Property_type.unique()), placeholder="Select property_type")
        # room = st.multiselect(label='Select room_type', options=sorted(
        #     df.Room_type.unique()), placeholder="Select room_type")
        # price = st.slider(label='Select price', min_value=df.Price.min(),
        #                 max_value=df.Price.max(), value=(df.Price.min(), df.Price.max()))
        
        # # CONVERTING THE USER INPUT INTO QUERY
        # query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'

            # HEADING 1
        st.markdown("## Price Analysis")

        # CREATING COLUMNS
        col1, col2 = st.columns(2, gap='medium')

        with col1:
            # AVG PRICE BY ROOM TYPE BARCHART
            pr_df = df.query(query).groupby('Room_type', as_index=False)[
                'Price'].mean().sort_values(by='Price')
            fig = px.bar(data_frame=pr_df,
                        x='Room_type',
                        y='Price',
                        color='Price',
                        title='Avg Price in each Room type'
                        )
            st.plotly_chart(fig, use_container_width=True)

            # HEADING 2
            st.markdown("## Availability Analysis")

            # AVAILABILITY BY ROOM TYPE BOX PLOT
            fig = px.box(data_frame=df.query(query),
                        x='Room_type',
                        y='Availability_365',
                        color='Room_type',
                        title='Availability by Room_type'
                        )
            st.plotly_chart(fig, use_container_width=True)

            with col2:

                # AVG PRICE IN COUNTRIES SCATTERGEO
                country_df = df.query(query).groupby(
                    'Country', as_index=False)['Price'].mean()
                fig = px.scatter_geo(data_frame=country_df,
                                    locations='Country',
                                    color='Price',
                                    hover_data=['Price'],
                                    locationmode='country names',
                                    size='Price',
                                    title='Avg Price in each Country',
                                    color_continuous_scale='agsunset'
                                    )
                col2.plotly_chart(fig, use_container_width=True)

                # BLANK SPACE
                st.markdown("#   ")
                st.markdown("#   ")

                # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
                country_df = df.query(query).groupby('Country', as_index=False)['Availability_365'].mean()
                country_df.Availability_365 = country_df.Availability_365.astype(int)
                fig = px.scatter_geo(data_frame=country_df,
                                    locations='Country',
                                    color='Availability_365',
                                    hover_data=['Availability_365'],
                                    locationmode='country names',
                                    size='Availability_365',
                                    title='Avg Availability in each Country',
                                    color_continuous_scale='agsunset'
                                    )
                st.plotly_chart(fig, use_container_width=True)