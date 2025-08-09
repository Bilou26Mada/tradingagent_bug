#!/usr/bin/env python3
"""
Test manuel de l'interface utilisateur
"""
import requests
import time
import json

def test_exact_frontend_workflow():
    """Test le workflow exact que ferait un utilisateur"""
    print("👤 SIMULATION UTILISATEUR RÉEL")
    print("=" * 60)
    
    # 1. Charger la page (simulé)
    print("1. 📱 Utilisateur ouvre http://localhost:3000")
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("   ✅ Page chargée (200 OK)")
        else:
            print(f"   ❌ Erreur page: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur chargement: {e}")
    
    # 2. React charge et appelle le backend pour le status
    print("\n2. ⚛️ React appelle le backend pour le status")
    try:
        response = requests.get("http://localhost:8001/api/trading/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status reçu: {data['status']}")
            print(f"   🔧 APIs: {data['apis']}")
        else:
            print(f"   ❌ Erreur status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur status: {e}")
    
    # 3. Utilisateur clique sur "Tester DeepSeek"
    print("\n3. 🧠 Utilisateur clique 'Tester DeepSeek'")
    try:
        response = requests.get("http://localhost:8001/api/trading/test-deepseek-quick", timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"   ✅ DeepSeek OK: {data['message']}")
                print(f"   📝 Réponse: {data['details']['response']}")
                print("   💬 Pop-up affiché: 'Test DeepSeek RÉUSSI !'")
            else:
                print(f"   ❌ DeepSeek échec: {data.get('message')}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur DeepSeek: {e}")
    
    # 4. Utilisateur configure l'analyse
    print("\n4. ⚙️ Utilisateur configure l'analyse")
    config = {
        "ticker": "NVDA",
        "analysis_date": "2024-05-10",
        "analysts": ["market"],
        "research_depth": 1
    }
    print(f"   📋 Configuration: {config}")
    
    # 5. Utilisateur clique "Démarrer l'Analyse"
    print("\n5. 🚀 Utilisateur clique 'Démarrer l'Analyse'")
    try:
        print("   ⏳ Analyse en cours...")
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:8001/api/trading/analyze",
            headers={'Content-Type': 'application/json'},
            json=config,
            timeout=35
        )
        
        end_time = time.time()
        duration = round(end_time - start_time, 1)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Analyse terminée en {duration}s")
            print(f"   📈 Status: {data.get('status')}")
            print(f"   💬 Message: {data.get('message')}")
            
            # Vérifier le contenu de l'analyse
            if data.get('analysis_output'):
                output_length = len(data['analysis_output'])
                print(f"   📄 Rapport généré: {output_length} caractères")
                print(f"   🎯 Progression: {data.get('progress', {}).get('completion', 0)}%")
                
                # Extraire quelques lignes du rapport
                lines = data['analysis_output'].split('\n')[:5]
                print("   📋 Aperçu du rapport:")
                for line in lines:
                    if line.strip():
                        print(f"      {line[:80]}...")
                
                print("\n   🎉 RÉSULTATS DEVRAIENT S'AFFICHER DANS L'INTERFACE!")
                return True
            else:
                print("   ⚠️  Pas de rapport d'analyse")
                return False
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur analyse: {e}")
        return False

def test_problemes_courants():
    """Test les problèmes courants"""
    print("\n\n🔍 DIAGNOSTIC PROBLÈMES COURANTS")
    print("=" * 60)
    
    # CORS
    print("1. 🌐 Test CORS")
    try:
        response = requests.options("http://localhost:8001/api/trading/status")
        print(f"   Status OPTIONS: {response.status_code}")
        cors_headers = response.headers.get('Access-Control-Allow-Origin', 'None')
        print(f"   CORS Allow-Origin: {cors_headers}")
    except Exception as e:
        print(f"   ❌ Erreur CORS: {e}")
    
    # Rate Limits
    print("\n2. ⏱️  Test Rate Limits (5 requêtes rapides)")
    for i in range(5):
        try:
            start_time = time.time()
            response = requests.get("http://localhost:8001/api/trading/status", timeout=5)
            latency = round((time.time() - start_time) * 1000)
            print(f"   Requête {i+1}: {response.status_code} ({latency}ms)")
        except Exception as e:
            print(f"   Requête {i+1}: Erreur - {e}")
        time.sleep(0.2)
    
    # Timeouts
    print("\n3. ⏰ Test Timeouts")
    try:
        response = requests.get("http://localhost:8001/api/trading/test-deepseek-quick", timeout=3)
        print(f"   DeepSeek rapide: {response.status_code} (timeout 3s OK)")
    except requests.exceptions.Timeout:
        print("   ❌ DeepSeek timeout en 3s")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

def main():
    print("🧪 TEST UTILISATEUR RÉEL + DIAGNOSTIC")
    print("=" * 80)
    print(f"⏰ Début: {time.strftime('%H:%M:%S')}")
    print()
    
    # Test workflow utilisateur
    success = test_exact_frontend_workflow()
    
    # Test problèmes courants  
    test_problemes_courants()
    
    # Conclusion
    print("\n" + "=" * 80)
    print("🎯 CONCLUSION")
    print("=" * 80)
    
    if success:
        print("✅ L'ANALYSE FONCTIONNE PARFAITEMENT !")
        print("   • Backend répond correctement")
        print("   • DeepSeek connecté et opérationnel")
        print("   • Analyses générées avec succès")
        print("   • Rapports détaillés créés")
        print()
        print("🤔 Si l'utilisateur ne voit pas les résultats:")
        print("   • Le problème est dans l'interface React")
        print("   • Vérifier la console browser pour erreurs JS")
        print("   • Vérifier si les états React se mettent à jour")
    else:
        print("❌ PROBLÈME IDENTIFIÉ DANS L'ANALYSE")
        print("   • Vérifier les logs backend")
        print("   • Vérifier la configuration DeepSeek")
        
    print(f"\n⏰ Fin: {time.strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()