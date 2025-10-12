# GitHub Actions CI/CD Templates for Genkit

Production-ready GitHub Actions workflows for deploying Firebase Genkit applications.

## 📋 Available Templates

### 1. Firebase Cloud Functions (`firebase-functions.yml`)
Complete workflow for deploying Genkit apps to Firebase Cloud Functions with multi-environment support.

**Features:**
- ✅ Dev, Staging, Production environments
- ✅ Automatic deployments on branch push
- ✅ Security scanning and dependency audits
- ✅ Health checks and smoke tests
- ✅ Automatic rollback on failure
- ✅ Slack notifications

**Use when:**
- Using Firebase as your backend
- Need serverless function deployment
- Want integrated Firebase services

### 2. Google Cloud Run (`cloud-run.yml`)
Containerized deployment to Google Cloud Run with canary releases.

**Features:**
- ✅ Docker container builds
- ✅ Canary deployment (25% → 100%)
- ✅ Container security scanning
- ✅ Auto-scaling configuration
- ✅ Traffic splitting
- ✅ Automatic rollback

**Use when:**
- Need containerized deployment
- Want more control over infrastructure
- Require custom runtime environments
- Need advanced traffic management

### 3. Vercel Deployment (Coming soon)
Optimized for Edge Functions and serverless deployment on Vercel.

### 4. AWS Lambda (Coming soon)
Deploy Genkit applications to AWS Lambda with API Gateway.

## 🚀 Quick Start

### Step 1: Choose Your Template

Copy the appropriate workflow file to your repository:

```bash
# For Firebase Functions
mkdir -p .github/workflows
cp cicd-templates/github-actions/firebase-functions.yml .github/workflows/deploy.yml

# For Cloud Run
cp cicd-templates/github-actions/cloud-run.yml .github/workflows/deploy.yml
cp cicd-templates/github-actions/Dockerfile.template ./Dockerfile
```

### Step 2: Configure Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

#### Common Secrets (All Templates)

```
ANTHROPIC_API_KEY_DEV       # Claude API key for development
ANTHROPIC_API_KEY_STAGING   # Claude API key for staging
ANTHROPIC_API_KEY_PROD      # Claude API key for production

GOOGLE_AI_API_KEY_DEV       # Gemini API key for development
GOOGLE_AI_API_KEY_STAGING   # Gemini API key for staging
GOOGLE_AI_API_KEY_PROD      # Gemini API key for production

SLACK_WEBHOOK_URL           # Slack webhook for notifications (optional)
```

#### Firebase Functions Secrets

```
FIREBASE_SERVICE_ACCOUNT_DEV      # Firebase service account (dev)
FIREBASE_SERVICE_ACCOUNT_STAGING  # Firebase service account (staging)
FIREBASE_SERVICE_ACCOUNT_PROD     # Firebase service account (prod)

FIREBASE_PROJECT_ID_DEV           # Firebase project ID (dev)
FIREBASE_PROJECT_ID_STAGING       # Firebase project ID (staging)
FIREBASE_PROJECT_ID_PROD          # Firebase project ID (prod)

FIREBASE_TOKEN                    # Firebase CI token (alternative)
```

**Get Firebase Service Account:**
```bash
# Go to Firebase Console
# Project Settings → Service Accounts
# Generate new private key
# Copy JSON content to secret
```

**Get Firebase Token:**
```bash
firebase login:ci
# Copy the token to FIREBASE_TOKEN secret
```

#### Cloud Run Secrets

```
GCP_SERVICE_ACCOUNT_KEY    # Google Cloud service account JSON key
GCP_PROJECT_ID             # Google Cloud project ID
```

**Get GCP Service Account:**
```bash
# Create service account
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions"

# Grant necessary roles
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:github-actions@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:github-actions@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:github-actions@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

# Create and download key
gcloud iam service-accounts keys create key.json \
  --iam-account=github-actions@PROJECT_ID.iam.gserviceaccount.com

# Copy key.json content to GCP_SERVICE_ACCOUNT_KEY secret
# Delete local key file
rm key.json
```

### Step 3: Configure Environments

Create GitHub environments for deployment protection:

1. Go to Settings → Environments
2. Create environments: `development`, `staging`, `production`
3. Configure protection rules for `production`:
   - Required reviewers (1-6 people)
   - Wait timer (optional)
   - Deployment branches (only `main`)

### Step 4: Customize Workflow

Edit the workflow file to match your project:

```yaml
env:
  NODE_VERSION: '20'          # Your Node.js version
  SERVICE_NAME: 'your-app'    # Your app name
  GCP_REGION: 'us-central1'   # Your preferred region
```

Update URLs in health checks:
```yaml
- name: Health check
  run: |
    curl -f https://your-app-url.web.app/health || exit 1
```

