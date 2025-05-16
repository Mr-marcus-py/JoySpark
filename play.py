import streamlit as st
import random
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="JoySpark",
    page_icon="🧠",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "🌟 **Welcome Buddy!**\n\nI'm here to support your mental health and entertain you when needed.\n\nHow can I be of help today buddy?\n\n1. 🧠 **Mental Health Support**\n2. 🎮 **Games**\n3. 😂 **Jokes**\n4. 🤔 **Riddles**\n5. ℹ️ **Resources**"
    }]

if "game_state" not in st.session_state:
    st.session_state.game_state = {
        "current_activity": None,
        "current_joke": None,
        "current_riddle": None,
        "current_game": None,
        "gratitude_counter": 0,
        "gratitude_answers": [],
        "last_word": "",
        "mood_ratings": []
    }

# Enhanced Mental Health Resources
RESOURCES = {
    "Crisis Hotlines": {
        "National Suicide Prevention Lifeline (US)": "988",
        "Crisis Text Line": "Text HOME to 741741",
        "Veterans Crisis Line": "1-800-273-8255, press 1",
        "Trevor Project (LGBTQ+)": "1-866-488-7386",
        "Disaster Distress Helpline": "1-800-985-5990",
        "SAMHSA National Helpline": "1-800-662-HELP (4357)"
    },
    "Online Resources": {
        "Mental Health America Screening Tools": "https://screening.mhanational.org/",
        "NAMI Support Groups": "https://www.nami.org/Support-Education/Support-Groups",
        "7 Cups (Free Online Therapy)": "https://www.7cups.com/",
        "Headspace (Meditation App)": "https://www.headspace.com/",
        "Calm (Meditation App)": "https://www.calm.com/",
        "Mental Health America": "https://www.mhanational.org/",
        "NAMI": "https://www.nami.org/Home"
    },
    "Self-Help Tools": {
        "CBT Thought Record Worksheet": "https://www.therapistaid.com/worksheets/cbt-thought-record",
        "DBT Distress Tolerance Skills": "https://dialecticalbehaviortherapy.com/distress-tolerance/",
        "Mindfulness Exercises": "https://positivepsychology.com/mindfulness-exercises-techniques-activities/"
    }
}

# Enhanced Mental Health Responses with more nuanced support
MENTAL_HEALTH_RESPONSES = {
    "greetings": [
        "Hello! I'm here to listen. How are you feeling today?",
        "Hi there! Your mental health matters. What's on your mind?",
        "Welcome back! I'm here to support you. How can I help today?"
    ],
    "positive": [
        "That's wonderful to hear! Would you like to explore what's contributing to these positive feelings?",
        "I'm so glad you're feeling good! Research shows savoring positive moments can boost wellbeing. Want to reflect on what made this moment positive?",
        "Your positivity is contagious! Would you like to capture this moment in a gratitude journal?"
    ],
    "negative": {
        "depression": [
            "I hear you're feeling down. Depression can feel heavy, but you're not alone in this. Would you like to try a grounding exercise?",
            "That sounds really hard. When depression feels overwhelming, small steps matter. Would a self-care suggestion help?",
            "I'm sorry you're feeling this way. Remember depression lies - you matter more than you feel right now."
        ],
        "anxiety": [
            "Anxiety can feel overwhelming. Let's try the 5-4-3-2-1 grounding technique: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.",
            "I hear your anxiety. Remember this will pass. Would a breathing exercise help right now?",
            "Anxiety can make everything feel urgent. Let's pause together - you're safe in this moment."
        ],
        "stress": [
            "Stress can feel overwhelming. Let's break things down - what's one small thing that might help right now?",
            "I hear you're feeling stressed. The body keeps score - would a quick body scan meditation help?",
            "Stress often comes from feeling out of control. What's one thing within your control right now?"
        ],
        "general": [
            "I'm sorry you're feeling this way. Would you like to talk more about what's going on?",
            "That sounds really difficult. You're showing strength by reaching out. How can I best support you right now?",
            "I'm here to listen without judgment. Whatever you're feeling is valid."
        ]
    },
    "neutral": [
        "Thanks for sharing that. Would you like to explore this feeling more deeply?",
        "I hear you. Sometimes just naming our feelings helps. Would any resources be helpful right now?",
        "I'm here for whatever you need - whether that's support, distraction, or just someone to listen."
    ],
    "coping_skills": {
        "quick": [
            "Try the 5-4-3-2-1 grounding technique: Notice 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste",
            "Box breathing: Inhale 4 sec, hold 4 sec, exhale 6 sec, repeat 5 times",
            "Place both feet flat on the ground and notice the support beneath you"
        ],
        "long_term": [
            "Consider keeping a mood journal to track patterns and triggers",
            "Research shows regular exercise can be as effective as medication for mild-moderate depression",
            "Practicing daily gratitude has been shown to increase happiness over time"
        ]
    }
}

