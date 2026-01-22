import { useState, useEffect } from 'react'
import { AlertTriangle, Server, Database, Activity, RefreshCw } from 'lucide-react'

// Helper for API calls
const API_URL = import.meta.env.VITE_API_URL || '/ai-backend/api';

export default function Analytics() {
    const [predictions, setPredictions] = useState([])
    const [loading, setLoading] = useState(true)

    const fetchPredictions = async () => {
        setLoading(true)
        try {
            const res = await fetch(`${API_URL}/analytics/predictions`)
            const data = await res.json()
            setPredictions(data)
        } catch (err) {
            console.error("Failed to fetch analytics", err)
        }
        setLoading(false)
    }

    useEffect(() => {
        fetchPredictions()
    }, [])

    return (
        <div className="flex flex-col h-full bg-slate-900 p-8 overflow-y-auto">
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-400">
                        Predictive Analytics
                    </h2>
                    <p className="text-slate-400 mt-1">AI-driven insights on potential system failures.</p>
                </div>
                <button
                    onClick={fetchPredictions}
                    className="p-2 bg-slate-800 rounded-lg hover:bg-slate-700 transition-colors border border-slate-700"
                >
                    <RefreshCw size={20} className={loading ? "animate-spin" : ""} />
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {predictions.map((pred, idx) => (
                    <div key={idx} className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 backdrop-blur hover:border-slate-600 transition-colors group">
                        <div className="flex justify-between items-start mb-4">
                            <div className="p-3 bg-red-500/10 rounded-lg border border-red-500/20 group-hover:border-red-500/40 transition-colors">
                                <AlertTriangle className="text-red-500" size={24} />
                            </div>
                            <span className="px-3 py-1 bg-red-500/20 text-red-300 text-xs font-semibold rounded-full border border-red-500/20">
                                {pred.severity} Risk
                            </span>
                        </div>

                        <h3 className="text-lg font-semibold text-slate-100 mb-1">{pred.host}</h3>
                        <p className="text-sm text-slate-400 mb-4 flex items-center gap-2">
                            <Server size={14} /> {pred.service}
                        </p>

                        <div className="space-y-3">
                            <div className="bg-slate-900/50 p-3 rounded-lg border border-slate-800">
                                <p className="text-sm text-slate-300">
                                    <span className="text-blue-400 font-medium">Prediction:</span> {pred.prediction}
                                </p>
                            </div>
                            <div className="bg-emerald-900/20 p-3 rounded-lg border border-emerald-900/30">
                                <p className="text-sm text-emerald-300">
                                    <span className="font-medium">Recommendation:</span> {pred.recommendation}
                                </p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {predictions.length === 0 && !loading && (
                <div className="text-center py-20 text-slate-500">
                    <Activity size={48} className="mx-auto mb-4 opacity-50" />
                    <p>No high-risk predictions detected at this time.</p>
                </div>
            )}
        </div>
    )
}
