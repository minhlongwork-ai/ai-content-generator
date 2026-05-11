/* src/components/Settings.tsx — API Keys & Model Configuration */
import { useState, useEffect } from 'react';
import { apiFetch } from '../api';

interface ApiKeysConfigured {
  openrouter: boolean;
  fal: boolean;
  replicate: boolean;
  elevenlabs: boolean;
  openai: boolean;
  '9router': boolean;
}

interface SettingField {
  key: string;
  label: string;
  type: 'text' | 'password' | 'select' | 'url';
  placeholder: string;
  description: string;
  group: 'llm' | 'video' | 'tts' | 'general';
  options?: { value: string; label: string }[];
}

const SETTING_FIELDS: SettingField[] = [
  // LLM
  {
    key: 'OPENROUTER_API_KEY',
    label: 'OpenRouter API Key',
    type: 'password',
    placeholder: 'sk-or-v1-xxxxxxxx',
    description: 'Required for text generation. Get from openrouter.ai/keys',
    group: 'llm',
  },
  {
    key: 'DEFAULT_MODEL',
    label: 'Default LLM Model',
    type: 'select',
    placeholder: '',
    description: 'Model used for text generation',
    group: 'llm',
    options: [
      { value: 'nvidia/nemotron-3-super-120b-a12b:free', label: 'Nemotron 3 Super 120B (Free)' },
      { value: 'nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free', label: 'Nemotron 3 Nano (Free)' },
      { value: 'google/gemma-4-26b-a4b-it:free', label: 'Gemma 4 26B (Free)' },
      { value: 'minimax/minimax-m2.5:free', label: 'MiniMax M2.5 (Free)' },
      { value: 'qwen/qwen3-next-80b-a3b-instruct:free', label: 'Qwen3 Next 80B (Free)' },
      { value: 'openai/gpt-4o-mini', label: 'GPT-4o Mini (Paid)' },
      { value: 'anthropic/claude-sonnet-4-5', label: 'Claude Sonnet 4.5 (Paid)' },
      { value: 'deepseek/deepseek-chat', label: 'DeepSeek Chat (Paid)' },
    ],
  },
  {
    key: 'AI_BACKEND',
    label: 'AI Backend',
    type: 'select',
    placeholder: '',
    description: 'Choose between OpenRouter or 9Router (local gateway)',
    group: 'llm',
    options: [
      { value: 'openrouter', label: 'OpenRouter (Cloud)' },
      { value: '9router', label: '9Router (Local Gateway)' },
    ],
  },
  {
    key: 'NINEROUTER_URL',
    label: '9Router URL',
    type: 'url',
    placeholder: 'http://localhost:3000',
    description: 'Local 9Router gateway URL (only needed if AI_BACKEND=9router)',
    group: 'llm',
  },
  // Video
  {
    key: 'FAL_API_KEY',
    label: 'fal.ai API Key',
    type: 'password',
    placeholder: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
    description: 'For AI video generation (Seedance, Kling, Veo, etc.). Get from fal.ai/dashboard/keys',
    group: 'video',
  },
  {
    key: 'REPLICATE_API_KEY',
    label: 'Replicate API Key',
    type: 'password',
    placeholder: 'r8_xxxxxxxx',
    description: 'Alternative video generation via Replicate (optional)',
    group: 'video',
  },
  // TTS
  {
    key: 'ELEVENLABS_API_KEY',
    label: 'ElevenLabs API Key',
    type: 'password',
    placeholder: 'xxxxxxxx',
    description: 'Premium TTS with voice cloning. Get from elevenlabs.io/app/settings/api-keys',
    group: 'tts',
  },
  {
    key: 'OPENAI_API_KEY',
    label: 'OpenAI API Key',
    type: 'password',
    placeholder: 'sk-xxxxxxxx',
    description: 'For OpenAI TTS or Sora 2 video (optional)',
    group: 'tts',
  },
];

const GROUPS = [
  { id: 'llm', label: '🤖 LLM (Text Generation)', description: 'API keys for AI text generation' },
  { id: 'video', label: '🎬 Video Generation', description: 'API keys for AI video models' },
  { id: 'tts', label: '🎙️ Text-to-Speech', description: 'API keys for voice synthesis' },
];

interface SettingsProps {
  token?: string | null;
  user?: any;
  onLogout?: () => void;
}

