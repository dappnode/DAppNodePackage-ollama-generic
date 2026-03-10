## Welcome to Ollama: Run LLMs locally on your DAppNode

Now you can:

- Open the **Model Manager** from your package links to browse, pull, and manage your models.
- Browse the full [Ollama model library](https://ollama.com/library) to find models.
- Use the Ollama API to integrate with your apps.

### Quick start

1. Open the **Model Manager** from the package links in your DAppNode dashboard.
2. Search for a model (e.g. `llama3.2`, `mistral`, `qwen3.5`) and click **Pull** on the tag you want.
3. Once downloaded, the model is ready to use via the API.

### API usage

The API endpoint is available at port `11434` of the Ollama service. You can find the exact URL in your package links.

```bash
# Chat with a model
curl http://<ollama-api-url>:11434/api/chat -d '{
  "model": "qwen3.5:0.8b",
  "messages": [{"role": "user", "content": "Hello!"}],
  "stream": false
}'

# List installed models
curl http://<ollama-api-url>:11434/api/tags
```

### Connecting other apps

Point any Ollama-compatible app (Open WebUI, OpenClaw, etc.) to the API URL shown in your package links.

### Resources

- [Ollama documentation](https://github.com/ollama/ollama/blob/main/README.md)
- [Ollama API reference](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Model library](https://ollama.com/library)
