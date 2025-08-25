# DummyAI  

**DummyAI** is an **OpenAI-compatible mock server** built with **FastAPI**.  
It replicates the OpenAI API surface and returns **schema-valid dummy responses** for all major endpoints, including chat, completions, embeddings, images, audio, files, fine-tuning, and moderations.  

## Features  
- Fully **OpenAI API compatible**  
- **Dummy responses** with valid JSON schema  
- **Streaming simulation** (SSE) for chat completions  
- **File upload support** with placeholder IDs  
- Lightweight, configurable, and **open source**  

## Use cases  
- Develop OpenAI-based apps **without real API calls**  
- Run in **CI/CD pipelines** for integration testing  
- Work **offline** without API keys or credits  
- Simulate errors or edge cases safely  
