import shutil
import json
from typing import NewType
import os

pair = NewType("pair", dict[str, str])

dir = os.path.dirname(os.path.realpath(__file__))
file_path = dir + "/brof_files/file_pairs.json"

def setup_file(path: str):
    
    if os.path.isfile(path):
        return 

    os.mkdir(dir + "/brof_files/")

    with open(path, "w+") as f:
        f.write('{"pairs": []}')

def add_pair_to_store(src: str, dst: str) -> None:
    pair = {"src": os.path.abspath(src), "dst": os.path.abspath(dst)}
    
    with open(file_path, "r+") as fjs:
        content = json.load(fjs)
        content["pairs"].append(pair)
        fjs.seek(0)
        json.dump(content, fjs, indent=4)

def find_changed() -> list[pair]:
    changed_pairs = []

    with open(file_path, "r+") as fjs:
        for pair in json.load(fjs)["pairs"]:
            import difflib

            with open(pair['src']) as src:
                src_cont = src.readlines()

            with open(pair['dst']) as dst:
                dst_cont = dst.readlines()

            if len(list(difflib.unified_diff(src_cont, dst_cont))) != 0:
                changed_pairs.append(pair)

    return changed_pairs

def refresh_pair(pair: pair) -> None:
    shutil.copy(pair['src'], pair['dst'])

def refresh_pairs(pairs: list[pair]) -> None:
    for pair in pairs:
        refresh_pair(pair)
    
def clear_file_pairs_file() -> None:
    content = json.load(open(file_path))
    content['pairs'] = []
    open(file_path, "w").write(json.dumps(content, indent=4))

def remove_sub_folders(folder: str, crr_list: list[str]=[]) -> list[str]:
    content = os.listdir(folder)

    for p in content:
        if os.path.isdir(os.path.join(folder, p)):
            crr_list = remove_sub_folders(os.path.join(folder, p), crr_list)
        elif os.path.isfile(os.path.join(folder, p)):
            crr_list.append(os.path.join(folder, p))
    return crr_list

def add_folders(f1: str, f2:str) -> None:
    a = []
    content1 = remove_sub_folders(f1, a)
    b = []
    content2 = remove_sub_folders(f2, b)

    def relativize_file(file: str, folder: str) -> str:
        arr = file.split("/")
        for i, part in enumerate(arr):
            if part == folder:
                for j in range(0, i+1):
                    arr.pop(j)
                    break
        return "/".join(arr)

    files1 = [relativize_file(file, f1) for file in content1]
    files2 = [relativize_file(file, f2) for file in content2]

    big = max(files1, files2, key=lambda x: len(x))
    for file in big:
        try:
            src = content1[files1.index(file)]
        except:
            continue
        try:
            dst = content2[files2.index(file)]
        except:
            continue
        add_pair_to_store(src, dst)

def show_pairs() -> None:
    with open(file_path, "r") as fjs:
        print(fjs.read())

def remove_pair(src: str, dst: str) -> None:
    with open(file_path, "r+") as fjs:
        content = json.load(fjs)
        for idx, pair in enumerate(content["pairs"]):
            if pair["src"] == src and pair["dst"] == dst:
                del content["pairs"][idx]
                with open(file_path, "w") as fw:
                    fw.write(json.dumps(content, indent=4))
                return

def get_pairs() -> list[pair]:
    with open(file_path, "r+") as fjs:
        content = json.load(fjs)
        return content["pairs"]

def has_pair(src: str, dst:str) -> bool:
    for p in get_pairs():
        if p["src"] == os.path.abspath(src) and p["dst"] == os.path.abspath(dst):
            return True
    return False

