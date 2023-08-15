import pandas as pd
import folium
from IPython.display import IFrame

# Latitude e Longitude de Portugal
latitude = 39.3999
longitude = -8.2245


# define portugal_nuts2
portugal_nuts2 = {
    "PT11": "Lisboa",
    "PT15": "Centro",
    "PT16": "Alentejo",
    "PT17": "Algarve",
    "PT18": "Região Autónoma dos Açores",
    "PT20": "Região Autónoma da Madeira",
    "PT30": "Norte"
}

# Define the coordinates for each region
nuts2_coordinates = {
    "PT11": [38.7253, -9.1500],   # Lisboa
    "PT15": [39.7500, -8.0000],   # Centro
    "PT16": [38.5333, -7.9000],   # Alentejo
    "PT17": [37.1667, -8.0000],   # Algarve
    "PT18": [37.7412, -25.6750],  # Região Autónoma dos Açores
    "PT20": [32.6333, -16.9000],  # Região Autónoma da Madeira
    "PT30": [41.5346, -8.6163]    # Norte
}

import geopandas as gpd

nuts2 = gpd.read_file('shapefiles/NUTS_RG_20M_2021_3035.shp')

nuts2_pt = nuts2[(nuts2['CNTR_CODE'] == 'PT') & (nuts2['LEVL_CODE'] == 2)]
nuts2_pt = nuts2_pt.to_crs(epsg=4326)


colors = [
    "red",
    "green",
    "blue",
    "yellow",
    "orange",
    "purple",
    "pink"
]



# Crie um objeto de mapa com o centro em Portugal
m = folium.Map(location=[latitude, longitude], zoom_start=6)

folium.Choropleth(
    geo_data=nuts2_pt.to_json(),
    name='choropleth',
    data=nuts2_pt.NUTS_ID,
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='NUTS 2 Regions',
    highlight=True,
).add_to(m)



folium.LayerControl().add_to(m)


m.save("mapa_nuts2.html")

# Exibe o mapa no notebook
IFrame(src='mapa_nuts2.html', width=700, height=600)


import geopandas as gpd
import folium

# Load the NUTS2 shapefile and convert it to EPSG 4326
nuts2 = gpd.read_file('shapefiles/NUTS_RG_20M_2021_3035.shp')
nuts2 = nuts2[(nuts2['CNTR_CODE'] == 'PT') & (nuts2['LEVL_CODE'] == 2)]
nuts2 = nuts2.to_crs(epsg=4326)

# Define the colors for each NUTS2 region
colors = {
    "PT11": "red",
    "PT15": "green",
    "PT16": "blue",
    "PT17": "yellow",
    "PT18": "orange",
    "PT20": "purple",
    "PT30": "pink"
}

# Create a Folium map centered on Portugal
m2 = folium.Map(location=[39.3999, -8.2245], zoom_start=6)

# Add a GeoJSON layer with the NUTS2 boundaries and color each region according to the colors dictionary
folium.GeoJson(
    nuts2,
    style_function=lambda feature: {
        "fillColor": colors[feature["properties"]["NUTS_ID"]],
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.7
    }
).add_to(m2)

# Add a layer control to the map
folium.LayerControl().add_to(m2)

# Display the map
m2.save('map_nuts2222.html')






import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster

# Load the NUTS2 shapefile and convert it to EPSG 4326
nuts2 = gpd.read_file('shapefiles/NUTS_RG_20M_2021_3035.shp')
nuts2 = nuts2[(nuts2['CNTR_CODE'] == 'PT') & (nuts2['LEVL_CODE'] == 2)]
nuts2 = nuts2.to_crs(epsg=4326)

# Define the colors for each NUTS2 region
colors = {
    "PT11": "red",
    "PT15": "green",
    "PT16": "blue",
    "PT17": "pink",
    "PT18": "orange",
    "PT20": "purple",
    "PT30": "yellow"
}

# Create a Folium map centered on Portugal
m2 = folium.Map(location=[39.3999, -8.2245], zoom_start=6)

# Add a GeoJSON layer with the NUTS2 boundaries and color each region according to the colors dictionary
folium.GeoJson(
    nuts2,
    style_function=lambda feature: {
        "fillColor": colors[feature["properties"]["NUTS_ID"]],
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.7
    }
).add_to(m2)

# Add markers for the locations in the final_fiscrep.pickle file
df = pd.read_pickle('final_fiscrep.pickle')

