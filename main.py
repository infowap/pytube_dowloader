"""
Script principal do downloader YouTube.

- Usa pytubefix para obter e baixar o vídeo.
- Registra cada etapa em arquivos de log separados por nível.
"""
from pytubefix import YouTube   # Cliente para baixar vídeos do YouTube
from log import get_logger  # Logger customizado que separa arquivos por nível
import os  # Para manipular caminhos e criar diretórios

logger = get_logger("main.py")  # Obtém logger já configurado com handlers e rotação

VIDEOS_DIR = "videos"  # Pasta onde os videos serão gravados
os.makedirs(VIDEOS_DIR, exist_ok=True)  # Cria a pasta de videos, se não existir
logger.info("Pasta de vídeos validada: %s", VIDEOS_DIR)  # Loga a criação/garantia da pasta

url = "https://cole_aqui_sua_url"    # URL do vídeo a baixar (substitua pelo desejado)
def main(): # Função principal do script
    yt = YouTube(url)   # Instancia o objeto YouTube
    logger.info("Buscando streams disponíveis...")  # Informa início da busca de streams
    video = yt.streams.get_highest_resolution() # Seleciona a melhor resolução disponível
    if video is None:   # Verifica se algum stream foi encontrado
        logger.error("Nenhum stream encontrado para o vídeo")   # Loga o erro
        return  # Sai da função se não houver stream
    logger.info("Baixando: %s", yt.title)   # Loga o título que será baixado
    video.download(output_path="videos")    # Faz o download para a pasta "videos"

    logger.info("Download concluído!")  # Confirma o término do download

if __name__ == "__main__":
    main()  # Executa a função principal