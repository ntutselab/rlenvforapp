from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import IEpisodeHandler


class IRewardCalculatorService:
    def __init__(self):
        pass

    def calculateReward(self, episodeHandler: IEpisodeHandler):
        pass

    def getCosineSimilarityText(self):
        pass
