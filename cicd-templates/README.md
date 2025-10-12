# CI/CD Pipeline Templates for Genkit

Production-ready CI/CD pipeline templates for Firebase Genkit applications across multiple platforms.

## 📋 Overview

This directory contains comprehensive CI/CD pipeline templates for deploying Genkit applications to various cloud platforms with best practices built-in.

## 🚀 Available Templates

### Platform Templates
- **GitHub Actions** - Complete workflows for GitHub repositories
- **GitLab CI** - GitLab CI/CD pipeline configurations
- **Azure Pipelines** - Azure DevOps pipeline templates
- **CircleCI** - CircleCI configuration files
- **Jenkins** - Jenkinsfile templates

### Deployment Targets
- ✅ Firebase Cloud Functions
- ✅ Google Cloud Run
- ✅ Google Cloud Functions (2nd gen)
- ✅ Vercel
- ✅ AWS Lambda
- ✅ Docker / Kubernetes
- ✅ Self-hosted servers

## 🎯 Features

All templates include:

- ✅ **Multi-environment support** (dev, staging, production)
- ✅ **Automated testing** (unit, integration, e2e)
- ✅ **Security scanning** (dependencies, secrets, SAST)
- ✅ **Code quality checks** (linting, formatting, type checking)
- ✅ **Build optimization** (caching, parallel jobs)
- ✅ **Deployment strategies** (blue-green, canary, rolling)
- ✅ **Rollback mechanisms** (automatic on failure)
- ✅ **Notifications** (Slack, Discord, email)
- ✅ **Monitoring integration** (health checks, metrics)
- ✅ **Secret management** (secure API keys, tokens)
- ✅ **Branch protection** (main, develop, release branches)
- ✅ **Semantic versioning** (automatic version bumps)
- ✅ **Changelog generation** (automated release notes)

## 📁 Template Structure

```
cicd-templates/
├── github-actions/
│   ├── firebase-functions.yml
│   ├── cloud-run.yml
│   ├── vercel.yml
│   ├── aws-lambda.yml
│   ├── docker.yml
│   ├── multi-environment.yml
│   └── README.md
├── gitlab-ci/
│   ├── .gitlab-ci.yml
│   └── README.md
├── azure-pipelines/
│   ├── azure-pipelines.yml
│   └── README.md
├── circleci/
│   ├── config.yml
│   └── README.md
├── jenkins/
│   ├── Jenkinsfile
│   └── README.md
└── README.md (this file)
```

## 🔧 Quick Start

### 1. Choose Your Platform

Select the CI/CD platform you're using:
- [GitHub Actions](./github-actions/README.md) - Most popular
- [GitLab CI](./gitlab-ci/README.md) - GitLab users
- [Azure Pipelines](./azure-pipelines/README.md) - Azure DevOps
- [CircleCI](./circleci/README.md) - CircleCI users
- [Jenkins](./jenkins/README.md) - Self-hosted CI/CD

### 2. Choose Your Deployment Target

Each platform has templates for different deployment targets:
- Firebase Cloud Functions
- Google Cloud Run
- Vercel
- AWS Lambda
- Docker/Kubernetes

### 3. Copy Template to Your Project

```bash
# Example: Copy GitHub Actions template for Firebase Functions
cp cicd-templates/github-actions/firebase-functions.yml .github/workflows/deploy.yml

# Configure secrets in your repository settings
# Update environment variables
# Commit and push
```

### 4. Configure Secrets

Each template requires specific secrets. See platform-specific README for details.

**Common secrets:**
- `ANTHROPIC_API_KEY` - Claude API key
- `GOOGLE_AI_API_KEY` - Gemini API key
- `FIREBASE_TOKEN` - Firebase deployment token
- `GCP_SERVICE_ACCOUNT_KEY` - Google Cloud credentials

### 5. Test Your Pipeline

```bash
# Trigger the pipeline
git add .
git commit -m "chore: add CI/CD pipeline"
git push origin main

# Watch the pipeline run in your CI/CD platform
```

## 📊 Pipeline Workflows

### Development Workflow
```
Pull Request → Run Tests → Code Quality → Security Scan → Preview Deploy
```

### Staging Workflow
```
Merge to develop → Build → Test → Deploy to Staging → Integration Tests
```

### Production Workflow
```
Merge to main → Build → Test → Security Scan → Deploy to Production → Health Check → Notify
```

## 🔐 Security Best Practices

### Secret Management
- ✅ Use platform secret management (GitHub Secrets, etc.)
- ✅ Never commit secrets to git
- ✅ Rotate secrets regularly
- ✅ Use least-privilege access
- ✅ Audit secret usage

### Dependency Security
- ✅ Automated dependency scanning
- ✅ Vulnerability alerts
- ✅ Automatic security updates
- ✅ License compliance checks

### Code Security
- ✅ SAST (Static Application Security Testing)
- ✅ Secret scanning in code
- ✅ Container security scanning
- ✅ Infrastructure as Code scanning

## 🎨 Deployment Strategies

### Blue-Green Deployment
Deploy new version alongside old version, switch traffic when ready.

**Benefits:**
- Zero downtime
- Easy rollback
- Full testing in production environment

**Use cases:**
- Production deployments
- Critical applications
- High-availability requirements

### Canary Deployment
Gradually roll out to subset of users, monitor, then full rollout.

**Benefits:**
- Risk mitigation
- Real-world testing
- Gradual rollout

**Use cases:**
- Large user bases
- High-risk changes
- Performance testing