### Step 5: Test Your Workflow

```bash
# Make a change
echo "// test" >> src/index.ts

# Commit and push to develop
git add .
git commit -m "test: CI/CD pipeline"
git push origin develop

# Watch the workflow run in GitHub Actions tab
```

## 📊 Workflow Structure

### Firebase Functions Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    Pull Request                         │
│  Quality → Security → Test → Build                      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              Push to develop branch                      │
│  Quality → Security → Test → Build → Deploy (Dev)       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│               Push to main branch                        │
│  Quality → Security → Test → Build                      │
│     ↓                                                    │
│  Deploy (Staging) → Smoke Tests                         │
│     ↓                                                    │
│  Deploy (Production) → Health Check → Release           │
└─────────────────────────────────────────────────────────┘
```

### Cloud Run Workflow

```
┌─────────────────────────────────────────────────────────┐
│               Push to main/develop                       │
│  Build & Test → Build Docker Image → Security Scan      │
│     ↓                                                    │
│  Deploy (Staging) → Health Check                        │
│     ↓                                                    │
│  Deploy (Production - Canary 25%)                       │
│     ↓                                                    │
│  Monitor (5 min) → Success/Rollback                     │
│     ↓                                                    │
│  Route 100% traffic → Create Release                    │
└─────────────────────────────────────────────────────────┘
```

## 🔐 Security Best Practices

### Secret Management

✅ **DO:**
- Use GitHub Secrets for all sensitive data
- Rotate secrets regularly (every 90 days)
- Use different secrets per environment
- Limit secret access with environment protection
- Audit secret usage regularly

❌ **DON'T:**
- Commit secrets to git
- Share secrets across projects
- Use production secrets in development
- Log secret values
- Use weak API keys

### Dependency Security

The workflows include:
- `npm audit` - Vulnerability scanning
- Dependency Review Action - PR dependency checks
- TruffleHog - Secret scanning in code
- Trivy - Container security scanning (Cloud Run)

### Code Security

- SAST scanning (coming soon)
- License compliance checks
- Security headers verification
- API rate limiting checks

## 🎯 Deployment Strategies

### Blue-Green Deployment (Firebase)

The Firebase template uses blue-green deployment:
1. Deploy new version to staging
2. Run smoke tests
3. Deploy to production (instant switch)
4. Rollback on failure

**Pros:** Zero downtime, instant rollback
**Cons:** Requires double resources temporarily

### Canary Deployment (Cloud Run)

The Cloud Run template uses canary deployment:
1. Deploy new version with 0% traffic
2. Route 25% traffic to canary
3. Monitor for 5 minutes
4. Route 100% on success, rollback on failure

**Pros:** Risk mitigation, gradual rollout
**Cons:** Longer deployment time

## 📈 Monitoring & Observability

### Health Checks

All templates include health check endpoints:

```typescript
// src/health.ts
import { defineFlow } from '@genkit-ai/flow';
import { z } from 'zod';

export const healthFlow = defineFlow({
  name: 'health',
  inputSchema: z.object({}),
  outputSchema: z.object({
    status: z.enum(['healthy', 'degraded', 'unhealthy']),
    version: z.string(),
    timestamp: z.string(),
    checks: z.object({
      database: z.boolean(),
      ai_models: z.boolean(),
      external_apis: z.boolean(),
    }),
  }),
}, async () => {
  // Check database connection
  const dbHealthy = await checkDatabase();

  // Check AI model availability
  const aiHealthy = await checkAIModels();

  // Check external APIs
  const apisHealthy = await checkExternalAPIs();

  const allHealthy = dbHealthy && aiHealthy && apisHealthy;

  return {
    status: allHealthy ? 'healthy' : 'degraded',
    version: process.env.APP_VERSION || '1.0.0',
    timestamp: new Date().toISOString(),
    checks: {
      database: dbHealthy,
      ai_models: aiHealthy,
      external_apis: apisHealthy,
    },
  };
});

async function checkDatabase(): Promise<boolean> {
  // Implement database health check
  return true;
}

async function checkAIModels(): Promise<boolean> {
  // Check if AI models are accessible
  return true;
}

async function checkExternalAPIs(): Promise<boolean> {
  // Check external API dependencies
  return true;
}
```

### Metrics Collection

Integrate with monitoring services:

```typescript
// src/metrics.ts
import { defineFlow } from '@genkit-ai/flow';

