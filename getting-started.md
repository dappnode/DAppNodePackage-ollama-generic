## Welcome to Ollama: Run LLMs locally on your DAppNode

Now you can:

- Open the **Model Manager** from your package links to browse, pull, and manage your models.
- Browse the full [Ollama model library](https://ollama.com/library) to find models.
- Use the Ollama API to integrate with your apps.
- Run Jev-style decisions locally: choose a label, estimate a yes/no probability, or score text against a rubric.

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

### Decision models (System One)

Use **Decision models only** in Model Manager to filter the catalog. Decision models show a **decision** badge; installed models are identified through their reported capabilities.

Pull a compatible model such as `tev1:0.8b`, `tev1`, `nimble`, `clef`, or `clef-flash`, then use **`POST /v1/systemone`** from your application for choices, yes/no probabilities, and scoring. This is the Jev-compatible API for supported Ollama models; it does not install TypeSafe's hosted Jev model.

The endpoint is available directly at `http://ollama-<variant>.dappnode:11434/v1/systemone` and through Model Manager at `http://ui.ollama-<variant>.dappnode/v1/systemone`. Replace `<variant>` with `cpu`, `amd`, or `nvidia`. Local requests do not require an API key.

See the [decision guide](https://docs.ollama.com/capabilities/decision) and [System One API reference](https://docs.ollama.com/api/systemone) for request formats and limits.

### Resources

- [Ollama documentation](https://github.com/ollama/ollama/blob/main/README.md)
- [Ollama API reference](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Model library](https://ollama.com/library)
