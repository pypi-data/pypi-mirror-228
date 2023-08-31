import logging
import pytest
import uuid
from pygame.math import Vector2
import time
import numpy as np
import cv2
import pygame
import pickle

from gobigger.agents import BotAgent
from gobigger.utils import Border
from gobigger.server import Server
from gobigger.render import RealtimeRender, RealtimePartialRender, EnvRender
from gobigger.envs import GoBiggerEnv, create_env

logging.basicConfig(level=logging.DEBUG)


def demo_bot():
    env = GoBiggerEnv(dict(
        team_num=4, 
        player_num_per_team=3,
        frame_limit=60*20*1,
        playback_settings=dict(
            save_video=True,
            save_all=True,
            save_partial=True,
        ),
    ))
    obs = env.reset()
    bot_agents = []
    team_infos = env.get_team_infos()
    for team_id, player_ids in team_infos:
        for player_id in player_ids:
            bot_agents.append(BotAgent(player_id, level=2))
    time_step_all = 0
    for i in range(100000):
        actions = {bot_agent.name: bot_agent.step(obs[1][bot_agent.name]) for bot_agent in bot_agents}
        t1 = time.time()
        obs, reward, done, info = env.step(actions=actions)
        t2 = time.time()
        time_step_all += t2-t1
        logging.debug('{} {:.4f} envstep {:.3f} / {:.3f}, leaderboard={}'\
            .format(i, obs[0]['last_frame_count'], t2-t1, time_step_all/(i+1), obs[0]['leaderboard']))
        if done:
            logging.debug('Game Over')
            break
    env.close()


def demo_bot_st_t2p2():
    env = create_env('st_t3p2', dict(
        playback_settings=dict(
            playback_type='by_frame',
            by_frame=dict(
                save_frame=True,
            ),
        ),
    ), step_mul=10)
    obs = env.reset()
    bot_agents = []
    team_infos = env.get_team_infos()
    print(team_infos)
    for team_id, player_ids in team_infos:
        for player_id in player_ids:
            bot_agents.append(BotAgent(player_id, level=2))
    time_step_all = 0
    for i in range(100000):
        actions = {bot_agent.name: bot_agent.step(obs[1][bot_agent.name]) for bot_agent in bot_agents}
        t1 = time.time()
        obs, reward, done, info = env.step(actions=actions)
        t2 = time.time()
        time_step_all += t2-t1
        logging.debug('{} {:.4f} envstep {:.3f} / {:.3f}, leaderboard={}'\
            .format(i, obs[0]['last_frame_count'], t2-t1, time_step_all/(i+1), obs[0]['leaderboard']))
        if done:
            logging.debug('Game Over')
            break
    env.close()

if __name__ == '__main__':
    # demo_bot()
    demo_bot_st_t2p2()
