# 🚀 AutoDevCore Load Test Report
**Test Date:** 2025-08-10 18:00:47

## 📊 Test Summary
- **Total Scenarios:** 4
- **Total Requests:** 8,460
- **Total Errors:** 404
- **Average Throughput:** 1050.46 RPS

## 📈 Scenario Results
### Light Load
- **Total Requests:** 60
- **Error Rate:** 8.33%
- **Throughput:** 29.92 RPS
- **Avg Response Time:** 1064.65ms
- **P95 Response Time:** 1928.69ms

### Medium Load
- **Total Requests:** 600
- **Error Rate:** 6.00%
- **Throughput:** 299.12 RPS
- **Avg Response Time:** 1053.72ms
- **P95 Response Time:** 1902.82ms

### Heavy Load
- **Total Requests:** 1,800
- **Error Rate:** 4.06%
- **Throughput:** 898.40 RPS
- **Avg Response Time:** 1057.07ms
- **P95 Response Time:** 1897.54ms

### Stress Test
- **Total Requests:** 6,000
- **Error Rate:** 4.83%
- **Throughput:** 2974.38 RPS
- **Avg Response Time:** 1050.71ms
- **P95 Response Time:** 1901.19ms

## 🔍 Performance Analysis
**Best Throughput:** Stress Test (2974.38 RPS)
**Slowest Response:** Light Load (1064.65ms)

## 💡 Recommendations
- 📊 **Monitor system resources** during peak load
- 🔄 **Implement caching** for frequently accessed data
- ⚡ **Consider horizontal scaling** for higher loads
