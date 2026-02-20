from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import time
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

# Modular production-grade engines
from app.graph_engine import build_graph, analyze_graph_intelligence
from app.cycle_detector import detect_cycles
from app.smurf_detector import detect_smurfing
from app.shell_detector import detect_shell_networks
from app.anomaly_engine import detect_anomalies
from app.risk_engine import calculate_final_scores
from app.explanation_engine import batch_explain

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Simplified for production-grade demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    start_time = time.time()

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV: {str(e)}")

    required_columns = ["transaction_id", "sender_id", "receiver_id", "amount", "timestamp"]
    for col in required_columns:
        if col not in df.columns:
            raise HTTPException(status_code=400, detail=f"Missing column: {col}")

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # 1. GRAPH FOUNDATION
    G = build_graph(df)
    
    # 2. ADVANCED GRAPH INTELLIGENCE
    graph_intel = analyze_graph_intelligence(G)
    
    # 3. PATTERN DETECTION
    cycle_rings = detect_cycles(G)
    smurf_rings = detect_smurfing(df)
    shell_rings = detect_shell_networks(G, df)
    all_rings = cycle_rings + smurf_rings + shell_rings
    
    # 4. ML ANOMALY DETECTION
    anomaly_results = detect_anomalies(df, G)
    
    # 5. RISK CALIBRATION (WEIGHTED MODEL)
    accounts = list(G.nodes())
    risk_results = calculate_final_scores(accounts, graph_intel, anomaly_results, all_rings, df)
    
    # 6. EXPLANATION ENGINE
    account_patterns = {}
    for ring in all_rings:
        for acc in ring["member_accounts"]:
            if acc not in account_patterns: account_patterns[acc] = []
            account_patterns[acc].append(ring["pattern_type"])
            
    explanations = batch_explain(risk_results, account_patterns, graph_intel)
    
    # 7. RESPONSE FORMATTING
    suspicious_accounts = []
    for acc, data in risk_results.items():
        if data["score"] > 25: # Filtering threshold for 'suspicious' tag
            suspicious_accounts.append({
                "account_id": acc,
                "suspicion_score": data["score"],
                "confidence": data["confidence"],
                "detected_patterns": account_patterns.get(acc, ["anomaly"]),
                "risk_breakdown": data["breakdown"]
            })
            
    suspicious_accounts.sort(key=lambda x: x["suspicion_score"], reverse=True)
    
    processing_time = round(time.time() - start_time, 3)

    return {
        "suspicious_accounts": suspicious_accounts,
        "fraud_rings": all_rings,
        "graph_clusters": [
            {"cluster_id": cid, "members": [node for node, c in graph_intel["communities"].items() if c == cid]}
            for cid in set(graph_intel["communities"].values())
        ],
        "anomaly_scores": [
            {"account_id": acc, "score": round(float(score), 3)}
            for acc, score in anomaly_results["anomaly_score"].items() if score > 0.5
        ],
        "explanations": [
            {"account_id": acc, "text": text} for acc, text in explanations.items()
        ],
        "graph": {
            "nodes": [{"id": node, "community": graph_intel["communities"].get(node)} for node in G.nodes()],
            "edges": [{"source": u, "target": v, "amount": d["amount"]} for u, v, d in G.edges(data=True)]
        },
        "summary": {
            "total_accounts_analyzed": len(G.nodes()),
            "suspicious_accounts_flagged": len(suspicious_accounts),
            "fraud_rings_detected": len(all_rings),
            "avg_risk_score": round(sum(acc["suspicion_score"] for acc in suspicious_accounts) / len(suspicious_accounts), 2) if suspicious_accounts else 0,
            "processing_time_seconds": processing_time
        }
    }

# ── Groq AI Summary ──

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL   = "llama-3.3-70b-versatile"

class SummarizeRequest(BaseModel):
    total_accounts: int = 0
    fraud_rings: int = 0
    suspicious_accounts: int = 0
    avg_risk_score: float = 0.0
    processing_time: float = 0.0
    rings_detail: str = ""
    top_flagged_reasons: str = ""
    graph_hubs: str = ""

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    context: dict

@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    prompt = f"""
As a senior AML compliance officer, review this study of transaction data:
- Dataset: {req.total_accounts} accounts analyzed.
- Findings: {req.fraud_rings} fraud rings discovered, {req.suspicious_accounts} accounts flagged as high-risk.
- Intelligence: Avg Risk {req.avg_risk_score}/100.
- Critical Hubs: {req.graph_hubs or 'None detected'}.
- Pattern Evidence: {req.rings_detail}.
- Behavioral Context: {req.top_flagged_reasons}.

Provide a high-level expert summary of this study. Focus on the structural integrity of the network and the severity of the found patterns (cycles, shells, smurfing).
    """.strip()

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "system", 
                "content": "You are a senior AML Compliance Architect. Provide a sophisticated, professional summary of the fraud analysis 'study' provided. Synthesize the findings into 4-5 high-impact bullet points (-). Do not use headings or introductory filler. Focus on network risk, laundering complexity, and immediate compliance priority. Keep it under 120 words."
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 500
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(GROQ_API_URL, json=payload, headers={"Authorization": f"Bearer {GROQ_API_KEY}"})
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Groq API error: {response.text}")
        return {"summary": response.json()["choices"][0]["message"]["content"]}
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Could not reach Groq: {str(e)}")


@app.post("/chat")
async def chat(req: ChatRequest):
    # Construct a system message that includes the analysis context
    context_str = f"""
    You are an expert AML Compliance Assistant. You are analyzing a specific transaction study.
    Study Context:
    - Accounts: {req.context.get('total_accounts', 'Unknown')}
    - Fraud Rings: {req.context.get('fraud_rings', 'Unknown')}
    - Avg Risk Score: {req.context.get('avg_risk_score', 'Unknown')}
    - Top Flagged: {req.context.get('top_flagged_reasons', 'None')}
    - Key Hubs: {req.context.get('graph_hubs', 'None')}
    
    Answer the user's questions strictly based on this context and AML best practices. 
    Be professional, concise, and helpful.
    """

    messages = [{"role": "system", "content": context_str.strip()}]
    for msg in req.messages:
        messages.append({"role": msg.role, "content": msg.content})

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.5,
        "max_tokens": 600
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                GROQ_API_URL,
                json=payload,
                headers={"Authorization": f"Bearer {GROQ_API_KEY}"}
            )
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Groq Chat API error: {response.text}")
        
        result = response.json()
        return {"content": result["choices"][0]["message"]["content"]}
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Could not reach Groq: {str(e)}")