# New Mental Health Activities
MENTAL_HEALTH_ACTIVITIES = {
    "Mood Tracker": {
        "description": "Track your mood patterns over time",
        "instructions": "Rate your mood from 1-10 each day and note any patterns"
    },
    "Thought Challenger": {
        "description": "Challenge negative thoughts using CBT techniques",
        "steps": [
            "Identify the troubling thought",
            "Examine evidence for and against it",
            "Consider alternative perspectives",
            "Develop a more balanced thought"
        ]
    },
    "Self-Compassion Break": {
        "description": "Practice kindness toward yourself in difficult moments",
        "steps": [
            "Acknowledge your pain: 'This is hard right now'",
            "Remember you're not alone: 'Others feel this way too'",
            "Offer yourself kindness: 'May I be gentle with myself'"
        ]
    }
}

# Enhanced game database
GAMES = {
    "Mindful Breathing": {
        "description": "Guided breathing exercise to help you relax",
        "steps": [
            "Find a comfortable position, sitting or lying down",
            "Close your eyes if you feel comfortable doing so",
            "Breathe in slowly through your nose for 4 seconds",
            "Hold your breath for 4 seconds",
            "Exhale slowly through your mouth for 6 seconds",
            "Repeat this cycle 5 times",
            "Notice how your body feels after this exercise"
        ]
    },
    "Gratitude Journal": {
        "description": "List things you're grateful for to boost positivity",
        "prompts": [
            "Name one person you're grateful for and why",
            "What's one positive experience you had recently?",
            "What's something in nature you appreciate?",
            "What's a personal strength you're thankful for?",
            "What's a simple pleasure that made you smile today?"
        ]
    },
    "Word Association": {
        "description": "Free association game to get thoughts flowing",
        "instructions": "I'll say a word, you respond with the first word that comes to mind"
    },
    "20 Questions": {
        "description": "I'll think of something and you ask yes/no questions to guess it",
        "instructions": "Ask questions like 'Is it an animal?' or 'Can it fly?'"
    },
    "Would You Rather": {
        "description": "Choose between two funny or challenging scenarios",
        "instructions": "Pick option A or B when presented with choices"
    },
    "True or False": {
        "description": "I'll give statements and you decide if they're true or false",
        "instructions": "Respond with 'true' or 'false' to each statement"
    },
    "This or That": {
        "description": "Pick your preference between two options",
        "instructions": "Choose between things like 'Pizza or Burgers?'"
    },
    "Two Truths and a Lie": {
        "description": "Guess which of three statements is false",
        "instructions": "Pick 1, 2, or 3 for which one you think is the lie"
    }
}

# Enhanced joke database (setup/punchline format)
JOKES = [
    {"setup": "Why don't skeletons fight each other?", "punchline": "They don't have the guts!"},
    {"setup": "What do you call a fake noodle?", "punchline": "An impasta!"},
    {"setup": "How do you organize a space party?", "punchline": "You planet!"},
    {"setup": "Why did the scarecrow win an award?", "punchline": "Because he was outstanding in his field!"},
    {"setup": "What do you call a bear with no teeth?", "punchline": "A gummy bear!"},
    {"setup": "Why can't you trust an atom?", "punchline": "Because they make up everything!"},
    {"setup": "What's orange and sounds like a parrot?", "punchline": "A carrot!"},
    {"setup": "Why did the math book look sad?", "punchline": "It had too many problems."},
    {"setup": "What's brown and sticky?", "punchline": "A stick!"},
    {"setup": "Why did the golfer bring two pairs of pants?", "punchline": "In case he got a hole in one!"}
]

