import streamlit as st
import SimpleITK as sk
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import zipfile
import os
import io



# uploaded_file = st.file_uploader("Upload a ZIP folder", type=["zip"])
# if uploaded_file is not None:
#     with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
#         zip_ref.extractall("uploaded_folder")


@st.cache_data
def load_dicom(uploaded_file): # Extract ZIP into a temp folder 
    with zipfile.ZipFile(uploaded_file, "r") as zip_ref: zip_ref.extractall("uploaded_folder") # Read DICOM series 
    reader = sk.ImageSeriesReader() 
    series_IDs = reader.GetGDCMSeriesIDs("uploaded_folder") 
    if not series_IDs: raise ValueError("No DICOM series found in uploaded folder.") 
    series_file_names = reader.GetGDCMSeriesFileNames("uploaded_folder", series_IDs[0]) 
    reader.SetFileNames(series_file_names) 
    image = reader.Execute()
    return sk.GetArrayFromImage(image)

uploaded_file = st.file_uploader("Upload a ZIP folder", type=["zip"]) 
if uploaded_file is not None:
    imarray = load_dicom(uploaded_file)



def HU_mask(ct,hu_l,hu_h):
    ct_l = np.where(((ct>=hu_l) & (ct<=hu_h)),ct,np.where(ct>hu_h ,imarray.max(),imarray.min()) )
    return ct_l


    
    
    
    slice_number = st.slider("Slice Number: ",1,imarray.shape[0]-1,1)
    hu_low =st.slider("Lower HU value: ",imarray.min(),imarray.max(),1)
    hu_high =st.slider("Higher HU value: ",imarray.min(),imarray.max(),1)
    
    
    #add a drop down for window level presets
    #add a ruler tool to measure the distance between points
    #dropdown to switch to axial/sagital/coronal view
    #tool to measure distance
    
    
    
    
    
    
    
    
    fig=px.imshow(HU_mask(imarray[slice_number],hu_low,hu_high),color_continuous_scale="gray")
    fig.update_layout( xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False),
    coloraxis_showscale=False,
    width=1000, height=800
    
    )  
    st.plotly_chart(fig, use_container_width=True)
    
    




