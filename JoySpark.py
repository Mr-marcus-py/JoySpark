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
        "content": "🌟 **Welcome  Buddy!*\n\nI'm here to support your mental health and entertain you when needed.\n\nHow can i be of help today buddy?\n\n1. 🧠 **Mental Health Support**\n2. 🎮 **Games**\n3. 😂 **Jokes**\n4. 🤔 **Riddles**\n5. ℹ️ **Resources**"
    }]

if "game_state" not in st.session_state:
    st.session_state.game_state = {
        "current_activity": None,
        "current_joke": None,
        "current_riddle": None,
        "current_game": None,
        "gratitude_counter": 0,
        "gratitude_answers": [],
        "last_word": ""
    }

# Mental health resources
RESOURCES = {
    "Crisis Hotlines": {
        "National Suicide Prevention Lifeline (US)": "988",
        "Crisis Text Line": "Text HOME to 741741",
        "SAMHSA National Helpline": "1-800-662-HELP (4357)"
    },
    "Online Resources": {
        "Mental Health America": "https://www.mhanational.org/",
        "NAMI": "https://www.nami.org/Home",
        "7 Cups (Online Therapy)": "https://www.7cups.com/"
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

# Mental health responses
MENTAL_HEALTH_RESPONSES = {
    "greetings": [
        "Hello! How are you feeling today?",
        "Hi there! What's on your mind?",
        "Welcome back! How can I support you today?"
    ],
    "positive": [
        "That's wonderful to hear! What's bringing you joy today?",
        "I'm so glad you're feeling good! Would you like to play a game to keep the positive vibes going?",
        "Your positivity is contagious! Let me know if you'd like to chat, play a game, or hear a joke."
    ],
    "negative": [
        "I'm sorry you're feeling this way. Would you like to talk about it?",
        "That sounds difficult. Remember it's okay to feel this way. Would a breathing exercise help?",
        "I'm here to listen. You're not alone in this. Would you like to share more?"
    ],
    "neutral": [
        "I see. Is there anything specific you'd like to discuss?",
        "Thanks for sharing that. How can I best support you right now?",
        "I'm here for you. Would you like to talk, play a game, or need some resources?"
    ]
}

def get_bot_response(user_input):
    user_input = user_input.lower().strip()
    
    # Main menu navigation
    if any(word in user_input for word in ["hi", "hello", "hey", "menu", "back", "home"]):
        st.session_state.game_state["current_activity"] = None
        return "🌟 **Main Menu:**\n\n1. 🧠 **Mental Health Support**\n2. 🎮 **Games**\n3. 😂 **Jokes**\n4. 🤔 **Riddles**\n5. ℹ️ **Resources**"
    
    # Mental health section
    elif any(word in user_input for word in ["mental", "health", "support", "1", "feel"]):
        st.session_state.game_state["current_activity"] = "mental_health"
        return "🧠 **Mental Health Support**\n\nHow are you feeling today? You can share your thoughts, or we can:\n\n- Do a breathing exercise\n- Start a gratitude journal\n- Play a mindful game\n\nOr just say what's on your mind."
    
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
        return f"😂 **Joke Setup:**\n\n{joke['setup']}\n\nType 'punchline' to hear the funny part!"
    
    # Riddles section
    elif any(word in user_input for word in ["riddle", "4", "puzzle"]):
        st.session_state.game_state["current_activity"] = "riddles"
        riddle = random.choice(RIDDLES)
        st.session_state.game_state["current_riddle"] = riddle
        return f"🤔 **Riddle:**\n\n{riddle['question']}\n\nTake a guess or type 'answer' to see the solution!"
    
    # Resources section
    elif any(word in user_input for word in ["resource", "5", "help", "info"]):
        resource_text = ""
        for category, items in RESOURCES.items():
            resource_text += f"\n\n**{category}**:\n"
            resource_text += "\n".join(f"- {name}: {value}" for name, value in items.items())
        return "ℹ️ **Mental Health Resources:**\nHere are some resources that might help:" + resource_text
    
    # Handling mental health conversation
    elif st.session_state.game_state["current_activity"] == "mental_health":
        # Check for positive sentiment
        if any(word in user_input for word in ["good", "great", "happy", "awesome", "well"]):
            return random.choice(MENTAL_HEALTH_RESPONSES["positive"])
        
        # Check for negative sentiment
        elif any(word in user_input for word in ["bad", "sad", "depressed", "anxious", "stressed", "overwhelmed"]):
            return random.choice(MENTAL_HEALTH_RESPONSES["negative"])
        
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
        if any(word in user_input for word in ["punchline", "what", "why"]):
            joke = st.session_state.game_state["current_joke"]
            return f"😂 **Punchline:**\n\n{joke['punchline']}\n\nWant another joke? (yes/no)"
        elif "yes" in user_input:
            joke = random.choice(JOKES)
            st.session_state.game_state["current_joke"] = joke
            return f"😂 **Joke Setup:**\n\n{joke['setup']}\n\nType 'punchline' to hear the funny part!"
        else:
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
            return f"🤔 **New Riddle:**\n\n{new_riddle['question']}\n\nGuess or type 'answer'!"
        elif "no" in user_input:
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
    if game_name not in GAMES:
        return "I don't know that game. Please choose from the menu."
    
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
    
    else:
        return f"🎮 **{game_name}**\n\n{game['instructions']}\n\nLet's begin! (Say 'stop' to end the game)"

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
            "content": "🌟 **Welcome to  JoySpark a Mindful Companion!**\n\nI'm here to support your mental health and entertain you when needed.\n\nChoose an option:\n\n1. 🧠 **Mental Health Support**\n2. 🎮 **Games**\n3. 😂 **Jokes**\n4. 🤔 **Riddles**\n5. ℹ️ **Resources**"
        }]
        st.session_state.game_state = {
            "current_activity": None,
            "current_joke": None,
            "current_riddle": None,
            "current_game": None,
            "gratitude_counter": 0,
            "gratitude_answers": [],
            "last_word": ""
        }
        st.rerun()