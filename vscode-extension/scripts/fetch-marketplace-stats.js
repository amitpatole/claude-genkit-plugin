#!/usr/bin/env node

/**
 * VS Code Marketplace Statistics Fetcher
 *
 * This script fetches download and usage statistics for your VS Code extension
 * from the Visual Studio Marketplace API.
 *
 * Usage:
 *   node scripts/fetch-marketplace-stats.js
 *   node scripts/fetch-marketplace-stats.js --json
 *   node scripts/fetch-marketplace-stats.js --log >> stats-history.log
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Configuration
const EXTENSION_ID = 'amitpatole.genkit-vscode';
const PUBLISHER_NAME = 'amitpatole';
const EXTENSION_NAME = 'genkit-vscode';

// Parse command line arguments
const args = process.argv.slice(2);
const outputJson = args.includes('--json');
const outputLog = args.includes('--log');

/**
 * Fetch extension statistics from VS Code Marketplace API
 */
function fetchMarketplaceStats() {
    return new Promise((resolve, reject) => {
        const postData = JSON.stringify({
            filters: [{
                criteria: [
                    { filterType: 7, value: EXTENSION_ID }
                ],
                pageSize: 1
            }],
            flags: 914  // Flags to include: Statistics, Versions, Files, etc.
        });

        const options = {
            hostname: 'marketplace.visualstudio.com',
            port: 443,
            path: '/_apis/public/gallery/extensionquery',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json;api-version=3.0-preview.1',
                'Content-Length': Buffer.byteLength(postData)
            }
        };

        const req = https.request(options, (res) => {
            let data = '';

            res.on('data', (chunk) => {
                data += chunk;
            });

            res.on('end', () => {
                if (res.statusCode === 200) {
                    try {
                        const json = JSON.parse(data);
                        resolve(json);
                    } catch (error) {
                        reject(new Error(`Failed to parse response: ${error.message}`));
                    }
                } else {
                    reject(new Error(`HTTP ${res.statusCode}: ${data}`));
                }
            });
        });

        req.on('error', (error) => {
            reject(error);
        });

        req.write(postData);
        req.end();
    });
}

/**
 * Extract relevant statistics from the API response
 */
function extractStatistics(response) {
    if (!response.results || response.results.length === 0) {
        throw new Error('No extension found in marketplace');
    }

    const extension = response.results[0].extensions[0];
    if (!extension) {
        throw new Error('Extension data not found');
    }

    const statistics = {};
    if (extension.statistics) {
        extension.statistics.forEach(stat => {
            statistics[stat.statisticName] = stat.value;
        });
    }

    const versions = extension.versions || [];
    const latestVersion = versions[0] || {};

    return {
        extensionId: EXTENSION_ID,
        extensionName: extension.displayName || EXTENSION_NAME,
        publisher: extension.publisher?.publisherName || PUBLISHER_NAME,
        version: latestVersion.version || 'unknown',
        lastUpdated: latestVersion.lastUpdated || extension.lastUpdated,
        releaseDate: extension.releaseDate,
        publishedDate: extension.publishedDate,
        statistics: {
            install: statistics.install || 0,
            averagerating: statistics.averagerating || 0,
            ratingcount: statistics.ratingcount || 0,
            trendingdaily: statistics.trendingdaily || 0,
            trendingmonthly: statistics.trendingmonthly || 0,
            trendingweekly: statistics.trendingweekly || 0,
            updateCount: statistics.updateCount || 0,
            weightedRating: statistics.weightedRating || 0
        },
        timestamp: new Date().toISOString()
    };
}

/**
 * Format statistics for display
 */
