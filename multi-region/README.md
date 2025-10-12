# Multi-Region Deployment for Genkit Applications

Deploy Genkit applications across multiple geographic regions for improved performance, reliability, and compliance.

## 🌍 Overview

Multi-region deployment distributes your Genkit application across multiple geographic locations to provide:

- ⚡ **Lower Latency** - Serve users from the nearest region
- 🛡️ **High Availability** - Failover protection if one region goes down
- 📊 **Load Distribution** - Distribute traffic across regions
- 🌐 **Data Residency** - Comply with regional data regulations
- 🚀 **Disaster Recovery** - Business continuity planning

## 🎯 Deployment Strategies

### 1. Active-Active (Multi-Master)
All regions actively serve traffic simultaneously.

**Benefits:**
- Maximum performance
- Full redundancy
- Optimal resource utilization

**Use Cases:**
- Global applications
- High-traffic services
- Mission-critical systems

### 2. Active-Passive (Failover)
Primary region serves traffic, secondary regions on standby.

**Benefits:**
- Cost-effective
- Simple management
- Fast failover

**Use Cases:**
- Disaster recovery
- Budget-conscious deployments
- Regulatory compliance

### 3. Geo-Routing
Route users to nearest region based on location.

**Benefits:**
- Optimal latency
- Better user experience
- Regional customization

**Use Cases:**
- Content delivery
- Regional services
- Compliance requirements

## 🚀 Quick Start

### Option 1: Terraform (Infrastructure as Code)
```bash
cd multi-region/terraform
terraform init
terraform plan
terraform apply
```

### Option 2: GitHub Actions (Automated)
```bash
# Copy workflow template
cp multi-region/templates/multi-region-deploy.yml .github/workflows/

# Configure secrets and deploy
git push origin main
```

### Option 3: Manual Setup
```bash
# Deploy to each region
./multi-region/scripts/deploy-all-regions.sh
```

## 📁 Directory Structure

```
multi-region/
├── README.md (this file)
├── templates/
│   ├── multi-region-deploy.yml (GitHub Actions)
│   ├── terraform/ (IaC templates)
│   └── docker-compose.yml (local testing)
├── config/
│   ├── regions.json (region configuration)
│   ├── traffic-split.json (traffic routing)
│   └── health-checks.json (monitoring)
├── scripts/
│   ├── deploy-all-regions.sh
│   ├── failover.sh
│   └── health-check.sh
└── docs/
    ├── firebase-multi-region.md
    ├── cloud-run-multi-region.md
    └── monitoring.md
```

## 🌐 Supported Platforms

### Firebase (Cloud Functions)
- Multiple function locations
- Global CDN
- Automatic failover

### Google Cloud Run
- Multi-region services
- Global load balancing
- Traffic splitting

### Vercel
- Edge Functions
- Global CDN
- Automatic geo-routing

### AWS Lambda
- Multi-region deployment
- Route 53 routing
- CloudFront integration

## 🔧 Configuration

### regions.json
Define your deployment regions:

```json
{
  "regions": [
    {
      "id": "us-central",
      "name": "US Central",
      "provider": "gcp",
      "location": "us-central1",
      "primary": true,
      "weight": 50
    },
    {
      "id": "europe-west",
      "name": "Europe West",
      "provider": "gcp",
      "location": "europe-west1",
      "primary": false,
      "weight": 30
    },
    {
      "id": "asia-east",
      "name": "Asia East",
      "provider": "gcp",
      "location": "asia-east1",
      "primary": false,
      "weight": 20
    }
  ],
  "failover": {
    "enabled": true,
    "health_check_interval": 30,
    "unhealthy_threshold": 3,
    "healthy_threshold": 2
  }
}
```

### traffic-split.json
Configure traffic routing:

```json
{
  "strategy": "geo-proximity",
  "rules": [
    {
      "region": "us-central",
      "traffic_percent": 50,
      "geo_targets": ["US", "CA", "MX"]
    },
    {
      "region": "europe-west",
      "traffic_percent": 30,
      "geo_targets": ["EU", "GB", "CH"]
    },
    {
      "region": "asia-east",
      "traffic_percent": 20,
      "geo_targets": ["JP", "CN", "SG", "IN"]
    }
  ],
  "fallback": "us-central"
}
```

## 📊 Traffic Management

### Geographic Routing
Route based on user location:

