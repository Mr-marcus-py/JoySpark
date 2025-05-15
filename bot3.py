import streamlit as st
import random
import time
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="MindWell Companion",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS for white and light blue color scheme
st.markdown("""
<style>
    .main {
        background-color: white;
    }
    .stApp {
        background-color: white;
    }
    .st-bx {
        background-color: #e6f2ff;
    }
    .st-c7 {
        background-color: #e6f2ff;
    }
    .st-c8 {
        background-color: white;
    }
    .st-emotion-cache-16txtl3 {
        padding: 1rem;
        border-radius: 10px;
        background-color: #e6f2ff;
    }
    .st-emotion-cache-16idsys {
        background-color: #4da6ff;
    }
    .st-emotion-cache-16idsys:hover {
        background-color: #3399ff;
    }
    .st-emotion-cache-19rxjzo {
        border: 1px solid #e6f2ff;
    }
    h1, h2, h3 {
        color: #0066cc;
    }
    .user-bubble {
        background-color: #e6f2ff;
        padding: 10px 15px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        display: inline-block;
        max-width: 80%;
        align-self: flex-end;
    }
    .bot-bubble {
        background-color: #cce6ff;
        padding: 10px 15px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        display: inline-block;
        max-width: 80%;
        align-self: flex-start;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
    }
    .user-container {
        display: flex;
        justify-content: flex-end;
        margin: 5px 0;
    }
    .bot-container {
        display: flex;
        justify-content: flex-start;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "chat"
if 'game_state' not in st.session_state:
    st.session_state.game_state = None
if 'riddle_answer' not in st.session_state:
    st.session_state.riddle_answer = None

# Mental health responses database
mental_health_responses = {
    "anxiety": [
        "It's normal to feel anxious sometimes. Try deep breathing exercises: breathe in for 4 counts, hold for 7, and exhale for 8.",
        "Anxiety can be managed with mindfulness techniques. Focus on the present moment and acknowledge your feelings without judgment.",
        "Consider writing down your anxious thoughts to help process them. This can make them feel less overwhelming."
    ],
    "depression": [
        "Depression is a common condition that can improve with proper support. Have you considered talking to a mental health professional?",
        "Small steps can help with depression. Try setting one small achievable goal each day.",
        "Remember that depression often lies to you about your worth. Your feelings are valid, but they don't define you."
    ],
    "stress": [
        "Stress management is important. Consider activities like walking, yoga, or meditation to help reduce stress levels.",
        "Setting boundaries can help manage stress. It's okay to say no to additional responsibilities when you're overwhelmed.",
        "Try the 5-5-5 technique: name 5 things you can see, 5 things you can hear, and 5 things you can feel to ground yourself."
    ],
    "sleep": [
        "Consistent sleep schedules can improve mental health. Try to go to bed and wake up at the same time each day.",
        "Avoid screens an hour before bedtime as blue light can interfere with sleep quality.",
        "Creating a relaxing bedtime routine can signal to your body that it's time to sleep."
    ],
    "motivation": [
        "Lack of motivation can be challenging. Break tasks into smaller, manageable steps.",
        "Consider the 5-minute rule: commit to just 5 minutes of an activity, and often you'll continue beyond that.",
        "Celebrate small victories and progress, not just the end result."
    ],
    "loneliness": [
        "Loneliness is a common feeling. Consider joining community groups or classes to meet new people.",
        "Quality connections matter more than quantity. Reach out to one person you trust for a meaningful conversation.",
        "Online communities can provide support and connection around shared interests."
    ],
    "self_care": [
        "Self-care isn't selfish—it's necessary. Make time for activities that replenish your energy.",
        "Physical self-care like proper nutrition, exercise, and sleep forms the foundation of mental well-being.",
        "Emotional self-care might include setting boundaries, practicing self-compassion, or engaging in creative expression."
    ]
}

# General responses for when no specific topic is detected
general_responses = [
    "How are you feeling today?",
    "Remember that it's okay to prioritize your mental health.",
    "What self-care activities have you enjoyed recently?",
    "Is there something specific on your mind that you'd like to talk about?",
    "Remember to be kind to yourself today.",
    "Taking small steps is still progress.",
    "How can I support you today?"
]

# Greetings and farewells
greetings = ["hi", "hello", "hey", "greetings", "howdy", "hiya"]
farewells = ["bye", "goodbye", "see you", "farewell", "cya", "good night", "good day"]

# Jokes database
jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "What did the ocean say to the beach? Nothing, it just waved!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "How does a penguin build its house? Igloos it together!",
    "Why don't eggs tell jokes? They'd crack each other up!",
    "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised!",
    "Why did the bicycle fall over? Because it was two-tired!",
    "What do you call a fake noodle? An impasta!",
    "How do you organize a space party? You planet!"
]

# Riddles database with answers
riddles = [
    {
        "question": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
        "answer": "An echo"
    },
    {
        "question": "The more you take, the more you leave behind. What am I?",
        "answer": "Footsteps"
    },
    {
        "question": "What has keys but no locks, space but no room, and you can enter but not go in?",
        "answer": "A keyboard"
    },
    {
        "question": "What gets wetter as it dries?",
        "answer": "A towel"
    },
    {
        "question": "I'm tall when I'm young, and short when I'm old. What am I?",
        "answer": "A candle"
    },
    {
        "question": "What has a head and a tail but no body?",
        "answer": "A coin"
    },
    {
        "question": "What can travel around the world while staying in a corner?",
        "answer": "A stamp"
    }
]

# Number guessing game
def number_guessing_game():
    if st.session_state.game_state is None:
        st.session_state.game_state = {
            "target": random.randint(1, 100),
            "attempts": 0,
            "max_attempts": 7,
            "guesses": []
        }
    
    game = st.session_state.game_state
    
    st.markdown("<h3 style='color:#0066cc;'>Number Guessing Game</h3>", unsafe_allow_html=True)
    st.write("I'm thinking of a number between 1 and 100. Can you guess it?")
    st.write(f"Attempts remaining: {game['max_attempts'] - game['attempts']}")
    
    if game['guesses']:
        st.write("Your guesses so far: " + ", ".join(map(str, game['guesses'])))
    
    col1, col2 = st.columns([3, 1])
    with col1:
        guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1)
    with col2:
        submit = st.button("Submit Guess")
    
    if submit:
        game['attempts'] += 1
        game['guesses'].append(guess)
        
        if guess == game['target']:
            st.success(f"🎉 Congratulations! You guessed the number {game['target']} in {game['attempts']} attempts!")
            if st.button("Play Again"):
                st.session_state.game_state = None
                st.experimental_rerun()
        elif game['attempts'] >= game['max_attempts']:
            st.error(f"Game over! The number was {game['target']}.")
            if st.button("Play Again"):
                st.session_state.game_state = None
                st.experimental_rerun()
        elif guess < game['target']:
            st.info("Too low! Try a higher number.")
        else:
            st.info("Too high! Try a lower number.")

# Word scramble game
def word_scramble_game():
    words = ["happiness", "mindfulness", "relaxation", "wellness", "balance", "peaceful", "tranquility", "harmony", "serenity", "calm"]
    
    if st.session_state.game_state is None:
        word = random.choice(words)
        letters = list(word)
        random.shuffle(letters)
        scrambled = ''.join(letters)
        st.session_state.game_state = {
            "word": word,
            "scrambled": scrambled,
            "solved": False,
            "attempts": 0
        }
    
    game = st.session_state.game_state
    
    st.markdown("<h3 style='color:#0066cc;'>Word Scramble</h3>", unsafe_allow_html=True)
    st.write("Unscramble the letters to form a word related to mental wellness:")
    st.markdown(f"<h2 style='color:#0066cc;letter-spacing:3px;'>{game['scrambled']}</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        answer = st.text_input("Your answer:").lower().strip()
    with col2:
        submit = st.button("Check Answer")
    
    if submit and answer:
        game['attempts'] += 1
        
        if answer == game['word']:
            game['solved'] = True
            st.success(f"🎉 Correct! The word is {game['word']}. You solved it in {game['attempts']} attempts!")
            if st.button("Play Again"):
                st.session_state.game_state = None
                st.experimental_rerun()
        else:
            st.error("That's not correct. Try again!")
            
    if game['attempts'] >= 3 and not game['solved']:
        hint_length = len(game['word']) // 2
        hint = game['word'][:hint_length] + '_' * (len(game['word']) - hint_length)
        st.info(f"Hint: The word starts with '{hint}'")

# Function to analyze user input and generate a response
def get_response(user_input):
    user_input_lower = user_input.lower()
    
    # Check for greetings
    if any(greeting in user_input_lower for greeting in greetings):
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            return "Good morning! How are you feeling today?"
        elif 12 <= current_hour < 18:
            return "Good afternoon! How can I support you today?"
        else:
            return "Good evening! How has your day been?"
    
    # Check for farewells
    if any(farewell in user_input_lower for farewell in farewells):
        return "Take care of yourself! Remember I'm here whenever you need support."
    
    # Check for requests for jokes
    if "joke" in user_input_lower:
        return random.choice(jokes)
    
    # Check for requests for riddles
    if "riddle" in user_input_lower:
        riddle = random.choice(riddles)
        st.session_state.riddle_answer = riddle["answer"]
        return f"Here's a riddle for you: {riddle['question']}"
    
    # Check if user is trying to answer a riddle
    if st.session_state.riddle_answer and "answer" in user_input_lower:
        answer = st.session_state.riddle_answer
        st.session_state.riddle_answer = None
        return f"The answer is: {answer}"
    
    # Check for game requests
    if "game" in user_input_lower:
        return "I can offer you a number guessing game or a word scramble game. Type 'number game' or 'word game' to play!"
    
    if "number game" in user_input_lower:
        st.session_state.current_mode = "number_game"
        return "Let's play the number guessing game! I'll think of a number between 1 and 100."
    
    if "word game" in user_input_lower:
        st.session_state.current_mode = "word_game"
        return "Let's play word scramble! I'll give you a scrambled word related to mental wellness."
    
    # Check for mental health topics
    for topic, responses in mental_health_responses.items():
        if topic in user_input_lower:
            return random.choice(responses)
    
    # If no specific topic is detected, provide a general response
    return random.choice(general_responses)

# Main app layout
st.title("🧠 MindWell Companion")
st.markdown("### Your Mental Health Support Chatbot")

# Sidebar for navigation
with st.sidebar:
    st.markdown("<h2 style='color:#0066cc;'>Menu</h2>", unsafe_allow_html=True)
    
    if st.button("💬 Chat Mode"):
        st.session_state.current_mode = "chat"
        st.experimental_rerun()
        
    if st.button("🎮 Number Guessing Game"):
        st.session_state.current_mode = "number_game"
        st.session_state.game_state = None
        st.experimental_rerun()
        
    if st.button("🔤 Word Scramble Game"):
        st.session_state.current_mode = "word_game"
        st.session_state.game_state = None
        st.experimental_rerun()
        
    if st.button("😂 Tell me a joke"):
        joke = random.choice(jokes)
        st.session_state.messages.append({"role": "user", "content": "Tell me a joke"})
        st.session_state.messages.append({"role": "assistant", "content": joke})
        st.experimental_rerun()
        
    if st.button("🧩 Give me a riddle"):
        riddle = random.choice(riddles)
        st.session_state.riddle_answer = riddle["answer"]
        st.session_state.messages.append({"role": "user", "content": "Give me a riddle"})
        st.session_state.messages.append({"role": "assistant", "content": f"Here's a riddle for you: {riddle['question']}"})
        st.experimental_rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #0066cc;'>
        <h3>Mental Health Resources</h3>
        <p>If you're experiencing a crisis:</p>
        <p><b>Crisis Text Line:</b> Text HOME to 741741</p>
        <p><b>National Suicide Prevention Lifeline:</b> 988 or 1-800-273-8255</p>
    </div>
    """, unsafe_allow_html=True)

# Display different content based on current mode
if st.session_state.current_mode == "chat":
    # Display chat messages
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"<div class='user-container'><div class='user-bubble'>{message['content']}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-container'><div class='bot-bubble'>{message['content']}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Chat input
    with st.container():
        user_input = st.chat_input("Type your message here...")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            response = get_response(user_input)
            
            # Simulate typing effect by rerunning
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.experimental_rerun()

elif st.session_state.current_mode == "number_game":
    number_guessing_game()
    
    if st.button("Return to Chat", key="return_from_number"):
        st.session_state.current_mode = "chat"
        st.experimental_rerun()
        
elif st.session_state.current_mode == "word_game":
    word_scramble_game()
    
    if st.button("Return to Chat", key="return_from_word"):
        st.session_state.current_mode = "chat"
        st.experimental_rerun()

# First-time user welcome message
if not st.session_state.messages:
    welcome_message = """
    Hello! I'm MindWell Companion, your mental health support chatbot. 
    
    I'm here to:
    • Chat about mental health topics
    • Offer coping strategies for anxiety, stress, and more
    • Play games to help you relax
    • Share jokes and riddles to brighten your day
    
    How are you feeling today?
    """
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})
    st.experimental_rerun()