rows_to_drop = [6233, 4249, 5776, 1502, 10352, 3089, 9462, 1076, 2207, 4147, 4853, 3683, 1339, 9129, 1787, 8480, 3903, 5885, 4910, 4928, 1657, 3375, 5105, 6393, 5336, 9336, 9335, 6531, 52, 2358, 300]  # List of row indices to be dropped
df = df.drop(rows_to_drop)


markercluster = MarkerCluster().add_to(m2)
for index, row in df.iterrows():
    if row['Result'] == 'PRESUM':
        marker_color = 'red'
        marker_icon = folium.Icon(color=marker_color, icon='times', prefix='fa')
    else:
        marker_color = 'blue'
        marker_icon = folium.Icon(color=marker_color, icon='circle', prefix='fa')
    folium.Marker(
        location=[row['lat_DD'], row['lon_DD']],
        icon=marker_icon,
        popup=index
    ).add_to(markercluster)

# Add a layer control to the map
folium.LayerControl().add_to(m2)

# Display the map
m2.save('map_infraccolor_cluster.html')







#map without clusters
import pandas as pd
import geopandas as gpd
import folium

# Load the NUTS2 shapefile and convert it to EPSG 4326
nuts2 = gpd.read_file('shapefiles/NUTS_RG_20M_2021_3035.shp')
nuts2 = nuts2[(nuts2['CNTR_CODE'] == 'PT') & (nuts2['LEVL_CODE'] == 2)]
nuts2 = nuts2.to_crs(epsg=4326)

# Define the colors for each NUTS2 region
colors = {
    "PT11": "red",
    "PT15": "green",
    "PT16": "blue",
    "PT17": "pink",
    "PT18": "orange",
    "PT20": "purple",
    "PT30": "yellow"
}

# Create a Folium map centered on Portugal
m2 = folium.Map(location=[39.3999, -8.2245], zoom_start=6)

# Add a GeoJSON layer with the NUTS2 boundaries and color each region according to the colors dictionary
folium.GeoJson(
    nuts2,
    style_function=lambda feature: {
        "fillColor": colors[feature["properties"]["NUTS_ID"]],
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.7
    }
).add_to(m2)

# Add markers for the locations in the final_fiscrep.pickle file
df = pd.read_pickle('final_fiscrep.pickle')

rows_to_drop = [6233, 4249, 5776, 1502, 10352, 3089, 9462, 1076, 2207, 4147, 4853, 3683, 1339, 9129, 1787, 8480, 3903, 5885, 4910, 4928, 1657, 3375, 5105, 6393, 5336, 9336, 9335, 6531, 52, 2358, 300]  # List of row indices to be dropped
df = df.drop(rows_to_drop)


for index, row in df.iterrows():
    if row['Result'] == 'PRESUM':
        marker_color = 'red'
    else:
        marker_color = 'blue'
    folium.CircleMarker(
        location=[row['lat_DD'], row['lon_DD']],
        radius=0.3,
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.7,
        popup=index
    ).add_to(m2)

# Add a layer control to the map
folium.LayerControl().add_to(m2)

# Display the map
m2.save('map_infraccolor_nocluster.html')



#cluster and colour of nuts 
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster

# Load the NUTS2 shapefile and convert it to EPSG 4326
nuts2 = gpd.read_file('shapefiles/NUTS_RG_20M_2021_3035.shp')
nuts2 = nuts2[(nuts2['CNTR_CODE'] == 'PT') & (nuts2['LEVL_CODE'] == 2)]
nuts2 = nuts2.to_crs(epsg=4326)

# Create a Folium map centered on Portugal
m2 = folium.Map(location=[39.3999, -8.2245], zoom_start=6)

# Add a GeoJSON layer with the NUTS2 boundaries and color each region
folium.GeoJson(
    nuts2,
    style_function=lambda feature: {
        "fillColor": colors.get(feature["properties"]["NUTS_ID"], "blue"),
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.7
    }
).add_to(m2)

# Add markers for the locations in the final_fiscrep.pickle file
df = pd.read_pickle('final_fiscrep.pickle')

rows_to_drop = [6233, 4249, 5776, 1502, 10352, 3089, 9462, 1076, 2207, 4147, 4853, 3683, 1339, 9129, 1787, 8480, 3903, 5885, 4910, 4928, 1657, 3375, 5105, 6393, 5336, 9336, 9335, 6531, 52, 2358, 300]  # List of row indices to be dropped
df = df.drop(rows_to_drop) 

