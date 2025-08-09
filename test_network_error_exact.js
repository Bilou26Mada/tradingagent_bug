// Test exact pour reproduire Network Error
const axios = require('axios');

const API_URL = 'http://localhost:8001/api';

async function testExactError() {
    console.log('🔍 REPRODUCTION EXACTE NETWORK ERROR');
    console.log('================================');
    
    try {
        console.log('1. Test Status...');
        const statusResponse = await axios.get(`${API_URL}/trading/status`, {
            timeout: 10000
        });
        console.log('✅ Status OK:', statusResponse.data.status);
        
        console.log('\n2. Test DeepSeek...');
        const deepseekResponse = await axios.get(`${API_URL}/trading/test-deepseek-quick`, {
            timeout: 15000
        });
        console.log('✅ DeepSeek OK:', deepseekResponse.data.status);
        
        console.log('\n3. Test Analysis...');
        const analysisResponse = await axios.post(`${API_URL}/trading/analyze`, {
            ticker: 'TSLA',
            analysis_date: '2024-05-10',
            analysts: ['market'],
            research_depth: 1
        }, {
            timeout: 30000,
            headers: {
                'Content-Type': 'application/json'
            }
        });
        console.log('✅ Analysis OK:', analysisResponse.data.status);
        
        console.log('\n🎉 AUCUNE ERREUR RÉSEAU DÉTECTÉE');
        
    } catch (error) {
        console.log('\n🚨 NETWORK ERROR REPRODUITE!');
        console.log('Type:', error.constructor.name);
        console.log('Message:', error.message);
        console.log('Code:', error.code);
        
        if (error.response) {
            console.log('HTTP Status:', error.response.status);
            console.log('HTTP Data:', error.response.data);
        }
        
        console.log('Config URL:', error.config?.url);
        console.log('Config Method:', error.config?.method);
        console.log('Config Timeout:', error.config?.timeout);
    }
}

testExactError();