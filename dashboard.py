import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from drug_text_drugs_forum import free_text

#background color
st.markdown(
    """
    <style>
    body {
        background-color: #FFC0CB; /* Pink color */
        margin: 0;
        padding: 0;
    }
    .reportview-container .main {
        max-width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#Replace with file path
df_wastewater = pd.read_csv('/Users/fanfan/Desktop/1.21/waste_water_prediction.csv')
df_unreport = pd.read_csv('/Users/fanfan/Desktop/1.21/mergedforUNdrug1.csv')
df_emcdda = pd.read_csv('/Users/fanfan/Desktop/1.21/all_drugs.csv')
df_reddit = pd.read_csv('/Users/fanfan/Desktop/1.21/reddit_formatted.csv')
df_drugset = pd.read_csv('/Users/fanfan/Desktop/1.21/drugs_forum_final1.csv')

# Convert all country names to lowercase
df_wastewater['Country'] = df_wastewater['Country'].str.lower()
df_unreport['Country'] = df_unreport['Country'].str.lower()
df_emcdda['Country'] = df_emcdda['Country'].str.lower()
df_reddit['Country'] = df_reddit['Country'].str.lower()
df_drugset['Country'] = df_drugset['Country'].str.lower()

# Combine unique country values from all dataframes
all_countries_set = set(df_wastewater['Country'].str.lower()).union(
    set(df_unreport['Country'].str.lower())).union(set(df_emcdda['Country'].str.lower())).union(set(df_drugset['Country'].str.lower()))
all_countries = list(all_countries_set)

# data sources
data_sources = ['EMCDDA Wastewater', 'UN World Drug Report', 'EMCDDA Drug Report', 'Reddit','DrugsForum.nl']

# Streamlit UI
st.title("Illicit-Drug Trends Across European Countries")

# Folium Map
latitude = 50.8503
longitude = 4.3517
map = folium.Map(location=[latitude, longitude], zoom_start=4,
                 scrollWheelZoom=False, tiles='OpenStreetMap')

st.sidebar.title("Illicit-Drug Trends Across European Countries")

selected_countries = st.sidebar.multiselect(
    "**Country**", sorted(all_countries), format_func=lambda x: x.capitalize())

selected_countries_lower = []



selected_sources = st.sidebar.multiselect("**Data Source**", data_sources)

# Multiselect for years
selected_years = st.sidebar.multiselect(
        "**Year**", [2020,2021,2022,2023])


# Multiselect for years
#selected_years = st.sidebar.multiselect(
#    "Select Years:", sorted(df_wastewater['Year'].unique()), default=df_wastewater['Year'].unique())

#highlight selected countries on the map
if selected_countries:
    #lowercase
    selected_countries_lower = [country.lower()
                                for country in selected_countries]

    
    selected_df_wastewater = df_wastewater[df_wastewater['Country'].isin(
        selected_countries_lower)]
    selected_df_unreport = df_unreport[df_unreport['Country'].isin(
        selected_countries_lower)]
    selected_df_emcdda = df_emcdda[df_emcdda['Country'].isin(
        selected_countries_lower)]
    selected_df_reddit = df_reddit[df_reddit['Country'].isin(
        selected_countries_lower)]
    selected_df_drugset = df_drugset[df_drugset['Country'].isin(
        selected_countries_lower)]

    #mean latitude and longitude for each selected country
    mean_coords = {}

    def add_mean_coords(row, color):
        country = row['Country']
        if 'latitude' in row and 'longitude' in row:
            if country not in mean_coords:
                mean_coords[country] = {
                    'latitude': row['latitude'], 'longitude': row['longitude'], 'color': color}
            else:
                mean_coords[country]['latitude'] = (
                    mean_coords[country]['latitude'] + row['latitude']) / 2
                mean_coords[country]['longitude'] = (
                    mean_coords[country]['longitude'] + row['longitude']) / 2

    #wastewater dataframe
    selected_df_wastewater.apply(
        lambda row: add_mean_coords(row, 'blue'), axis=1)

    #=UN report dataframe
    selected_df_unreport.apply(
        lambda row: add_mean_coords(row, 'green'), axis=1)

    #emcdda dataframe
    selected_df_emcdda.apply(lambda row: add_mean_coords(row, 'red'), axis=1)

    #reddit dataframe
    selected_df_reddit.apply(
        lambda row: add_mean_coords(row, 'orange'), axis=1)

    selected_df_drugset.apply(
        lambda row: add_mean_coords(row, 'yellow'), axis=1)

    #markers for each selected country using mean coordinates
    for country, coords in mean_coords.items():
        # Exclude EUROPEAN UNION
        if pd.notna(country) and str(country).lower() != 'european union':
            folium.Marker(
                location=[coords['latitude'], coords['longitude']],
                popup=str(country),
                icon=folium.Icon(color=coords['color'])
            ).add_to(map)



#filter for 'Year' if data source is 'wastewater'
if 'EMCDDA Wastewater' in selected_sources:
    #selected_year = st.sidebar.multiselect(
    #    "Select Year for Wastewater:", sorted(df_wastewater['Year'].unique()), default=selected_years)

    selected_df_wastewater = df_wastewater[(df_wastewater['Country'].isin(
        selected_countries_lower)) & (df_wastewater['Year'].isin(selected_years))]

else:
    selected_df_wastewater = None

#filter for 'Year' if data source is 'UN report'
if 'UN World Drug Report' in selected_sources:
    #selected_year_unreport = st.sidebar.multiselect(
    #    "Select Year for UN report:", sorted(df_unreport['Year'].unique()), default=selected_years)

    selected_df_unreport = df_unreport[(df_unreport['Country'].isin(
        selected_countries_lower)) & (df_unreport['Year'].isin(selected_years))]

else:
    selected_df_unreport = None

if 'EMCDDA Drug Report' in selected_sources:
    selected_df_emcdda = df_emcdda[(df_emcdda['Country'].isin(
        selected_countries_lower))]

else:
    selected_df_emcdda = None


if 'Reddit' in selected_sources:
    selected_df_reddit = df_reddit[(df_reddit['Country'].isin(
        selected_countries_lower)) & (df_reddit['year'].isin(selected_years))]

else:
    selected_df_reddit = None


if 'DrugsForum.nl' in selected_sources:
    selected_df_drugset = df_drugset[(df_drugset['Country'].isin(
        selected_countries_lower)) & (df_drugset['year'].isin(selected_years))]

else:
    selected_df_drugset = None



# Highlight selected countries on the map for each selected data source
if selected_df_wastewater is not None and not selected_df_wastewater.empty:
    for index, row in selected_df_wastewater.iterrows():
        if 'latitude' in row and 'longitude' in row:
            folium.Marker(
                location=[row['latitude'], row['longitude']], popup=row['Country'], icon=folium.Icon(color='blue')).add_to(map)

if selected_df_unreport is not None and not selected_df_unreport.empty:
    for index, row in selected_df_unreport.iterrows():
        if 'latitude' in row and 'longitude' in row:
            folium.Marker(
                location=[row['latitude'], row['longitude']], popup=row['Country'], icon=folium.Icon(color='green')).add_to(map)

if selected_df_reddit is not None and not selected_df_reddit.empty:
    for index, row in selected_df_reddit.iterrows():
        if 'latitude' in row and 'longitude' in row:
            folium.Marker(
                location=[row['latitude'], row['longitude']], popup=row['Country'], icon=folium.Icon(color='orange')).add_to(map)

if selected_df_emcdda is not None and not selected_df_emcdda.empty:
    for index, row in selected_df_emcdda.iterrows():
        if 'latitude' in row and 'longitude' in row:
            folium.Marker(
                location=[row['latitude'], row['longitude']], popup=row['Country'], icon=folium.Icon(color='red')).add_to(map)
if selected_df_drugset is not None and not selected_df_drugset.empty:
    for index, row in selected_df_drugset.iterrows():
        if 'latitude' in row and 'longitude' in row:
            folium.Marker(
                location=[row['latitude'], row['longitude']], popup=row['Country'], icon=folium.Icon(color='yellow')).add_to(map)


# Folium map
folium_static(map)

st.sidebar.markdown("The drug data in DrugsForum.nl is exclusively available for the Netherlands.")

#selected data for 'UN report'
if selected_df_unreport is not None:
    selected_df_unreport["Year"] = selected_df_unreport["Year"].astype(str)

    blue_shade = 'rgb(0, 0, 128)'  # Darker blue
    gold_shade = 'rgb(218, 165, 32)'  # Darker gold

    #color map for each unique year
    color_map = {
        year: blue_shade if year == '2020' else gold_shade for year in selected_df_unreport['Year'].unique()
    }

    for country in selected_countries:
        country_data = selected_df_unreport[selected_df_unreport['Country'] == country]
        if not selected_years:
                st.warning("Please select a year.")

        if len(set(country_data['Year'])) > 1:
            #discrete variable
            country_data['Year'] = country_data['Year'].astype(str)

            #bar plot with years side by side
            fig = px.bar(country_data, x='Metabolite', y='Percentage of the population', color='Year',
                         title=f'Metabolite Comparison for {country.capitalize()}',
                         labels={'Percentage of the population': 'Percentage of the population'},
                         barmode='group', category_orders={"Year": sorted(country_data['Year'].unique())},
                         color_discrete_map=color_map)

            fig.update_layout(
                xaxis_title='Metabolite',
                yaxis_title='Percentage of the population',
                title_text=f'Metabolite Comparison for {country.capitalize()}',
                title_x=0.05,
                showlegend=True,
                barmode='group'  # Display bars side by side
            )

            st.plotly_chart(fig)
            result = free_text(country_data)
            st.markdown(result)

        else:
            #if there's no data for the selected year and a year is selected
            if not country_data.empty and selected_years:
                single_year = country_data['Year'].iloc[0]
                fig = px.bar(country_data, x='Metabolite', y='Percentage of the population', color='Year',
                            title=f'Metabolite Comparison for {country.capitalize()}',
                            labels={'Percentage of the population': 'Percentage of the population'},
                            category_orders={"Year": [single_year]},
                            color_discrete_map={single_year: color_map[single_year]})
                fig.update_layout(
                    xaxis_title='Metabolite',
                    yaxis_title='Percentage of the population',
                    title_text=f'Metabolite Comparison for {country.capitalize()}',
                    title_x=0.05,
                    showlegend=True
                )

                st.plotly_chart(fig)
                result = free_text(country_data)
                st.markdown(result)

            else:
                st.warning(f"No data available for {country.capitalize()} in UN World Drug Report")

#selected data for other sources
if selected_df_wastewater is not None and not selected_df_wastewater.empty:
    selected_df_wastewater["Year"] = selected_df_wastewater["Year"].astype(str)
    if not selected_years:
        st.warning("Please select a year.")
    else:
        for country in selected_countries:
            country_data = selected_df_wastewater[selected_df_wastewater['Country'] == country]
            
            if country_data.empty:
                st.warning(f"No data available for {country.capitalize()} in EMCDDA Wastewater")
            else:
                st.header(f"EMCDDA Wastewater Data for {country.capitalize()}")
                #if there are multiple years for the country
                if len(set(country_data['Year'])) > 1:
                    
                    country_data['Year'] = country_data['Year'].astype(str)
                    
                    #bar plot with years side by side
                    fig = px.bar(country_data, x='Metabolite', y='litre/day per 1 000 inhabitants', color='Year',
                                 title=f'Metabolite Comparison for {country.capitalize()} (Multiple Years)',
                                 labels={'litre/day per 1 000 inhabitants': 'Metabolite Amount'},
                                 barmode='group', category_orders={"Year": sorted(country_data['Year'].unique())})
                    
                    fig.update_layout(
                        xaxis_title='Metabolite',
                        yaxis_title='litre/day per 1 000 inhabitants',
                        title_text=f'Metabolite Comparison for {country.capitalize()} (Multiple Years)',
                        title_x=0.05,
                        showlegend=True,
                        barmode='group'  # Display bars side by side
                    )

                    st.plotly_chart(fig)
                    
                    result = free_text(country_data)
                    st.markdown(result)
                else:
                    #bar plot for a single year
                    fig = px.bar(country_data, x='Metabolite', y='litre/day per 1 000 inhabitants',
                                 title=f'Metabolite Comparison for {country.capitalize()}', labels={'litre/day per 1 000 inhabitants': 'Metabolite Amount'})
                    st.plotly_chart(fig)
                    
                    result = free_text(country_data)
                    st.markdown(result)


if selected_df_emcdda is not None and not selected_df_emcdda.empty:
    for country in selected_countries:
        country_data_emcdda = selected_df_emcdda[selected_df_emcdda['Country'] == country]
        if not country_data_emcdda.empty and not (country_data_emcdda['percentage_of_post'] == 0).all():
            st.header(f"EMCDDA Drug Report Data for {country.capitalize()}")
            fig_emcdda = px.pie(country_data_emcdda, names='drug', values='percentage_of_post',
                                title=f'Drug Distribution for {country.capitalize()}')
            st.plotly_chart(fig_emcdda)
            result = free_text(country_data_emcdda)
            st.markdown(result)
        elif country_data_emcdda.empty:
            st.warning(f"No data available for {country.capitalize()} in EMCDDA Drug Report")

#selected data for Reddit
if selected_df_reddit is not None and not selected_df_reddit.empty:
    for country in selected_countries:
        country_data_reddit = selected_df_reddit[selected_df_reddit['Country'] == country]
        if not country_data_reddit.empty:
            st.header(f"Reddit Data for {country.capitalize()}")
            result = free_text(country_data_reddit)
            st.markdown(result)
        elif country_data_reddit.empty:
            st.warning(f"No data available for {country.capitalize()} in Reddit")

#selected data for drugsforum
if selected_df_drugset is not None and not selected_df_drugset.empty:
    for country in selected_countries:
        country_data_drugset = selected_df_drugset[selected_df_drugset['Country'] == country]
        if not country_data_drugset.empty:
            st.header(f"DrugsForum.nl Data for {country.capitalize()}")
            result = free_text(country_data_drugset)
            st.markdown(result)
        elif country_data_drugset.empty:
            st.warning(f"No data available for {country.capitalize()} in DrugsForum.nl")

#message if no data source is selected
if not selected_countries:
    st.warning( ':blue[Please select at least one country]')
if not selected_sources:
    st.warning( ':blue[Please select at least one data source]')
#message if no years are selected
if not selected_years:
    st.warning(":blue[Please select at least one year]")


