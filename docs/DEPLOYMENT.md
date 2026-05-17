# Deployment Notes

Captain Cool can be deployed anywhere that supports a Python ASGI app and static files.

## Required Environment Variables

```env
GEMINI_API_KEY=your_gemini_api_key_here
RAPIDAPI_KEY=your_rapidapi_key_here
GEMINI_MODEL=gemini-2.5-pro
```

`GEMINI_API_KEY` powers the strategy debate. `RAPIDAPI_KEY` powers live/recent IPL data. The frontend still serves without those keys, but protected API calls return clear error payloads.

## Generic ASGI Command

```bash
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
```

## Platform Checklist

- Set Python version to 3.10 or newer.
- Install dependencies from `requirements.txt`.
- Configure the environment variables above.
- Expose the app on the platform-provided `PORT`.
- Use `/api/health` as the readiness probe.

## Static Frontend

The FastAPI app mounts `frontend/` at `/`, so no separate frontend build step is required.
