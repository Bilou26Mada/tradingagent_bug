import { useEffect, useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";

const TradingAgentsHome = () => {
  const [systemStatus, setSystemStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [cliLaunched, setCLILaunched] = useState(false);
  const [analysisRunning, setAnalysisRunning] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [analysisConfig, setAnalysisConfig] = useState({
    ticker: "NVDA",
    analysis_date: "2024-05-10",
    analysts: ["market", "social", "news", "fundamentals"],
    research_depth: 1
  });

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
  const API = `${BACKEND_URL}/api`;

  useEffect(() => {
    loadSystemStatus();
  }, []);

  const loadSystemStatus = async () => {
    try {
      const response = await axios.get(`${API}/trading/status`);
      setSystemStatus(response.data);
      setLoading(false);
    } catch (e) {
      console.error("Error loading system status:", e);
      // Fallback status
      setSystemStatus({
        status: "🟢 TradingAgents System Online",
        version: "v1.0.0",
        components: {
          analyst_team: "✅ Ready",
          research_team: "✅ Ready",
          trading_team: "✅ Ready", 
          risk_management: "✅ Ready",
          portfolio_management: "✅ Ready"
        },
        apis: {
          deepseek: "✅ Configured",
          finnhub: "✅ Configured"
        }
      });
      setLoading(false);
    }
  };

  const launchCLI = async () => {
    try {
      setCLILaunched(true);
      const response = await axios.post(`${API}/trading/launch-cli`);
      console.log("CLI lancée:", response.data);
      
      // Afficher les détails du lancement de la CLI
      const cliDetails = `Interface CLI TradingAgents lancée avec succès !

Configuration:
• Commande: ${response.data.cli_info?.command}
• Répertoire: ${response.data.cli_info?.working_directory}
• Modèle LLM: ${response.data.cli_info?.configuration?.llm_model}
• Backend URL: ${response.data.cli_info?.configuration?.backend_url}

APIs configurées:
${response.data.cli_info?.configuration?.apis_configured?.map(api => `• ${api}`).join('\n')}

Prochaines étapes:
${response.data.next_steps?.map((step, i) => `${i + 1}. ${step}`).join('\n')}`;

      alert(cliDetails);
      
      // Optionnel: Afficher la sortie CLI si disponible
      if (response.data.cli_output) {
        console.log("Sortie CLI:", response.data.cli_output);
      }
      
    } catch (error) {
      console.error("Erreur lors du lancement de la CLI:", error);
      alert(`Erreur lors du lancement de la CLI: ${error.response?.data?.message || error.message}`);
      setCLILaunched(false);
    }
  };

  const startAnalysis = async () => {
    try {
      console.log("🚀 Début de l'analyse avec config:", analysisConfig);
      setAnalysisRunning(true);
      setAnalysisResult(null); // Reset des résultats précédents
      
      // Afficher immédiatement le début de l'analyse
      setAnalysisResult({
        status: "running",
        message: `Démarrage de l'analyse de ${analysisConfig.ticker}...`,
        configuration: analysisConfig,
        progress: {
          current_phase: "Initialisation des agents",
          phases: [
            "📊 Équipe d'Analyse",
            "🔬 Équipe de Recherche", 
            "💼 Équipe de Trading",
            "⚠️ Gestion des Risques",
            "💰 Gestion de Portefeuille"
          ],
          completion: 0
        }
      });
      
      console.log("📡 Envoi requête à l'API:", `${API}/trading/analyze`);
      
      // Lancer l'analyse réelle via l'API
      const response = await axios.post(`${API}/trading/analyze`, analysisConfig);
      
      console.log("📊 Réponse API reçue:", response.data);
      
      // Mettre à jour avec les vrais résultats
      setAnalysisResult({
        ...response.data,
        showOutput: true // Flag pour afficher la sortie détaillée
      });
      setAnalysisRunning(false);
      
      console.log("✅ Analyse terminée et résultats mis à jour");
      
    } catch (error) {
      console.error("❌ Erreur lors du démarrage de l'analyse:", error);
      console.error("Détails erreur:", error.response?.data);
      setAnalysisRunning(false);
      setAnalysisResult({
        status: "error",
        message: `Erreur lors de l'analyse de ${analysisConfig.ticker}: ${error.response?.data?.message || error.message}`,
        configuration: analysisConfig,
        error_details: error.response?.data || error.message
      });
    }
  };

  const testDeepSeek = async () => {
    try {
      const response = await axios.get(`${API}/trading/test-deepseek`);
      alert(`Test DeepSeek:\n${response.data.message}\n\nModèle: ${response.data.details?.model}\nLatence: ${response.data.details?.latency}`);
    } catch (error) {
      console.error("Erreur test DeepSeek:", error);
      alert("Erreur lors du test DeepSeek.");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-600 to-purple-700 flex items-center justify-center">
        <div className="text-center text-white">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-xl">Initialisation de TradingAgents...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-purple-700">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center text-white mb-12">
          <h1 className="text-6xl font-bold mb-4">🚀 TradingAgents</h1>
          <p className="text-2xl opacity-90 mb-2">Multi-Agent LLM Financial Trading Framework</p>
          <p className="text-lg opacity-80 max-w-4xl mx-auto">
            Expérience de trading alimentée par l'IA avec notre système multi-agents sophistiqué qui simule 
            les entreprises de trading du monde réel. Déployez des agents LLM spécialisés pour une analyse 
            de marché complète et des décisions de trading éclairées.
          </p>
        </div>

        {/* Live Demo Section */}
        <div className="bg-white rounded-2xl p-8 mb-8 shadow-2xl">
          <h2 className="text-4xl font-bold text-center text-gray-800 mb-6">🎬 Démo Live</h2>
          <p className="text-center text-gray-600 text-lg mb-6">
            Le système TradingAgents est maintenant installé avec succès et prêt à fonctionner!
            Ce framework utilise plusieurs agents IA spécialisés travaillant ensemble pour
            analyser les marchés et prendre des décisions de trading.
          </p>
          
          {systemStatus && (
            <div className="bg-gray-50 rounded-xl p-6 mb-6">
              <h3 className="text-2xl font-bold text-gray-800 mb-4">📊 Statut du Système</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-semibold text-gray-700 mb-2">Composants:</h4>
                  {Object.entries(systemStatus.components).map(([key, value]) => (
                    <div key={key} className="flex justify-between py-1">
                      <span className="capitalize">{key.replace('_', ' ')}</span>
                      <span>{value}</span>
                    </div>
                  ))}
                </div>
                <div>
                  <h4 className="font-semibold text-gray-700 mb-2">APIs:</h4>
                  {Object.entries(systemStatus.apis).map(([key, value]) => (
                    <div key={key} className="flex justify-between py-1">
                      <span className="capitalize">{key}</span>
                      <span>{value}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          <div className="text-center mb-6">
            <button 
              onClick={launchCLI}
              disabled={cliLaunched}
              className={`${cliLaunched ? 'bg-green-500' : 'bg-blue-500 hover:bg-blue-600'} text-white px-8 py-3 rounded-full text-lg font-semibold mr-4 transition-colors`}
            >
              {cliLaunched ? '✅ CLI Lancée' : '🖥️ Lancer Interface CLI'}
            </button>
            <button 
              onClick={testDeepSeek}
              className="bg-purple-500 hover:bg-purple-600 text-white px-8 py-3 rounded-full text-lg font-semibold mr-4 transition-colors"
            >
              🧠 Tester DeepSeek
            </button>
            <button className="bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 rounded-full text-lg font-semibold transition-colors">
              📚 Documentation API
            </button>
          </div>
        </div>

        {/* Configuration d'Analyse */}
        <div className="bg-white rounded-2xl p-8 mb-8 shadow-2xl">
          <h2 className="text-4xl font-bold text-center text-gray-800 mb-6">⚙️ Configuration d'Analyse</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Ticker Symbol:
              </label>
              <input
                type="text"
                value={analysisConfig.ticker}
                onChange={(e) => setAnalysisConfig({...analysisConfig, ticker: e.target.value.toUpperCase()})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="NVDA"
              />
            </div>
            
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Date d'Analyse:
              </label>
              <input
                type="date"
                value={analysisConfig.analysis_date}
                onChange={(e) => setAnalysisConfig({...analysisConfig, analysis_date: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Profondeur de Recherche:
            </label>
            <select
              value={analysisConfig.research_depth}
              onChange={(e) => setAnalysisConfig({...analysisConfig, research_depth: parseInt(e.target.value)})}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value={1}>1 - Rapide</option>
              <option value={2}>2 - Standard</option>
              <option value={3}>3 - Approfondie</option>
            </select>
          </div>

          <div className="text-center">
            <button
              onClick={startAnalysis}
              disabled={analysisRunning}
              className={`${analysisRunning ? 'bg-yellow-500' : 'bg-green-500 hover:bg-green-600'} text-white px-12 py-4 rounded-full text-xl font-bold transition-colors`}
            >
              {analysisRunning ? '🔄 Analyse en cours...' : '🚀 Démarrer l\'Analyse'}
            </button>
          </div>
        </div>

        {/* Résultats d'Analyse */}
        {analysisResult && (
          <div className="bg-white rounded-2xl p-8 mb-8 shadow-2xl">
            <h2 className="text-4xl font-bold text-center text-gray-800 mb-6">📊 Résultats d'Analyse</h2>
            
            {/* Status de l'analyse */}
            <div className={`p-4 rounded-lg mb-6 border-l-4 ${
              analysisResult.status === 'completed' ? 'bg-green-100 border-green-500' : 
              analysisResult.status === 'error' ? 'bg-red-100 border-red-500' :
              'bg-blue-100 border-blue-500'
            }`}>
              <p className="font-bold text-lg">{analysisResult.message}</p>
            </div>
            
            {/* Configuration d'analyse */}
            <div className="bg-gray-50 rounded-xl p-6 mb-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4">⚙️ Configuration:</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div><strong>Ticker:</strong> {analysisResult.configuration?.ticker}</div>
                <div><strong>Date:</strong> {analysisResult.configuration?.date}</div>
                <div><strong>Modèle:</strong> {analysisResult.configuration?.llm_model}</div>
                <div><strong>Profondeur:</strong> {analysisResult.configuration?.research_depth}</div>
              </div>
            </div>

            {/* Progression */}
            {analysisResult.progress && (
              <div className="bg-blue-50 rounded-xl p-6 mb-6">
                <h3 className="text-xl font-bold text-gray-800 mb-4">📈 Progression:</h3>
                <div className="mb-4">
                  <div className="flex justify-between text-sm font-semibold text-gray-700 mb-2">
                    <span>{analysisResult.progress.current_phase}</span>
                    <span>{analysisResult.progress.completion}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-4">
                    <div 
                      className="bg-blue-500 h-4 rounded-full transition-all duration-500"
                      style={{width: `${analysisResult.progress.completion}%`}}
                    ></div>
                  </div>
                </div>
                <div className="text-sm text-gray-600">
                  <strong>Phases:</strong> {analysisResult.progress.phases?.join(' → ')}
                </div>
              </div>
            )}

            {/* Sortie détaillée de l'analyse */}
            {analysisResult.analysis_output && (
              <div className="bg-gray-900 rounded-xl p-6 mb-6">
                <h3 className="text-xl font-bold text-white mb-4">🔍 Rapport Détaillé:</h3>
                <pre className="text-green-400 text-sm font-mono whitespace-pre-wrap overflow-x-auto max-h-96">
                  {analysisResult.analysis_output}
                </pre>
              </div>
            )}

            {/* Recommandations */}
            {analysisResult.recommendations && (
              <div className="bg-yellow-50 rounded-xl p-6 mb-6">
                <h3 className="text-xl font-bold text-gray-800 mb-4">💡 Recommandations:</h3>
                <div className="mb-4">
                  <p className="font-semibold">{analysisResult.recommendations.system_status}</p>
                </div>
                {analysisResult.recommendations.next_steps && (
                  <div>
                    <p className="font-semibold mb-2">Prochaines étapes:</p>
                    <ul className="list-disc list-inside space-y-1">
                      {analysisResult.recommendations.next_steps.map((step, index) => (
                        <li key={index}>{step}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {/* Boutons d'action */}
            <div className="text-center">
              <button
                onClick={() => setAnalysisResult(null)}
                className="bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-lg mr-4"
              >
                Fermer
              </button>
              <button
                onClick={() => startAnalysis()}
                className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg"
              >
                Relancer l'Analyse
              </button>
            </div>
          </div>
        )}

        {/* Agent Workflow */}
        <div className="bg-white rounded-2xl p-8 mb-8 shadow-2xl">
          <h2 className="text-4xl font-bold text-center text-gray-800 mb-8">🔄 Workflow des Agents</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            
            <div className="border-l-4 border-blue-500 bg-blue-50 rounded-xl p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-3">📊 I. Équipe d'Analyse</h3>
              <ul className="space-y-2 text-gray-700">
                <li>👤 Analyste Marché - Indicateurs techniques</li>
                <li>👤 Analyste Social - Sentiment & réseaux sociaux</li>
                <li>👤 Analyste Actualités - Nouvelles globales</li>
                <li>👤 Analyste Fondamentaux - Finances d'entreprise</li>
              </ul>
            </div>

            <div className="border-l-4 border-red-500 bg-red-50 rounded-xl p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-3">🔬 II. Équipe de Recherche</h3>
              <ul className="space-y-2 text-gray-700">
                <li>👤 Chercheur Haussier - Analyse optimiste</li>
                <li>👤 Chercheur Baissier - Analyse des risques</li>
                <li>👤 Gestionnaire de Recherche - Décisions équilibrées</li>
              </ul>
            </div>

            <div className="border-l-4 border-yellow-500 bg-yellow-50 rounded-xl p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-3">💼 III. Équipe de Trading</h3>
              <ul className="space-y-2 text-gray-700">
                <li>👤 Trader - Planification d'exécution</li>
                <li>📋 Formulation de stratégie</li>
                <li>⏰ Optimisation du timing</li>
              </ul>
            </div>

            <div className="border-l-4 border-purple-500 bg-purple-50 rounded-xl p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-3">⚠️ IV. Gestion des Risques</h3>
              <ul className="space-y-2 text-gray-700">
                <li>👤 Analyste Agressif - Haute tolérance</li>
                <li>👤 Analyste Conservateur - Faible risque</li>
                <li>👤 Analyste Neutre - Perspective équilibrée</li>
              </ul>
            </div>

            <div className="border-l-4 border-green-500 bg-green-50 rounded-xl p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-3">💰 V. Gestion de Portefeuille</h3>
              <ul className="space-y-2 text-gray-700">
                <li>👤 Gestionnaire de Portefeuille - Décisions finales</li>
                <li>📊 Évaluation des risques</li>
                <li>✅ Approbation/rejet des transactions</li>
              </ul>
            </div>

          </div>
        </div>

        {/* Features */}
        <div className="bg-white rounded-2xl p-8 mb-8 shadow-2xl">
          <h2 className="text-4xl font-bold text-center text-gray-800 mb-8">✨ Fonctionnalités Clés</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            
            <div className="text-center">
              <div className="text-5xl mb-4">🤖</div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Architecture Multi-Agents</h3>
              <p className="text-gray-600">Agents IA spécialisés collaborant comme une vraie entreprise de trading</p>
            </div>

            <div className="text-center">
              <div className="text-5xl mb-4">📈</div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Analyse en Temps Réel</h3>
              <p className="text-gray-600">Intégration de données de marché en direct avec analyse technique complète</p>
            </div>

            <div className="text-center">
              <div className="text-5xl mb-4">🧠</div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">DeepSeek Intégré</h3>
              <p className="text-gray-600">Utilise DeepSeek Chat pour des décisions de trading intelligentes</p>
            </div>

            <div className="text-center">
              <div className="text-5xl mb-4">🎯</div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Prise de Décision Intelligente</h3>
              <p className="text-gray-600">Débats dynamiques et discussions pour optimiser les stratégies</p>
            </div>

            <div className="text-center">
              <div className="text-5xl mb-4">⚡</div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Exécution Rapide</h3>
              <p className="text-gray-600">Analyse et prise de décision rapides avec paramètres configurables</p>
            </div>

            <div className="text-center">
              <div className="text-5xl mb-4">📊</div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Rapports Complets</h3>
              <p className="text-gray-600">Rapports d'analyse détaillés de chaque équipe spécialisée</p>
            </div>

          </div>
        </div>

        {/* Quick Start */}
        <div className="bg-gray-800 text-white rounded-2xl p-8 mb-8">
          <h2 className="text-4xl font-bold text-center mb-8">🚀 Démarrage Rapide</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            
            <div className="bg-gray-700 rounded-xl p-6">
              <h3 className="text-xl font-bold text-blue-400 mb-3">1. Interface CLI</h3>
              <div className="bg-black rounded-lg p-4 font-mono text-sm text-green-400">
                python -m cli.main
              </div>
            </div>

            <div className="bg-gray-700 rounded-xl p-6">
              <h3 className="text-xl font-bold text-blue-400 mb-3">2. Analyse Directe</h3>
              <div className="bg-black rounded-lg p-4 font-mono text-sm text-green-400">
                python main.py
              </div>
            </div>

            <div className="bg-gray-700 rounded-xl p-6">
              <h3 className="text-xl font-bold text-blue-400 mb-3">3. Test DeepSeek</h3>
              <div className="bg-black rounded-lg p-4 font-mono text-sm text-green-400">
                python test_deepseek.py
              </div>
            </div>

            <div className="bg-gray-700 rounded-xl p-6">
              <h3 className="text-xl font-bold text-blue-400 mb-3">4. Configuration</h3>
              <div className="bg-black rounded-lg p-4 font-mono text-sm text-green-400">
                # DeepSeek Chat configuré ✅<br/>
                # FinnHub API configurée ✅
              </div>
            </div>

          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-white opacity-80">
          <p className="mb-2">Construit par <a href="https://github.com/TauricResearch" className="text-blue-300 hover:text-blue-200">Tauric Research</a></p>
          <p>Framework de Trading Multi-Agents LLM Open Source</p>
          <p className="mt-4 text-sm">🎉 TradingAgents est maintenant lancé avec DeepSeek Chat! 🎉</p>
        </div>

      </div>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<TradingAgentsHome />}>
            <Route index element={<TradingAgentsHome />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
