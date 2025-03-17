import numpy as np
import scipy.io.wavfile as wav
import noisereduce as nr
from pydub import AudioSegment
import os

def reduce_noise(input_wav, output_wav):
    """ Reduz o ruido do arquivo de audio .wav """
    rate, data = wav.read(input_wav)

    # Se for estereo, converter para mono antes do processamento
    if len(data.shape) > 1:
        data = data.mean(axis=1)

    # Aplicar reduaco de ruido
    reduced_noise = nr.reduce_noise(y=data, sr=rate, prop_decrease=0.9)

    # Salvar o audio filtrado
    wav.write(output_wav, rate, reduced_noise.astype(np.int16))
    print(f"Ruido reduzido e salvo em: {output_wav}")

def convert_wav_to_m4a(input_wav, output_m4a):
    """ Converte um arquivo .wav para .m4a """
    audio = AudioSegment.from_wav(input_wav)
    audio.export(output_m4a, format="ipod")  # 'ipod' gera m4a (AAC)
    print(f"Conversao concluida: {output_m4a}")

if __name__ == "__main__":
    input_wav = "audio.wav"  # Nome do arquivo original
    noise_reduced_wav = "audio_clean.wav"  # Audio apos reducao de ruido
    output_m4a = "audio_clean.m4a"  # Audio final em .m4a

    if os.path.exists(input_wav):
        reduce_noise(input_wav, noise_reduced_wav)  # Remover ruido
        convert_wav_to_m4a(noise_reduced_wav, output_m4a)  # Converter para m4a
    else:
        print("Arquivo .wav nao encontrado!")