markercluster = MarkerCluster().add_to(m2)
for index, row in df.iterrows():
    marker_color = colors.get(row['NUTSII_code'], 'blue')
    if row['Result'] == 'PRESUM':
        marker_icon = folium.Icon(color=marker_color, icon='times', prefix='fa')
    else:
        marker_icon = folium.Icon(color=marker_color, icon='circle', prefix='fa')
    folium.Marker(
        location=[row['lat_DD'], row['lon_DD']],
        icon=marker_icon,
        popup=index
    ).add_to(markercluster)

# Add a layer control to the map
folium.LayerControl().add_to(m2)

# Display the map
m2.save('map_nutscolor_cluster.html')







#done
import pandas as pd
import geopandas as gpd
import folium

# Load the NUTS2 shapefile and convert it to EPSG 4326
nuts2 = gpd.read_file('shapefiles/NUTS_RG_20M_2021_3035.shp')
nuts2 = nuts2[(nuts2['CNTR_CODE'] == 'PT') & (nuts2['LEVL_CODE'] == 2)]
nuts2 = nuts2.to_crs(epsg=4326)

# Define the colors for each NUTS2 region
colors = {
    "PT11": "red",
    "PT15": "green",
    "PT16": "blue",
    "PT17": "pink",
    "PT18": "orange",
    "PT20": "purple",
    "PT30": "yellow"
}

# Create a Folium map centered on Portugal
m2 = folium.Map(location=[39.3999, -8.2245], zoom_start=6)

# Add a GeoJSON layer with the NUTS2 boundaries and color each region according to the colors dictionary
folium.GeoJson(
    nuts2,
    style_function=lambda feature: {
        "fillColor": colors.get(feature["properties"]["NUTS_ID"], "blue"),
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.7
    }
).add_to(m2)

# Add markers for the locations in the final_fiscrep.pickle file
df = pd.read_pickle('final_fiscrep.pickle')

rows_to_drop = [6233, 4249, 5776, 1502, 10352, 3089, 9462, 1076, 2207, 4147, 4853, 3683, 1339, 9129, 1787, 8480, 3903, 5885, 4910, 4928, 1657, 3375, 5105, 6393, 5336, 9336, 9335, 6531, 52, 2358, 300]  # List of row indices to be dropped
df = df.drop(rows_to_drop) 


for index, row in df.iterrows():
    marker_color = colors.get(row['NUTSII_code'], 'blue')
    if row['Result'] == 'PRESUM':
        marker_icon = folium.Icon(color=marker_color, icon='times', prefix='fa')
    else:
        marker_icon = folium.Icon(color=marker_color, icon='circle', prefix='fa')
    folium.CircleMarker(
        location=[row['lat_DD'], row['lon_DD']],
        radius=1,
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.7,
        popup=index
    ).add_to(m2)

# Add a layer control to the map
folium.LayerControl().add_to(m2)

# Display the map
m2.save('map_nutscolor_nocluster.html')



import pandas as pd
import geopandas as gpd
import folium

# Load the NUTS2 shapefile and convert it to EPSG 4326
nuts2 = gpd.read_file('shapefiles/NUTS_RG_20M_2021_3035.shp')
nuts2 = nuts2[(nuts2['CNTR_CODE'] == 'PT') & (nuts2['LEVL_CODE'] == 2)]
nuts2 = nuts2.to_crs(epsg=4326)

# Define the colors for each NUTS2 region
colors = {
    "PT11": "red",
    "PT15": "green",
    "PT16": "blue",
    "PT17": "pink",
    "PT18": "orange",
    "PT20": "purple",
    "PT30": "yellow"
}

# Create a Folium map centered on Portugal
m2 = folium.Map(location=[39.3999, -8.2245], zoom_start=6)

# Add a GeoJSON layer with the NUTS2 boundaries and color each region according to the colors dictionary
folium.GeoJson(
    nuts2,
    style_function=lambda feature: {
        "fillColor": colors.get(feature["properties"]["NUTS_ID"], "blue"),
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.7
    }
).add_to(m2)

# Add markers for the locations in the final_fiscrep.pickle file
df = pd.read_pickle('final_fiscrep.pickle')

rows_to_drop = [6233, 4249, 5776, 1502, 10352, 3089, 9462, 1076, 2207, 4147, 4853, 3683, 1339, 9129, 1787, 8480, 3903, 5885, 4910, 4928, 1657, 3375, 5105, 6393, 5336, 9336, 9335, 6531, 52, 2358, 300]  # List of row indices to be dropped
df = df.drop(rows_to_drop)

