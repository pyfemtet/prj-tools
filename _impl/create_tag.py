import re
import subprocess
from packaging.version import Version


def run_git_command(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


if __name__ == '__main__':
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

    # 最新のタグを取得
    last_tag = sorted(version_tags, key=Version)[-1]

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
        new_tag = f'v{major}.{minor}.{str(new_patch)}'

    # git でタグをつける
    run_git_command(['git', 'tag', new_tag])
    print(f'新しいタグ {new_tag} を作成しました')