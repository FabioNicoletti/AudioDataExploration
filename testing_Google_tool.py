import os
import speech_recognition as sr
from pydub import AudioSegment

def transcrever_audios():
    recognizer = sr.Recognizer()
    arquivos_audio = [f for f in os.listdir() if f.endswith(".m4a")]
    
    if not arquivos_audio:
        print("Nenhum arquivo .m4a encontrado.")
        return
    
    with open("transcricoes.txt", "w", encoding="utf-8") as arquivo_saida:
        for arquivo in arquivos_audio:
            print(f"Transcrevendo: {arquivo}...")
            
            # Converter para WAV
            audio = AudioSegment.from_file(arquivo, format="m4a")
            audio.export("temp.wav", format="wav")
            
            with sr.AudioFile("temp.wav") as source:
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

    print("Todas as transcrições foram salvas em 'transcricoes.txt'")

if __name__ == "__main__":
    transcrever_audios()
