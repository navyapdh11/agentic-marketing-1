# 🚀 Agentic ML Marketing Platform v5.0.0
**COMPLETE PRODUCTION MONOREPO** | REST API + SDK + Widget | Istio | Grafana | Sydney Apr 2026

## 🎯 Live URLs
| Service | URL |
|---------|-----|
| **API + Landing** | https://agentic-marketing-umber.vercel.app |
| **API Docs** | https://agentic-marketing-umber.vercel.app/docs |
| **Health Check** | https://agentic-marketing-umber.vercel.app/health |
| **JavaScript SDK** | https://agentic-marketing-umber.vercel.app/sdk/agentic-marketing.js |
| **Embeddable Widget** | See integration guide below |
| **Grafana** | http://localhost:3001 (admin/hermes2026) |

## 🔌 Quick Integration (3 Lines)
```html
<script src="https://agentic-marketing-umber.vercel.app/sdk/agentic-marketing.js"></script>
<script>
  const am = new AgenticMarketing('amk-demo-key-001');
  const result = await am.humanize('Your AI text here');
</script>
```

## 📋 REST API Endpoints

### SEO
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/seo/audit?domain=example.com` | Run SEO audit |
| GET | `/api/seo/schema?page_type=Article` | Generate JSON-LD schema |
| GET | `/api/seo/rank-prediction?keyword=test` | Predict SERP rank |

### Content Humanization
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/content/humanize` | Humanize AI content |
| POST | `/api/content/analyze` | Analyze AI detection score |

### ML Marketing
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/ml/optimize` | MCTS + Thompson optimization |
| POST | `/api/ml/predict?budget=5000` | Predict outcomes |
| GET | `/api/ml/channels` | Channel performance |

### Auth & Management
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/token` | Exchange API key for JWT |
| POST | `/api/keys` | Create API key |
| GET | `/api/keys` | List API keys |
| POST | `/api/webhooks` | Register webhook |

## 🧩 Widget Embed
```html
<script src="https://agentic-marketing-umber.vercel.app/widget/embed.js"
  data-api-key="amk-demo-key-001"
  data-theme="dark"
  data-position="bottom-right"
  data-base-url="https://agentic-marketing-umber.vercel.app">
</script>
```

## 🔬 Technologies
```
FastAPI + Uvicorn | Thompson Sampling MAB | MCTS Planner
RAG Semantic Memory | DFS Navigation | Istio mTLS
Grafana 11 | Prometheus | Redis | Docker Compose
```

## 🚀 Deploy
```bash
git clone https://github.com/navyapdh11/agentic-marketing-1.git
cd agentic-marketing-1
cp .env.example .env
docker compose -f docker-compose.prod.yml up -d --build
```

## ✅ Git History
```
feat(api): complete REST API + SDK + Widget [33/40]
feat(webhooks): external integration system [34/40]
security(auth): API keys + JWT + rate limiting [35/40]
feat(sdk): JavaScript SDK for any website [36/40]
feat(widget): embeddable marketing widget [37/40]
```

**STATUS**: ✅ API Live | SDK Ready | Widget Embeddable | v5.0.0
