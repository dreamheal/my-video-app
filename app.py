import streamlit as st
import requests
import time

# 1. Set up a clean webpage layout
st.set_page_config(page_title="My Free AI Video App", layout="centered")
st.title("🎬 My Free AI Video Generator")
st.write("Type a prompt below to generate a short AI video clip completely for free!")

# 2. Sidebar configuration for your Fal.ai API Key
st.sidebar.header("🔑 Setup")
api_key = st.sidebar.text_input("Enter your Fal.ai API Key:", type="password")
st.sidebar.markdown("[Get a free key from Fal.ai](https://fal.ai)")

# 3. Main user input text box
prompt = st.text_input("What do you want the AI to create?", placeholder="A cute golden retriever puppy playing in the autumn leaves...")

# 4. What happens when the user clicks the button
if st.button("Generate Video ✨", type="primary"):
    if not api_key:
        st.error("⚠️ Please enter your Fal.ai API Key in the left sidebar first!")
    elif not prompt:
        st.error("⚠️ Please type a description of the video you want!")
    else:
        with st.spinner("🎬 Sending your request to the AI kitchen... Please wait..."):
            
            # Prepare the delivery request to Fal.ai
            headers = {
                "Authorization": f"Key {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "prompt": prompt,
                "seconds_total": 5
            }
            
            # Using the MiniMax video generator endpoint
            queue_url = "https://fal.run"
            response = requests.post(queue_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                request_id = response.json().get("request_id")
                status_url = f"https://fal.run/requests/{request_id}"
                
                # 5. Check the oven loop: Keep asking if the video is finished cooking
                progress_text = st.empty()
                while True:
                    status_check = requests.get(status_url, headers=headers).json()
                    status = status_check.get("status")
                    
                    if status == "COMPLETED":
                        # Try to grab the video URL from the server response
                        video_url = status_check.get("logs", {}).get("video", {}).get("url")
                        if not video_url:
                            video_url = status_check.get("video", {}).get("url")
                        
                        progress_text.empty()
                        st.success("🎉 Video successfully generated!")
                        st.video(video_url) # This automatically embeds a playable video on your site
                        break
                        
                    elif status == "FAILED":
                        progress_text.empty()
                        st.error("❌ The AI failed to generate this video. Try changing your words slightly.")
                        break
                    
                    else:
                        progress_text.info(f"⏳ Still cooking... Status: {status}. Checking again in 3 seconds...")
                    
                    time.sleep(3) # Wait 3 seconds before checking again
            else:
                st.error("❌ Error: Couldn't talk to the AI servers. Check your API key!")
