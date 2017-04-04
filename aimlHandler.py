import aiml
import os
import settings

kernel = aiml.Kernel()

if os.path.isfile("/opt/jarvis/bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    os.chdir("/opt/jarvis/aiml/")
    kernel.bootstrap(learnFiles = settings.learn_file, commands = settings.respond)
    os.chdir("/opt/jarvis/")
    kernel.saveBrain("bot_brain.brn")
