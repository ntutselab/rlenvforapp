from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler


class IRewardCalculatorService:
    def __init__(self):
        pass

    def calculate_reward(self, episode_handler: IEpisodeHandler):
        pass

    def get_cosine_similarity_text(self):
        pass
