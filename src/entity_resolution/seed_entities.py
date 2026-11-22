"""
Seed database of known AI startups and companies for deterministic entity resolution.
Contains canonical names, known aliases, corporate legal variants, and primary domains.
"""

from typing import Dict, List, Any

SEED_AI_STARTUPS: Dict[str, Dict[str, Any]] = {
    "OpenAI": {
        "canonical_name": "OpenAI",
        "aliases": ["Open AI", "OpenAI, Inc.", "OpenAI Inc", "OpenAI LLC", "OpenAI OpCo LLC", "OpenAI Global LLC"],
        "domain": "openai.com",
        "role": "Frontier Model Developer"
    },
    "Anthropic": {
        "canonical_name": "Anthropic",
        "aliases": ["Anthropic, PBC", "Anthropic PBC", "Anthropic Inc.", "Anthropic AI"],
        "domain": "anthropic.com",
        "role": "Frontier Model Developer"
    },
    "Mistral AI": {
        "canonical_name": "Mistral AI",
        "aliases": ["Mistral", "MistralAI", "Mistral AI SAS", "Mistral-AI"],
        "domain": "mistral.ai",
        "role": "Open & Commercial LLM Provider"
    },
    "Stability AI": {
        "canonical_name": "Stability AI",
        "aliases": ["StabilityAI", "Stability AI Ltd.", "Stability AI Inc", "Stability.ai"],
        "domain": "stability.ai",
        "role": "Generative Media & Models"
    },
    "Cohere": {
        "canonical_name": "Cohere",
        "aliases": ["Cohere Inc.", "Cohere AI", "Cohere Technologies"],
        "domain": "cohere.com",
        "role": "Enterprise NLP & Embeddings"
    },
    "Perplexity AI": {
        "canonical_name": "Perplexity AI",
        "aliases": ["Perplexity", "Perplexity.ai", "Perplexity AI, Inc.", "Perplexity Inc"],
        "domain": "perplexity.ai",
        "role": "AI Conversational Search"
    },
    "Midjourney": {
        "canonical_name": "Midjourney",
        "aliases": ["Midjourney, Inc.", "Midjourney Inc", "Midjourney Research"],
        "domain": "midjourney.com",
        "role": "Text-to-Image Generation"
    },
    "Runway": {
        "canonical_name": "Runway",
        "aliases": ["RunwayML", "Runway AI, Inc.", "Runway AI", "Runway Research"],
        "domain": "runwayml.com",
        "role": "Generative Video & Creative Tools"
    },
    "Character.ai": {
        "canonical_name": "Character.ai",
        "aliases": ["Character AI", "Character Technologies, Inc.", "Character Technologies", "c.ai"],
        "domain": "character.ai",
        "role": "Conversational Entertainment Agents"
    },
    "Hugging Face": {
        "canonical_name": "Hugging Face",
        "aliases": ["HuggingFace", "Hugging Face, Inc.", "Hugging Face Inc", "Huggingface Inc."],
        "domain": "huggingface.co",
        "role": "Open AI Community & Model Repository"
    },
    "Scale AI": {
        "canonical_name": "Scale AI",
        "aliases": ["Scale", "Scale.ai", "Scale AI, Inc.", "Scale Media, Inc."],
        "domain": "scale.com",
        "role": "Data Annotation & AI Infrastructure"
    },
    "ElevenLabs": {
        "canonical_name": "ElevenLabs",
        "aliases": ["Eleven Labs", "ElevenLabs, Inc.", "ElevenLabs Inc", "ElevenLabs AI"],
        "domain": "elevenlabs.io",
        "role": "Voice Synthesis & Audio AI"
    },
    "DeepSeek": {
        "canonical_name": "DeepSeek",
        "aliases": ["DeepSeek AI", "DeepSeek-AI", "Hangzhou DeepSeek AI"],
        "domain": "deepseek.com",
        "role": "Open Weight Frontier Reasoning LLMs"
    },
    "Together AI": {
        "canonical_name": "Together AI",
        "aliases": ["Together", "Together.xyz", "Together Computer, Inc."],
        "domain": "together.ai",
        "role": "Cloud Inference & Fine-Tuning"
    },
    "Groq": {
        "canonical_name": "Groq",
        "aliases": ["Groq, Inc.", "Groq Inc", "Groq AI"],
        "domain": "groq.com",
        "role": "LPU Semiconductor & High-Speed Inference"
    },
    "Databricks": {
        "canonical_name": "Databricks",
        "aliases": ["Databricks, Inc.", "Databricks Inc", "MosaicML"],
        "domain": "databricks.com",
        "role": "Lakehouse & Unified Data Intelligence"
    },
    "Anyscale": {
        "canonical_name": "Anyscale",
        "aliases": ["Anyscale, Inc.", "Anyscale Inc", "Ray Project"],
        "domain": "anyscale.com",
        "role": "Distributed AI Infrastructure (Ray)"
    },
    "Pinecone": {
        "canonical_name": "Pinecone",
        "aliases": ["Pinecone Systems, Inc.", "Pinecone Systems", "Pinecone AI", "Pinecone.io"],
        "domain": "pinecone.io",
        "role": "Serverless Vector Database"
    },
    "Weaviate": {
        "canonical_name": "Weaviate",
        "aliases": ["Weaviate B.V.", "Weaviate Inc", "SeMI Technologies"],
        "domain": "weaviate.io",
        "role": "Open-Source Vector Database"
    },
    "Qdrant": {
        "canonical_name": "Qdrant",
        "aliases": ["Qdrant Solutions GmbH", "Qdrant Solutions", "Qdrant Vector DB"],
        "domain": "qdrant.tech",
        "role": "Rust-Based Vector Database"
    },
    "Chroma": {
        "canonical_name": "Chroma",
        "aliases": ["Chroma DB", "ChromaDB", "Chroma Core"],
        "domain": "trychroma.com",
        "role": "AI Embedding Database"
    },
    "LangChain": {
        "canonical_name": "LangChain",
        "aliases": ["LangChain, Inc.", "LangChain Inc", "LangSmith"],
        "domain": "langchain.com",
        "role": "LLM Orchestration Framework"
    },
    "LlamaIndex": {
        "canonical_name": "LlamaIndex",
        "aliases": ["Llama Index", "Run Llama", "GPT Index"],
        "domain": "llamaindex.ai",
        "role": "Data Framework for LLM Applications"
    },
    "Weights & Biases": {
        "canonical_name": "Weights & Biases",
        "aliases": ["W&B", "Weights and Biases", "Weights & Biases, Inc."],
        "domain": "wandb.ai",
        "role": "MLOps & Experiment Tracking"
    },
    "Replicate": {
        "canonical_name": "Replicate",
        "aliases": ["Replicate, Inc.", "Replicate Inc", "Replicate.com"],
        "domain": "replicate.com",
        "role": "Cloud API for Machine Learning"
    },
    "Fireworks AI": {
        "canonical_name": "Fireworks AI",
        "aliases": ["Fireworks", "Fireworks.ai", "Fireworks AI, Inc."],
        "domain": "fireworks.ai",
        "role": "Fast Compound AI Inference"
    },
    "Baseten": {
        "canonical_name": "Baseten",
        "aliases": ["Baseten, Inc.", "Baseten Labs", "Baseten Inc"],
        "domain": "baseten.co",
        "role": "Model Serving & Cloud Infrastructure"
    },
    "Modal": {
        "canonical_name": "Modal",
        "aliases": ["Modal Labs", "Modal Labs, Inc.", "Modal Inc"],
        "domain": "modal.com",
        "role": "Serverless Cloud for Data & AI"
    },
    "Cursor": {
        "canonical_name": "Cursor",
        "aliases": ["Anysphere", "Anysphere, Inc.", "Cursor AI", "Cursor Editor"],
        "domain": "cursor.com",
        "role": "AI Code Editor"
    },
    "Cognition AI": {
        "canonical_name": "Cognition AI",
        "aliases": ["Cognition", "Cognition Labs", "Devin AI", "Cognition Labs, Inc."],
        "domain": "cognition.ai",
        "role": "Autonomous Software Engineer (Devin)"
    },
    "Harvey AI": {
        "canonical_name": "Harvey AI",
        "aliases": ["Harvey", "Harvey Technologies, Inc.", "Harvey Legal AI"],
        "domain": "harvey.ai",
        "role": "Legal Generative AI Platform"
    },
    "Synthesia": {
        "canonical_name": "Synthesia",
        "aliases": ["Synthesia, Ltd.", "Synthesia Ltd", "Synthesia AI"],
        "domain": "synthesia.io",
        "role": "AI Video Avatars & Production"
    },
    "Jasper AI": {
        "canonical_name": "Jasper AI",
        "aliases": ["Jasper", "Jasper.ai", "Jasper AI, Inc."],
        "domain": "jasper.ai",
        "role": "AI Marketing Platform"
    },
    "Writer": {
        "canonical_name": "Writer",
        "aliases": ["Writer, Inc.", "Writer Inc", "Writer AI"],
        "domain": "writer.com",
        "role": "Enterprise Generative AI Platform"
    },
    "Shield AI": {
        "canonical_name": "Shield AI",
        "aliases": ["Shield AI, Inc.", "Shield AI Inc"],
        "domain": "shield.ai",
        "role": "Defense AI & Autonomous Aircraft"
    },
    "Glean": {
        "canonical_name": "Glean",
        "aliases": ["Glean Technologies, Inc.", "Glean Work AI", "Glean Search"],
        "domain": "glean.com",
        "role": "Enterprise AI Search & Work Assistant"
    },
    "Helsing": {
        "canonical_name": "Helsing",
        "aliases": ["Helsing GmbH", "Helsing AI", "Helsing Technologies"],
        "domain": "helsing.ai",
        "role": "Defense Live AI Processing"
    },
    "Inflection AI": {
        "canonical_name": "Inflection AI",
        "aliases": ["Inflection", "Inflection AI, Inc.", "Pi AI"],
        "domain": "inflection.ai",
        "role": "Personal AI Assistant & Enterprise Solutions"
    },
    "Sakana AI": {
        "canonical_name": "Sakana AI",
        "aliases": ["Sakana", "Sakana AI Inc", "Sakana AI Japan"],
        "domain": "sakana.ai",
        "role": "Nature-Inspired & Evolutionary AI"
    },
    "Thinking Machines": {
        "canonical_name": "Thinking Machines",
        "aliases": ["Thinking Machines Data Science", "Thinking Machines Lab"],
        "domain": "thinkingmachin.es",
        "role": "AI Solutions & Data Intelligence"
    },
    "Adept AI": {
        "canonical_name": "Adept AI",
        "aliases": ["Adept", "Adept Labs, Inc.", "Adept AI Labs"],
        "domain": "adept.ai",
        "role": "General Intelligence for Software"
    },
    "Poolside": {
        "canonical_name": "Poolside",
        "aliases": ["Poolside AI", "Poolside SAS"],
        "domain": "poolside.ai",
        "role": "AI for Software Development"
    },
    "Cresta": {
        "canonical_name": "Cresta",
        "aliases": ["Cresta, Inc.", "Cresta AI"],
        "domain": "cresta.com",
        "role": "Contact Center Real-Time AI"
    },
    "Hippocratic AI": {
        "canonical_name": "Hippocratic AI",
        "aliases": ["Hippocratic", "Hippocratic AI, Inc."],
        "domain": "hippocraticai.com",
        "role": "Safety-Focused Healthcare LLMs"
    },
    "Inworld AI": {
        "canonical_name": "Inworld AI",
        "aliases": ["Inworld", "Inworld Technologies, Inc."],
        "domain": "inworld.ai",
        "role": "AI Characters for Games & Virtual Worlds"
    },
    "Pika Labs": {
        "canonical_name": "Pika Labs",
        "aliases": ["Pika", "Pika Art", "Pika AI", "Pika Labs, Inc."],
        "domain": "pika.art",
        "role": "AI Video Generation"
    },
    "Black Forest Labs": {
        "canonical_name": "Black Forest Labs",
        "aliases": ["Black Forest Labs, Inc.", "FLUX AI", "BFL"],
        "domain": "blackforestlabs.ai",
        "role": "FLUX Image & Video Models"
    },
    "Essential AI": {
        "canonical_name": "Essential AI",
        "aliases": ["Essential AI, Inc.", "Essential"],
        "domain": "essential.ai",
        "role": "Enterprise AI Automation"
    },
    "Imbue": {
        "canonical_name": "Imbue",
        "aliases": ["Generally Intelligent", "Imbue AI"],
        "domain": "imbue.com",
        "role": "Reasoning & Coding Agents"
    },
    "Liquid AI": {
        "canonical_name": "Liquid AI",
        "aliases": ["Liquid AI, Inc.", "Liquid Foundation Models"],
        "domain": "liquid.ai",
        "role": "Dynamical & Liquid Neural Networks"
    }
}
