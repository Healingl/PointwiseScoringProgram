conda create --name JudgeQT python=3.9

pyinstaller --onefile --upx-dir='D:\GithubProject\PointwiseScoringProgram\upx-4.2.4-win64' --clean --name=JudgeScoringProgram JudgeScoringProgram.py