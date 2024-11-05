from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer

# Inicializar FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode especificar os domínios permitidos, por exemplo: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (POST, GET, etc.)
    allow_headers=["*"],   # Permite todos os cabeçalhos
)

# Carregar configuração do Dejavu
with open("dejavu.cnf.SAMPLE") as f:
    config = json.load(f)

# Instanciar Dejavu
djv = Dejavu(config)

@app.post("/compare-audio/")
async def compare_audio(target_song_id: int = Form(...), audio: UploadFile = File(...)):
    # Verifique se o ID da música foi fornecido
    if target_song_id is None:
        raise HTTPException(status_code=400, detail="target_song_id é obrigatório.")

    # Salvar o arquivo de áudio recebido
    audio_path = "temp_audio.wav"
    with open(audio_path, "wb") as f:
        content = await audio.read()
        f.write(content)

    # Comparar o áudio com as músicas treinadas usando Dejavu
    recognizer = FileRecognizer(djv)
    try:
        result = recognizer.recognize_file(audio_path)
    finally:
        # Remover o arquivo temporário
        os.remove(audio_path)

    # Verificar se há resultados
    if not result or "results" not in result:
        raise HTTPException(status_code=404, detail="Nenhuma similaridade encontrada.")

    # Filtrar o resultado para o ID específico enviado na requisição
    matching_result = next((res for res in result["results"] if res["song_id"] == target_song_id), None)

    if not matching_result:
        return {"similarity_percentage": 0, "song_name": "Nenhuma correspondência encontrada para a música tocada."}

    # Calcular a porcentagem de similaridade
    input_hashes = int(matching_result["input_total_hashes"])
    matched_hashes = int(matching_result["hashes_matched_in_input"])
    similarity_percentage = (matched_hashes / input_hashes) * 100 if input_hashes > 0 else 0

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