# Enhanced riddle database
RIDDLES = [
    {"question": "What has keys but can't open locks?", "answer": "piano"},
    {"question": "What gets wetter as it dries?", "answer": "towel"},
    {"question": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "answer": "echo"},
    {"question": "The more you take, the more you leave behind. What am I?", "answer": "footsteps"},
    {"question": "What has a head, a tail, is brown, and has no legs?", "answer": "penny"},
    {"question": "What is always in front of you but can't be seen?", "answer": "future"},
    {"question": "What can you break without touching it?", "answer": "promise"},
    {"question": "What gets bigger the more you take away?", "answer": "hole"},
    {"question": "What has a face and two hands but no arms or legs?", "answer": "clock"},
    {"question": "What can you hold in your right hand but not in your left?", "answer": "your left elbow"}
]

# Greeting responses
GREETING_RESPONSES = {
    "hello": [
        "Hello there! How can I help you today?",
        "Hi! I'm JoySpark, your mental health companion. What would you like to do?",
        "Hey! Ready for some fun or support today?"
    ],
    "name": [
        "I'm JoySpark, your friendly mental health companion!",
        "You can call me JoySpark - here to support and entertain you!",
        "My name is JoySpark, and I'm here to help you with mental health and fun activities!"
    ],
    "how_are_you": [
        "I'm just a bot, but I'm always here and ready to help you! How about you?",
        "I don't have feelings, but I'm functioning perfectly to support you! How are you feeling?",
        "As an AI, I don't experience emotions, but I'm here to help with yours. How can I assist you today?"
    ],
    "thanks": [
        "You're very welcome! I'm happy to help.",
        "No problem at all! Let me know if you need anything else.",
        "Glad I could assist! What else can I do for you today?"
    ]
}