```typescript
// src/routing.ts
import { defineFlow } from '@genkit-ai/flow';

export const routingFlow = defineFlow({
  name: 'route-request',
  // ... config
}, async (input) => {
  const userLocation = input.headers['cf-ipcountry'];
  const region = selectRegion(userLocation);

  return {
    region,
    endpoint: `https://${region}.your-app.com`,
  };
});
```

### Load Balancing
Distribute traffic across regions:

```typescript
// src/loadbalancer.ts
export function selectRegion(userLocation: string): string {
  const regions = loadRegionConfig();

  // Find region by geo-proximity
  const nearestRegion = regions.find(r =>
    r.geo_targets.includes(userLocation)
  );

  // Fallback to least loaded region
  return nearestRegion?.id || getLeastLoadedRegion();
}
```

### Health-Based Routing
Route to healthy regions only:

```typescript
// src/health.ts
export async function getHealthyRegions(): Promise<Region[]> {
  const regions = loadRegionConfig();
  const healthChecks = await Promise.all(
    regions.map(r => checkRegionHealth(r))
  );

  return regions.filter((r, i) => healthChecks[i].healthy);
}
```

## 🏥 Health Checks

### Regional Health Endpoint
```typescript
// src/health.ts
export const regionalHealthFlow = defineFlow({
  name: 'regional-health',
  inputSchema: z.object({}),
  outputSchema: z.object({
    region: z.string(),
    status: z.enum(['healthy', 'degraded', 'unhealthy']),
    latency: z.number(),
    timestamp: z.string(),
  }),
}, async () => {
  const startTime = Date.now();

  // Check dependencies
  const dbHealthy = await checkDatabase();
  const aiHealthy = await checkAIModels();

  const latency = Date.now() - startTime;

  return {
    region: process.env.REGION || 'unknown',
    status: dbHealthy && aiHealthy ? 'healthy' : 'degraded',
    latency,
    timestamp: new Date().toISOString(),
  };
});
```

### Cross-Region Health Monitoring
```bash
#!/bin/bash
# scripts/health-check.sh

REGIONS=("us-central1" "europe-west1" "asia-east1")

for region in "${REGIONS[@]}"; do
  echo "Checking $region..."
  response=$(curl -sf "https://$region-app.run.app/health")

  if [ $? -eq 0 ]; then
    echo "✅ $region: healthy"
  else
    echo "❌ $region: unhealthy"
    # Trigger failover
    ./scripts/failover.sh "$region"
  fi
done
```

## 🔄 Failover Strategies

### Automatic Failover
```typescript
// src/failover.ts
export async function handleFailover(failedRegion: string) {
  const healthyRegions = await getHealthyRegions();

  if (healthyRegions.length === 0) {
    throw new Error('No healthy regions available');
  }

  // Update traffic routing
  await updateTrafficRouting({
    remove: failedRegion,
    redistribute: true,
  });

  // Notify team
  await sendAlert({
    type: 'failover',
    from: failedRegion,
    to: healthyRegions.map(r => r.id),
  });
}
```

### Manual Failover Script
```bash
#!/bin/bash
# scripts/failover.sh

FAILED_REGION=$1
BACKUP_REGION=${2:-"us-central1"}

echo "Initiating failover from $FAILED_REGION to $BACKUP_REGION"

# Update Cloud Load Balancer
gcloud compute backend-services update genkit-app \
  --global \
  --enable-logging \
  --custom-request-header="X-Failover:true"

# Route all traffic to backup region
gcloud compute url-maps invalidate-cdn-cache genkit-app-lb \
  --path="/*"

echo "Failover complete. Monitor $BACKUP_REGION"
```

## 💾 Data Synchronization

### Cross-Region Data Replication
```typescript
// src/replication.ts
import { Firestore } from '@google-cloud/firestore';

