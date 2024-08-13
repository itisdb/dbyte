import streamlit as st
import requests
import streamlit.components.v1 as components

# Title of the app
st.title("WebTorrent Video Streaming App")

# Input for the magnet link
magnet_link = st.text_input("Enter the magnet link:")

if magnet_link:
    video_url = f"http://localhost:3000/stream?magnet={magnet_link}"
    
    # Embed the video in the app
    video_html = f"""
    <video width="600" controls>
      <source src="{video_url}" type="video/mp4">
      Your browser does not support the video tag.
    </video>
    """
    
    components.html(video_html, height=400)