### Rolling Deployment
Replace instances one at a time.

**Benefits:**
- Resource efficient
- Continuous availability
- Simple implementation

**Use cases:**
- Standard deployments
- Kubernetes environments
- Microservices

## 📈 Monitoring & Observability

### Health Checks
All templates include health check endpoints:
```typescript
// src/health.ts
export const healthCheck = defineFlow({
  name: 'health',
  inputSchema: z.object({}),
  outputSchema: z.object({
    status: z.enum(['healthy', 'degraded', 'unhealthy']),
    version: z.string(),
    timestamp: z.string(),
  }),
}, async () => {
  return {
    status: 'healthy',
    version: process.env.APP_VERSION || '1.0.0',
    timestamp: new Date().toISOString(),
  };
});
```

### Metrics Integration
- Request count
- Error rate
- Response time
- Resource usage
- API quotas

### Logging
- Structured logging
- Log aggregation
- Error tracking
- Audit trails

## 🔔 Notifications

Configure notifications for:
- ✅ Deployment success/failure
- ✅ Test failures
- ✅ Security vulnerabilities
- ✅ Performance issues
- ✅ Error rate spikes

**Supported channels:**
- Slack
- Discord
- Microsoft Teams
- Email
- SMS
- PagerDuty

## 🧪 Testing Strategy

### Unit Tests
```bash
npm test
```

### Integration Tests
```bash
npm run test:integration
```

### End-to-End Tests
```bash
npm run test:e2e
```

### Performance Tests
```bash
npm run test:performance
```

### Security Tests
```bash
npm audit
npm run test:security
```

## 🔄 Rollback Procedures

### Automatic Rollback
All templates include automatic rollback on:
- Health check failures
- Error rate threshold exceeded
- Performance degradation
- Manual trigger

### Manual Rollback
```bash
# Using Firebase
firebase functions:config:set version=1.0.0
firebase deploy --only functions

# Using Cloud Run
gcloud run services update SERVICE_NAME \
  --revision-suffix=v1-0-0 \
  --traffic=v1-0-0=100

# Using Vercel
vercel rollback
```

## 📝 Environment Variables

### Required
```bash
NODE_ENV=production
APP_VERSION=1.0.0
LOG_LEVEL=info
```

### AI Model Keys
```bash
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_AI_API_KEY=AIza...
OPENAI_API_KEY=sk-...
```

### Platform-Specific
```bash
# Firebase
FIREBASE_PROJECT_ID=my-project
FIREBASE_TOKEN=...

# Google Cloud
GCP_PROJECT_ID=my-project
GCP_REGION=us-central1

# Vercel
VERCEL_TOKEN=...
VERCEL_ORG_ID=...
VERCEL_PROJECT_ID=...
```

## 🎓 Platform-Specific Guides

### [GitHub Actions](./github-actions/README.md)
- Complete workflow files
- Reusable workflows
- Custom actions
- Matrix builds
- Secrets management

### [GitLab CI](./gitlab-ci/README.md)
- Pipeline configuration
- Job templates
- Variables
- Environments
- Deployment strategies

### [Azure Pipelines](./azure-pipelines/README.md)
- YAML pipelines
- Classic pipelines
- Variable groups
- Service connections
- Release management

### [CircleCI](./circleci/README.md)
- Config version 2.1
- Orbs
- Workflows
- Contexts
- Docker layer caching

### [Jenkins](./jenkins/README.md)
- Declarative pipelines
- Scripted pipelines
- Shared libraries
- Credentials
- Build agents

## 🔧 Customization

### Modify Environment Variables
```yaml
env:
  NODE_ENV: production
  APP_VERSION: ${{ github.sha }}
  CUSTOM_VAR: your-value
```

### Add Custom Steps
```yaml
- name: Custom Step
  run: |
    echo "Your custom commands"
    npm run custom-script
```

### Change Deployment Target
Update the deployment section with your target platform configuration.

### Add Notifications
```yaml
- name: Notify on success
  if: success()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Deployment successful! 🎉"
      }
```

## 📊 Cost Optimization

### Build Optimization
- Use caching for dependencies
- Parallel job execution
- Incremental builds
- Build artifacts reuse

### Deployment Optimization
- Cold start reduction
- Resource right-sizing
- Regional deployment
- Traffic-based scaling

### Monitoring Optimization
- Log sampling
- Metric aggregation
- Alert tuning
- Cost anomaly detection

## 🤝 Contributing

Want to add a template or improve existing ones?

1. Fork the repository
2. Create a feature branch
3. Add your template with documentation
4. Test thoroughly
5. Submit a pull request

## 📚 Resources

- [Genkit Documentation](https://genkit.dev/docs/get-started/)
- [Firebase CI/CD](https://firebase.google.com/docs/hosting/github-integration)
- [Cloud Run CI/CD](https://cloud.google.com/run/docs/continuous-deployment)
- [GitHub Actions](https://docs.github.com/actions)
- [GitLab CI](https://docs.gitlab.com/ee/ci/)
- [Azure Pipelines](https://docs.microsoft.com/azure/devops/pipelines/)
- [CircleCI](https://circleci.com/docs/)
- [Jenkins](https://www.jenkins.io/doc/)

## 🆘 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/amitpatole/claude-genkit-plugin/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/amitpatole/claude-genkit-plugin/discussions)
- 📧 **Email**: amit.patole@gmail.com

## 📄 License

MIT License - see [LICENSE](../LICENSE) file for details

---

**Ready to deploy?** Choose your platform above and follow the quickstart guide! 🚀
