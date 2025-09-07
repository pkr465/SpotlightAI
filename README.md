# OTT Promo Agent

An agentic workflow (LangGraph + LangChain) for automated promo generation on OTT platforms.
It ingests existing content, selects highlights, writes scripts/taglines, assembles/renders promos,
personalizes variants, and closes the loop with analytics for continuous optimization.


## Core ideas

- **Graph-first orchestration** with LangGraph for clarity, retries, and conditional routing.
- **Separation of concerns**: node logic in `graph/nodes`, infra/model adapters in `tools`, prompts in `agents`.
- **Observability** hooks to push metrics to your analytics store.
- **A/B testing** and **personalization** built-in.
- **Stateless API** with persisted artifacts in object storage (S3/GCS/Azure Blob).

See code comments in each file for integration notes.

⸻

# High-level design

## Goals
	•	Autonomously generate short promos from long-form OTT assets.
	•	Pick emotionally engaging highlights, write scripts/taglines, assemble edits, and export in common aspect ratios.
	•	Personalize variants per audience/locale; run A/B tests; close the loop with analytics.

## Agentic workflow (LangGraph)
	1.	ingest → fetch asset to local cache; record metadata.
	2.	transcode → (optional) normalize to mezzanine (codec/framerate/audio).
	3.	asr → transcribe/align subtitles (e.g., Whisper) and attach text cues.
	4.	scene_detect → rough scene boundaries/duration for downstream passes.
	5.	sentiment → emotion/sentiment/energy time-series over the timeline.
	6.	highlight_rank → peak-picking + constraints; cut n best micro-segments.
	7.	script_gen → LLM writes a 15–30s script, taglines, SEO keywords.
	8.	edit_assemble → assemble highlight clips (concat in stub; real impl adds titles, overlays, music ducking).
	9.	render → export AR variants (9:16, 1:1, 16:9), loudness targets, bitrates.
	10.	qc → guardrails: duration, silence/black detection, loudness, safe words.
	11.	personalize → LLM rewrites script/taglines for each audience/locale.
	12.	ab_test → generate test hypotheses + metrics; name variants.
	13.	publish → write master + variants to storage (S3/GCS/local).
	14.	analytics → emit events (CTR/CVR hooks) and persist feedback.

The repo includes this exact graph with async nodes and typed state. Swap the stubs with your production adapters.

