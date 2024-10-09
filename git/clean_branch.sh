#!/bin/bash

# 切換到 develop 分支
git checkout develop

# 更新本地 develop 分支
git pull origin develop

# 列出所有已經合併到 develop 分支的本地分支，排除 develop 和 main 分支
branches=$(git branch --merged develop | grep -v 'develop' | grep -v 'main')

# 迴圈遍歷所有已經合併的分支，並刪除它們
for branch in $branches; do
    echo $branch
    git branch -d $branch
    # 如果要刪除遠端分支，取消下面一行的註釋
    git push origin --delete $branch
done

