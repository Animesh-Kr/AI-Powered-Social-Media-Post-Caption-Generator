# RAG Pipeline Architecture

## How RAG (Retrieval-Augmented Generation) Works

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        RAG PIPELINE WORKFLOW                             │
└─────────────────────────────────────────────────────────────────────────┘

Step 1: USER INPUT
┌──────────────────────┐
│ User enters:         │
│ "New AI product      │
│  launch"             │
└──────────┬───────────┘
           │
           ▼
Step 2: EMBEDDING GENERATION (GPU-Accelerated)
┌──────────────────────────────────────────────┐
│ Sentence Transformer Model                   │
│ ┌────────────────────────────────────────┐   │
│ │ "New AI product launch"                │   │
│ │         ↓                              │   │
│ │ [0.234, -0.891, 0.456, ...]           │   │
│ │ (384-dimensional vector)               │   │
│ └────────────────────────────────────────┘   │
│ Device: GPU (CUDA) - 20-50ms                 │
└──────────────┬───────────────────────────────┘
               │
               ▼
Step 3: VECTOR SIMILARITY SEARCH (FAISS)
┌─────────────────────────────────────────────────────────────┐
│ Brand Content Vector Database                               │
│ ┌─────────────────────────────────────────────────────┐     │
│ │ Example 1: "🚀 Excited to announce..." [0.92 match] │     │
│ │ Example 2: "Introducing our latest..." [0.88 match] │     │
│ │ Example 3: "Big news! Our new..." [0.85 match]      │     │
│ └─────────────────────────────────────────────────────┘     │
│ Retrieved: Top 3 most similar examples                      │
│ Search time: 10-30ms                                        │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
Step 4: CONTEXT INJECTION
┌────────────────────────────────────────────────────────────┐
│ Enhanced Prompt Builder                                    │
│ ┌────────────────────────────────────────────────────┐     │
│ │ Original: "New AI product launch"                  │     │
│ │                                                     │     │
│ │ + BRAND CONTEXT:                                   │     │
│ │   Example 1: "🚀 Excited to announce..."          │     │
│ │   Example 2: "Introducing our latest..."          │     │
│ │   Example 3: "Big news! Our new..."               │     │
│ │                                                     │     │
│ │ Instruction: Match the style and tone above        │     │
│ └────────────────────────────────────────────────────┘     │
└──────────────┬─────────────────────────────────────────────┘
               │
               ▼
Step 5: AI GENERATION (Gemini 2.0)
┌────────────────────────────────────────────────────────────┐
│ Google Gemini API                                          │
│ ┌────────────────────────────────────────────────────┐     │
│ │ Generates content using:                           │     │
│ │ • User keywords                                    │     │
│ │ • Retrieved brand examples                         │     │
│ │ • Brand voice guidelines                           │     │
│ └────────────────────────────────────────────────────┘     │
│ Generation time: 2-3 seconds                               │
└──────────────┬─────────────────────────────────────────────┘
               │
               ▼
Step 6: OUTPUT (Brand-Consistent Content)
┌────────────────────────────────────────────────────────────┐
│ Generated Post:                                            │
│ ┌────────────────────────────────────────────────────┐     │
│ │ Caption: "🚀 Thrilled to unveil our groundbreaking │     │
│ │ AI solution that's transforming how businesses     │     │
│ │ operate. Join us in this innovation journey!"      │     │
│ │                                                     │     │
│ │ Hashtags: #AI #Innovation #ProductLaunch           │     │
│ │ Sentiment: POSITIVE (0.96)                         │     │
│ │ Context Match: 94% similar to brand examples       │     │
│ └────────────────────────────────────────────────────┘     │
└────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         PERFORMANCE METRICS                              │
├─────────────────────────────────────────────────────────────────────────┤
│ Embedding Generation:    20-50ms  (GPU-accelerated)                     │
│ Vector Search (FAISS):    10-30ms  (Optimized indexing)                 │
│ Context Injection:        <5ms     (String operations)                  │
│ AI Generation:            2-3s     (Gemini API)                          │
│ ─────────────────────────────────────────────────────────────────────── │
│ Total RAG Overhead:       ~50-100ms (Minimal impact!)                   │
│ Quality Improvement:      Significant (Brand consistency + relevance)   │
└─────────────────────────────────────────────────────────────────────────┘
```

## GPU Acceleration Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    GPU ACCELERATION COMPARISON                           │
└─────────────────────────────────────────────────────────────────────────┘

WITHOUT GPU (CPU Only)                    WITH GPU (RTX Acceleration)
═══════════════════════                   ═══════════════════════════

App Startup:                              App Startup:
┌──────────────────┐                      ┌──────────────────┐
│ ⏳ Loading...    │                      │ ⚡ Loading...    │
│ 10-15 seconds    │                      │ 5-10 seconds     │
│ (Every time!)    │                      │ (First time)     │
└──────────────────┘                      └──────────────────┘
                                          
Page Refresh:                             Page Refresh:
┌──────────────────┐                      ┌──────────────────┐
│ ⏳ Reloading...  │                      │ ⚡ Instant!      │
│ 10-15 seconds    │                      │ <1 second        │
│ (Reloads model)  │                      │ (Cached in VRAM) │
└──────────────────┘                      └──────────────────┘

Sentiment Analysis:                       Sentiment Analysis:
┌──────────────────┐                      ┌──────────────────┐
│ 🐌 Processing... │                      │ 🚀 Processing... │
│ 500-1000ms       │                      │ 50-100ms         │
│ per caption      │                      │ per caption      │
└──────────────────┘                      └──────────────────┘

                    @st.cache_resource
                    ═══════════════════
                    ┌─────────────────────────┐
                    │ • Model loaded ONCE     │
                    │ • Stays in GPU VRAM     │
                    │ • Shared across users   │
                    │ • Ultra-fast inference  │
                    └─────────────────────────┘

Performance Comparison Chart:
═══════════════════════════════════════════════════════════════

Startup Time:
CPU  ████████████████ 15s
GPU  ████ 5s (first) / <1s (cached)

Inference Speed:
CPU  ████████████ 800ms
GPU  █ 75ms

Page Refresh:
CPU  ████████████████ 15s
GPU  █ <1s

Memory Efficiency:
CPU  ████████ Reloads each time
GPU  ██████████████████ Persistent in VRAM

Speedup: 10-15x faster! 🚀
```

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        SYSTEM ARCHITECTURE                               │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                          FRONTEND (Streamlit)                        │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐    │
│  │  Image     │  │  Keywords  │  │  Platform  │  │  RAG       │    │
│  │  Upload    │  │  Input     │  │  Selector  │  │  Toggle    │    │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘    │
└────────┼───────────────┼───────────────┼───────────────┼───────────┘
         │               │               │               │
         └───────────────┴───────────────┴───────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER (app.py)                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  • Request validation                                        │   │
