import folium

office_lat = 35.66687568
office_lng = 139.74947495

fmap2 = folium.Map(
    location=[office_lat, office_lng], 
    zoom_start=20
)

folium.Marker([office_lat, office_lng], popup="Here it is").add_to(fmap2)
fmap2.save("1.html")