df_presum = df[df['Result'] == 'PRESUM']  # Filter rows with 'PRESUM' in the 'Result' column

for index, row in df_presum.iterrows():
    marker_color = colors.get(row['NUTSII_code'], 'blue')
    marker_icon = folium.Icon(color=marker_color, icon='times', prefix='fa')
    folium.CircleMarker(
        location=[row['lat_DD'], row['lon_DD']],
        radius=1,
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.7,
        popup=index
    ).add_to(m2)

# Add a layer control to the map
folium.LayerControl().add_to(m2)

# Display the map
m2.save('map_nutscolor_nocluster_infrac.html')




#HEATMAP JUST CONSIDERED THE FISCALIZATIONS THAT WERE CONSIDERED PI
import pandas as pd
import geopandas as gpd
import folium
from folium import plugins

# Load the NUTS2 shapefile and convert it to EPSG 4326
nuts2 = gpd.read_file('shapefiles/NUTS_RG_20M_2021_3035.shp')
nuts2 = nuts2[(nuts2['CNTR_CODE'] == 'PT') & (nuts2['LEVL_CODE'] == 2)]
nuts2 = nuts2.to_crs(epsg=4326)

# Define the colors for each NUTS2 region
colors = {
    "PT11": "red",
    "PT15": "green",
    "PT16": "blue",
    "PT17": "pink",
    "PT18": "orange",
    "PT20": "purple",
    "PT30": "yellow"
}

# Create a Folium map centered on Portugal
m2 = folium.Map(location=[39.3999, -8.2245], zoom_start=6)

# Add a GeoJSON layer with the NUTS2 boundaries and color each region according to the colors dictionary
folium.GeoJson(
    nuts2,
    style_function=lambda feature: {
        "fillColor": colors.get(feature["properties"]["NUTS_ID"], "blue"),
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.7
    }
).add_to(m2)

# Create a list of latitudes and longitudes from the DataFrame
locations = df_presum[['lat_DD', 'lon_DD']].values

# Create a HeatMap layer with the locations
heatmap = plugins.HeatMap(locations)

# Add the HeatMap layer to the map
heatmap.add_to(m2)

# Add a layer control to the map
folium.LayerControl().add_to(m2)

# Display the map
m2.save('HM_NUTSCOLOR_NOCLUSTER_INFRAC.html')


import pandas as pd
import geopandas as gpd
import folium
from folium import plugins

# Load the NUTS2 shapefile and convert it to EPSG 4326
nuts2 = gpd.read_file('shapefiles/NUTS_RG_20M_2021_3035.shp')
nuts2 = nuts2[(nuts2['CNTR_CODE'] == 'PT') & (nuts2['LEVL_CODE'] == 2)]
nuts2 = nuts2.to_crs(epsg=4326)

# Define the colors for each NUTS2 region
colors = {
    "PT11": "red",
    "PT15": "green",
    "PT16": "blue",
    "PT17": "pink",
    "PT18": "orange",
    "PT20": "purple",
    "PT30": "yellow"
}

# Create a Folium map centered on Portugal
m2 = folium.Map(location=[39.3999, -8.2245], zoom_start=6)

# Add a GeoJSON layer with the NUTS2 boundaries and color each region according to the colors dictionary
folium.GeoJson(
    nuts2,
    style_function=lambda feature: {
        "fillColor": colors.get(feature["properties"]["NUTS_ID"], "blue"),
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.7
    }
).add_to(m2)

# Add markers for the locations in the final_fiscrep.pickle file
df = pd.read_pickle('final_fiscrep.pickle')

rows_to_drop = [6233, 4249, 5776, 1502, 10352, 3089, 9462, 1076, 2207, 4147, 4853, 3683, 1339, 9129, 1787, 8480, 3903, 5885, 4910, 4928, 1657, 3375, 5105, 6393, 5336, 9336, 9335, 6531, 52, 2358, 300]  # List of row indices to be dropped
df = df.drop(rows_to_drop)

# Create a list of latitudes and longitudes from the DataFrame
heatmap_data = df[['lat_DD', 'lon_DD']].values

# Add the heatmap layer to the map
m2.add_child(plugins.HeatMap(heatmap_data))

# Display the map
m2.save('HM_NUTSCOLOR_NOCLUSTER.html')