def get_bot_response(user_input):
    user_input = user_input.lower().strip()
    
    # Handle basic greetings and small talk
    if any(word in user_input for word in ["hi", "hello", "hey"]):
        return random.choice(GREETING_RESPONSES["hello"])
    
    if any(word in user_input for word in ["your name", "who are you", "what are you"]):
        return random.choice(GREETING_RESPONSES["name"])
    
    if any(word in user_input for word in ["how are you", "how you doing"]):
        return random.choice(GREETING_RESPONSES["how_are_you"])
    
    if any(word in user_input for word in ["thank", "thanks", "appreciate"]):
        return random.choice(GREETING_RESPONSES["thanks"])
    
    # Main menu navigation
    if any(word in user_input for word in ["menu", "back", "home", "main"]):
        st.session_state.game_state["current_activity"] = None
        st.session_state.game_state["current_game"] = None
        return "🌟 **Main Menu:**\n\n1. 🧠 **Mental Health Support**\n2. 🎮 **Games**\n3. 😂 **Jokes**\n4. 🤔 **Riddles**\n5. ℹ️ **Resources**"
    
    # Mental health section
    elif any(word in user_input for word in ["mental", "health", "support", "1", "feel"]):
        st.session_state.game_state["current_activity"] = "mental_health"
        return "🧠 **Mental Health Support**\n\nHow are you feeling today? You can share your thoughts, or we can:\n\n- Track your mood\n- Challenge negative thoughts\n- Practice self-compassion\n- Try a breathing exercise\n- Start a gratitude journal\n\nOr just say what's on your mind."
    
    # Games section
    elif any(word in user_input for word in ["game", "2", "play"]):
        st.session_state.game_state["current_activity"] = "games"
        game_list = "\n".join([f"{num}. {game} - {GAMES[game]['description']}" 
                             for num, game in enumerate(GAMES.keys(), 1)])
        return f"🎮 **Available Games:**\n\n{game_list}\n\nType the number of the game you want to play!"
    
    # Jokes section
    elif any(word in user_input for word in ["joke", "3", "laugh"]):
        st.session_state.game_state["current_activity"] = "jokes"
        joke = random.choice(JOKES)
        st.session_state.game_state["current_joke"] = joke
        return f"😂 **Joke:**\n\n{joke['setup']}"
    
    # Riddles section
    elif any(word in user_input for word in ["riddle", "4", "puzzle"]):
        st.session_state.game_state["current_activity"] = "riddles"
        riddle = random.choice(RIDDLES)
        st.session_state.game_state["current_riddle"] = riddle
        return f"🤔 **Riddle:**\n\n{riddle['question']}"
    
    # Resources section
    elif any(word in user_input for word in ["resource", "5", "help", "info"]):
        resource_text = ""
        for category, items in RESOURCES.items():
            resource_text += f"\n\n**{category}**:\n"
            resource_text += "\n".join(f"- {name}: {value}" for name, value in items.items())
        return "ℹ️ **Mental Health Resources:**\nHere are some resources that might help:" + resource_text
    
    # Handling mental health conversation
    elif st.session_state.game_state["current_activity"] == "mental_health":
        # Sentiment analysis with more nuance
        if any(word in user_input for word in ["good", "great", "happy", "awesome", "well"]):
            return random.choice(MENTAL_HEALTH_RESPONSES["positive"])
        
        elif any(word in user_input for word in ["bad", "sad", "depressed", "down", "low"]):
            return random.choice(MENTAL_HEALTH_RESPONSES["negative"]["depression"])
            
        elif any(word in user_input for word in ["anxious", "panic", "nervous", "worried"]):
            return random.choice(MENTAL_HEALTH_RESPONSES["negative"]["anxiety"])
            
        elif any(word in user_input for word in ["stress", "overwhelmed", "pressure"]):
            return random.choice(MENTAL_HEALTH_RESPONSES["negative"]["stress"])
            
        elif any(word in user_input for word in ["help", "cope", "skill"]):
            skill = random.choice(MENTAL_HEALTH_RESPONSES["coping_skills"]["quick"] + 
                                MENTAL_HEALTH_RESPONSES["coping_skills"]["long_term"])
            return f"Here's a coping skill to try:\n\n{skill}\n\nWould you like another?"
        
        # Enhanced activity options
        elif "track" in user_input or "mood" in user_input:
            st.session_state.game_state["current_game"] = "Mood Tracker"
            return handle_game("Mood Tracker")
            
        elif "thought" in user_input or "cbt" in user_input:
            st.session_state.game_state["current_game"] = "Thought Challenger"
            return handle_game("Thought Challenger")
            
        elif "compassion" in user_input or "kind" in user_input:
            st.session_state.game_state["current_game"] = "Self-Compassion Break"
            return handle_game("Self-Compassion Break")
            
        # Check for breathing exercise
        elif "breath" in user_input or "breathe" in user_input:
            st.session_state.game_state["current_game"] = "Mindful Breathing"
            return handle_game("Mindful Breathing")
        
        # Check for gratitude journal
        elif "gratitude" in user_input or "thankful" in user_input:
            st.session_state.game_state["current_game"] = "Gratitude Journal"
            return handle_game("Gratitude Journal")
        
        # Default mental health response
        else:
            return random.choice(MENTAL_HEALTH_RESPONSES["neutral"])
    
    # Handling jokes
    elif st.session_state.game_state["current_activity"] == "jokes":
        if any(word in user_input for word in ["punchline", "what", "why", "tell me", "answer"]):
            joke = st.session_state.game_state["current_joke"]
            return f"😂 **Punchline:**\n\n{joke['punchline']}\n\nWant another joke? (yes/no)"
        elif "yes" in user_input:
            joke = random.choice(JOKES)
            st.session_state.game_state["current_joke"] = joke
            return f"😂 **Joke:**\n\n{joke['setup']}"
        else:
            st.session_state.game_state["current_activity"] = None
            return "🌟 **Main Menu:**\n\n1. 🧠 **Mental Health Support**\n2. 🎮 **Games**\n3. 😂 **Jokes**\n4. 🤔 **Riddles**\n5. ℹ️ **Resources**"
    
    # Handling riddles
    elif st.session_state.game_state["current_activity"] == "riddles":
        riddle = st.session_state.game_state["current_riddle"]
        
        if "answer" in user_input:
            return f"✅ **Answer:** {riddle['answer']}\n\nWant another riddle? (yes/no)"
        elif user_input == riddle['answer'].lower():
            return f"🎉 **Correct!** The answer is {riddle['answer']}!\n\nWant another riddle? (yes/no)"
        elif "yes" in user_input:
            new_riddle = random.choice(RIDDLES)
            st.session_state.game_state["current_riddle"] = new_riddle
            return f"🤔 **New Riddle:**\n\n{new_riddle['question']}"
        elif "no" in user_input:
            st.session_state.game_state["current_activity"] = None
            return "🌟 **Main Menu:**\n\n1. 🧠 **Mental Health Support**\n2. 🎮 **Games**\n3. 😂 **Jokes**\n4. 🤔 **Riddles**\n5. ℹ️ **Resources**"
        else:
            return "🤔 Not quite right! Try again or type 'answer' to see the solution."
    
    # Handling game selection and play
    elif st.session_state.game_state["current_activity"] == "games":
        # If a game is already selected
        if st.session_state.game_state["current_game"]:
            return continue_game(user_input)
        
        # Selecting a game
        if user_input.isdigit() and 1 <= int(user_input) <= len(GAMES):
            game_name = list(GAMES.keys())[int(user_input)-1]
            st.session_state.game_state["current_game"] = game_name
            return f"🎮 **{game_name}**\n\n{GAMES[game_name]['instructions']}\n\nType 'start' to begin or 'menu' to go back."
        elif "start" in user_input and st.session_state.game_state["current_game"]:
            return handle_game(st.session_state.game_state["current_game"])
        else:
            return f"Please choose a game by number (1-{len(GAMES)}) or say 'menu'."
    
    # Default response
    else:
        return "🌟 **Main Menu:**\n\n1. 🧠 **Mental Health Support**\n2. 🎮 **Games**\n3. 😂 **Jokes**\n4. 🤔 **Riddles**\n5. ℹ️ **Resources**"

