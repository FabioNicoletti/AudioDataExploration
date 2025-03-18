import os
import speech_recognition as sr
from pydub import AudioSegment

def converter_wav_para_m4a(pasta_audio):
    arquivos_wav = [f for f in os.listdir(pasta_audio) if f.endswith(".wav")]
    
    if not arquivos_wav:
        print("Nenhum arquivo .wav encontrado para conversão.")
        return
    
    for arquivo in arquivos_wav:
        caminho_wav = os.path.join(pasta_audio, arquivo)
        caminho_m4a = os.path.join(pasta_audio, arquivo.replace(".wav", ".m4a"))

        try:
            audio = AudioSegment.from_wav(caminho_wav)
            audio.export(caminho_m4a, format="mp4", codec="aac")  # Exportando corretamente
            os.remove(caminho_wav)  # Remove o original .wav
            print(f"Convertido: {arquivo} -> {caminho_m4a}")
        except Exception as e:
            print(f"Erro ao converter {arquivo}: {e}")

def transcrever_audios():
    pasta_audio = "Real Audios"

    if not os.path.exists(pasta_audio):
        print(f"A pasta '{pasta_audio}' não foi encontrada.")
        return

    # Converter os arquivos .wav para .m4a corretamente
    converter_wav_para_m4a(pasta_audio)

    arquivos_audio = [f for f in os.listdir(pasta_audio) if f.endswith(".m4a")]

    if not arquivos_audio:
        print("Nenhum arquivo .m4a encontrado na pasta.")
        return

    recognizer = sr.Recognizer()

    with open("transcricoes.txt", "w", encoding="utf-8") as arquivo_saida:
        for arquivo in arquivos_audio:
            caminho_audio = os.path.join(pasta_audio, arquivo)
            print(f"Transcrevendo: {caminho_audio}...")

            try:
                # Converter para WAV temporário para transcrição
                audio = AudioSegment.from_file(caminho_audio, format="mp4")
                temp_wav = f"temp_{arquivo}.wav"
                audio.export(temp_wav, format="wav")

                with sr.AudioFile(temp_wav) as source:
                    audio_data = recognizer.record(source)
                    try:
                        texto = recognizer.recognize_google(audio_data, language="pt-BR")
                    except sr.UnknownValueError:
                        texto = "[Inaudível]"
                    except sr.RequestError:
                        texto = "[Erro ao acessar o serviço de reconhecimento]"

                    arquivo_saida.write(f"### Transcrição de {arquivo} ###\n")
                    arquivo_saida.write(texto + "\n\n")
                    print(f"Transcrição de {arquivo} concluída!\n")

                os.remove(temp_wav)  # Remove o arquivo temporário

            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")

    print("Todas as transcrições foram salvas em 'transcricoes.txt'")

if __name__ == "__main__":
    transcrever_audios()
