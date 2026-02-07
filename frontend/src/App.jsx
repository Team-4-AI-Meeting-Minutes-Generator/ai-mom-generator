import React, { useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Upload, FileText, CheckCircle2, AlertCircle, Loader2, Sparkles, User, Calendar } from 'lucide-react'

function App() {
    const [file, setFile] = useState(null)
    const [loading, setLoading] = useState(false)
    const [results, setResults] = useState(null)
    const [error, setError] = useState(null)

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0]
        if (selectedFile) {
            setFile(selectedFile)
            setError(null)
        }
    }

    const handleUpload = async () => {
        if (!file) return

        setLoading(true)
        setError(null)
        setResults(null)

        const formData = new FormData()
        formData.append('file', file)

        try {
            const response = await fetch('/api/process', {
                method: 'POST',
                body: formData,
            })

            if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.detail || 'Failed to process file')
            }

            const data = await response.json()
            setResults(data)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="app-container">
            <div className="hero">
                <motion.h1
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    AI Meeting Minutes
                </motion.h1>
                <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.3, duration: 0.6 }}
                >
                    Transform your transcripts and recordings into structured, professional meeting minutes in seconds.
                </motion.p>
            </div>

            <motion.div
                className="glass-card"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
            >
                {!results && (
                    <div className="upload-section">
                        <div
                            className="upload-zone"
                            onClick={() => document.getElementById('file-input').click()}
                        >
                            <input
                                id="file-input"
                                type="file"
                                style={{ display: 'none' }}
                                onChange={handleFileChange}
                                accept=".txt,.json,.mp3,.wav,.m4a,.mp4"
                            />
                            <Upload className="upload-icon" />
                            <h3>{file ? file.name : "Click or Drag & Drop to Upload"}</h3>
                            <p>Supports .txt, .json, .mp3, .wav, .m4a</p>
                        </div>

                        <div style={{ textAlign: 'center', marginTop: '30px' }}>
                            <button
                                className="btn-primary"
                                disabled={!file || loading}
                                onClick={handleUpload}
                            >
                                {loading ? <Loader2 className="loading-spinner" style={{ width: 20, height: 20, margin: 0 }} /> : "Generate Minutes"}
                            </button>
                        </div>
                    </div>
                )}

                <AnimatePresence>
                    {error && (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            style={{ color: '#ff7b72', marginTop: 20, textAlign: 'center', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8 }}
                        >
                            <AlertCircle size={20} />
                            {error}
                        </motion.div>
                    )}

                    {results && (
                        <motion.div
                            className="results-section"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                        >
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 30 }}>
                                <h2 className="section-title"><Sparkles /> Generated Minutes</h2>
                                <button className="btn-primary" onClick={() => { setResults(null); setFile(null); }}>Process Another</button>
                            </div>

                            <div className="section-title"><FileText size={24} /> Key Discussion Points</div>
                            <ul className="points-list">
                                {results.key_points.map((point, i) => (
                                    <motion.li
                                        key={i}
                                        className="point-item"
                                        initial={{ opacity: 0, x: -20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: i * 0.1 }}
                                    >
                                        {point}
                                    </motion.li>
                                ))}
                            </ul>

                            <div className="section-title"><CheckCircle2 size={24} /> Action Items</div>
                            <div style={{ overflowX: 'auto' }}>
                                <table className="actions-table">
                                    <thead>
                                        <tr>
                                            <th>Action Item</th>
                                            <th>Owner</th>
                                            <th>Deadline</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {results.action_items.map((item, i) => (
                                            <motion.tr
                                                key={i}
                                                initial={{ opacity: 0, y: 10 }}
                                                animate={{ opacity: 1, y: 0 }}
                                                transition={{ delay: (results.key_points.length + i) * 0.1 }}
                                            >
                                                <td>{item.action}</td>
                                                <td><div style={{ display: 'flex', alignItems: 'center', gap: 6 }}><User size={14} /> {item.owner}</div></td>
                                                <td><div style={{ display: 'flex', alignItems: 'center', gap: 6 }}><Calendar size={14} /> {item.deadline}</div></td>
                                            </motion.tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </motion.div>

            <div style={{ marginTop: 'auto', paddingTop: '40px', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                Powered by AI • Premium Meeting Assistant
            </div>
        </div>
    )
}

export default App
