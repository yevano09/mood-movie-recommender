import os
import json
from crewai import Agent, Task, Crew, LLM


class MoodCrew:
    def __init__(self):
        os.environ["NO_PROXY"] = "localhost,127.0.0.1"
        os.environ["no_proxy"] = "localhost,127.0.0.1"
        os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"
        self.llm = LLM(model="ollama/llama3.2", base_url="http://127.0.0.1:11434")
        self._setup_agents()

    def _setup_agents(self):
        self.movie_recommender_agent = Agent(
            role="Movie Recommender",
            goal="Recommend movies based on the detected mood",
            backstory="Expert in entertainment and movie recommendations, tailored to emotional states",
            llm=self.llm,
            verbose=False
        )

    def generate_all_details(self, movies_by_mood):
        cache = {}
        for mood, movies in movies_by_mood.items():
            prompt = f"""The user's current mood is: {mood}

Here are the recommended movies for this mood:
{chr(10).join(f'{i+1}. {m}' for i, m in enumerate(movies))}

For each movie, provide:
- A one-line hook or tagline
- Why it fits this mood (1 sentence)
- A fun fact or notable detail

Keep the total response under 600 characters so it fits on screen."""

            task = Task(
                description=prompt,
                agent=self.movie_recommender_agent,
                expected_output="A short personalized summary with movie details for each recommendation"
            )

            crew = Crew(agents=[self.movie_recommender_agent], tasks=[task], verbose=False)
            result = crew.kickoff()
            cache[mood] = str(result)
            print(f"  Generated details for: {mood}")

        return cache

    def save_cache(self, cache, path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(base_dir, path)
        with open(full_path, "w") as f:
            json.dump(cache, f, indent=2)

    def load_cache(self, path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(base_dir, path)
        if not os.path.exists(full_path):
            return None
        with open(full_path, "r") as f:
            return json.load(f)
