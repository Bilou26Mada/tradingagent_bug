#!/usr/bin/env python3
"""
Test final complet de tous les composants
"""
import requests
import time
import json
from datetime import datetime

def test_complete_workflow():
    """Test du workflow complet"""
    print("🧪 TEST WORKFLOW COMPLET - TRADINGAGENTS")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    backend_url = "http://localhost:8001"
    results = {}
    
    # Test 1: Status backend
    print("1️⃣  Test Status Backend...")
    try:
        response = requests.get(f"{backend_url}/api/trading/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Backend en ligne: {data['status']}")
            results['backend'] = True
        else:
            print(f"   ❌ Backend erreur: {response.status_code}")
            results['backend'] = False
    except Exception as e:
        print(f"   ❌ Backend inaccessible: {e}")
        results['backend'] = False
    
    # Test 2: DeepSeek rapide
    print("\n2️⃣  Test DeepSeek Rapide...")
    try:
        start_time = time.time()
        response = requests.get(f"{backend_url}/api/trading/test-deepseek-quick", timeout=15)
        latency = round((time.time() - start_time) * 1000)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"   ✅ DeepSeek OK: {data['message']} ({latency}ms)")
                print(f"   📊 Réponse: {data['details']['response']}")
                results['deepseek'] = True
            else:
                print(f"   ❌ DeepSeek échec: {data['message']}")
                results['deepseek'] = False
        else:
            print(f"   ❌ DeepSeek erreur HTTP: {response.status_code}")
            results['deepseek'] = False
    except Exception as e:
        print(f"   ❌ DeepSeek erreur: {e}")
        results['deepseek'] = False
    
    # Test 3: Analyse complète
    print("\n3️⃣  Test Analyse TradingAgents Complète...")
    try:
        start_time = time.time()
        response = requests.post(
            f"{backend_url}/api/trading/analyze",
            headers={'Content-Type': 'application/json'},
            json={
                'ticker': 'NVDA',
                'analysis_date': '2024-05-10', 
                'analysts': ['market'],
                'research_depth': 1
            },
            timeout=35
        )
        latency = round((time.time() - start_time) * 1000)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'completed':
                print(f"   ✅ Analyse terminée: {data['message']} ({latency}ms)")
                print(f"   📈 Ticker: {data['configuration']['ticker']}")
                print(f"   🤖 Modèle: {data['configuration']['llm_model']}")
                
                # Vérifier qu'il y a bien un rapport
                if data.get('analysis_output'):
                    print(f"   📄 Rapport généré: {len(data['analysis_output'])} caractères")
                    results['analysis'] = True
                else:
                    print(f"   ⚠️  Pas de rapport d'analyse")
                    results['analysis'] = False
            else:
                print(f"   ❌ Analyse incomplète: {data.get('status')} - {data.get('message')}")
                results['analysis'] = False
        else:
            print(f"   ❌ Analyse erreur HTTP: {response.status_code}")
            results['analysis'] = False
    except Exception as e:
        print(f"   ❌ Analyse erreur: {e}")
        results['analysis'] = False
    
    # Test 4: Frontend accessibility
    print("\n4️⃣  Test Accessibilité Frontend...")
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200 and "TradingAgents" in response.text:
            print("   ✅ Frontend accessible et contient TradingAgents")
            results['frontend'] = True
        else:
            print("   ❌ Frontend problème ou contenu incorrect")
            results['frontend'] = False
    except Exception as e:
        print(f"   ❌ Frontend inaccessible: {e}")
        results['frontend'] = False
    
    # Test 5: Configuration frontend
    print("\n5️⃣  Test Configuration Frontend...")
    try:
        with open('/app/frontend/.env', 'r') as f:
            env_content = f.read()
        
        if 'REACT_APP_BACKEND_URL=http://localhost:8001' in env_content:
            print("   ✅ URL backend correctement configurée")
            results['frontend_config'] = True  
        else:
            print("   ❌ URL backend mal configurée")
            print(f"   📋 Contenu .env: {env_content}")
            results['frontend_config'] = False
    except Exception as e:
        print(f"   ❌ Erreur lecture config: {e}")
        results['frontend_config'] = False
    
    # Résumé final
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ FINAL DES TESTS")
    print("=" * 80)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name.replace('_', ' ').title()}")
    
    print(f"\n🎯 Score: {passed_tests}/{total_tests} tests réussis")
    
    if passed_tests == total_tests:
        print("\n🎉 TOUS LES TESTS RÉUSSIS !")
        print("L'application TradingAgents est 100% fonctionnelle !")
        print("✅ Backend opérationnel")
        print("✅ DeepSeek connecté")
        print("✅ Analyses fonctionnelles") 
        print("✅ Frontend accessible")
        print("✅ Configuration correcte")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} PROBLÈME(S) DÉTECTÉ(S)")
        
        failed_tests = [name for name, result in results.items() if not result]
        print("📋 Tests échoués:")
        for test in failed_tests:
            print(f"   • {test.replace('_', ' ').title()}")
        
        print("\n🔧 Actions recommandées:")
        if not results.get('backend'):
            print("   • Redémarrer le backend: sudo supervisorctl restart backend")
        if not results.get('deepseek'):
            print("   • Vérifier la clé API DeepSeek")
        if not results.get('frontend'):
            print("   • Redémarrer le frontend: sudo supervisorctl restart frontend")
        if not results.get('frontend_config'):
            print("   • Corriger l'URL backend dans /app/frontend/.env")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = test_complete_workflow()
    exit(0 if success else 1)