export async function replicateData(
  sourceRegion: string,
  targetRegion: string,
  collection: string
) {
  const sourceDb = new Firestore({
    projectId: process.env.PROJECT_ID,
    databaseId: `${collection}-${sourceRegion}`,
  });

  const targetDb = new Firestore({
    projectId: process.env.PROJECT_ID,
    databaseId: `${collection}-${targetRegion}`,
  });

  const snapshot = await sourceDb.collection(collection).get();
  const batch = targetDb.batch();

  snapshot.docs.forEach(doc => {
    const ref = targetDb.collection(collection).doc(doc.id);
    batch.set(ref, doc.data());
  });

  await batch.commit();
}
```

### Eventual Consistency
```typescript
// src/consistency.ts
export async function syncWithEventualConsistency(
  data: any,
  regions: string[]
) {
  // Write to primary region first
  await writeToPrimary(data);

  // Async replication to other regions
  regions.forEach(region => {
    replicateToRegion(data, region).catch(err => {
      console.error(`Replication to ${region} failed:`, err);
      // Queue for retry
      queueReplication(data, region);
    });
  });
}
```

## 📈 Monitoring & Observability

### Regional Metrics
```typescript
// src/metrics.ts
export const regionalMetricsFlow = defineFlow({
  name: 'regional-metrics',
  // ... config
}, async () => {
  const region = process.env.REGION;

  return {
    region,
    metrics: {
      requests_per_second: getRequestRate(),
      error_rate: getErrorRate(),
      p95_latency: getP95Latency(),
      active_connections: getActiveConnections(),
    },
  };
});
```

### Cross-Region Dashboard
```typescript
// src/dashboard.ts
export async function getGlobalMetrics() {
  const regions = loadRegionConfig();

  const metrics = await Promise.all(
    regions.map(async (region) => {
      const health = await fetch(`https://${region.location}-app/health`);
      const metrics = await fetch(`https://${region.location}-app/metrics`);

      return {
        region: region.id,
        health: await health.json(),
        metrics: await metrics.json(),
      };
    })
  );

  return {
    timestamp: new Date().toISOString(),
    regions: metrics,
    global: aggregateMetrics(metrics),
  };
}
```

## 💰 Cost Optimization

### Regional Pricing
Different regions have different costs:

```json
{
  "pricing": {
    "us-central1": { "cpu": 0.00002400, "memory": 0.00000250 },
    "europe-west1": { "cpu": 0.00002640, "memory": 0.00000275 },
    "asia-east1": { "cpu": 0.00002760, "memory": 0.00000290 }
  }
}
```

### Cost-Optimized Routing
```typescript
// src/cost-routing.ts
export function selectCostOptimizedRegion(
  userLocation: string,
  regions: Region[]
): Region {
  // Find regions serving user's area
  const availableRegions = regions.filter(r =>
    r.geo_targets.includes(userLocation)
  );

  // Select cheapest region with capacity
  return availableRegions.reduce((cheapest, current) => {
    if (current.pricing.total < cheapest.pricing.total &&
        current.utilization < 0.8) {
      return current;
    }
    return cheapest;
  });
}
```

## 🔐 Security & Compliance

### Data Residency
```typescript
// src/compliance.ts
export function enforceDataResidency(
  userLocation: string,
  data: any
) {
  const complianceRules = loadComplianceRules();
  const allowedRegions = complianceRules[userLocation];

  if (!allowedRegions) {
    throw new Error(`No compliant region for ${userLocation}`);
  }

  // Ensure data stays in compliant region
  return {
    region: allowedRegions[0],
    data,
    compliance: true,
  };
}
```

### Regional Encryption
```typescript
// src/encryption.ts
export async function encryptForRegion(
  data: any,
  region: string
) {
  const kmsClient = new KeyManagementServiceClient();
  const keyName = `projects/${PROJECT_ID}/locations/${region}/keyRings/genkit/cryptoKeys/data`;

  const [encrypted] = await kmsClient.encrypt({
    name: keyName,
    plaintext: Buffer.from(JSON.stringify(data)),
  });

  return encrypted.ciphertext;
}
```

## 🧪 Testing Multi-Region Setup

### Local Testing with Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  us-central:
    build: .
    environment:
      - REGION=us-central1
      - PORT=8080
    ports:
      - "8080:8080"

  europe-west:
    build: .
    environment:
      - REGION=europe-west1
      - PORT=8081
    ports:
      - "8081:8081"

  asia-east:
    build: .
    environment:
      - REGION=asia-east1
      - PORT=8082
    ports:
      - "8082:8082"

  load-balancer:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - us-central
      - europe-west
      - asia-east
```

### Integration Tests
```typescript
// tests/multi-region.test.ts
describe('Multi-Region Deployment', () => {
  it('should route to nearest region', async () => {
    const response = await fetch('http://localhost/health', {
      headers: { 'cf-ipcountry': 'US' },
    });

    const data = await response.json();
    expect(data.region).toBe('us-central1');
  });

  it('should failover to healthy region', async () => {
    // Simulate region failure
    await simulateRegionFailure('us-central1');

    const response = await fetch('http://localhost/health');
    const data = await response.json();

    expect(data.region).not.toBe('us-central1');
    expect(data.status).toBe('healthy');
  });
});
```

## 📚 Platform-Specific Guides

- [Firebase Multi-Region](./docs/firebase-multi-region.md)
- [Cloud Run Multi-Region](./docs/cloud-run-multi-region.md)
- [Vercel Edge Functions](./docs/vercel-edge.md)
- [AWS Multi-Region](./docs/aws-multi-region.md)

## 🆘 Troubleshooting

### Issue: High Cross-Region Latency
**Solution:** Enable regional caching and data replication

### Issue: Inconsistent Data Across Regions
**Solution:** Implement proper synchronization strategy

### Issue: Failover Not Triggering
**Solution:** Check health check configuration and thresholds

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/amitpatole/claude-genkit-plugin/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/amitpatole/claude-genkit-plugin/discussions)
- 📧 **Email**: amit.patole@gmail.com

---

**Ready to go global?** Choose your deployment strategy and follow the quickstart guide! 🌍
