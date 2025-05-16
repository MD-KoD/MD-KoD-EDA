import math
import folium
from get_df import get_information_df
from sklearn.cluster import KMeans
from collections import Counter
import os

def create_jeju_map(n_clusters=10):
    df = get_information_df()

    if not os.path.exists('map'):
        os.makedirs('map')

    color_dict = {
        "1_상위 10% 이하": "blue",
        "2_10~25%": "lightblue",
        "3_25~50%": "yellow",
        "4_50~75%": "orange",
        "5_75~90%": "orangered",
        "6_90% 초과": "red"
    }

    X = df[['Latitude', 'Longitude']].values

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['Cluster'] = kmeans.fit_predict(X)

    cluster_colors = {}
    for cluster in range(n_clusters):
        cluster_data = df[df['Cluster'] == cluster]
        most_common_group = Counter(cluster_data['UE_CNT_GRP']).most_common(1)[0][0]
        cluster_colors[cluster] = color_dict[most_common_group]

    center_lat = df['Latitude'].mean()
    center_lon = df['Longitude'].mean()

    m = folium.Map(location=[center_lat, center_lon], 
                   zoom_start=11)

    legend_html = '''
    <p>각 매출별 가게 비율은 모두 동일하다고 가정.</p>
    <div style="position: fixed; 
                bottom: 50px; right: 50px; 
                border:2px solid grey; z-index:9999; 
                background-color:white;
                padding: 10px;
                font-size:14px;">
    '''

    for group, color in color_dict.items():
        legend_html += f'<p><i class="fa fa-circle fa-1x" style="color:{color}"></i> {group}</p>'
    legend_html += '</div>'
    m.get_root().html.add_child(folium.Element(legend_html))

    cluster_centers = kmeans.cluster_centers_
    base_radius = 600 * ((320/(math.log(n_clusters, 2))) * 1.2) #### 적당한 값 찾는 거 왤케 어렵나요
    
    for i, center in enumerate(cluster_centers):
        folium.Circle(
            location=[center[0], center[1]],
            popup=f'Cluster {i}',
            tooltip=f'Cluster {i}',
            color=cluster_colors[i],
            fill=True,
            fill_color=cluster_colors[i],
            fill_opacity=0.8,
            radius=base_radius,
            weight=0
        ).add_to(m)

    m.save(f'map/jeju_map_{n_clusters}.html')
    
    return m

if __name__ == "__main__":
    create_jeju_map(n_clusters=10)
    create_jeju_map(n_clusters=20)
    create_jeju_map(n_clusters=40)
    create_jeju_map(n_clusters=80)
    create_jeju_map(n_clusters=160)
    create_jeju_map(n_clusters=320)
    create_jeju_map(n_clusters=640)
    create_jeju_map(n_clusters=1280)
    create_jeju_map(n_clusters=2560)
