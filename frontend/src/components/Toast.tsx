/* src/components/Toast.tsx — Notification System */
import { useState, useEffect, useCallback } from 'react';

export interface ToastMessage {
  id: number;
  type: 'success' | 'error' | 'info' | 'warning';
  text: string;
}

let toastId = 0;
const listeners: Set<(toast: ToastMessage) => void> = new Set();

export function showToast(type: ToastMessage['type'], text: string) {
  const toast: ToastMessage = { id: ++toastId, type, text };
  listeners.forEach((fn) => fn(toast));
}

export function ToastContainer() {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const addToast = useCallback((toast: ToastMessage) => {
    setToasts((prev) => [...prev, toast]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== toast.id));
    }, 4000);
  }, []);

  useEffect(() => {
    listeners.add(addToast);
    return () => { listeners.delete(addToast); };
  }, [addToast]);

  const removeToast = (id: number) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  const icons: Record<string, string> = {
    success: '✅',
    error: '❌',
    info: 'ℹ️',
    warning: '⚠️',
  };

  return (
    <div className="toast-container">
      {toasts.map((toast) => (
        <div key={toast.id} className={`toast toast-${toast.type}`} onClick={() => removeToast(toast.id)}>
          <span className="toast-icon">{icons[toast.type]}</span>
          <span className="toast-text">{toast.text}</span>
          <button className="toast-close" onClick={() => removeToast(toast.id)}>×</button>
        </div>
      ))}
    </div>
  );
}
