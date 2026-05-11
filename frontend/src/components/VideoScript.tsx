/* src/components/VideoScript.tsx — Full Video Generation UI */
import { useState, useEffect, useRef } from 'react';
import { apiGenerate, apiFetch } from '../api';

// ─── Types ─────────────────────────────────────────────────

interface Scene {
  scene_number: number;
  visual: string;
  narration: string;
  duration: number;
  audio_url?: string;
}

interface Hook { text: string; visual: string; duration: number; }
interface CTA { text: string; visual: string; duration: number; }

interface VideoScript {
  title: string;
  hook: Hook;
  scenes: Scene[];
  cta: CTA;
  music_suggestion: string;
  hashtags: string[];
}

interface AudioResult {
  full_narration_url?: string;
  hook_url?: string;
  cta_url?: string;
  scenes: { scene_number: number; audio_url?: string; duration: number }[];
  total_duration: number;
  error?: string;
  available?: boolean;
}

interface VideoModel {
  id: string;
  price_per_sec: number;
  max_duration: number;
  native_audio: boolean;
}

interface ProviderStatus {
  [key: string]: boolean;
}

type SubTab = 'script' | 'generate' | 'preview';

// ─── Component ─────────────────────────────────────────────

export default function VideoScript({ token: _token }: { token?: string | null }) {
  const [subTab, setSubTab] = useState<SubTab>('script');

  // Form state
  const [productName, setProductName] = useState('');
  const [category, setCategory] = useState('');
  const [features, setFeatures] = useState('');
  const [targetAudience, setTargetAudience] = useState('general');
  const [platform, setPlatform] = useState('tiktok');
  const [language, setLanguage] = useState('Vietnamese');
  const [tone, setTone] = useState('engaging');
  const [duration, setDuration] = useState(30);
  const [nScenes, setNScenes] = useState(4);

  // TTS options
  const [generateAudio, setGenerateAudio] = useState(true);
  const [ttsProvider, setTtsProvider] = useState('edge');
  const [voiceLanguage, setVoiceLanguage] = useState('vi');
  const [voiceGender, setVoiceGender] = useState('female');
  const [ttsSpeed, setTtsSpeed] = useState(1.0);

  // Video generation options
  const [videoModel, setVideoModel] = useState('SEEDANCE_2_FAST');
  const [videoDuration, setVideoDuration] = useState(5);
  const [videoStyle, setVideoStyle] = useState('');
  const [aspectRatio, setAspectRatio] = useState('9:16');

  // Results
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [script, setScript] = useState<VideoScript | null>(null);
  const [audio, setAudio] = useState<AudioResult | null>(null);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [videoCost, setVideoCost] = useState(0);

  // Providers & models
  const [providers, setProviders] = useState<ProviderStatus>({});
  const [models, setModels] = useState<VideoModel[]>([]);
  const [, setPrices] = useState<VideoModel[]>([]);

  // Audio playback
  const [playingAudio, setPlayingAudio] = useState<string | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // Fetch providers on mount
  useEffect(() => {
    fetchProviders();
    fetchPrices();
  }, []);

  const fetchProviders = async () => {
    try {
      const data = await apiFetch('/api/video/providers');
      setProviders(data.providers || {});
      setModels(data.models || []);
    } catch (e) {
      console.error('Failed to fetch providers:', e);
    }
  };

  const fetchPrices = async () => {
    try {
      const data = await apiFetch('/api/video/prices?duration=5');
      setPrices(data.prices || []);
    } catch (e) {
      console.error('Failed to fetch prices:', e);
    }
  };

  // ─── Script Generation ───────────────────────────────────

  const handleGenerateScript = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!productName || !category || !features) {
      setError('Please fill in all required fields');
      return;
    }

    setLoading(true);
    setError('');
    setScript(null);
    setAudio(null);
    setVideoUrl(null);

    try {
      const data = await apiGenerate('video-script', {
        product_name: productName,
        category,
        features,
        target_audience: targetAudience,
        platform,
        language,
        tone,
        duration,
        n_scenes: nScenes,
        generate_audio: generateAudio,
        voice_language: voiceLanguage,
        voice_gender: voiceGender,
        tts_speed: ttsSpeed,
      });

      if (!data.success) throw new Error(data.error || 'Generation failed');
      if (data.success) {
        setScript(data.script);
        setAudio(data.audio || null);
      } else {
        throw new Error(data.error || 'Generation failed');
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // ─── Video Generation ────────────────────────────────────

  const handleGenerateVideo = async () => {
    if (!script) return;

    setLoading(true);
    setError('');
    setVideoUrl(null);

    try {
      // Build visual prompt from script
      const visualParts: string[] = [];
      if (script.hook.visual) visualParts.push(`Hook: ${script.hook.visual}`);
      for (const scene of script.scenes) {
        if (scene.visual) visualParts.push(`Scene ${scene.scene_number}: ${scene.visual}`);
      }
      if (script.cta.visual) visualParts.push(`CTA: ${script.cta.visual}`);

      // visualPrompt is built from script visuals for the AI video model
      // The script-to-video endpoint uses the full script object
      void visualParts; // used for video generation context

      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/video/script-to-video`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          script,
          model: videoModel,
          duration_per_scene: videoDuration,
          tts_provider: ttsProvider,
          tts_language: voiceLanguage,
          tts_gender: voiceGender,
          tts_speed: ttsSpeed,
          add_bgm: false,
        }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Video generation failed');
      if (data.success) {
        setVideoUrl(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${data.video_url}`);
        setVideoCost(data.cost_usd || 0);
        setSubTab('preview');
      } else {
        throw new Error(data.error || 'Video generation failed');
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // ─── Quick Generate (prompt → video) ─────────────────────

  const handleQuickGenerate = async (prompt: string) => {
    if (!prompt.trim()) return;

    setLoading(true);
    setError('');
    setVideoUrl(null);

    try {
      const [w, h] = aspectRatio === '9:16' ? [1080, 1920] : aspectRatio === '16:9' ? [1920, 1080] : [1080, 1080];

      const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${baseUrl}/api/video/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt,
          model: videoModel,
          duration: videoDuration,
          width: w,
          height: h,
          style_prompt: videoStyle || undefined,
          add_tts: generateAudio,
          tts_text: prompt,
          tts_provider: ttsProvider,
          tts_language: voiceLanguage,
          tts_gender: voiceGender,
          tts_speed: ttsSpeed,
        }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Video generation failed');
      if (data.success) {
        setVideoUrl(`${baseUrl}${data.video_url}`);
        setVideoCost(data.cost_usd || 0);
        setSubTab('preview');
      } else {
        throw new Error(data.error || 'Video generation failed');
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // ─── Audio Playback ──────────────────────────────────────

  const playAudio = (url: string) => {
    if (playingAudio === url) {
      audioRef.current?.pause();
      setPlayingAudio(null);
      return;
    }
    if (audioRef.current) {
      audioRef.current.pause();
    }
    const fullUrl = url.startsWith('http') ? url : `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${url}`;
    const audioEl = new Audio(fullUrl);
    audioEl.play();
    audioEl.onended = () => setPlayingAudio(null);
    audioRef.current = audioEl;
    setPlayingAudio(url);
  };

  // ─── Helpers ──────────────────────────────────────────────

  const copyScript = () => {
    if (!script) return;
    const text = [
      `# ${script.title}`,
      '',
      `## Hook (${script.hook.duration}s)`,
      script.hook.text,
      `*Visual: ${script.hook.visual}*`,
      '',
      ...script.scenes.flatMap(s => [
        `## Scene ${s.scene_number} (${s.duration}s)`,
        s.narration,
        `*Visual: ${s.visual}*`,
        '',
      ]),
      `## CTA (${script.cta.duration}s)`,
      script.cta.text,
      `*Visual: ${script.cta.visual}*`,
      '',
      `**Music:** ${script.music_suggestion}`,
      `**Hashtags:** ${script.hashtags.join(' ')}`,
    ].join('\n');
    navigator.clipboard.writeText(text);
  };

  const selectedModel = models.find(m => m.id === videoModel);
  const estimatedCost = selectedModel
    ? (selectedModel.price_per_sec * videoDuration).toFixed(4)
    : '0';

  const hasVideoProvider = providers['fal.ai'] || providers['replicate'];

  // ─── Render ──────────────────────────────────────────────

  return (
    <div className="video-gen">
      {/* Sub-tabs */}
      <div className="sub-tabs">
        <button
          className={`sub-tab ${subTab === 'script' ? 'active' : ''}`}
          onClick={() => setSubTab('script')}
        >
          📝 Script
        </button>
        <button
          className={`sub-tab ${subTab === 'generate' ? 'active' : ''} ${!script ? 'disabled' : ''}`}
          onClick={() => script && setSubTab('generate')}
          disabled={!script}
        >
          🎬 Generate Video
        </button>
        <button
          className={`sub-tab ${subTab === 'preview' ? 'active' : ''} ${!videoUrl ? 'disabled' : ''}`}
          onClick={() => videoUrl && setSubTab('preview')}
          disabled={!videoUrl}
        >
          ▶️ Preview
        </button>
      </div>

      {/* ─── Script Tab ─────────────────────────────────── */}
      {subTab === 'script' && (
        <div className="form-section">
          <h2>🎬 Video Script Generator</h2>
          <p>Create engaging short-form video scripts with AI-powered narration</p>

          <form onSubmit={handleGenerateScript}>
            <div className="form-grid">
              <div className="form-group">
                <label>Product Name *</label>
                <input type="text" value={productName} onChange={(e) => setProductName(e.target.value)}
                  placeholder="e.g., Wireless Earbuds Pro" />
              </div>
              <div className="form-group">
                <label>Category *</label>
                <input type="text" value={category} onChange={(e) => setCategory(e.target.value)}
                  placeholder="e.g., Electronics" />
              </div>
              <div className="form-group full-width">
                <label>Key Features *</label>
                <input type="text" value={features} onChange={(e) => setFeatures(e.target.value)}
                  placeholder="e.g., noise cancellation, 30hr battery, waterproof" />
              </div>
              <div className="form-group">
                <label>Target Audience</label>
                <input type="text" value={targetAudience} onChange={(e) => setTargetAudience(e.target.value)}
                  placeholder="e.g., young professionals" />
              </div>
              <div className="form-group">
                <label>Platform</label>
                <select value={platform} onChange={(e) => setPlatform(e.target.value)}>
                  <option value="tiktok">TikTok</option>
                  <option value="reels">Instagram Reels</option>
                  <option value="shorts">YouTube Shorts</option>
                </select>
              </div>
              <div className="form-group">
                <label>Language</label>
                <select value={language} onChange={(e) => setLanguage(e.target.value)}>
                  <option value="Vietnamese">Vietnamese</option>
                  <option value="English">English</option>
                  <option value="Chinese">Chinese</option>
                  <option value="Japanese">Japanese</option>
                  <option value="Korean">Korean</option>
                </select>
              </div>
              <div className="form-group">
                <label>Tone</label>
                <select value={tone} onChange={(e) => setTone(e.target.value)}>
                  <option value="engaging">Engaging</option>
                  <option value="professional">Professional</option>
                  <option value="fun">Fun</option>
                  <option value="urgent">Urgent</option>
                  <option value="emotional">Emotional</option>
                </select>
              </div>
              <div className="form-group">
                <label>Duration (seconds)</label>
                <input type="number" min={15} max={120} value={duration}
                  onChange={(e) => setDuration(Number(e.target.value))} />
              </div>
              <div className="form-group">
                <label>Number of Scenes</label>
                <input type="number" min={2} max={10} value={nScenes}
                  onChange={(e) => setNScenes(Number(e.target.value))} />
              </div>
            </div>

            {/* TTS Options */}
            <div className="tts-options">
              <h3>🎙️ Voice Settings</h3>
              <label className="checkbox-label">
                <input type="checkbox" checked={generateAudio}
                  onChange={(e) => setGenerateAudio(e.target.checked)} />
                Generate TTS Audio
              </label>
              {generateAudio && (
                <div className="form-grid">
                  <div className="form-group">
                    <label>TTS Provider</label>
                    <select value={ttsProvider} onChange={(e) => setTtsProvider(e.target.value)}>
                      <option value="edge">Edge-TTS (Free)</option>
                      <option value="elevenlabs">ElevenLabs (Premium)</option>
                      <option value="openai_tts">OpenAI TTS</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Voice Language</label>
                    <select value={voiceLanguage} onChange={(e) => setVoiceLanguage(e.target.value)}>
                      <option value="vi">Vietnamese</option>
                      <option value="en">English</option>
                      <option value="zh">Chinese</option>
                      <option value="ja">Japanese</option>
                      <option value="ko">Korean</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Voice Gender</label>
                    <select value={voiceGender} onChange={(e) => setVoiceGender(e.target.value)}>
                      <option value="female">Female</option>
                      <option value="male">Male</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Speed: {ttsSpeed}x</label>
                    <input type="range" min={0.5} max={2.0} step={0.1} value={ttsSpeed}
                      onChange={(e) => setTtsSpeed(Number(e.target.value))} />
                  </div>
                </div>
              )}
            </div>

            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? '⏳ Generating...' : '🎬 Generate Video Script'}
            </button>
          </form>

          {/* Script Result */}
          {script && (
            <div className="script-result">
              <div className="result-header">
                <h2>{script.title}</h2>
                <div className="result-actions">
                  {audio?.full_narration_url && (
                    <button className={`audio-btn ${playingAudio === audio.full_narration_url ? 'playing' : ''}`}
                      onClick={() => playAudio(audio.full_narration_url!)}>
                      {playingAudio === audio.full_narration_url ? '⏸️ Pause' : '▶️ Play Full Narration'}
                    </button>
                  )}
                  <button className="copy-btn" onClick={copyScript}>📋 Copy Script</button>
                  <button className="next-btn" onClick={() => setSubTab('generate')}>
                    Next: Generate Video →
                  </button>
                </div>
              </div>

              {audio && !audio.error && (
                <div className="audio-info">
                  <span>🎙️ Total narration: ~{audio.total_duration}s</span>
                  {audio.available === false && (
                    <span className="warning">⚠️ TTS not available (install edge-tts)</span>
                  )}
                </div>
              )}

              <div className="script-section hook">
                <div className="section-header">
                  <h3>🪝 Hook ({script.hook.duration}s)</h3>
                  {audio?.hook_url && (
                    <button className={`audio-btn small ${playingAudio === audio.hook_url ? 'playing' : ''}`}
                      onClick={() => playAudio(audio.hook_url!)}>
                      {playingAudio === audio.hook_url ? '⏸️' : '▶️'}
                    </button>
                  )}
                </div>
                <p className="narration">{script.hook.text}</p>
                <p className="visual">📷 {script.hook.visual}</p>
              </div>

              {script.scenes.map((scene) => (
                <div key={scene.scene_number} className="script-section scene">
                  <div className="section-header">
                    <h3>🎬 Scene {scene.scene_number} ({scene.duration}s)</h3>
                    {audio?.scenes?.find(s => s.scene_number === scene.scene_number)?.audio_url && (
                      <button className={`audio-btn small ${playingAudio === audio.scenes.find(s => s.scene_number === scene.scene_number)?.audio_url ? 'playing' : ''}`}
                        onClick={() => playAudio(audio.scenes.find(s => s.scene_number === scene.scene_number)!.audio_url!)}>
                        {playingAudio === audio.scenes.find(s => s.scene_number === scene.scene_number)?.audio_url ? '⏸️' : '▶️'}
                      </button>
                    )}
                  </div>
                  <p className="narration">{scene.narration}</p>
                  <p className="visual">📷 {scene.visual}</p>
                </div>
              ))}

              <div className="script-section cta">
                <div className="section-header">
                  <h3>📢 Call-to-Action ({script.cta.duration}s)</h3>
                  {audio?.cta_url && (
                    <button className={`audio-btn small ${playingAudio === audio.cta_url ? 'playing' : ''}`}
                      onClick={() => playAudio(audio.cta_url!)}>
                      {playingAudio === audio.cta_url ? '⏸️' : '▶️'}
                    </button>
                  )}
                </div>
                <p className="narration">{script.cta.text}</p>
                <p className="visual">📷 {script.cta.visual}</p>
              </div>

<div className="video-gen">
                <div className="music"><strong>🎵 Music:</strong> {script.music_suggestion}</div>
                <div className="hashtags">
                  <strong>🏷️ Hashtags:</strong>
                  {script.hashtags.map((tag, i) => (
                    <span key={i} className="hashtag">{tag}</span>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ─── Generate Tab ────────────────────────────────── */}
      {subTab === 'generate' && script && (
        <div className="form-section">
          <h2>🎬 Generate AI Video</h2>
          <p>Convert your script to video with AI generation</p>

          {!hasVideoProvider && (
            <div className="provider-warning">
              ⚠️ No video generation provider configured.
              Set <code>FAL_API_KEY</code> or <code>REPLICATE_API_KEY</code> in .env
            </div>
          )}

<div className="video-gen">
            <div className="option-group">
              <h3>🤖 Video Model</h3>
              <div className="model-grid">
                {models.filter(m => m.max_duration >= 5).map((model) => (
                  <div
                    key={model.id}
                    className={`model-card ${videoModel === model.id ? 'selected' : ''}`}
                    onClick={() => setVideoModel(model.id)}
                  >
                    <div className="model-name">{model.id.replace(/_/g, ' ')}</div>
                    <div className="model-price">${model.price_per_sec}/s</div>
                    <div className="model-meta">
                      Max {model.max_duration}s
                      {model.native_audio && ' • 🔊 Audio'}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="form-grid">
              <div className="form-group">
                <label>Duration per Scene</label>
                <select value={videoDuration} onChange={(e) => setVideoDuration(Number(e.target.value))}>
                  {[3, 5, 8, 10].filter(d => !selectedModel || d <= selectedModel.max_duration).map(d => (
                    <option key={d} value={d}>{d}s</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Aspect Ratio</label>
                <select value={aspectRatio} onChange={(e) => setAspectRatio(e.target.value)}>
                  <option value="9:16">9:16 (Portrait)</option>
                  <option value="16:9">16:9 (Landscape)</option>
                  <option value="1:1">1:1 (Square)</option>
                </select>
              </div>
              <div className="form-group">
                <label>Style (optional)</label>
                <select value={videoStyle} onChange={(e) => setVideoStyle(e.target.value)}>
                  <option value="">Default</option>
                  <option value="cinematic">Cinematic</option>
                  <option value="anime">Anime</option>
                  <option value="cartoon">Cartoon</option>
                  <option value="realistic">Realistic</option>
                  <option value="3d">3D Render</option>
                </select>
              </div>
            </div>

            {/* Cost Estimate */}
            <div className="cost-estimate">
              <div className="cost-row">
                <span>Video ({videoDuration}s × ${selectedModel?.price_per_sec || 0}/s):</span>
                <span>${estimatedCost}</span>
              </div>
              <div className="cost-row">
                <span>TTS ({ttsProvider === 'edge' ? 'Free' : ttsProvider === 'elevenlabs' ? '~$0.005' : '~$0.007'}):</span>
                <span>{ttsProvider === 'edge' ? '$0' : '~$0.01'}</span>
              </div>
              <div className="cost-row total">
                <span>Estimated Total:</span>
                <span>${(parseFloat(estimatedCost) + (ttsProvider === 'edge' ? 0 : 0.01)).toFixed(4)}</span>
              </div>
            </div>

            <button
              className="submit-btn"
              onClick={handleGenerateVideo}
              disabled={loading || !hasVideoProvider}
            >
              {loading ? '⏳ Generating Video...' : '🎬 Generate Video'}
            </button>
          </div>

          {/* Quick Generate (without script) */}
          <div className="quick-generate">
            <h3>⚡ Quick Generate (from prompt)</h3>
            <div className="quick-form">
              <input
                type="text"
                placeholder="Enter a video prompt (e.g., 'A cat dancing in the rain, cinematic style')"
                onKeyDown={(e) => {
                  if (e.key === 'Enter') handleQuickGenerate((e.target as HTMLInputElement).value);
                }}
              />
              <button
                className="quick-btn"
                onClick={() => {
                  const input = document.querySelector('.quick-form input') as HTMLInputElement;
                  if (input) handleQuickGenerate(input.value);
                }}
                disabled={loading || !hasVideoProvider}
              >
                ⚡ Generate
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ─── Preview Tab ─────────────────────────────────── */}
      {subTab === 'preview' && videoUrl && (
        <div className="form-section preview-section">
          <h2>▶️ Video Preview</h2>

<div className="video-gen">
            <video
              src={videoUrl}
              controls
              autoPlay
              loop
              playsInline
              className="video-element"
            >
              Your browser does not support video playback.
            </video>
          </div>

<div className="video-gen">
            <div className="info-row">
              <span>Model:</span>
              <span>{videoModel.replace(/_/g, ' ')}</span>
            </div>
            <div className="info-row">
              <span>Cost:</span>
              <span>${videoCost.toFixed(4)}</span>
            </div>
            <div className="info-row">
              <span>TTS:</span>
              <span>{ttsProvider === 'edge' ? 'Edge-TTS (Free)' : ttsProvider}</span>
            </div>
          </div>

          <div className="preview-actions">
            <a href={videoUrl} download className="download-btn">
              ⬇️ Download Video
            </a>
            <button className="back-btn" onClick={() => setSubTab('generate')}>
              ← Back to Generate
            </button>
          </div>
        </div>
      )}

      {/* Error */}
      {error && <div className="error">❌ {error}</div>}
    </div>
  );
}