export const metricsFlow = defineFlow({
  name: 'metrics',
  // ... config
}, async () => {
  return {
    requests_total: getRequestCount(),
    errors_total: getErrorCount(),
    latency_p95: getP95Latency(),
    ai_tokens_used: getTokensUsed(),
  };
});
```

### Alerting

Configure alerts in your monitoring system:
- Error rate > 5%
- P95 latency > 1000ms
- Health check failures
- Deployment failures

## 🔔 Notifications

### Slack Integration

The templates include Slack notifications for:
- ✅ Successful deployments
- ❌ Failed deployments
- 🔄 Deployment started
- 📊 Performance metrics

**Setup:**
1. Create Slack webhook: https://api.slack.com/messaging/webhooks
2. Add `SLACK_WEBHOOK_URL` to GitHub Secrets
3. Customize notification messages in workflow

### Discord Integration

Replace Slack action with Discord webhook:
```yaml
- name: Notify Discord
  run: |
    curl -H "Content-Type: application/json" \
      -d '{"content": "Deployment successful! 🎉"}' \
      ${{ secrets.DISCORD_WEBHOOK_URL }}
```

### Email Notifications

GitHub Actions automatically sends email notifications for:
- Workflow failures
- First successful run after failures

Configure in: Profile → Settings → Notifications

## 🧪 Testing Integration

### Unit Tests

```yaml
- name: Run unit tests
  run: npm test
  env:
    NODE_ENV: test
```

**Required scripts in package.json:**
```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  }
}
```

### Integration Tests

```yaml
- name: Run integration tests
  run: npm run test:integration
  env:
    API_URL: https://staging-app.web.app
```

### Smoke Tests

```yaml
- name: Run smoke tests
  run: npm run test:smoke
  env:
    API_URL: ${{ env.STAGING_URL }}
```

**Example smoke test:**
```typescript
// tests/smoke/api.test.ts
describe('API Smoke Tests', () => {
  const API_URL = process.env.API_URL;

  it('should return healthy status', async () => {
    const response = await fetch(`${API_URL}/health`);
    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.status).toBe('healthy');
  });

  it('should handle AI requests', async () => {
    const response = await fetch(`${API_URL}/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: 'test' }),
    });
    expect(response.status).toBe(200);
  });
});
```

## 🔄 Rollback Procedures

### Automatic Rollback

Both templates include automatic rollback on:
- Health check failures
- Error rate thresholds
- Manual failure detection

### Manual Rollback

**Firebase Functions:**
```bash
# List recent deployments
firebase functions:list

# Rollback to previous version
firebase functions:rollback
```

**Cloud Run:**
```bash
# List revisions
gcloud run revisions list --service=SERVICE_NAME --region=REGION

# Route traffic to previous revision
gcloud run services update-traffic SERVICE_NAME \
  --to-revisions=REVISION_NAME=100 \
  --region=REGION
```

## 🎨 Customization

### Add Custom Steps

```yaml
- name: Custom validation
  run: |
    npm run custom-validation
    ./scripts/pre-deploy-check.sh
```

### Multi-region Deployment

```yaml
strategy:
  matrix:
    region: [us-central1, europe-west1, asia-east1]
steps:
  - name: Deploy to ${{ matrix.region }}
    run: |
      gcloud run deploy --region=${{ matrix.region }}
```

### Performance Testing

```yaml
- name: Run performance tests
  run: |
    npm run test:performance
    artillery run tests/load-test.yml
```

### Database Migrations

```yaml
- name: Run database migrations
  run: |
    npm run migrate:latest
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

## 📊 Cost Optimization

### GitHub Actions Minutes

Free tier includes:
- 2,000 minutes/month for private repos
- Unlimited for public repos

**Optimization tips:**
- Use caching for dependencies
- Run jobs in parallel
- Skip redundant steps
- Use self-hosted runners for heavy workloads

### Cloud Resources

- Use minimum instances (0 or 1)
- Set appropriate memory/CPU limits
- Enable auto-scaling
- Use spot/preemptible instances
- Monitor unused resources

## 🆘 Troubleshooting

### Common Issues

**Issue: "Permission denied" during deployment**
```
Solution: Check service account permissions
- Firebase: roles/firebase.admin
- Cloud Run: roles/run.admin, roles/storage.admin
```

**Issue: "Health check failed"**
```
Solution:
1. Check health endpoint implementation
2. Verify environment variables are set
3. Check API quotas
4. Review application logs
```

**Issue: "Secret not found"**
```
Solution:
1. Verify secret name matches exactly
2. Check environment has access to secret
3. Ensure secret is set in repository settings
```

**Issue: "Build timeout"**
```
Solution:
1. Increase timeout in workflow
2. Optimize build process
3. Use caching effectively
4. Consider self-hosted runner
```

### Debug Mode

Enable debug logging:
```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Firebase CI/CD](https://firebase.google.com/docs/hosting/github-integration)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Genkit Documentation](https://genkit.dev/docs/get-started/)

## 🤝 Contributing

Improvements welcome! Please submit issues or pull requests.

---

**Ready to deploy?** Choose your template and follow the quick start guide! 🚀
