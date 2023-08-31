from gym.envs.registration import register

register(
    id='llcp_env-v0',
    entry_point='llcp_env.envs:CPEnv',
)