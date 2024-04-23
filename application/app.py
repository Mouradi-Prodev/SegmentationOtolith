import streamlit as st

def intro():
    import streamlit as st

    st.write("# Segmentation des otolithes 2D/3D 🐟")
    st.sidebar.success("Select a demonstration above.")

    st.markdown(
        """
       Le sulcus acusticus de l'otolithe, observé à partir d'images 3D, offre une méthode prometteuse 
pour classifier les poissons par stock ou par âge. L'analyse de ces marques à partir d'images 
3D peut aider à distinguer les poissons de différents stocks ou classes d'âge, ce qui est crucial 
pour la gestion et la conservation des populations de poissons. Cependant, cette méthode 
nécessite des techniques d'imagerie avancées et une analyse rigoureuse des données, ainsi 
qu'une validation par d'autres méthodes de classification des poissons. De plus, la variabilité 
individuelle et environnementale peut également influencer les résultats de cette 
classification.    """
    )



    

def Bidimension():
    import streamlit as st
    import time
    import numpy as np

    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!
"""
    )

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


def Tridimension():
    import streamlit as st
    import open3d as o3d
    import numpy as np
    from functions import save_ply, segment_file, save_point_cloud
    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
    st.write(
        """
        Cette demonstration retourne une segmentation du plan en utilisant 
        (l'algorithme [Plane_Segmentation](https://www.open3d.org/).)

    "La segmentation des nuages de points 3D est le processus de classification des 
    nuages de points en plusieurs régions homogènes,
    les points d'une même région auront les mêmes propriétés.
    La segmentation est difficile en raison de la redondance élevée, 
    de la densité d'échantillonnage inégale et du manque de structure explicite des données de nuages de points."

"""
    )
    uploaded_file = st.file_uploader("Choisir une otolithe 3D", type=['ply'])
    if uploaded_file is not None:
        ply_path = save_ply(uploaded_file)
        inlier_cloud = segment_file(ply_path)
        st.write("filename:", uploaded_file.name)
        if inlier_cloud is not None:
            temp_file_path = save_point_cloud(inlier_cloud)
            with open(temp_file_path, "rb") as file:
                st.download_button(
                        label="Download Data",
                        data=file,
                        file_name=temp_file_path,
                    )
                
    

page_names_to_funcs = {
    "—": intro,
    "Demonstration 2D": Bidimension,
    "Demonstration 3D": Tridimension,
}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()