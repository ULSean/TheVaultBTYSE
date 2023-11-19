from pydub import AudioSegment
from pydub.playback import play
from threading import Thread


clip = AudioSegment.from_file("/home/strimble/Documents/GIT/TheVaultBTYSE/Audio/Mission Impossible Themefull theme.mp3", format = 'mp3')


# thread = Thread(target = play, args =(clip,))
# thread.start()
# print('test')

# playsound("/home/strimble/Documents/GIT/TheVaultBTYSE/Audio/3-2-1_GO.wav")