def handle_game(game_name):
    """Start a new game"""
    if game_name in GAMES:
        game = GAMES[game_name]
        st.session_state.game_state["current_game"] = game_name
        
        if game_name == "Mindful Breathing":
            response = "🧘‍♀️ **Mindful Breathing Exercise**\n\n" + game["description"] + "\n\n" + "\n".join(game["steps"])
            return response + "\n\nHow did that feel for you?"
        
        elif game_name == "Gratitude Journal":
            if "gratitude_counter" not in st.session_state.game_state:
                st.session_state.game_state["gratitude_counter"] = 0
                st.session_state.game_state["gratitude_answers"] = []
            
            counter = st.session_state.game_state["gratitude_counter"]
            if counter < len(game["prompts"]):
                return "📝 **Gratitude Journal**\n\n" + game["prompts"][counter] + "\n\n(Type your response)"
            else:
                st.session_state.game_state["current_game"] = None
                answers = "\n".join(f"- {a}" for a in st.session_state.game_state["gratitude_answers"])
                return f"📝 **Your Gratitude Journal:**\n\n{answers}\n\nPracticing gratitude can improve your mood! Want to do another round?"
        
        elif game_name == "Word Association":
            st.session_state.game_state["last_word"] = random.choice(["happy", "sun", "blue", "peace", "friend"])
            return "💭 **Word Association Game**\n\n" + game["instructions"] + f"\n\nI'll start: {st.session_state.game_state['last_word']}"
        
        elif game_name == "Mood Tracker":
            return ("📊 **Mood Tracker**\n\n"
                   "Rate your current mood from 1 (very low) to 10 (very high):")
                   
        elif game_name == "Thought Challenger":
            return ("💭 **Thought Challenger**\n\n"
                   "What negative thought would you like to examine?")
                   
        elif game_name == "Self-Compassion Break":
            return ("💖 **Self-Compassion Break**\n\n"
                   "Let's practice kindness toward ourselves. What difficulty are you facing?")
        
        else:
            return f"🎮 **{game_name}**\n\n{game['instructions']}\n\nLet's begin! (Say 'stop' to end the game)"
    elif game_name in MENTAL_HEALTH_ACTIVITIES:
        activity = MENTAL_HEALTH_ACTIVITIES[game_name]
        st.session_state.game_state["current_game"] = game_name
        
        if game_name == "Mood Tracker":
            return ("📊 **Mood Tracker**\n\n"
                   "Rate your current mood from 1 (very low) to 10 (very high):")
                   
        elif game_name == "Thought Challenger":
            return ("💭 **Thought Challenger**\n\n"
                   "What negative thought would you like to examine?")
                   
        elif game_name == "Self-Compassion Break":
            return ("💖 **Self-Compassion Break**\n\n"
                   "Let's practice kindness toward ourselves. What difficulty are you facing?")
    else:
        return "I don't know that game. Please choose from the menu."

