import React, { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Upload, FileText, CheckCircle2, AlertCircle, Loader2, Sparkles, User, Calendar, ArrowRight, RefreshCw, Mic, MicOff, Play, Square, Globe } from 'lucide-react'

function App() {
    const [mode, setMode] = useState('upload') // 'upload', 'live', or 'google-meet'
    const [file, setFile] = useState(null)
    const [loading, setLoading] = useState(false)
    const [results, setResults] = useState(null)
    const [error, setError] = useState(null)

    // Live/Meet States
    const [isRecording, setIsRecording] = useState(false)
    const [isSyncing, setIsSyncing] = useState(false)
    const [transcript, setTranscript] = useState('')
    const [interimTranscript, setInterimTranscript] = useState('')
    const recognitionRef = useRef(null)
    const mediaStreamRef = useRef(null)

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0]
        if (selectedFile) {
            setFile(selectedFile)
            setError(null)
        }
    }

    const handleMeetSync = async () => {
        try {
            const stream = await navigator.mediaDevices.getDisplayMedia({
                video: { displaySurface: 'browser' },
                audio: { echoCancellation: true, noiseSuppression: true }
            });
            mediaStreamRef.current = stream;
            setIsSyncing(true);
            setIsRecording(true);
            setError(null);
            startRecording();
            stream.getVideoTracks()[0].onended = () => stopMeetSync();
        } catch (err) {
            console.error("Meet Sync Error:", err);
            setError("Failed to sync with Google Meet. Ensure you select 'Share tab audio'.");
        }
    };

    const stopMeetSync = () => {
        if (mediaStreamRef.current) {
            mediaStreamRef.current.getTracks().forEach(track => track.stop());
            mediaStreamRef.current = null;
        }
        setIsSyncing(false);
        stopRecording();
    };

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

            let data;
            const contentType = response.headers.get('content-type');

            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                const text = await response.text();
                throw new Error(text || `Server error: ${response.status}`);
            }

            if (!response.ok) {
                throw new Error(data?.detail || 'Failed to process file');
            }

            setResults(data)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const handleProcessLiveTranscript = async () => {
        if (!transcript) return

        setLoading(true)
        setError(null)
        setResults(null)

        try {
            const response = await fetch('/api/process-text', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: transcript }),
            })

            let data;
            const contentType = response.headers.get('content-type');

            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                const text = await response.text();
                throw new Error(text || `Server error: ${response.status}`);
            }

            if (!response.ok) {
                throw new Error(data?.detail || 'Failed to process transcript');
            }

            setResults(data)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const startRecording = () => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            setError("Your browser does not support speech recognition. Try Chrome or Edge.")
            return
        }

        const recognition = new SpeechRecognition()
        recognition.continuous = true
        recognition.interimResults = true
        recognition.lang = 'en-US'

        recognition.onresult = (event) => {
            let currentInterim = ''
            let currentFinal = ''

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcriptPart = event.results[i][0].transcript
                if (event.results[i].isFinal) {
                    currentFinal += transcriptPart + ' '
                } else {
                    currentInterim += transcriptPart
                }
            }

            if (currentFinal) {
                setTranscript(prev => prev + currentFinal)
            }
            setInterimTranscript(currentInterim)
        }

        recognition.onerror = (event) => {
            console.error("Speech Recognition Error:", event.error)
            if (event.error === 'not-allowed') {
                setError("Microphone access denied. Please allow microphone permissions.")
                stopRecording()
            }
        }

        recognition.onend = () => {
            // Restart if we are still supposed to be recording
            if (isRecording) {
                recognition.start()
            }
        }

        recognitionRef.current = recognition
        recognition.start()
        setIsRecording(true)
        setError(null)
    }

    const stopRecording = () => {
        if (recognitionRef.current) {
            recognitionRef.current.stop()
            recognitionRef.current = null
        }
        setIsRecording(false)
        setInterimTranscript('')
    }

    useEffect(() => {
        return () => {
            if (recognitionRef.current) {
                recognitionRef.current.stop()
            }
        }
    }, [])

    return (
        <div className="app-container">
            <div className="hero">
                <motion.div
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                    style={{ marginBottom: 20 }}
                >
                    <span className="badge" style={{ background: 'rgba(37, 99, 235, 0.08)', color: 'var(--accent-primary)', padding: '8px 16px', borderRadius: '30px', fontSize: '0.9rem', fontWeight: '600', border: '1px solid rgba(37, 99, 235, 0.15)' }}>
                        <Sparkles size={14} style={{ marginRight: 6, verticalAlign: 'middle' }} />
                        Introducing Thynk Tech AI
                    </span>
                </motion.div>

                <motion.h1
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 1, ease: "easeOut" }}
                >
                    Thynk Tech
                </motion.h1>

                <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.4, duration: 1 }}
                >
                    Revolutionizing meeting intelligence. Transform messy transcripts into laser-focused insights with the power of Thynk AI.
                </motion.p>
            </div>

            <div style={{ display: 'flex', gap: 12, marginBottom: 32 }}>
                <button
                    onClick={() => { setMode('upload'); setResults(null); stopRecording(); }}
                    style={{
                        padding: '10px 24px',
                        borderRadius: '12px',
                        border: '1px solid var(--glass-border)',
                        background: mode === 'upload' ? 'var(--accent-primary)' : 'rgba(0,0,0,0.03)',
                        color: mode === 'upload' ? '#fff' : 'var(--text-secondary)',
                        fontWeight: '600',
                        cursor: 'pointer',
                        transition: '0.3s'
                    }}
                >
                    <Upload size={18} style={{ marginRight: 8, verticalAlign: 'middle' }} />
                    Upload File
                </button>
                <button
                    onClick={() => { setMode('live'); setResults(null); }}
                    style={{
                        padding: '10px 24px',
                        borderRadius: '12px',
                        border: '1px solid var(--glass-border)',
                        background: mode === 'live' ? 'var(--accent-primary)' : 'rgba(0,0,0,0.03)',
                        color: mode === 'live' ? '#fff' : 'var(--text-secondary)',
                        fontWeight: '600',
                        cursor: 'pointer',
                        transition: '0.3s'
                    }}
                >
                    <Mic size={18} style={{ marginRight: 8, verticalAlign: 'middle' }} />
                    Live Recording
                </button>
                <button
                    onClick={() => { setMode('google-meet'); setResults(null); stopRecording(); }}
                    style={{
                        padding: '10px 24px',
                        borderRadius: '12px',
                        border: '1px solid var(--glass-border)',
                        background: mode === 'google-meet' ? 'var(--accent-primary)' : 'rgba(0,0,0,0.03)',
                        color: mode === 'google-meet' ? '#fff' : 'var(--text-secondary)',
                        fontWeight: '600',
                        cursor: 'pointer',
                        transition: '0.3s'
                    }}
                >
                    <Globe size={18} style={{ marginRight: 8, verticalAlign: 'middle' }} />
                    Google Meet
                </button>
            </div>

            <motion.div
                className="glass-card"
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2, duration: 0.8 }}
            >
                <AnimatePresence mode='wait'>
                    {!results && !loading && mode === 'upload' && (
                        <motion.div
                            key="upload"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: 20 }}
                            className="upload-section"
                        >
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
                                <h3 style={{ fontSize: '1.5rem', marginBottom: 12, color: 'var(--text-primary)' }}>
                                    {file ? file.name : "Drop your transcript here"}
                                </h3>
                                <p style={{ color: 'var(--text-secondary)' }}>
                                    Securely process .txt, .mp3, .wav, and more
                                </p>
                            </div>

                            <div style={{ textAlign: 'center', marginTop: '40px' }}>
                                <button
                                    className="btn-primary"
                                    disabled={!file}
                                    onClick={handleUpload}
                                >
                                    Generate Minutes
                                    <ArrowRight size={18} style={{ marginLeft: 10, verticalAlign: 'middle' }} />
                                </button>
                            </div>
                        </motion.div>
                    )}

                    {!results && !loading && mode === 'live' && (
                        <motion.div
                            key="live"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                        >
                            <div style={{ textAlign: 'center', marginBottom: 40 }}>
                                <div style={{
                                    width: 100,
                                    height: 100,
                                    borderRadius: '50%',
                                    background: isRecording ? 'rgba(239, 68, 68, 0.1)' : 'rgba(59, 130, 246, 0.1)',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    margin: '0 auto 24px',
                                    border: `2px solid ${isRecording ? 'var(--error)' : 'var(--accent-primary)'}`,
                                    position: 'relative'
                                }}>
                                    {isRecording && (
                                        <motion.div
                                            initial={{ scale: 1 }}
                                            animate={{ scale: 1.4, opacity: 0 }}
                                            transition={{ repeat: Infinity, duration: 1.5 }}
                                            style={{
                                                position: 'absolute',
                                                width: '100%',
                                                height: '100%',
                                                borderRadius: '50%',
                                                border: '2px solid var(--error)'
                                            }}
                                        />
                                    )}
                                    {isRecording ? <Mic size={40} color="var(--error)" /> : <MicOff size={40} color="var(--accent-primary)" />}
                                </div>
                                <h2 style={{ color: 'var(--text-primary)', fontSize: '1.75rem', marginBottom: 8 }}>
                                    {isRecording ? "Listening to Meeting..." : "Ready to Start"}
                                </h2>
                                <p style={{ color: 'var(--text-secondary)' }}>
                                    Place your device near the speakers for better accuracy
                                </p>
                            </div>

                            <div style={{
                                background: 'rgba(255,255,255,0.5)',
                                borderRadius: '24px',
                                padding: '24px',
                                minHeight: '200px',
                                maxHeight: '400px',
                                overflowY: 'auto',
                                border: '1px solid var(--glass-border)',
                                marginBottom: 40,
                                position: 'relative'
                            }}>
                                {!transcript && !interimTranscript && (
                                    <div style={{ color: 'var(--text-secondary)', textAlign: 'center', marginTop: 60 }}>
                                        <Globe size={48} style={{ opacity: 0.1, marginBottom: 16 }} />
                                        <p>Your live transcript will appear here...</p>
                                    </div>
                                )}
                                <div style={{ whiteSpace: 'pre-wrap', color: 'var(--text-primary)', lineHeight: '1.8', fontSize: '1.1rem' }}>
                                    {transcript}
                                    <span style={{ color: 'var(--accent-primary)', opacity: 0.7 }}>{interimTranscript}</span>
                                </div>
                            </div>

                            <div style={{ display: 'flex', justifyContent: 'center', gap: 16 }}>
                                {!isRecording ? (
                                    <button
                                        className="btn-primary"
                                        onClick={startRecording}
                                        style={{ background: 'var(--accent-primary)', display: 'flex', alignItems: 'center', gap: 10 }}
                                    >
                                        <Play size={18} fill="currentColor" />
                                        Start Recording
                                    </button>
                                ) : (
                                    <button
                                        className="btn-primary"
                                        onClick={stopRecording}
                                        style={{ background: 'var(--error)', display: 'flex', alignItems: 'center', gap: 10 }}
                                    >
                                        <Square size={18} fill="currentColor" />
                                        Stop Recording
                                    </button>
                                )}
                                {transcript && (
                                    <button
                                        className="btn-primary"
                                        onClick={handleProcessLiveTranscript}
                                        style={{ background: 'var(--success)', display: 'flex', alignItems: 'center', gap: 10 }}
                                    >
                                        <RefreshCw size={18} />
                                        Finish & Generate MOM
                                    </button>
                                )}
                            </div>
                        </motion.div>
                    )}

                    {!results && !loading && mode === 'google-meet' && (
                        <motion.div
                            key="google-meet"
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                        >
                            <div style={{ textAlign: 'center', marginBottom: 40 }}>
                                <div style={{
                                    width: 80, height: 80, borderRadius: '20px',
                                    background: 'linear-gradient(135deg, #4285F4, #34A853)',
                                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                                    margin: '0 auto 24px', boxShadow: '0 8px 32px rgba(66, 133, 244, 0.3)'
                                }}>
                                    <Globe size={40} color="#fff" />
                                </div>
                                <h2 style={{ color: 'var(--text-primary)', fontSize: '1.75rem', marginBottom: 12 }}>Google Meet Sync</h2>
                                <p style={{ color: 'var(--text-secondary)', maxWidth: '500px', margin: '0 auto' }}>
                                    Connect Thynk AI to your live Google Meet call for real-time insights.
                                </p>
                            </div>

                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginBottom: 40 }}>
                                <div className="glass-card" style={{ padding: '24px', border: '1px solid var(--glass-border)', background: 'rgba(255,255,255,0.02)' }}>
                                    <h4 style={{ color: 'var(--accent-primary)', marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
                                        <RefreshCw size={18} /> Live Tab Sync
                                    </h4>
                                    <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: 20 }}>
                                        Capture audio directly from your Google Meet browser tab.
                                    </p>
                                    {!isSyncing ? (
                                        <button className="btn-primary" onClick={handleMeetSync} style={{ width: '100%', fontSize: '0.9rem' }}>
                                            Sync with Meet Tab
                                        </button>
                                    ) : (
                                        <button className="btn-primary" onClick={stopMeetSync} style={{ width: '100%', fontSize: '0.9rem', background: 'var(--error)' }}>
                                            Stop Syncing
                                        </button>
                                    )}
                                </div>

                                <div className="glass-card" style={{ padding: '24px', border: '1px solid var(--glass-border)', background: 'rgba(255,255,255,0.02)', opacity: 0.6 }}>
                                    <h4 style={{ color: 'var(--accent-secondary)', marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
                                        <Calendar size={18} /> Archive Retrieval
                                    </h4>
                                    <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: 20 }}>
                                        Fetch transcripts from your Google Workspace archive.
                                    </p>
                                    <button className="btn-primary" disabled style={{ width: '100%', fontSize: '0.9rem', cursor: 'not-allowed' }}>
                                        Coming Soon
                                    </button>
                                </div>
                            </div>

                            {isSyncing && (
                                <motion.div
                                    initial={{ opacity: 0, height: 0 }}
                                    animate={{ opacity: 1, height: 'auto' }}
                                    style={{ background: 'rgba(0,0,0,0.2)', borderRadius: '24px', padding: '24px', border: '1px solid var(--glass-border)' }}
                                >
                                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
                                        <span style={{ color: 'var(--accent-primary)', fontSize: '0.9rem', fontWeight: '600' }}>LIVE SYNC ACTIVE</span>
                                        <span style={{ color: 'var(--success)', fontSize: '0.8rem' }}>● Capturing Tab Audio</span>
                                    </div>
                                    <div style={{ whiteSpace: 'pre-wrap', color: 'var(--text-primary)', fontSize: '1rem', lineHeight: '1.6', minHeight: '100px' }}>
                                        {transcript}
                                        <span style={{ color: 'var(--accent-primary)', opacity: 0.7 }}>{interimTranscript}</span>
                                    </div>
                                    <div style={{ textAlign: 'right', marginTop: 16 }}>
                                        <button className="btn-primary" onClick={handleProcessLiveTranscript} style={{ padding: '8px 20px', fontSize: '0.85rem', background: 'var(--success)' }}>
                                            Finish & Generate
                                        </button>
                                    </div>
                                </motion.div>
                            )}
                        </motion.div>
                    )}

                    {loading && (
                        <motion.div
                            key="loading"
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.9 }}
                            className="loading-container"
                        >
                            <Loader2 className="loading-spinner" />
                            <h3 style={{ color: 'var(--text-primary)', fontSize: '1.25rem' }}>Thynk AI is analyzing...</h3>
                            <p style={{ color: 'var(--text-secondary)' }}>Extracting key points and organizing action items</p>
                        </motion.div>
                    )}

                    {results && (
                        <motion.div
                            key="results"
                            className="results-section"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                        >
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 40 }}>
                                <h2 className="section-title" style={{ margin: 0 }}>
                                    <Sparkles size={28} />
                                    Meeting Insights
                                </h2>
                                <button
                                    className="btn-primary"
                                    style={{ padding: '10px 24px', fontSize: '0.9rem', background: 'rgba(0,0,0,0.03)', color: 'var(--text-secondary)', boxShadow: 'none', border: '1px solid var(--glass-border)' }}
                                    onClick={() => { setResults(null); setFile(null); setTranscript(''); }}
                                >
                                    <RefreshCw size={16} style={{ marginRight: 8, verticalAlign: 'middle' }} />
                                    New Meeting
                                </button>
                            </div>

                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ delay: 0.2 }}
                            >
                                <div className="section-title" style={{ fontSize: '1.25rem', color: 'var(--accent-primary)' }}>
                                    <FileText size={20} /> Discussion Summary
                                </div>
                                <div className="points-list">
                                    {results.key_points.map((point, i) => (
                                        <motion.div
                                            key={i}
                                            className="point-item"
                                            initial={{ opacity: 0, x: -30 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            transition={{ delay: 0.3 + i * 0.1 }}
                                        >
                                            <div style={{ width: 8, height: 8, background: 'var(--accent-primary)', borderRadius: '50%', marginTop: 8, flexShrink: 0 }} />
                                            {point}
                                        </motion.div>
                                    ))}
                                </div>
                            </motion.div>

                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ delay: 0.5 }}
                                style={{ marginTop: 40 }}
                            >
                                <div className="section-title" style={{ fontSize: '1.25rem', color: 'var(--accent-secondary)' }}>
                                    <CheckCircle2 size={20} /> Action Blueprint
                                </div>
                                <div style={{ overflowX: 'auto' }}>
                                    <table className="actions-table">
                                        <thead>
                                            <tr>
                                                <th>Task Details</th>
                                                <th>Owner</th>
                                                <th>Timeline</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {results.action_items.map((item, i) => (
                                                <motion.tr
                                                    key={i}
                                                    initial={{ opacity: 0, y: 10 }}
                                                    animate={{ opacity: 1, y: 0 }}
                                                    transition={{ delay: 0.6 + i * 0.1 }}
                                                >
                                                    <td style={{ fontWeight: '500', color: 'var(--text-primary)' }}>{item.action}</td>
                                                    <td>
                                                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: 'var(--text-secondary)' }}>
                                                            <div style={{ width: 24, height: 24, borderRadius: '50%', background: 'rgba(168, 85, 247, 0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                                                <User size={12} color='var(--accent-secondary)' />
                                                            </div>
                                                            {item.owner}
                                                        </div>
                                                    </td>
                                                    <td>
                                                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: 'var(--text-secondary)' }}>
                                                            <Calendar size={14} color='var(--accent-tertiary)' />
                                                            {item.deadline}
                                                        </div>
                                                    </td>
                                                </motion.tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </motion.div>
                        </motion.div>
                    )}
                </AnimatePresence>

                <AnimatePresence>
                    {error && (
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.9 }}
                            style={{
                                background: 'rgba(239, 68, 68, 0.1)',
                                border: '1px solid rgba(239, 68, 68, 0.2)',
                                borderRadius: '16px',
                                padding: '16px',
                                color: '#fca5a5',
                                marginTop: 32,
                                textAlign: 'center',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                gap: 12,
                                fontWeight: '500'
                            }}
                        >
                            <AlertCircle size={20} />
                            {error}
                        </motion.div>
                    )}
                </AnimatePresence>
            </motion.div>

            <motion.div
                style={{ marginTop: 'auto', paddingTop: '60px', color: 'var(--text-secondary)', fontSize: '0.85rem', textAlign: 'center' }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1 }}
            >
                <div style={{ fontWeight: '600', color: 'var(--text-primary)', marginBottom: 4 }}>THYNK TECH</div>
                © 2026 Next-Gen Meeting Intelligence • All Rights Reserved
            </motion.div>
        </div>
    )
}

export default App