export default function Settings({ user, onLogout }: SettingsProps) {
  const [settings, setSettings] = useState<Record<string, string>>({});
  const [apiKeysStatus, setApiKeysStatus] = useState<ApiKeysConfigured | null>(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [showKeys, setShowKeys] = useState<Record<string, boolean>>({});
  const [activeGroup, setActiveGroup] = useState('llm');

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    setLoading(true);
    try {
      const resp = await apiFetch('/api/settings');
      setSettings(resp.settings || {});
      setApiKeysStatus(resp.api_keys_configured || {});
    } catch (e) {
      console.error('Failed to fetch settings:', e);
      setMessage({ type: 'error', text: 'Failed to fetch settings' });
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage(null);
    try {
      const data = await apiFetch('/api/settings', {
        method: 'POST',
        body: JSON.stringify({ settings }),
      });
      if (data.success) {
        setMessage({ type: 'success', text: 'Settings saved successfully!' });
        setApiKeysStatus(data.api_keys_configured);
      } else {
        throw new Error(data.detail || 'Failed to save');
      }
    } catch (e: any) {
      setMessage({ type: 'error', text: e.message });
    } finally {
      setSaving(false);
    }
  };

  const handleInputChange = (key: string, value: string) => {
    setSettings((prev) => ({ ...prev, [key]: value }));
  };

  const toggleShowKey = (key: string) => {
    setShowKeys((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const getStatusBadge = (key: string) => {
    if (!apiKeysStatus) return null;
    const mapping: Record<string, keyof ApiKeysConfigured> = {
      OPENROUTER_API_KEY: 'openrouter',
      FAL_API_KEY: 'fal',
      REPLICATE_API_KEY: 'replicate',
      ELEVENLABS_API_KEY: 'elevenlabs',
      OPENAI_API_KEY: 'openai',
      NINEROUTER_URL: '9router',
    };
    const statusKey = mapping[key];
    if (!statusKey) return null;
    const isConfigured = apiKeysStatus[statusKey];
    return (
      <span className={`status-badge ${isConfigured ? 'configured' : 'missing'}`}>
        {isConfigured ? '✅ Configured' : '❌ Not set'}
      </span>
    );
  };

  const fieldsByGroup = (group: string) =>
    SETTING_FIELDS.filter((f) => f.group === group);

  if (loading) {
    return (
      <div className="settings-page">
        <div className="loading">⏳ Loading settings...</div>
      </div>
    );
  }

  return (
    <div className="settings-page">
      <div className="settings-header">
        <h2>⚙️ Settings</h2>
        <p>Configure API keys and model preferences</p>
      </div>

      {/* Group tabs */}
      <div className="settings-groups">
        {GROUPS.map((group) => (
          <button
            key={group.id}
            className={`group-tab ${activeGroup === group.id ? 'active' : ''}`}
            onClick={() => setActiveGroup(group.id)}
          >
            {group.label}
          </button>
        ))}
      </div>

      {/* Active group */}
      {GROUPS.filter((g) => g.id === activeGroup).map((group) => (
        <div key={group.id} className="settings-group">
          <div className="group-description">{group.description}</div>

          <div className="settings-fields">
            {fieldsByGroup(group.id).map((field) => (
              <div key={field.key} className="setting-field">
                <div className="field-header">
                  <label>{field.label}</label>
                  {getStatusBadge(field.key)}
                </div>
                <p className="field-description">{field.description}</p>

                <div className="field-input">
                  {field.type === 'select' ? (
                    <select
                      value={settings[field.key] || ''}
                      onChange={(e) => handleInputChange(field.key, e.target.value)}
                    >
                      <option value="">-- Select --</option>
                      {field.options?.map((opt) => (
                        <option key={opt.value} value={opt.value}>
                          {opt.label}
                        </option>
                      ))}
                    </select>
                  ) : field.type === 'password' ? (
                    <div className="password-input">
                      <input
                        type={showKeys[field.key] ? 'text' : 'password'}
                        value={settings[field.key] || ''}
                        onChange={(e) => handleInputChange(field.key, e.target.value)}
                        placeholder={field.placeholder}
                      />
                      <button
                        type="button"
                        className="toggle-visibility"
                        onClick={() => toggleShowKey(field.key)}
                      >
                        {showKeys[field.key] ? '🙈' : '👁️'}
                      </button>
                    </div>
                  ) : (
                    <input
                      type={field.type}
                      value={settings[field.key] || ''}
                      onChange={(e) => handleInputChange(field.key, e.target.value)}
                      placeholder={field.placeholder}
                    />
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}

      {/* Save button */}
      <div className="settings-actions">
        <button className="save-btn" onClick={handleSave} disabled={saving}>
          {saving ? '⏳ Saving...' : '💾 Save Settings'}
        </button>
        <button className="refresh-btn" onClick={fetchSettings}>
          🔄 Refresh
        </button>
      </div>

      {message && (
        <div className={`message ${message.type}`}>
          {message.type === 'success' ? '✅' : '❌'} {message.text}
        </div>
      )}

      {/* Quick links */}
      <div className="settings-links">
        <h3>🔗 Get API Keys</h3>
        <div className="links-grid">
          <a href="https://openrouter.ai/keys" target="_blank" rel="noopener noreferrer" className="link-card">
            <span className="link-icon">🤖</span>
            <span className="link-label">OpenRouter</span>
            <span className="link-desc">Free tier available</span>
          </a>
          <a href="https://fal.ai/dashboard/keys" target="_blank" rel="noopener noreferrer" className="link-card">
            <span className="link-icon">🎬</span>
            <span className="link-label">fal.ai</span>
            <span className="link-desc">Video generation</span>
          </a>
          <a href="https://replicate.com/account/api-tokens" target="_blank" rel="noopener noreferrer" className="link-card">
            <span className="link-icon">🔄</span>
            <span className="link-label">Replicate</span>
            <span className="link-desc">Alternative video</span>
          </a>
          <a href="https://elevenlabs.io/app/settings/api-keys" target="_blank" rel="noopener noreferrer" className="link-card">
            <span className="link-icon">🎙️</span>
            <span className="link-label">ElevenLabs</span>
            <span className="link-desc">Premium TTS</span>
          </a>
        </div>
      </div>

      {/* Account Section */}
      {user && (
        <div className="settings-account">
          <h3>👤 Account</h3>
          <div className="account-info">
            <div className="account-row">
              <span className="account-label">Name</span>
              <span className="account-value">{user.name}</span>
            </div>
            <div className="account-row">
              <span className="account-label">Email</span>
              <span className="account-value">{user.email}</span>
            </div>
            <div className="account-row">
              <span className="account-label">Plan</span>
              <span className="account-value plan-badge-inline">{user.plan || 'Free'}</span>
            </div>
          </div>
          {onLogout && (
            <button className="btn-logout" onClick={onLogout}>
              🚪 Sign Out
            </button>
          )}
        </div>
      )}
    </div>
  );
}
