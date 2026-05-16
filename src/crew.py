from crewai import Agent, Task, Crew
from langchain_ollama import OllamaLLM


class MoodCrew:
    def __init__(self):
        self.llm = OllamaLLM(model="llama3.2")
        self._setup_agents()

    def _setup_agents(self):
        self.face_detector_agent = Agent(
            role="Face Detector",
            goal="Detect faces and extract facial landmarks from webcam images",
            backstory="Expert in computer vision and facial landmark detection using MediaPipe",
            llm=self.llm,
            verbose=False
        )

        self.mood_analyzer_agent = Agent(
            role="Mood Analyzer",
            goal="Analyze facial landmarks to determine the person's emotional state",
            backstory="Expert in interpreting facial expressions and determining mood from facial geometry",
            llm=self.llm,
            verbose=False
        )

        self.movie_recommender_agent = Agent(
            role="Movie Recommender",
            goal="Recommend movies based on the detected mood",
            backstory="Expert in entertainment and movie recommendations, tailored to emotional states",
            llm=self.llm,
            verbose=False
        )

    def detect_face_task(self, frame_info):
        return Task(
            description=f"Process the webcam frame and detect facial landmarks. Frame info: {frame_info}",
            agent=self.face_detector_agent,
            expected_output="Facial landmark coordinates"
        )

    def analyze_mood_task(self, landmarks_info):
        return Task(
            description=f"Analyze the facial landmarks to determine mood: {landmarks_info}",
            agent=self.mood_analyzer_agent,
            expected_output="Mood classification (happy, sad, neutral, angry, surprised, tired, excited)"
        )

    def recommend_movies_task(self, mood_info):
        return Task(
            description=f"Based on the detected mood ({mood_info}), recommend 5 suitable movies",
            agent=self.movie_recommender_agent,
            expected_output="List of 5 movie recommendations with brief descriptions"
        )

    def run_simple_workflow(self, mood, movies):
        prompt = f"""Based on the detected mood '{mood}', here are the recommended movies:
{', '.join(movies)}

Please provide a brief personalized introduction for these recommendations."""

        task = Task(
            description=prompt,
            agent=self.movie_recommender_agent,
            expected_output="Movie recommendations with personalized intro"
        )

        crew = Crew(agents=[self.movie_recommender_agent], tasks=[task], verbose=False)
        result = crew.kickoff()
        return str(result)