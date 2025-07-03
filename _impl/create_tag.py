"""

Args:
    args[0]: The suffix of the tag
    args[1]: Choice the Nth from latest version

Usage:
    .\tools\_impl\create_tag.py
    .\tools\_impl\create_tag.py rc 1

"""

import re
import sys
import subprocess
from packaging.version import Version


def run_git_command(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


if __name__ == '__main__':

    # option の初期値
    additional = ''
    choice = -1

    # suffix
    if len(sys.argv) >= 2:
        additional = sys.argv[1]  # 'a', 'b' or 'rc'

    # 最新の N 個前
    if len(sys.argv) >= 3:
        # -1 が最新なので
        choice = -1 - int(sys.argv[2])

    # git からタグを取得
    output = run_git_command(['git', 'tag'])
    tag_names = output.splitlines()
    print('Tag names:')
    print(tag_names)
    print()

    # 'v0.1.2' や 'v1.10.2rc' の形式を満たすタグを抽出
    version_pattern = re.compile(r'^v\d+\.\d+\.\d+(?:[a-z]+)?$')
    version_tags = [tag for tag in tag_names if version_pattern.match(tag)]
    if not version_tags:
        raise RuntimeError('有効なタグが見つかりませんでした')

    # Nth タグを取得
    last_tag = sorted(version_tags, key=Version)[choice]

    # 'a' 'b' 'alpha' 'beta' 'rc' で終わっていればそれを取る
    new_tag: str
    suffixes = ('a', 'b', 'alpha', 'beta', 'rc')
    if any([last_tag.endswith(suf) for suf in suffixes]):
        idx = [last_tag.endswith(suf) for suf in suffixes].index(True)
        new_tag = last_tag.removesuffix(suffixes[idx])

    # そうでなければパッチバージョンをひとつ上げる
    else:
        major, minor, patch = last_tag[1:].split('.')
        new_patch = int(patch) + 1
        new_tag = f'v{major}.{minor}.{str(new_patch)}{additional}'

    # git でタグをつける
    run_git_command(['git', 'tag', new_tag])
    print(f'新しいタグ {new_tag} を作成しました')
