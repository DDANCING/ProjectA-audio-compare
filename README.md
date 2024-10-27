# Audio Compare API

A **Audio Compare API** é uma API desenvolvida com FastAPI para comparar amostras de áudio fornecidas via URL com áudios previamente treinados, utilizando a biblioteca Dejavu. Esta API foi criada para integrar o **ProjectA**, um site de aprendizado musical que ajuda os usuários a melhorar suas habilidades musicais por meio de atividades interativas, incluindo comparações de áudio em tempo real.

## Tecnologias Utilizadas

- **FastAPI**: Framework rápido e intuitivo para a construção de APIs em Python.
- **Dejavu**: Biblioteca de reconhecimento de áudio para identificação de músicas.
- **Requests**: Biblioteca para realizar requisições HTTP e baixar o áudio a partir de um URL.
- **Pydantic**: Usada para validação de dados de entrada na API.

## Funcionalidades

- **Comparação de Áudio**: Recebe uma URL de áudio e um ID de música alvo, faz o download do áudio e o compara com as músicas previamente treinadas.
- **Cálculo de Similaridade**: Retorna a porcentagem de similaridade entre o áudio baixado e a música treinada, além de detalhes da música correspondente.

## Propósito

Essa API é parte fundamental do **ProjectA**, uma plataforma de aprendizado musical que oferece aulas, atividades interativas e feedback em tempo real para ajudar músicos a aprimorar suas habilidades. A API de comparação de áudio permite que o **ProjectA** ofereça uma experiência personalizada de aprendizado, onde os usuários podem tocar e comparar seus áudios com músicas de referência.

## Pré-requisitos

1. **Python 3.8+**
2. **Dependências do Projeto** (especificadas no arquivo requirements.txt)

## Instalação

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/DDANCING/ProjectA-audio-compare
   cd ProjectA-audio-compare

## Instalação

1. **Crie um ambiente virtual**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
# Audio Compare API

## Instalação

1. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
# Audio Compare API

## Configuração do Dejavu

Crie o arquivo de configuração `dejavu.cnf.SAMPLE` com as informações do banco de dados e diretórios dos arquivos de áudio a serem treinados.

## Como Usar

1. **Treine as músicas usando a Dejavu**:

   ```python
   from dejavu import Dejavu
   import json

   with open("dejavu.cnf.SAMPLE") as f:
       config = json.load(f)

   djv = Dejavu(config)

   djv.fingerprint_directory("path/to/audio/files", [".wav"])

# Audio Compare API

## Iniciar a API

Para iniciar a API, execute o seguinte comando:

```bash

uvicorn main:app --reload

# Audio Compare API

## Como Usar

Faça uma requisição POST para o endpoint `/compare-audio/` com o JSON de entrada:

```json
{
  "audio_url": "http://url_do_audio.wav",
  "target_song_id": 1
}

# Audio Compare API

## Exemplo de Resposta

Ao fazer uma requisição para o endpoint `/compare-audio/`, você pode esperar uma resposta no seguinte formato:

```json
{
  "similarity_percentage": 85.6,
  "song_name": "Nome da Música",
  "details": {
    "input_total_hashes": 12345,
    "hashes_matched_in_input": 10567,
    "song_id": 1,
    "song_name": "Nome da Música"
  }
}

# Audio Compare API

## Estrutura do Projeto

- `main.py`: Arquivo principal contendo a lógica da API.
- `dejavu.cnf.SAMPLE`: Arquivo de configuração para Dejavu.
- `requirements.txt`: Lista de dependências necessárias para o projeto.

## Tratamento de Erros

- **Erro de Download**: Se o áudio não puder ser baixado, a API retorna um erro 400 com uma descrição detalhada.
- **Sem Similaridade Encontrada**: Se nenhuma correspondência for identificada, a API retorna um erro 404.

## Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b minha-feature`).
3. Faça o commit das mudanças (`git commit -m 'Adicionei uma nova feature'`).
4. Envie para o branch (`git push origin minha-feature`).
5. Abra um Pull Request.

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
