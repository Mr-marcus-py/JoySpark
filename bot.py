import streamlit as st
import random
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Boredom Buster Bot",
    page_icon="🤖",
    layout="centered"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "🌟 **Hi! I'm your Boredom Buster Bot!**\n\nChoose an option:\n\n1. 🎮 **Games**\n2. 😂 **Jokes**\n3. 🤔 **Riddles**"
    }]

# Game database
GAMES = {
    " 20 Questions": {
        "description": "I'll think of something and you ask yes/no questions to guess it",
        "instructions": "Ask questions like 'Is it an animal?' or 'Can it fly?'"
    },
    " Would You Rather": {
        "description": "Choose between two funny or challenging scenarios",
        "instructions": "Pick option A or B when presented with choices"
    },
    " True or False": {
        "description": "I'll give statements and you decide if they're true or false",
        "instructions": "Respond with 'true' or 'false' to each statement"
    },
    " This or That": {
        "description": "Pick your preference between two options",
        "instructions": "Choose between things like 'Pizza or Burgers?'"
    },
    " Hangman": {
        "description": "Guess letters to uncover a hidden word",
        "instructions": "Suggest letters one at a time"
    },
    " Two Truths and a Lie": {
        "description": "Guess which of three statements is false",
        "instructions": "Pick 1, 2, or 3 for which one you think is the lie"
    },
    " Name That Tune": {
        "description": "Guess songs from short clues",
        "instructions": "Type the name of the song you think it is"
    },
    " Odd One Out": {
        "description": "Find which item doesn't belong in a group",
        "instructions": "Type the number of the odd one out"
    },
    " Charades": {
        "description": "I'll describe something for you to guess",
        "instructions": "Type what you think I'm describing"
    }
}

# Joke database (setup/punchline format)
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
    {"setup": "Why did the golfer bring two pairs of pants?", "punchline": "In case he got a hole in one!"},
    {"setup": "What do you call cheese that isn't yours?", "punchline": "Nacho cheese!"},
    {"setup": "Why did the tomato turn red?", "punchline": "Because it saw the salad dressing!"},
    {"setup": "What's the best thing about Switzerland?", "punchline": "I don't know, but the flag is a big plus!"},
    {"setup": "How do you make a tissue dance?", "punchline": "Put a little boogie in it!"},
    {"setup": "Why don't eggs tell jokes?", "punchline": "They'd crack each other up!"},
    {"setup": "What's the difference between a poorly dressed man on a trampoline and a well-dressed man on a trampoline?", "punchline": "Attire!"},
    {"setup": "Why did the bicycle fall over?", "punchline": "Because it was two-tired!"},
    {"setup": "What's a vampire's favorite fruit?", "punchline": "A blood orange!"},
    {"setup": "Why don't scientists trust atoms?", "punchline": "Because they make up everything!"},
    {"setup": "What did one wall say to the other wall?", "punchline": "I'll meet you at the corner!"}
]

# Riddle database
RIDDLES = [
    {"question": "What has keys but can't open locks?", "answer": "piano"},
    {"question": "What gets wetter as it dries?", "answer": "towel"},
    {"question": "What has to be broken before you can use it?", "answer": "egg"},
    {"question": "I'm light as a feather, yet the strongest person can't hold me for long. What am I?", "answer": "breath"},
    {"question": "What can travel around the world while staying in a corner?", "answer": "stamp"},
    {"question": "What has a head, a tail, but no body?", "answer": "coin"},
    {"question": "What has many teeth but can't bite?", "answer": "comb"},
    {"question": "What goes up but never comes down?", "answer": "age"},
    {"question": "The more you take, the more you leave behind. What am I?", "answer": "footsteps"},
    {"question": "What belongs to you but others use it more than you?", "answer": "your name"},
    {"question": "What has a neck but no head?", "answer": "bottle"},
    {"question": "What is full of holes but still holds water?", "answer": "sponge"},
    {"question": "What can you catch but not throw?", "answer": "cold"},
    {"question": "What has words but never speaks?", "answer": "book"},
    {"question": "What runs but never walks?", "answer": "river"},
    {"question": "What has a thumb and four fingers but isn't alive?", "answer": "glove"},
    {"question": "What is always in front of you but can't be seen?", "answer": "future"},
    {"question": "What can you break without touching it?", "answer": "promise"},
    {"question": "What gets bigger the more you take away?", "answer": "hole"},
    {"question": "What has a face and two hands but no arms or legs?", "answer": "clock"}
]

# Game state
if "game_state" not in st.session_state:
    st.session_state.game_state = {
        "current_activity": None,
        "current_joke": None,
        "current_riddle": None,
        "current_game": None,
        "questions_left": 20,
        "secret_item": None
    }