│  │  • Error handling (sanitized messages)                       │   │
│  │  • UI rendering                                              │   │
│  └──────────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
┌───────────────────────────────┐  ┌──────────────────────────────┐
│   RAG PIPELINE (Optional)     │  │  CONTENT GENERATOR           │
│  ┌─────────────────────────┐  │  │ ┌──────────────────────────┐ │
│  │ Vector Store (FAISS)    │  │  │ │ Gemini API Client        │ │
│  │ • Brand examples        │  │  │ │ • Prompt building        │ │
│  │ • Voice guidelines      │  │  │ │ • Multi-modal support    │ │
│  └──────────┬──────────────┘  │  │ │ • Response parsing       │ │
│             │                  │  │ └──────────┬───────────────┘ │
│             ▼                  │  │            │                  │
│  ┌─────────────────────────┐  │  │            ▼                  │
│  │ Embedding Model (GPU)   │  │  │ ┌──────────────────────────┐ │
│  │ • Sentence Transformers │  │  │ │ Sentiment Analysis (GPU) │ │
│  │ • all-MiniLM-L6-v2      │  │  │ │ • DistilBERT             │ │
│  │ • Cached in VRAM        │  │  │ │ • Cached in VRAM         │ │
│  └──────────┬──────────────┘  │  │ └──────────┬───────────────┘ │
└─────────────┼──────────────────┘  └────────────┼──────────────────┘
              │                                   │
              └───────────────┬───────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        GPU LAYER (CUDA)                              │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  NVIDIA RTX GPU                                              │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐ │   │
│  │  │ Embedding      │  │ Sentiment      │  │ VRAM Cache     │ │   │
│  │  │ Model          │  │ Model          │  │ (Persistent)   │ │   │
│  │  └────────────────┘  └────────────────┘  └────────────────┘ │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     EXTERNAL SERVICES                                │
│  ┌──────────────────┐                    ┌──────────────────┐       │
│  │ Google Gemini AI │                    │ Brand Content DB │       │
│  │ (API)            │                    │ (Local Files)    │       │
│  └──────────────────┘                    └──────────────────┘       │
└─────────────────────────────────────────────────────────────────────┘

Data Flow:
1. User input → App validation
2. If RAG enabled → Retrieve similar examples → Enhance prompt
3. Enhanced prompt → Gemini API → Generate content
4. Generated content → GPU sentiment analysis → Display results
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────────────┐
│                      TECHNOLOGY STACK                                │
└─────────────────────────────────────────────────────────────────────┘

FRONTEND                  BACKEND                   AI/ML
═══════════              ═══════════              ═══════════
┌──────────┐             ┌──────────┐             ┌──────────┐
│Streamlit │             │ Python   │             │ Gemini   │
│  1.30+   │────────────▶│  3.11+   │────────────▶│  2.0     │
└──────────┘             └──────────┘             └──────────┘
                                │                       │
                                │                       │
                                ▼                       ▼
RAG PIPELINE              GPU ACCELERATION        SECURITY
═══════════              ═══════════              ═══════════
┌──────────┐             ┌──────────┐             ┌──────────┐
│LangChain │             │ PyTorch  │             │ Secure   │
│  0.1+    │             │  2.1+    │             │ Logging  │
└──────────┘             └──────────┘             └──────────┘
┌──────────┐             ┌──────────┐             ┌──────────┐
│  FAISS   │             │Transform-│             │ Error    │
│  1.7+    │             │  ers     │             │ Sanitize │
└──────────┘             └──────────┘             └──────────┘
┌──────────┐             ┌──────────┐             ┌──────────┐
│Sentence  │             │  CUDA    │             │ API Key  │
│Transform │             │  11.8+   │             │ Protect  │
└──────────┘             └──────────┘             └──────────┘
```
