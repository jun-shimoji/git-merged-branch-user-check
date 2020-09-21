import subprocess
import sys

# 引数にsemverを取る
if len(sys.argv) == 2:
    semver = sys.argv[1]
else:
    print("usage difference-set.py [semver]")
    exit()

# マージされたブランチを取得するコマンド
cmd_mrg         = "git branch -r --list --merged"
cmd_ver         = "git branch -r --list --merged " + str(semver)

# ブランチの作成者名を時系列で並べるコマンド
cmd_ref         = "git for-each-ref --format='%(refname:short),%(authorname),%(committerdate:short)'|sort -k 3 -t ,"

# b''型なのでutf-8に加工する
res_cmd_mrg     = subprocess.check_output(cmd_mrg, shell=True).decode('utf-8')
res_cmd_var     = subprocess.check_output(cmd_ver, shell=True).decode('utf-8')
res_cmd_ref     = subprocess.check_output(cmd_ref, shell=True).decode('utf-8')

# setオブジェクトを作成(差集合を取るため)
set_res_cmd     = set(res_cmd_mrg.split())
set_res_var     = set(res_cmd_var.split())

# ブランチの作成者名を二次元配列にする
ary_res_ref     = res_cmd_ref.split('\n')
ary_res_ref_2d  = []
for item in ary_res_ref:
    ary_res_ref_2d.append(item.split(','))

# 差集合を取得
ary_diff_set    = list((set_res_cmd^set_res_var))

# 差集合で残ったブランチの作成者を表示する
for item in ary_res_ref_2d:
    for value in ary_diff_set:
        if value in item:
            print(item)
