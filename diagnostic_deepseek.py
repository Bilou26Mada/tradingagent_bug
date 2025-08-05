#!/usr/bin/env python3
"""
Script de diagnostic complet pour les problèmes DeepSeek
"""
import requests
import sys
import os
import subprocess
import time

def test_network_connectivity():
    """Test la connectivité réseau de base"""
    print("🌐 Test de connectivité réseau...")
    print("=" * 50)
    
    try:
        # Test ping vers Google
        result = subprocess.run(['ping', '-c', '3', '8.8.8.8'], 
                              capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            print("✅ Connectivité internet: OK")
        else:
            print("❌ Connectivité internet: PROBLÈME")
            return False
    except:
        print("⚠️ Impossible de tester la connectivité")
    
    return True

def test_deepseek_endpoint():
    """Test l'endpoint DeepSeek"""
    print("\n🔗 Test endpoint DeepSeek...")
    print("=" * 50)
    
    try:
        response = requests.get("https://api.deepseek.com/v1", timeout=10)
        print(f"✅ DeepSeek endpoint accessible: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        return True
    except requests.exceptions.Timeout:
        print("❌ Timeout: DeepSeek endpoint inaccessible (>10s)")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Erreur de connexion: DeepSeek endpoint inaccessible")
        return False
    except Exception as e:
        print(f"❌ Erreur DeepSeek endpoint: {e}")
        return False

def test_deepseek_api():
    """Test l'API DeepSeek avec la vraie clé"""
    print("\n🧠 Test API DeepSeek...")
    print("=" * 50)
    
    api_key = "sk-15a5df3514064313b15f2127ebd6c22c"
    
    try:
        start_time = time.time()
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": "Test connexion"}],
                "max_tokens": 10
            },
            timeout=20
        )
        
        end_time = time.time()
        latency = round((end_time - start_time) * 1000)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API DeepSeek fonctionnelle")
            print(f"   Modèle: {data.get('model')}")
            print(f"   Latence: {latency}ms")
            print(f"   Réponse: {data['choices'][0]['message']['content']}")
            return True
        else:
            print(f"❌ API DeepSeek erreur: {response.status_code}")
            print(f"   Réponse: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout API DeepSeek (>20s)")
        return False
    except Exception as e:
        print(f"❌ Erreur API DeepSeek: {e}")
        return False

def test_langchain_deepseek():
    """Test DeepSeek via LangChain"""
    print("\n🔗 Test LangChain + DeepSeek...")
    print("=" * 50)
    
    try:
        sys.path.append("/app/TradingAgents")
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(
            model="deepseek-chat",
            base_url="https://api.deepseek.com/v1",
            api_key="sk-15a5df3514064313b15f2127ebd6c22c",
            temperature=0.1,
            timeout=15
        )
        
        response = llm.invoke("Test LangChain")
        print(f"✅ LangChain + DeepSeek fonctionnel")
        print(f"   Réponse: {response.content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Erreur LangChain + DeepSeek: {e}")
        return False

def test_backend_endpoints():
    """Test les endpoints backend"""
    print("\n🖥️ Test endpoints backend...")
    print("=" * 50)
    
    endpoints = [
        ("Status", "GET", "http://localhost:8001/api/trading/status"),
        ("Network Status", "GET", "http://localhost:8001/api/trading/network-status"),
        ("Test DeepSeek", "GET", "http://localhost:8001/api/trading/test-deepseek")
    ]
    
    for name, method, url in endpoints:
        try:
            if method == "GET":
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(url, timeout=10)
                
            if response.status_code == 200:
                print(f"✅ {name}: OK")
            else:
                print(f"❌ {name}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {name}: Erreur - {e}")

def main():
    """Diagnostic complet"""
    print("🔍 DIAGNOSTIC COMPLET DEEPSEEK")
    print("=" * 80)
    print()
    
    tests = [
        ("Connectivité Réseau", test_network_connectivity),
        ("Endpoint DeepSeek", test_deepseek_endpoint),
        ("API DeepSeek", test_deepseek_api),
        ("LangChain + DeepSeek", test_langchain_deepseek),
        ("Endpoints Backend", test_backend_endpoints)
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n❌ Erreur lors du test {name}: {e}")
            results[name] = False
    
    # Résumé
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 80)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
    
    # Conclusions
    if all(results.values()):
        print("\n🎉 TOUT FONCTIONNE ! Aucun problème détecté.")
    else:
        print("\n⚠️ PROBLÈMES DÉTECTÉS:")
        for name, result in results.items():
            if not result:
                print(f"   • {name}")
        
        print("\n🔧 ACTIONS RECOMMANDÉES:")
        if not results.get("Connectivité Réseau", True):
            print("   • Vérifiez votre connexion internet")
        if not results.get("Endpoint DeepSeek", True):
            print("   • DeepSeek peut être temporairement indisponible")
        if not results.get("API DeepSeek", True):
            print("   • Vérifiez la validité de votre clé API DeepSeek")
        if not results.get("LangChain + DeepSeek", True):
            print("   • Vérifiez l'installation de LangChain")

if __name__ == "__main__":
    main()