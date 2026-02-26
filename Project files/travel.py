import streamlit as st
import google.generativeai as genai
import os

# --- 1. INITIALIZATION & CONFIGURATION ---
# Replace 'YOUR_API_KEY' with your actual Gemini API Key from Google AI Studio
# In production, use st.secrets or environment variables
API_KEY = "AIzaSyCpMhjAt2VlxGOFqSOhaNWS2T5SRY0TZQI" 
genai.configure(api_key=API_KEY)

def generate_itinerary(destination, days, nights):
    """
    Interfaces with Gemini Pro to generate a travel plan.
    """
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        # Engineering the Prompt for high-quality output
        prompt = f"""
        You are an expert world-travel guide. 
        Create a detailed, day-wise travel itinerary for a trip to {destination}.
        Duration: {days} days and {nights} nights.
        
        Please include:
        1. A catchy title for the trip.
        2. Morning, Afternoon, and Evening activities for each day.
        3. Local dining suggestions (famous dishes or spots).
        4. Important travel tips (weather, transport, or etiquette).
        5. Use Markdown formatting with bold headings and bullet points.
        """
        
        # Generate content
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"

# --- 2. STREAMLIT UI SETUP ---
def main():
    st.set_page_config(page_title="TravelGuideAI", page_icon="✈️")
    
    st.title("🌍 Travel Itinerary Generator")
    st.markdown("Explore with AI: Custom Itineraries for Your Next Journey")

    # Sidebar for additional settings (Expert Tip: Improves UX)
    with st.sidebar:
        st.header("Settings")
        st.info("This app uses Gemini Pro to craft personalized travel plans.")

    # User Inputs
    col1, col2 = st.columns(2)
    
    with col1:
        destination = st.text_input("Enter your desired destination:", placeholder="e.g. Kedarnath, Paris, Tokyo")
    
    with col2:
        days = st.number_input("Number of days:", min_value=1, max_value=30, value=1)
        nights = st.number_input("Number of nights:", min_value=0, max_value=30, value=0)

    # Logic Execution
    if st.button("Generate Itinerary"):
        if destination.strip():
            with st.spinner(f"Mapping out your trip to {destination}..."):
                itinerary = generate_itinerary(destination, days, nights)
                
                st.subheader("Your Personalized Plan")
                # Using st.markdown instead of text_area for better readability
                st.markdown(itinerary)
                
                # Add a download button for the user
                st.download_button(
                    label="Download Itinerary as Text",
                    data=itinerary,
                    file_name=f"Itinerary_{destination}.txt",
                    mime="text/plain"
                )
        else:
            st.error("Please enter a destination to proceed.")

if __name__ == "__main__":
    main()