## Key components & where they live
	•	Graph orchestration: src/graph/builder.py, nodes in src/graph/nodes/*
	•	Typed state: src/graph/state.py (Pydantic v2)
	•	LLM clients: src/agents/llm.py (OpenAI or Anthropic, auto-selects via env)
	•	Prompts: src/agents/prompts.py (script, personalization, A/B hypotheses)
	•	Infra adapters: src/tools/storage.py, src/tools/video.py, src/tools/nlp.py, src/tools/analytics.py
	•	Service API: src/app.py (FastAPI) + src/api/routers.py (POST /run)
	•	Config: src/config.py (loads .env), .env.default provided
	•	Tests: src/tests/test_smoke.py
	•	Runtime: requirements.txt (LangGraph, LangChain, FastAPI, etc.)

⸻

## Folder & file layout (you’ll see this in the zip)

ott-promo-agent/
  README.md
  .env.default
  requirements.txt
  src/
    app.py
    config.py
    api/routers.py
    agents/
      __init__.py
      llm.py
      prompts.py
    graph/
      __init__.py
      builder.py
      state.py
      nodes/
        __init__.py
        ingest.py
        transcode.py
        asr.py
        scene_detect.py
        sentiment.py
        highlight_rank.py
        script_gen.py
        edit_assemble.py
        render.py
        qc.py
        personalize.py
        ab_test.py
        publish.py
        analytics.py
    tools/
      __init__.py
      storage.py
      video.py
      nlp.py
      analytics.py
    tests/
      __init__.py
      test_smoke.py


⸻

## Configuration

## Fill .env.default → copy to .env:
	•	LLMs: OPENAI_API_KEY, OPENAI_MODEL (default gpt-4o-mini) or Anthropic ANTHROPIC_API_KEY, ANTHROPIC_MODEL (default claude-3-5-sonnet-latest). The system auto-selects whichever key is present.
	•	Storage: STORAGE_BACKEND (s3|gcs|local), S3_BUCKET/GCS_BUCKET, LOCAL_MEDIA_ROOT
	•	Media tools: FFMPEG_BIN, FFPROBE_BIN
	•	Service: LOG_LEVEL, MAX_WORKERS
	•	Analytics sink settings (stubbed local by default)

⸻

## Run it

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.default .env  # then edit with your keys/buckets
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

Example request:

curl -X POST http://localhost:8000/run -H "Content-Type: application/json" -d '{
  "asset_uri": "s3://bucket/sample.mp4",
  "campaign_id": "cmp_001",
  "audiences": ["genpop","sports_fans"],
  "target_formats": ["9:16","16:9"],
  "show_title": "Road to Glory",
  "logline": "An underdog fights through adversity to win it all."
}'


⸻

## Implementation notes & how to extend

Replace stubs with real intelligence
	•	ASR (nodes/asr.py): swap mock transcript for WhisperX/Whisper large-v3 w/ word-level timestamps; store aligned captions in state.metadata["subtitles"].
	•	Scene detection (nodes/scene_detect.py): use ffprobe + histogram difference or a library like PySceneDetect; populate state.duration_s accurately.
	•	Sentiment/energy (nodes/sentiment.py): run audio energy + music intensity + voice emotion (e.g., a wav2vec/Emotion2Vec head) and visual excitement (shot scale, motion magnitude); aggregate into a per-second score.
	•	Highlight selection (nodes/highlight_rank.py): add constraints (no duplicates, narrative coverage, subtitle density, safety filters) and a learning-to-rank model trained on historical engagement.
	•	Edit/assemble (nodes/edit_assemble.py + render.py): replace concat with:
	•	Motion templates, brand pack (logos, fonts), lower thirds, end slates.
	•	Music bed selection + ducking with side-chain compression.
	•	Aspect-ratio smart crop (saliency tracking) for 9:16, 1:1, 16:9.
	•	Personalization (nodes/personalize.py): adjust CTA copy, tone, and overlays per segment/locale; include regulatory word lists per region.
	•	A/B testing (nodes/ab_test.py): generate variant matrix (hook_alt, CTA_alt, music_alt), auto-name variants, and return metrics to analytics.

Storage & publishing
	•	tools/storage.py is mocked; wire to S3/GCS (boto3 / google-cloud-storage). Persist:
	•	Source mezzanine, intermediate clips, final renders.
	•	JSON sidecars: script.json, variants.json, ab_tests.json.

Analytics/feedback
	•	tools/analytics.py currently logs; replace with Segment, Snowflake, or BigQuery writer.
	•	Add a feedback consumer to retrain highlight ranker and prompt heuristics from real CTR/CVR.

Testing
	•	tests/test_smoke.py runs the full graph with mocks.
	•	Add compute-light unit tests for each node (inputs → expected state deltas).

⸻

API surface (FastAPI)
	•	GET /health → {"ok": true}
	•	POST /run → kicks the agentic workflow with your payload and returns the final PromoState (including published_uri, script_json, and personalized_variants).

⸻

Why this architecture works
	•	Composable graph → easy to add/remove nodes (e.g., safety, compliance, brand approvals).
	•	Async, idempotent nodes → scale out horizontally; retry safely.
	•	Separation of adapters → swap models/providers without touching graph logic.
	•	Typed state → consistent contracts across nodes; easier debugging/observability.
	•	Extensibility → drop in real CV/audio models, RAG over brand guides, and policy filters.

Great choice 🎉 — SpotlightAI is clear, professional, and marketing-friendly. Here’s a polished branding package for you to start using right away:

⸻

✅ Project Identity: SpotlightAI

Tagline Options (pick one or rotate for A/B tests):
	•	“Shining on moments that matter.”
	•	“AI promos that capture attention.”
	•	“Find. Create. Engage. Automatically.”

One-line elevator pitch:
SpotlightAI turns hours of OTT content into ready-to-publish promos in minutes, using AI to find highlights, write scripts, and personalize videos for every audience.

⸻

🌟 Expanded Description

SpotlightAI is an AI-driven promo generation platform built for OTT marketing teams. It ingests video, audio, and subtitles from large content libraries, then uses deep learning to surface emotional peaks and audience-resonant moments. With built-in scriptwriting, automated editing, and personalization, SpotlightAI produces engaging promos at scale — tailored for different demographics, platforms, and formats. The system continuously learns from analytics (views, clicks, conversions) to refine future campaigns, enabling faster A/B testing and higher ROI.

⸻

📊 Key Value Props for Pitch Deck
	•	Faster: Create promos in hours instead of weeks.
	•	Cheaper: Cut manual editing and scriptwriting costs by up to 70%.
	•	Smarter: AI selects the most engaging moments automatically.
	•	Personalized: Tailor promos for audiences, regions, and platforms.
	•	Data-driven: Analytics feedback loop improves results over time.

⸻

🎨 Visual Branding Concept (suggestions)
	•	Logo motif: A spotlight beam forming the letter S, or a play button inside a glowing halo.
	•	Primary colors: Deep violet / midnight blue (trust + creativity), accented with neon yellow (energy + attention).
	•	Typography: Bold sans-serif (modern tech) for “Spotlight”, lighter humanist sans for “AI”.
	•	Style: Dynamic, cinematic feel — reflecting both media creativity and AI intelligence.

⸻