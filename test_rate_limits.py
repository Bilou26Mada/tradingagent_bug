#!/usr/bin/env python3
"""
Test des rate limits et timeouts DeepSeek
"""
import requests
import time
import json
from datetime import datetime

def test_deepseek_rate_limits():
    """Test rate limits DeepSeek"""
    print("🔍 Test Rate Limits DeepSeek")
    print("=" * 50)
    
    api_key = "sk-15a5df3514064313b15f2127ebd6c22c"
    url = "https://api.deepseek.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    results = []
    
    # Test 5 requêtes rapides
    for i in range(5):
        try:
            start_time = time.time()
            
            response = requests.post(
                url,
                headers=headers,
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": f"Test {i+1}"}],
                    "max_tokens": 5
                },
                timeout=15
            )
            
            end_time = time.time()
            latency = round((end_time - start_time) * 1000)
            
            if response.status_code == 200:
                data = response.json()
                results.append({
                    "test": i+1,
                    "status": "✅ OK",
                    "latency": f"{latency}ms",
                    "tokens": data.get("usage", {}).get("total_tokens", 0)
                })
                print(f"Test {i+1}: ✅ OK ({latency}ms, {data.get('usage', {}).get('total_tokens', 0)} tokens)")
            elif response.status_code == 429:
                results.append({
                    "test": i+1,
                    "status": "❌ RATE LIMIT",
                    "latency": f"{latency}ms",
                    "error": "Too many requests"
                })
                print(f"Test {i+1}: ❌ RATE LIMIT ({latency}ms)")
            else:
                results.append({
                    "test": i+1,
                    "status": f"❌ HTTP {response.status_code}",
                    "latency": f"{latency}ms",
                    "error": response.text[:100]
                })
                print(f"Test {i+1}: ❌ HTTP {response.status_code} ({latency}ms)")
                
        except requests.exceptions.Timeout:
            results.append({
                "test": i+1,
                "status": "❌ TIMEOUT",
                "latency": ">15000ms",
                "error": "Request timeout"
            })
            print(f"Test {i+1}: ❌ TIMEOUT (>15s)")
            
        except Exception as e:
            results.append({
                "test": i+1,
                "status": "❌ ERROR",
                "latency": "N/A",
                "error": str(e)
            })
            print(f"Test {i+1}: ❌ ERROR - {e}")
        
        # Pause entre les tests
        time.sleep(1)
    
    return results

def test_backend_endpoints():
    """Test des endpoints backend"""
    print("\n🔍 Test Endpoints Backend")
    print("=" * 50)
    
    endpoints = [
        ("Status", "GET", "http://localhost:8001/api/trading/status"),
        ("DeepSeek Quick", "GET", "http://localhost:8001/api/trading/test-deepseek-quick"),
        ("Network Status", "GET", "http://localhost:8001/api/trading/network-status")
    ]
    
    for name, method, url in endpoints:
        try:
            start_time = time.time()
            
            if method == "GET":
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(url, timeout=10)
            
            end_time = time.time()
            latency = round((end_time - start_time) * 1000)
            
            if response.status_code == 200:
                print(f"{name}: ✅ OK ({latency}ms)")
            else:
                print(f"{name}: ❌ HTTP {response.status_code} ({latency}ms)")
                
        except requests.exceptions.Timeout:
            print(f"{name}: ❌ TIMEOUT (>10s)")
        except Exception as e:
            print(f"{name}: ❌ ERROR - {e}")

def test_analysis_endpoint():
    """Test endpoint d'analyse"""
    print("\n🔍 Test Analyse TradingAgents")
    print("=" * 50)
    
    try:
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:8001/api/trading/analyze",
            headers={"Content-Type": "application/json"},
            json={
                "ticker": "TSLA",
                "analysis_date": "2024-05-10",
                "analysts": ["market"],
                "research_depth": 1
            },
            timeout=40  # Long timeout pour l'analyse
        )
        
        end_time = time.time()
        latency = round((end_time - start_time) * 1000)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Analyse TSLA: ✅ {data.get('status')} ({latency}ms)")
            print(f"Message: {data.get('message')}")
            return True
        else:
            print(f"Analyse TSLA: ❌ HTTP {response.status_code} ({latency}ms)")
            print(f"Erreur: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("Analyse TSLA: ❌ TIMEOUT (>40s)")
        return False
    except Exception as e:
        print(f"Analyse TSLA: ❌ ERROR - {e}")
        return False

def main():
    print("🧪 TEST COMPLET - RATE LIMITS & TIMEOUTS")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Test 1: Rate limits DeepSeek
    deepseek_results = test_deepseek_rate_limits()
    
    # Test 2: Endpoints backend
    test_backend_endpoints()
    
    # Test 3: Analyse complète
    analysis_ok = test_analysis_endpoint()
    
    # Résumé
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 80)
    
    deepseek_ok = sum(1 for r in deepseek_results if "✅" in r["status"])
    print(f"DeepSeek API: {deepseek_ok}/5 tests réussis")
    
    rate_limits = sum(1 for r in deepseek_results if "RATE LIMIT" in r["status"])
    if rate_limits > 0:
        print(f"⚠️  RATE LIMITS détectés: {rate_limits} requêtes bloquées")
    
    timeouts = sum(1 for r in deepseek_results if "TIMEOUT" in r["status"])
    if timeouts > 0:
        print(f"⚠️  TIMEOUTS détectés: {timeouts} requêtes timeout")
    
    print(f"Analyse TradingAgents: {'✅ OK' if analysis_ok else '❌ ÉCHEC'}")
    
    # Recommandations
    if rate_limits > 0 or timeouts > 0:
        print("\n🔧 RECOMMANDATIONS:")
        if rate_limits > 0:
            print("• Ajouter des délais entre les requêtes DeepSeek")
            print("• Implémenter un système de retry avec backoff")
        if timeouts > 0:
            print("• Augmenter les timeouts pour DeepSeek")
            print("• Optimiser les requêtes pour réduire la latence")
    else:
        print("\n✅ AUCUN PROBLÈME DE RATE LIMIT OU TIMEOUT DÉTECTÉ")

if __name__ == "__main__":
    main()