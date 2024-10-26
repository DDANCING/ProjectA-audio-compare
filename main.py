from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import requests
import json
import os
from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from typing import Optional

# Carregar configuração do Dejavu
with open("dejavu.cnf.SAMPLE") as f:
    config = json.load(f)

# Instanciar Dejavu
djv = Dejavu(config)

# Inicializar FastAPI
app = FastAPI()

# Modelo de entrada da API
class AudioRequest(BaseModel):
    audio_url: str
    target_song_id: int

@app.post("/compare-audio/")
async def compare_audio(request: AudioRequest):
    audio_url = request.audio_url
    target_song_id = request.target_song_id
    
    # Adicionar logs para debug
    print(f"Tentando baixar áudio de: {audio_url}")
    
    try:
        response = requests.get(audio_url)
        response.raise_for_status()
        print(f"Tamanho do arquivo baixado: {len(response.content)} bytes")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Erro ao baixar o áudio: {e}")
    
    # Verificar se o diretório existe
    audio_path = "temp_audio.wav"
    print(f"Salvando arquivo em: {os.path.abspath(audio_path)}")
    
    with open(audio_path, "wb") as f:
        f.write(response.content)
    
    # Verificar se o arquivo foi salvo
    print(f"Arquivo existe? {os.path.exists(audio_path)}")
    print(f"Tamanho do arquivo salvo: {os.path.getsize(audio_path)} bytes")

    # Comparar o áudio baixado com as músicas treinadas usando Dejavu
    recognizer = FileRecognizer(djv)
    try:
        result = recognizer.recognize_file(audio_path)
    finally:
        # Remover o arquivo temporário
        os.remove(audio_path)

    # Verificar se há resultados e calcular a similaridade
    if not result or "results" not in result:
        raise HTTPException(status_code=404, detail="Nenhuma similaridade encontrada.")

    # Filtrar o resultado para o ID específico enviado na requisição
    matching_result = next((res for res in result["results"] if res["song_id"] == target_song_id), None)

    if not matching_result:
        return {"message": "Nenhuma correspondência encontrada para a música especificada."}
    
    # Calcular porcentagem de similaridade correta como a proporção dos hashes que coincidiram
    input_hashes = int(matching_result["input_total_hashes"])
    matched_hashes = int(matching_result["hashes_matched_in_input"])
    similarity_percentage = (matched_hashes / input_hashes) * 100 if input_hashes > 0 else 0

    # Retornar a resposta com a porcentagem de similaridade correta
    return {
        "similarity_percentage": similarity_percentage,
        "song_name": matching_result["song_name"].decode("utf-8"),
        "details": {
            "input_total_hashes": input_hashes,
            "hashes_matched_in_input": matched_hashes,
            "song_id": int(matching_result["song_id"]),
            "song_name": matching_result["song_name"].decode("utf-8")
        }
    }
