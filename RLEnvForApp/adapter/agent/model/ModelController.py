import random


class ModelController:
    def __init__(self):
        self._model = None

    def set_model(self, model):
        self._model = model

    def is_model_set(self):
        return self._model is not None

    def learn(self, totalTimeSteps: int):
        self._model.learn(total_timesteps=totalTimeSteps, log_interval=1)

    def save(self, path: str):
        self._model.save(path)

    def play(self, environment):
        isContinue = True
        totalReward = 0
        observation = environment.env_method(method_name="reset")
        while isContinue:
            action, state = self._model.predict(observation)
            observation, reward, isDone, info = environment.env_method(
                method_name="step", action=action)[0]
            totalReward += reward
            isContinue = not isDone
        return totalReward

    def play_with_exploration(
            self, environment, explorationEpisodeEsp=0, explorationStepEsp=0):
        isContinue = True
        isRandomEpisode = explorationEpisodeEsp > random.random()
        totalReward = 0
        observation = environment.env_method(method_name="reset")
        while isContinue:
            observation, reward, isDone, info = self._do_one_step(environment=environment, observation=observation,
                                                                isRandomEpisode=isRandomEpisode,
                                                                explorationStepEsp=explorationStepEsp)
            totalReward += reward
            isContinue = not isDone
        return totalReward

    def play_by_total_step(self, environment, totalStep,
                        explorationEpisodeEsp=0, explorationStepEsp=0):
        timeStep = 0
        observation = environment.env_method(method_name="reset")[0]
        isRandomEpisode = False
        while totalStep > timeStep:
            observation, reward, isDone, info = self._do_one_step(environment=environment, observation=observation,
                                                                isRandomEpisode=isRandomEpisode,
                                                                explorationStepEsp=explorationStepEsp)
            timeStep += 1
            if isDone:
                isRandomEpisode = explorationEpisodeEsp > random.random()
                observation = environment.env_method(method_name="reset")[0]

    def _do_one_step(self, environment, observation,
                   isRandomEpisode, explorationStepEsp=0):
        isRandomStep = explorationStepEsp > random.random()
        action, state = self._model.predict(observation)
        if isRandomEpisode and isRandomStep:
            actionList = list(range(environment.action_space.n))
            actionList.remove(int(action))
            action = random.choice(actionList)
        return environment.env_method(method_name="step", action=action)[0]
