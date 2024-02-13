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
        is_continue = True
        total_reward = 0
        observation = environment.env_method(method_name="reset")
        while is_continue:
            action, state = self._model.predict(observation)
            observation, reward, is_done, info = environment.env_method(
                method_name="step", action=action)[0]
            total_reward += reward
            is_continue = not is_done
        return total_reward

    def play_with_exploration(
            self, environment, exploration_episode_esp=0, exploration_step_esp=0):
        is_continue = True
        is_random_episode = exploration_episode_esp > random.random()
        total_reward = 0
        observation = environment.env_method(method_name="reset")
        while is_continue:
            observation, reward, is_done, info = self._do_one_step(environment=environment, observation=observation,
                                                                is_random_episode=is_random_episode,
                                                                exploration_step_esp=exploration_step_esp)
            total_reward += reward
            is_continue = not is_done
        return total_reward

    def play_by_total_step(self, environment, totalStep,
                        exploration_episode_esp=0, exploration_step_esp=0):
        time_step = 0
        observation = environment.env_method(method_name="reset")[0]
        is_random_episode = False
        while totalStep > time_step:
            observation, reward, is_done, info = self._do_one_step(environment=environment, observation=observation,
                                                                is_random_episode=is_random_episode,
                                                                exploration_step_esp=exploration_step_esp)
            time_step += 1
            if is_done:
                is_random_episode = exploration_episode_esp > random.random()
                observation = environment.env_method(method_name="reset")[0]

    def _do_one_step(self, environment, observation,
                   is_random_episode, exploration_step_esp=0):
        is_random_step = exploration_step_esp > random.random()
        action, state = self._model.predict(observation)
        if is_random_episode and is_random_step:
            action_list = list(range(environment.action_space.n))
            action_list.remove(int(action))
            action = random.choice(action_list)
        return environment.env_method(method_name="step", action=action)[0]