def continue_game(user_input):
    """Continue the current game"""
    game_name = st.session_state.game_state["current_game"]
    
    if user_input == "stop":
        st.session_state.game_state["current_game"] = None
        return "Game stopped. What would you like to do now?"
    
    if game_name == "Gratitude Journal":
        counter = st.session_state.game_state["gratitude_counter"]
        st.session_state.game_state["gratitude_answers"].append(user_input)
        st.session_state.game_state["gratitude_counter"] += 1
        
        if counter + 1 < len(GAMES["Gratitude Journal"]["prompts"]):
            return GAMES["Gratitude Journal"]["prompts"][counter + 1]
        else:
            st.session_state.game_state["current_game"] = None
            answers = "\n".join(f"- {a}" for a in st.session_state.game_state["gratitude_answers"])
            return f"📝 **Your Gratitude Journal:**\n\n{answers}\n\nPracticing gratitude can improve your mood! Want to do another round?"
    
    elif game_name == "Word Association":
        new_word = random.choice(["happy", "sun", "blue", "peace", "friend", "love", "calm", "tree", "water", "smile"])
        st.session_state.game_state["last_word"] = new_word
        return f"💭 {new_word}\n\nYour turn! Or say 'stop' to end the game."
    
    elif game_name == "Mood Tracker":
        if user_input.isdigit() and 1 <= int(user_input) <= 10:
            st.session_state.game_state["mood_ratings"].append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "rating": int(user_input)
            })
            return ("Thank you! Over time we can spot patterns.\n"
                   "Would you like to:\n"
                   "1. Add a note about today's mood\n"
                   "2. See your mood history\n"
                   "3. Return to menu")
        else:
            return "Please enter a number between 1 and 10."
    
    elif game_name == "Thought Challenger":
        # Add CBT thought challenging logic
        return "Let's examine the evidence for this thought..."
    
    elif game_name == "Self-Compassion Break":
        return "That sounds difficult. Remember to be kind to yourself. Would you like to try another self-compassion exercise?"
    
    elif game_name == "20 Questions":
        return "20 Questions game logic would go here"
    
    # Add more game continuations as needed
    
    return "I'm not sure what game we're playing. Let's go back to the menu."

# Custom CSS for better appearance
st.markdown("""
<style>
    .stChatMessage {
        padding: 12px;
        border-radius: 15px;
        margin-bottom: 15px;
    }
    [data-testid="stChatMessageContent"] {
        font-size: 16px;
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
        padding: 12px;
    }
    .stButton>button {
        border-radius: 20px;
        padding: 10px 20px;
        background-color: #4CAF50;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Bot response
    with st.spinner("🤖 Thinking..."):
        response = get_bot_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# Sidebar with quick actions
with st.sidebar:
    st.title("JoySpark")
    st.markdown("### Quick Actions:")
    
    if st.button("🧠 Mental Health Check-in"):
        st.session_state.messages.append({"role": "user", "content": "mental health"})
        st.session_state.messages.append({"role": "assistant", "content": get_bot_response("mental health")})
        st.rerun()
    
    if st.button("🎮 Play a Game"):
        st.session_state.messages.append({"role": "user", "content": "games"})
        st.session_state.messages.append({"role": "assistant", "content": get_bot_response("games")})
        st.rerun()
    
    if st.button("😂 Tell Me a Joke"):
        st.session_state.messages.append({"role": "user", "content": "joke"})
        st.session_state.messages.append({"role": "assistant", "content": get_bot_response("joke")})
        st.rerun()
    
    if st.button("🤔 Give Me a Riddle"):
        st.session_state.messages.append({"role": "user", "content": "riddle"})
        st.session_state.messages.append({"role": "assistant", "content": get_bot_response("riddle")})
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Mental Health Resources**")
    for category, items in RESOURCES.items():
        with st.expander(category):
            for name, value in items.items():
                st.markdown(f"**{name}**: {value}")
    
    st.markdown("---")
    if st.button("🔄 Reset Conversation"):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "🌟 **Welcome to JoySpark, a Mindful Companion!**\n\nI'm here to support your mental health and entertain you when needed.\n\nChoose an option:\n\n1. 🧠 **Mental Health Support**\n2. 🎮 **Games**\n3. 😂 **Jokes**\n4. 🤔 **Riddles**\n5. ℹ️ **Resources**"
        }]
        st.session_state.game_state = {
            "current_activity": None,
            "current_joke": None,
            "current_riddle": None,
            "current_game": None,
            "gratitude_counter": 0,
            "gratitude_answers": [],
            "last_word": "",
            "mood_ratings": []
        }
        st.rerun()