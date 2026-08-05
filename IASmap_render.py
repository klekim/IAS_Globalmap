import folium
import pandas as pd

# Read IAS data from CSV
df = pd.read_csv("IAS_Worldwide.csv")

# FIXED SUMMARY
print("=== IAS Institutes Summary by NetIAS ===")

# IASsummary
netias_members = df['NetIAS'].astype(str).str.contains('yes|true', case=False, na=False).sum()
total_institutes = len(df)
netias_members_percent = int(netias_members*100/total_institutes) 

# Create legend HTML directly with counts
m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")

legend_content = f'''
<b><span style="color:black">IAS Global Network</b><br>
<span style="color:red">_★_</span><b>NetIAS Members ({netias_members:,} - {netias_members_percent}%)</span><br>
<span style="color:blue">_★_</span><b>Other Institutes ({total_institutes - netias_members:,} - {100-netias_members_percent}%)</span><br>
<b><span style="color:black">Total IAS: {total_institutes:,}</span><br>
<i>The statistics based on the number of IAS shown on this map</span></br>
'''

legend_html = f'''
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 440px; height: 130px; 
     background-color: white; border:2px solid grey; z-index:9999; 
     font-size:14px; padding: 12px; border-radius: 6px; box-shadow: 2px 2px 10px rgba(0,0,0,0.3);">
{legend_content}
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

print(f"NetIAS members: {netias_members}, Others: {total_institutes - netias_members}")

# SINGLE LOOP with color logic INSIDE
for _, row in df.iterrows():
    # Skip if coordinates missing
    if pd.isna(row["Latitude"]) or pd.isna(row["Longitude"]):
        continue
    
    # COLOR HIGHLIGHTING WORKS HERE
    if "yes" in str(row["NetIAS"]):
        icon_color = "red"      # HWK = RED 
        icon_icon = "star"      # Star icon
    else:
        icon_color = "blue"     # Others = BLUE
        icon_icon = "star"
    
    # Clickable website popup
    html = f'<a href="https://{row["Website"]}" target="_blank"><b>{row["Name"]}</b></a><br>{row["City"]}, {row["Country"]}'
    iframe = folium.IFrame(html, width=220, height=80)
    popup = folium.Popup(iframe, max_width=220)
   
    
    # USE THE COLOR & ICON HERE
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=popup,
        tooltip=row["Name"],
        icon=folium.Icon(color=icon_color, icon=icon_icon)  # ← THIS WAS MISSING
    ).add_to(m)

m.save("IAS_Global_Map.html")
