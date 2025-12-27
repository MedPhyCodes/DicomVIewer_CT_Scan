import streamlit as st
import SimpleITK as sk
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import zipfile
import os
import io
import tempfile




@st.cache_data
def load_dicom(uploaded_file):
    tempdir = tempfile.mkdtemp()
    reader = sk.ImageSeriesReader()

    # If Uploaded file is a ZIP (Android, or manual zip)
    if uploaded_file.name.lower().endswith(".zip"):
        zip_path = os.path.join(tempdir, uploaded_file.name)
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(tempdir)
        search_path = tempdir

    # If Uploaded file is a single DICOM
    elif uploaded_file.name.lower().endswith(".dcm"):
        file_path = os.path.join(tempdir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Read directly as a 2D image
        image = sk.ReadImage(file_path)
        return sk.GetArrayFromImage(image)

  
    else:
        if os.path.isdir(uploaded_file):
            search_path = uploaded_file
        else:
            file_path = os.path.join(tempdir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            search_path = tempdir

  
    dicom_files = []
    for root, _, files in os.walk(search_path):
        for f in files:
            if f.lower().endswith(".dcm"):
                dicom_files.append(os.path.join(root, f))

    if not dicom_files:
        raise ValueError("No DICOM files found in uploaded input.")


    reader = sk.ImageSeriesReader()
    series_IDs = reader.GetGDCMSeriesIDs(search_path)
    if not series_IDs:
        raise ValueError("No DICOM series found in uploaded folder.")


    series_file_names = reader.GetGDCMSeriesFileNames(search_path, series_IDs[0])
    reader.SetFileNames(series_file_names)
    image = reader.Execute()

    return sk.GetArrayFromImage(image)






uploaded_file = st.file_uploader("Upload the CT ZIP") 
if uploaded_file is not None:
    imarray = load_dicom(uploaded_file)



    def HU_mask(ct,hu_l,hu_h):
        ct_l = np.where(((ct>=hu_l) & (ct<=hu_h)),ct,np.where(ct>hu_h,imarray.max(),imarray.min()) )
        return ct_l





    slice_number = st.slider("Slice Number: ",1,imarray.shape[0]-1,1)
    hu_low =st.slider("Lower HU value: ",imarray.min(),imarray.max(),1)
    hu_high =st.slider("Higher HU value: ",imarray.min(),imarray.max(),1)


    # #add a drop down for window level presets
    # #add a ruler tool to measure the distance between points
    # #dropdown to switch to axial/sagital/coronal view
    # #tool to measure distance








    fig=px.imshow(HU_mask(imarray[slice_number],hu_low,hu_high),color_continuous_scale="gray")
    fig.update_layout( xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False),
    coloraxis_showscale=False,
    width=1000, height=800

    )  
    st.plotly_chart(fig, use_container_width=True)






