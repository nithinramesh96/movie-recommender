import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

st.set_page_config(
    page_title="What Should I Watch Tonight?",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 What Should I Watch Tonight?")
st.markdown("Get personalized movie recommendations based on your mood, time, and preferences!")

with st.form("recommendation_form"):
    st.subheader("Tell me about your situation:")
    
    mood = st.selectbox(
        "What's your mood?",
        ["Relaxed/Chill", "Excited/Energetic", "Thoughtful/Reflective", 
         "Sad/Need comfort", "Happy/Celebratory", "Stressed/Need escape",
         "Romantic", "Adventurous"]
    )
    
    time_available = st.selectbox(
        "How much time do you have?",
        ["Less than 1.5 hours", "1.5-2 hours", "2-3 hours", "More than 3 hours"],
        index=2
    )
    
    watching_with = st.selectbox(
        "Who are you watching with?",
        ["Alone", "Partner/Date", "Family (with kids)", "Family (adults only)", 
         "Friends", "Roommates"]
    )
    
    platforms = st.multiselect(
        "Which streaming platforms do you have?",
        ["Netflix", "Amazon Prime Video", "JioCinema (Hotstar)", "SonyLIV", 
         "Sun NXT", "Apple TV+", "ZEE5", "Other/Don't specify"]
    )
    
    languages = st.multiselect(
        "Language preferences?",
        ["Hindi", "Tamil", "Telugu", "Malayalam", "Kannada", "Bengali", 
         "Marathi", "Punjabi", "English", "Other Indian languages"],
        default=["Hindi", "English"]
    )
    
    genre_preferences = st.text_input(
        "Any genre preferences? (optional)",
        placeholder="e.g., thriller, comedy, romance, action..."
    )
    
    avoid = st.text_input(
        "Anything to avoid? (optional)",
        placeholder="e.g., horror, violence, sad endings..."
    )
    
    additional_context = st.text_area(
        "Any other preferences or context? (optional)",
        placeholder="e.g., My favorite actor is Vijay, I love movies from 2010s..."
    )
    
    submit_button = st.form_submit_button("Get Recommendations 🎯")

if submit_button:
    with st.spinner("Finding perfect movies for you..."):
        platforms_str = ', '.join(platforms) if platforms else 'Not specified'
        languages_str = ', '.join(languages) if languages else 'No preference'
        genre_pref = genre_preferences if genre_preferences else 'No specific preference'
        avoid_str = avoid if avoid else 'Nothing specific'
        context_str = additional_context if additional_context else 'None'
        
        prompt = (
            "You are a knowledgeable movie recommendation expert specializing in Indian cinema. "
            "INTERNAL ANALYSIS (Do this in your head, DO NOT write this): "
            "Read the Additional context and identify specific requirements. "
            "Prioritize: (1) Additional context specifics, (2) Language preferences, (3) Mood. "
            "If user mentions a favorite actor, ensure AT LEAST 2 out of 3 movies feature that actor. "
            "\n\nUser Input:\n"
            f"- Mood: {mood}\n"
            f"- Time available: {time_available}\n"
            f"- Watching with: {watching_with}\n"
            f"- Available platforms: {platforms_str}\n"
            f"- Language preferences: {languages_str}\n"
            f"- Genre preferences: {genre_pref}\n"
            f"- Things to avoid: {avoid_str}\n"
            f"- Additional context: {context_str}\n\n"
            "Guidelines:\n"
            "- Focus on Indian OTT platforms (Netflix India, Prime Video, JioCinema, SonyLIV, Sun NXT, Apple TV+, ZEE5)\n"
            "- Include Indian cinema (Bollywood, Tollywood, Kollywood, etc.) and international content\n\n"
            "CRITICAL: Use EXACTLY this format for each movie (copy this structure):\n\n"
            "Movie Title (Year)\n\n"
            "**Director:** [Name]\n\n"
            "**Cast:** [Actor 1], [Actor 2], [Actor 3]\n\n"
            "**Platform:** [Where to watch]\n\n"
            "**Plot:** [2-3 sentences summary]\n\n"
            "**Why Perfect:** [Explanation]\n\n"
            "**Runtime:** [Duration]\n\n"
            "**Match Score:** [X/10]\n\n"
            "---\n\n"
            "Provide exactly 3 movie recommendations using this exact format."
        )

        try:
            model = genai.GenerativeModel('gemini-flash-latest')
            response = model.generate_content(prompt)
            
            st.success("Here are your personalized recommendations!")
            st.markdown("---")
            
            response_text = response.text
            lines = response_text.split('\n')
            
            formatted_output = []
            for line in lines:
                if '(' in line and ')' in line and any(char.isdigit() for char in line):
                    year_match = line.find('(')
                    if year_match > 0 and len(line) < 150:
                        formatted_output.append(f"### {line}")
                    else:
                        formatted_output.append(line)
                else:
                    formatted_output.append(line)
            
            st.markdown('\n'.join(formatted_output))
            
            st.markdown("---")
            st.subheader("Was this helpful?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Yes, great picks!"):
                    st.balloons()
                    st.success("Enjoy your movie! 🍿")
            with col2:
                if st.button("👎 Not quite right"):
                    st.info("Try adjusting your preferences and search again!")
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please check your API key and try again.")

with st.sidebar:
    st.header("💡 Tips for Better Recommendations")
    st.markdown("""
    - Be specific about your mood
    - Mention if you've seen similar movies you liked
    - Include deal-breakers in the 'avoid' field
    - The more context, the better the match!
    """)
    
    st.header("📊 How it works")
    st.markdown("""
    This app uses Google's Gemini AI to understand your preferences and suggest movies that match your current situation.
    """)