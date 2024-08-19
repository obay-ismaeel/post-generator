import os
import pickle

from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
import textstat
from experta import Fact, KnowledgeEngine, DefFacts, Rule, MATCH, AS

def predict_success_score(new_post):
    # Define the current directory and model paths
    current_directory: str = os.getcwd()
    models_directory: str = f"{current_directory}/models"
    model_pkl_file: str = f"{models_directory}/post_score_model.pkl"
    vectorizer_pkl_file: str = f"{models_directory}/tfidf_vectorizer.pkl"

    # Load the trained model
    with open(model_pkl_file, 'rb') as model_file:  
        loaded_model = pickle.load(model_file)

    # Load the TF-IDF vectorizer
    with open(vectorizer_pkl_file, 'rb') as vectorizer_file:  
        loaded_vectorizer = pickle.load(vectorizer_file)

    # Transform the new post using the loaded TF-IDF vectorizer
    new_post_tfidf = loaded_vectorizer.transform([new_post])

    # Predict the success score using the loaded model
    predicted_score = loaded_model.predict(new_post_tfidf)

    return predicted_score[0]



# nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()
nlp = spacy.load('en_core_web_sm')

class Post(Fact):
    """Information about a post."""
    pass

class PostRating(KnowledgeEngine):
    feedback: list[str] = []  # Class-level list to store feedback messages
    score = None  # Class-level variable to store the score

    @DefFacts()
    def init(self):
        yield Post(content_relevance=0)

    @Rule(Post(text=MATCH.text), AS.fact << Post(content_relevance=0))
    def content_relevance(self, text, fact):
        # Keyword Extraction for Content Relevance
        doc = nlp(text)
        keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
        content_relevance = 1 if len(keywords) > 5 else 0

        if content_relevance == 1:
            self.retract(fact)
            self.declare(Post(content_relevance=1))

        self.declare(Post(engagement_and_tone=0))

    @Rule(Post(text=MATCH.text), AS.fact << Post(engagement_and_tone=0))
    def engagement_and_tone(self, text, fact):
        # Sentiment Analysis for Engagement and Tone
        sentiment = sia.polarity_scores(text)
        engagement_and_tone = 1 if sentiment['compound'] > 0 else 0

        if engagement_and_tone == 1:
            self.retract(fact)
            self.declare(Post(engagement_and_tone=1))

        self.declare(Post(clarity_and_specificity=0))

    @Rule(Post(text=MATCH.text), AS.fact << Post(clarity_and_specificity=0))
    def clarity_and_specificity(self, text, fact):
        # Clarity and Specificity
        clarity_and_specificity = 1 if len(text.split()) > 10 else 0

        if clarity_and_specificity == 1:
            self.retract(fact)
            self.declare(Post(clarity_and_specificity=1))

        self.declare(Post(readability=0))

    @Rule(Post(text=MATCH.text), AS.fact << Post(readability=0))
    def readability(self, text, fact):
        # Readability
        readability = 1 if textstat.textstat.flesch_reading_ease(text) > 50 else 0

        if readability == 1:
            self.retract(fact)
            self.declare(Post(readability=1))

        self.declare(Post(personal_touch=0))

    @Rule(Post(text=MATCH.text), AS.fact << Post(personal_touch=0))
    def personal_touch(self, text, fact):
        # Personal Touch
        doc = nlp(text)
        personal_touch = 1 if any(token.text.lower() in ['i', 'my', 'me', 'we', 'our'] for token in doc) else 0

        if personal_touch == 1:
            self.retract(fact)
            self.declare(Post(personal_touch=1))

        self.declare(Post(call_to_action=0))

    @Rule(Post(text=MATCH.text), AS.fact << Post(call_to_action=0))
    def call_to_action(self, text, fact):
        # Call-to-Action
        call_to_action = 1 if any(phrase in text.lower() for phrase in ['check out', 'click here', 'join us', 'sign up', 'learn more']) else 0

        if call_to_action == 1:
            self.retract(fact)
            self.declare(Post(call_to_action=1))

        self.declare(Post(achievements=0))

    @Rule(Post(text=MATCH.text), AS.fact << Post(achievements=0))
    def achievements(self, text, fact):
        # Achievements or Milestones
        achievements = 1 if any(word in text.lower() for word in ['promotion', 'completed', 'achieved', 'milestone', 'award']) else 0

        if achievements == 1:
            self.retract(fact)
            self.declare(Post(achievements=1))

        self.declare(Post(num_mentions=0))

    @Rule(Post(text=MATCH.text), AS.fact << Post(num_mentions=0))
    def num_mentions(self, text, fact):
        # Presence of Mentions
        doc = nlp(text)
        mentions = [token.text for token in doc if token.text.startswith('@')]
        num_mentions = 1 if len(mentions) > 0 else 0

        if num_mentions == 1:
            self.retract(fact)
            self.declare(Post(num_mentions=1))

        self.declare(Post(num_hashtags=0))

    @Rule(Post(text=MATCH.text), AS.fact << Post(num_hashtags=0))
    def num_hashtags(self, text, fact):
        # Number of Hashtags
        doc = nlp(text)
        hashtags = [token.text for token in doc if token.text.startswith('#')]
        num_hashtags = 1 if len(hashtags) > 0 else 0

        if num_hashtags == 1:
            self.retract(fact)
            self.declare(Post(num_hashtags=1))

        self.declare(Post(industry_keywords=0))

    @Rule(Post(text=MATCH.text), AS.fact << Post(industry_keywords=0))
    def industry_keywords(self, text, fact):
        # Industry-Specific Keywords
        industry_keywords = 1 if any(word in text.lower() for word in ['marketing', 'sales', 'development', 'engineering', 'finance']) else 0

        if industry_keywords == 1:
            self.retract(fact)
            self.declare(Post(industry_keywords=1))

        self.declare(Post(post_length=0))

    @Rule(Post(text=MATCH.text), AS.fact << Post(post_length=0))
    def post_length(self, text, fact):
        # Length of Post
        post_length = 1 if len(text.split()) > 20 else 0

        if post_length == 1:
            self.retract(fact)
            self.declare(Post(post_length=1))

        self.declare(Post(use_of_emojis=0))

    @Rule(Post(text=MATCH.text), AS.fact << Post(use_of_emojis=0))
    def use_of_emojis(self, text, fact):
        # Use of Emojis
        emojis = [token for token in text if token in "😀😃😄😁😆😅😂🤣😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😜🤪😝🤑🤗🤭🤫🤔🤐🤨😐😑😶😏😒🙄😬🤥😌😔😪🤤😴😷🤒🤕🤑🤠😈👿👹👺🤡💩👻💀☠️👽👾🤖🎃😺😸😹😻😼😽🙀😿😾🌟🔹"]
        use_of_emojis = 1 if len(emojis) > 0 else 0

        if use_of_emojis == 1:
            self.retract(fact)
            self.declare(Post(use_of_emojis=1))

        self.declare(Post(combine=True))

    @Rule(
            Post(combine=True),
            Post(content_relevance=MATCH.a),
            Post(engagement_and_tone=MATCH.b),
            Post(clarity_and_specificity=MATCH.c),
            Post(readability=MATCH.d),
            Post(personal_touch=MATCH.e),
            Post(call_to_action=MATCH.f),
            Post(achievements=MATCH.g),
            Post(num_mentions=MATCH.h),
            Post(num_hashtags=MATCH.i),
            Post(industry_keywords=MATCH.j),
            Post(post_length=MATCH.k),
            Post(use_of_emojis=MATCH.l),
         )
    def combine_features(self, a, b, c, d, e, f, g, h, i, j, k, l):
        # Combine features into a single score
        combined_score = (a + b + c + d + e + f + g + h + i + j + k + l) / 12 * 5

        # Scale the combined score to a 0-5 rating
        self.score = round(combined_score, 1)  # Store the score
        self.feedback.append(f"Rating: {self.score}")

    # Define rules here, as before, with modified feedback methods
    @Rule(Post(engagement_and_tone=1))
    def rule_engagement_and_tone(self):
        self.feedback.append("The post is engaging and written in a positive, professional tone.")

    @Rule(Post(content_relevance=1))
    def rule_content_relevance(self):
        self.feedback.append("The content is relevant to the user's professional network and provides value.")

    @Rule(Post(clarity_and_specificity=1))
    def rule_clarity_and_specificity(self):
        self.feedback.append("The message is clear and includes specific details or examples.")

    @Rule(Post(personal_touch=1))
    def rule_personal_touch(self):
        self.feedback.append("The post includes personal elements, showing authenticity and connecting on a human level.")

    @Rule(Post(num_hashtags=1))
    def rule_num_hashtags(self):
        self.feedback.append("The post includes hashtags to increase visibility.")

    @Rule(Post(num_mentions=1))
    def rule_num_mentions(self):
        self.feedback.append("The post includes mentions to engage with specific individuals or organizations.")

    @Rule(Post(post_length=1))
    def rule_post_length(self):
        self.feedback.append("The post is of sufficient length to provide detailed information.")

    @Rule(Post(use_of_emojis=1))
    def rule_use_of_emojis(self):
        self.feedback.append("The post includes emojis to enhance engagement.")

    @Rule(Post(call_to_action=1))
    def rule_call_to_action(self):
        self.feedback.append("The post includes a call-to-action to encourage interaction.")

    @Rule(Post(readability=1))
    def rule_readability(self):
        self.feedback.append("The post is easy to read and understand.")

    @Rule(Post(achievements=1))
    def rule_achievements(self):
        self.feedback.append("The post highlights achievements or milestones.")

    @Rule(Post(industry_keywords=1))
    def rule_industry_keywords(self):
        self.feedback.append("The post includes industry-specific keywords.")

    # Added method to retrieve feedback
    def get_feedback(self):
        return '\n'.join(self.feedback)

def analyze_post(post_text):
    engine = PostRating()
    engine.reset()
    engine.declare(Post(text=post_text))
    engine.run()
    return (engine.score, engine.get_feedback())


# Example usage
if __name__ == "__main__":
    # post_text = """Your post content goes here."""
    post_text = '''🌟 Exciting Career Update! 🌟

    I am thrilled to announce that I have joined @Tech Innovators Inc. as a Senior Software Engineer. This new role is an incredible opportunity to grow and contribute to an innovative team that is making a significant impact in the technology field.

    🔹 Why I’m Excited:

    Collaborating with a talented team: Working alongside some of the brightest minds in the industry.
    Innovative projects and challenges: Engaging in cutting-edge projects that push the boundaries of technology.
    Opportunities for professional growth: Continuous learning and development in a dynamic environment.
    I am grateful for the support and encouragement from my mentors, colleagues, and friends who have been part of my journey. Looking forward to this new chapter and the exciting challenges ahead!
    click here for more information about the company.

    #NewBeginnings #CareerGrowth #Excited #Grateful
    '''
    result = analyze_post(post_text)
    print(result)

