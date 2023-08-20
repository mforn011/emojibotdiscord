import subprocess

s1 = subprocess.Popen(['python', 'emojibot.py'], stdout=subprocess.PIPE)
s2 = subprocess.Popen(['python', 'main.py'], stdout=subprocess.PIPE)

s2.wait()
s1.poll()
s1.terminate()