function formatStats(stats) {
    const lines = [
        '',
        '┌─────────────────────────────────────────────────────────────┐',
        '│     VS Code Extension Marketplace Statistics               │',
        '├─────────────────────────────────────────────────────────────┤',
        `│ Extension: ${stats.extensionName.padEnd(45)} │`,
        `│ Publisher: ${stats.publisher.padEnd(45)} │`,
        `│ Version: ${stats.version.padEnd(47)} │`,
        '├─────────────────────────────────────────────────────────────┤',
        `│ Total Installs:        ${String(stats.statistics.install).padStart(32)} │`,
        `│ Average Rating:        ${String(stats.statistics.averagerating.toFixed(2)).padStart(32)} │`,
        `│ Rating Count:          ${String(stats.statistics.ratingcount).padStart(32)} │`,
        `│ Weighted Rating:       ${String(stats.statistics.weightedRating.toFixed(2)).padStart(32)} │`,
        '├─────────────────────────────────────────────────────────────┤',
        `│ Trending Daily:        ${String(stats.statistics.trendingdaily).padStart(32)} │`,
        `│ Trending Weekly:       ${String(stats.statistics.trendingweekly).padStart(32)} │`,
        `│ Trending Monthly:      ${String(stats.statistics.trendingmonthly).padStart(32)} │`,
        `│ Update Count:          ${String(stats.statistics.updateCount).padStart(32)} │`,
        '├─────────────────────────────────────────────────────────────┤',
        `│ Last Updated: ${new Date(stats.lastUpdated).toLocaleString().padEnd(41)} │`,
        `│ Fetched At: ${new Date(stats.timestamp).toLocaleString().padEnd(43)} │`,
        '└─────────────────────────────────────────────────────────────┘',
        ''
    ];

    return lines.join('\n');
}

/**
 * Format statistics for log file (CSV-like format)
 */
function formatLogEntry(stats) {
    return `${stats.timestamp},${stats.version},${stats.statistics.install},${stats.statistics.averagerating},${stats.statistics.ratingcount},${stats.statistics.trendingdaily},${stats.statistics.trendingweekly},${stats.statistics.trendingmonthly}`;
}

/**
 * Save statistics to a JSON file
 */
function saveStatsToFile(stats) {
    const statsDir = path.join(__dirname, '..', 'stats');
    if (!fs.existsSync(statsDir)) {
        fs.mkdirSync(statsDir, { recursive: true });
    }

    const filename = `stats-${new Date().toISOString().split('T')[0]}.json`;
    const filepath = path.join(statsDir, filename);

    // Load existing stats if file exists
    let existingStats = [];
    if (fs.existsSync(filepath)) {
        try {
            existingStats = JSON.parse(fs.readFileSync(filepath, 'utf8'));
        } catch (error) {
            console.error('Warning: Could not read existing stats file');
        }
    }

    // Append new stats
    existingStats.push(stats);

    // Save to file
    fs.writeFileSync(filepath, JSON.stringify(existingStats, null, 2));

    return filepath;
}

/**
 * Main execution
 */
async function main() {
    try {
        console.error('Fetching marketplace statistics...');

        const response = await fetchMarketplaceStats();
        const stats = extractStatistics(response);

        if (outputJson) {
            // Output as JSON
            console.log(JSON.stringify(stats, null, 2));
        } else if (outputLog) {
            // Output as log entry (CSV format)
            console.log(formatLogEntry(stats));
        } else {
            // Output formatted table
            console.log(formatStats(stats));

            // Save to file
            const filepath = saveStatsToFile(stats);
            console.error(`\n✅ Statistics saved to: ${filepath}`);
            console.error(`📊 View marketplace: https://marketplace.visualstudio.com/items?itemName=${EXTENSION_ID}`);
            console.error(`⚙️  Manage publisher: https://marketplace.visualstudio.com/manage/publishers/${PUBLISHER_NAME}\n`);
        }

        process.exit(0);
    } catch (error) {
        console.error(`\n❌ Error fetching marketplace statistics:`);
        console.error(`   ${error.message}\n`);
        process.exit(1);
    }
}

// Run if executed directly
if (require.main === module) {
    main();
}

module.exports = { fetchMarketplaceStats, extractStatistics };
