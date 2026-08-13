import importlib.util
import sys
from pathlib import Path

SCRIPT = Path('/mnt/data/rl_replay_analyzer_v0_2.py')
REPLAY = Path('/mnt/data/AE6DD28411F1508AD67AA6A178296A08(1).replay')

spec = importlib.util.spec_from_file_location('rl_replay_analyzer_v0_2', SCRIPT)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def test_header_core_fields():
    h = mod.parse_replay_header(REPLAY)
    p = h['properties']
    assert h['size_bytes'] == 1467811
    assert p['MatchGUID'] == 'AE6DD28411F1508AD67AA6A178296A08'
    assert p['MapName'] == 'EuroStadium_Dusk_P'
    assert p['Team0Score'] == 2
    assert p['Team1Score'] == 4
    assert p['NumFrames'] == 7102


def test_players_and_goals():
    h = mod.parse_replay_header(REPLAY)
    b = mod.parse_replay_body(REPLAY, h)
    a = mod.build_match_analysis(h, b, 'Naveax')
    assert len(a['players']) == 4
    assert a['focus_player_stats']['goals'] == 1
    assert a['focus_player_stats']['assists'] == 3
    assert len(a['goals_timeline']) == 6
    assert [g['player'] for g in a['goals_timeline']] == [
        'Vogod', 'Naveax', 'meyvesuyuoldukya', 'Vogod', 'meyvesuyuoldukya', 'meyvesuyuoldukya'
    ]


def test_body_footer_sections():
    h = mod.parse_replay_header(REPLAY)
    b = mod.parse_replay_body(REPLAY, h)
    assert b['body_size_matches_file'] is True
    assert b['network_stream']['length'] == 1427456
    assert len(b['tick_marks']) == 11
    assert len(b['packages']) == 3
    assert b['objects_summary']['count'] == 443
    assert b['dynamic_names_summary']['count'] == 249
    assert len(b['class_index']) == 43


def test_event_windows_priority():
    h = mod.parse_replay_header(REPLAY)
    b = mod.parse_replay_body(REPLAY, h)
    a = mod.build_match_analysis(h, b, 'Naveax')
    windows = a['event_windows_for_v1']
    assert len(windows) == 11
    assert windows[0]['kind'] == 'goal_against_review'
    assert windows[0]['priority'] == 'high_negative'
    assert windows[0]['window']['start_t'] == '0:17.53'
    assert len(a['assist_candidates']) == 3


if __name__ == '__main__':
    for name, obj in sorted(globals().items()):
        if name.startswith('test_') and callable(obj):
            obj()
            print(f'PASS {name}')