def get_bot_response(user_input):
    user_input = user_input.lower().strip()
    
    # Main menu
    if any(word in user_input for word in ["hi", "hello", "hey", "menu"]):
        st.session_state.game_state["current_activity"] = None
        return "🌟 **Choose an option:**\n\n1. 🎮 **Games**\n2. 😂 **Jokes**\n3. 🤔 **Riddles**"
    
    # Games section
    elif any(word in user_input for word in ["game", "1", "play"]):
        st.session_state.game_state["current_activity"] = "games"
        game_list = "\n".join([f"{num}. {game} - {GAMES[game]['description']}" 
                             for num, game in enumerate(GAMES.keys(), 1)])
        return f"🎮 **Available Games:**\n\n{game_list}\n\nType the number of the game you want to play!"
    
    # Jokes section
    elif any(word in user_input for word in ["joke", "2", "laugh"]):
        st.session_state.game_state["current_activity"] = "jokes"
        joke = random.choice(JOKES)
        st.session_state.game_state["current_joke"] = joke
        return f"😂 **Joke Setup:**\n\n{joke['setup']}\n\nType 'what' or 'why' to hear the punchline!"
    
    # Riddles section
    elif any(word in user_input for word in ["riddle", "3", "puzzle"]):
        st.session_state.game_state["current_activity"] = "riddles"
        riddle = random.choice(RIDDLES)
        st.session_state.game_state["current_riddle"] = riddle
        return f"🤔 **Riddle:**\n\n{riddle['question']}\n\nTake a guess or type 'answer' to see the solution!"
    
    # Handling jokes
    elif st.session_state.game_state["current_activity"] == "jokes":
        if any(word in user_input for word in ["what", "why"]):
            joke = st.session_state.game_state["current_joke"]
            return f"😂 **Punchline:**\n\n{joke['punchline']}\n\nWant another joke? (yes/no)"
        elif "yes" in user_input:
            joke = random.choice(JOKES)
            st.session_state.game_state["current_joke"] = joke
            return f"😂 **Joke Setup:**\n\n{joke['setup']}\n\nType 'what' to hear the punchline!"
        else:
            st.session_state.game_state["current_activity"] = None
            return "🌟 **Choose an option:**\n\n1. 🎮 **Games**\n2. 😂 **Jokes**\n3. 🤔 **Riddles**"
    
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
            st.session_state.game_state["current_activity"] = None
            return "🌟 **Choose an option:**\n\n1. 🎮 **Games**\n2. 😂 **Jokes**\n3. 🤔 **Riddles**"
        else:
            return "🤔 Not quite right! Try again or type 'answer' to see the solution."
    
    # Handling game selection
    elif st.session_state.game_state["current_activity"] == "games":
        if user_input.isdigit() and 1 <= int(user_input) <= 20:
            game_name = list(GAMES.keys())[int(user_input)-1]
            st.session_state.game_state["current_game"] = game_name
            return f"🎮 **{game_name}**\n\n{GAMES[game_name]['instructions']}\n\nType 'start' to begin or 'menu' to go back."
        elif "start" in user_input:
            return "🚀 Game started! Follow the instructions above.\nSay 'menu' when you're done playing."
        else:
            return "Please choose a game by number (1-9) or say 'menu'."
    
    # Default response
    else:
        return "🌟 **Choose an option:**\n\n1. 🎮 Games\n2. 😂 Jokes\n3. 🤔 Riddles"

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your choice (1-3) or say 'menu'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Bot response
    with st.spinner("🤖 Thinking..."):
        response = get_bot_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# Sidebar
with st.sidebar:
    st.title("Boredom Buster Bot")
    st.markdown("### How to Play:")
    st.markdown("- 🎮 **Games**: 20 different games to play")
    st.markdown("- 😂 **Jokes**: Type 'what' to hear punchlines")
    st.markdown("- 🤔 **Riddles**: Guess or say 'answer'")
    st.markdown("---")
    st.markdown("**Quick Commands:**")
    st.markdown("- `menu`: Return to main menu")
    st.markdown("- `what/why`: Reveal joke punchline")
    st.markdown("- `answer`: Show riddle solution")
    st.markdown("- `yes/no`: Continue or stop activities")
    st.markdown("---")
    st.markdown(f"⏰ {datetime.now().strftime('%H:%M')}")
    
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "🌟 **Hi! I'm your Boredom Buster Bot!**\n\nChoose an option:\n\n1. 🎮 **Games**\n2. 😂 **Jokes**\n3. 🤔 **Riddles**"
        }]
        st.session_state.game_state = {
            "current_activity": None,
            "current_joke": None,
            "current_riddle": None,
            "current_game": None,
            "questions_left": 20,
            "secret_item": None
        }
        st.rerun()