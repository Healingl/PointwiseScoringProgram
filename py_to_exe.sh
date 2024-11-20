conda create --name JudgeQT python=3.9

pip install -r requirements.txt

# origin
pyinstaller --onefile --icon=logo_512.ico --name=JudgeScoringProgram JudgeScoringProgram.py

# light
pyinstaller --onefile --icon=logo.ico --upx-dir='D:\GithubProject\PointwiseScoringProgram\upx-4.2.4-win64' --clean -w --name=JudgeScoringProgram JudgeScoringProgram.py

vim JudgeScoringProgram.spec

"""
Analysis={
hiddenimports=['pandas','numpy']
excludes=[
        'pip',
        'setuptools',
        'six',
        'wheel'
    ]
}
"""
# -F 生成单一的 exe 文件
# -p 有些需要手动添加包的位置（dir1，dir2）多个地址时以分号分开
# -i 后接exe图标文件
# -w 代表不显示 console 窗口

pyinstaller JudgeScoringProgram.spec
