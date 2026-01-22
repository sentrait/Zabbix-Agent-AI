import { useState, useEffect } from 'react'
import { Save, Loader } from 'lucide-react'

// Fetch dynamically from environment or default path
const API_URL = import.meta.env.VITE_API_URL || '/ai-backend/api';

export default function Settings() {
    const [loading, setLoading] = useState(true)
    const [saving, setSaving] = useState(false)
    const [config, setConfig] = useState({
        provider: 'bedrock', // bedrock, openai, gemini
        aws_region: 'us-east-1',
        aws_access_key: '',
        aws_secret_key: '',
        bedrock_model_id: 'us.anthropic.claude-3-5-sonnet-20241022-v2:0',
        openai_api_key: '',
        openai_model: 'gpt-4o',
        gemini_api_key: '',
        gemini_model: 'gemini-1.5-pro-latest'
    })

    useEffect(() => {
        fetchConfig();
    }, []);

    const fetchConfig = async () => {
        try {
            const res = await fetch(`${API_URL}/config`)
            const data = await res.json()
            setConfig(prev => ({ ...prev, ...data }))
        } catch (err) {
            console.error("Error fetching config", err)
        }
        setLoading(false)
    }

    const handleSave = async () => {
        setSaving(true)
        try {
            await fetch(`${API_URL}/config`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(config)
            })
            alert('Settings saved successfully!')
        } catch (err) {
            alert('Error saving settings.')
            console.error(err)
        }
        setSaving(false)
    }

    if (loading) return <div className="p-8 text-slate-400">Loading settings...</div>

    return (
        <div className="flex flex-col h-full bg-slate-900 p-8 overflow-y-auto">
            <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-400 mb-8">
                Configuration
            </h2>

            <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-8 max-w-2xl backdrop-blur">
                <div className="space-y-6">

                    {/* Provider Selection */}
                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">AI Provider</label>
                        <select
                            value={config.provider}
                            onChange={(e) => setConfig({ ...config, provider: e.target.value })}
                            className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2.5 px-4 text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
                        >
                            <option value="bedrock">AWS Bedrock (Claude)</option>
                            <option value="openai">OpenAI (GPT-4)</option>
                            <option value="gemini">Google Gemini</option>
                        </select>
                    </div>

                    <hr className="border-slate-700 my-4" />

                    {/* AWS Bedrock Settings */}
                    {config.provider === 'bedrock' && (
                        <div className="space-y-4 animate-fadeIn">
                            <h3 className="text-lg font-medium text-slate-200">AWS Bedrock Settings</h3>
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-1">AWS Region</label>
                                <input
                                    type="text"
                                    value={config.aws_region}
                                    onChange={(e) => setConfig({ ...config, aws_region: e.target.value })}
                                    className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 px-4 text-slate-200"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-1">AWS Access Key ID</label>
                                <input
                                    type="text"
                                    value={config.aws_access_key}
                                    onChange={(e) => setConfig({ ...config, aws_access_key: e.target.value })}
                                    className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 px-4 text-slate-200"
                                    placeholder="AKIA..."
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-1">AWS Secret Access Key</label>
                                <input
                                    type="password"
                                    value={config.aws_secret_key}
                                    onChange={(e) => setConfig({ ...config, aws_secret_key: e.target.value })}
                                    className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 px-4 text-slate-200"
                                    placeholder="Secret Key"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-1">Model ID</label>
                                <input
                                    type="text"
                                    value={config.bedrock_model_id}
                                    onChange={(e) => setConfig({ ...config, bedrock_model_id: e.target.value })}
                                    className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 px-4 text-slate-200"
                                />
                            </div>
                        </div>
                    )}

                    {/* OpenAI Settings */}
                    {config.provider === 'openai' && (
                        <div className="space-y-4 animate-fadeIn">
                            <h3 className="text-lg font-medium text-slate-200">OpenAI Settings</h3>
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-1">API Key</label>
                                <input
                                    type="password"
                                    value={config.openai_api_key}
                                    onChange={(e) => setConfig({ ...config, openai_api_key: e.target.value })}
                                    className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 px-4 text-slate-200"
                                    placeholder="sk-..."
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-1">Model</label>
                                <input
                                    type="text"
                                    value={config.openai_model}
                                    onChange={(e) => setConfig({ ...config, openai_model: e.target.value })}
                                    className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 px-4 text-slate-200"
                                    placeholder="gpt-4o"
                                />
                            </div>
                        </div>
                    )}

                    {/* Gemini Settings */}
                    {config.provider === 'gemini' && (
                        <div className="space-y-4 animate-fadeIn">
                            <h3 className="text-lg font-medium text-slate-200">Google Gemini Settings</h3>
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-1">API Key</label>
                                <input
                                    type="password"
                                    value={config.gemini_api_key}
                                    onChange={(e) => setConfig({ ...config, gemini_api_key: e.target.value })}
                                    className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 px-4 text-slate-200"
                                    placeholder="AI..."
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-1">Model</label>
                                <input
                                    type="text"
                                    value={config.gemini_model}
                                    onChange={(e) => setConfig({ ...config, gemini_model: e.target.value })}
                                    className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 px-4 text-slate-200"
                                    placeholder="gemini-1.5-pro-latest"
                                />
                            </div>
                        </div>
                    )}

                    <div className="pt-6">
                        <button
                            onClick={handleSave}
                            disabled={saving}
                            className="w-full flex justify-center items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 rounded-lg font-medium transition-colors disabled:opacity-50"
                        >
                            {saving ? <Loader className="animate-spin" size={20} /> : <Save size={20} />}
                            Save Configuration
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}
