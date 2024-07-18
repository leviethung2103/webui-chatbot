docker rm pipelines -f 
docker rm open-webui -f
curl http://localhost:11434/api/chat -d '{"model": "phi3", "keep_alive": 0}'