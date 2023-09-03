
import requests
import re
import os
import random
# from random import sample
from tqdm import tqdm
# from utils.voice import get_random_voice, set_random_voice
# from utils.words import get_words


class Utils:
    def __init__(self):
        self.voices = ["oliver", "russell", "olivia", "charlotte"]

    def get_random_voice(self):
        return random.choice(self.voices)

    def get_random_voices(self, n):
        return random.sample(self.voices, n)

    def set_random_voice(self, voices):
        self.voices = voices

    def get_words(self, filename='text.txt'):
        # check if file exists
        if not os.path.exists(filename):
            raise ValueError(f'{filename} does not exist')
        # open text.txt file
        with open(filename, 'r') as f:
            # read file
            text = f.read()
            # split text into words
            words = [word for word in text.split('\n') if word != '']
            return words


class PlayHT:
    def __init__(self, user_id, secret_key):
        self.user_id = user_id
        self.secret_key = secret_key
        self.headers = {
            'AUTHORIZATION': f'Bearer {self.secret_key}',
            'X-USER-ID': self.user_id,
            'accept': 'text/event-stream',
            'content-type': 'application/json'
        }
        self.utils = Utils()

    def get_random_voice(self):
        # return get_random_voice()
        return self.utils.get_random_voice()

    def get_random_voices(self, n):
        # return get_random_voices(n)
        return self.utils.get_random_voices(n)

    def set_random_voice(self, voices):
        # set_random_voice(voices)
        self.utils.set_random_voice(voices)

    def get_words(self, filename='text.txt'):
        # return get_words(filename=filename)
        return self.utils.get_words(filename=filename)

    def get_mp3_url(self, text, voice):
        response = requests.post("https://play.ht/api/v2/tts",
                                 headers=self.headers,
                                 json={
                                        "text": text,
                                        "voice": voice
                                 },
                                 stream=True)
        chunk_list = []
        if response.status_code == 200:
            for chunk in response.iter_content(chunk_size=3):
                if chunk:
                    chunk_list.append(chunk.decode('utf-8'))

        chunk_data = ''.join(chunk_list)
        url = re.findall(r'"url":"(.*?)"', chunk_data)
        if len(url) > 0:
            return url[0]
        else:
            return None

    def download_mp3(self, url, filename):
        doc = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(doc.content)

    def get_mp3_url_and_download(self, text, voice, filename):
        url_reponse = self.get_mp3_url(text=text, voice=voice)
        if url_reponse is not None:
            self.download_mp3(url=url_reponse, filename=filename)
        else:
            error_msg = 'url_reponse is None, text: {}, voice: {}'
            raise ValueError(error_msg.format(
                    text,
                    voice,
                    filename
                )
            )

    def _tts(
        self,
        text,
        index,
        voice,
        filename,
        output_folder,
        repeat_index
    ):
        retry = 0
        if text is None or text == '':
            raise ValueError('text is None or empty')
        if voice is None:
            voice = self.get_random_voice()
        if filename is None:
            filename = f'{index}_{text}_{repeat_index}_{voice}.mp3'
        if output_folder is not None:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            filename = os.path.join(output_folder, filename)
        while retry < 3:
            try:
                self.get_mp3_url_and_download(
                    text=text,
                    voice=voice,
                    filename=filename
                )
                break
            except Exception as e:
                print(f'Error: {e}')
                retry += 1

    def tts(
        self,
        text=None,
        index=None,
        voice=None,
        filename=None,
        output_folder=None,
        repeat=2
    ):
        if repeat <= 0:
            raise ValueError('repeat must be greater than 0')
        voices = self.get_random_voices(n=repeat)
        for i in range(repeat):
            self._tts(
                text=text,
                index=index,
                voice=voices[i],
                filename=filename,
                output_folder=output_folder,
                repeat_index=i
                )


if __name__ == '__main__':
    ht = PlayHT(
        user_id='',
        secret_key=''
    )
    ht.tts(text='Hello World', voice='larry', filename='hello_world.mp3')

    # or
    text_list = ht.get_words(filename='text.txt')

    for i, text in tqdm(enumerate(text_list)):
        ht.tts(text=text, index=i, output_folder='20230822', repeat=2)
