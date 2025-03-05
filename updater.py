import subprocess
import os
import signal

#TODO NOT FINISHED , being coding
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {command}")
        print(result.stderr)
    else:
        print(result.stdout)

def main():
    bot_directory = "home/leg/Desktop/botCrypto"

    # change folder
    os.chdir(bot_directory)

    # Stop bot if it is running
    # find python process bot.py
    result = subprocess.run("pgrep -f bot.py", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        pid = result.stdout.strip()
        print(f"Stop bot process with PID {pid}")
        os.kill(int(pid), signal.SIGTERM)

    run_command("git pull origin main")

    # activate virtual environnement 
    venv_activate = os.path.join(bot_directory, "venv/bin/preBotEnvs.py")
    with open(venv_activate) as f:
        exec(f.read(), {'__file__': venv_activate})

    # intall requirements
    run_command("pip install -r requirements.txt")

    # restart bot in background
    run_command("nohup python bot.py &")

if __name__ == "__main__":
    main()
