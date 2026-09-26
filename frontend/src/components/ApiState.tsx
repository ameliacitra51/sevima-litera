import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

export const LoadingState: React.FC<{ label?: string }> = ({ label = 'Loading...' }) => (
  <div className="flex min-h-48 flex-col items-center justify-center gap-3 text-slate-500">
    <RefreshCw className="h-6 w-6 animate-spin text-indigo-600" />
    <span className="text-sm">{label}</span>
  </div>
);

export const ErrorState: React.FC<{ message?: string; onRetry?: () => void }> = ({ message, onRetry }) => (
  <div className="rounded-2xl border border-rose-200 bg-rose-50 p-6 text-center">
    <AlertCircle className="mx-auto mb-2 h-6 w-6 text-rose-600" />
    <p className="text-sm font-semibold text-rose-900">Unable to load data</p>
    <p className="mt-1 text-xs text-rose-700">{message || 'Please make sure the backend is running.'}</p>
    {onRetry && <button onClick={onRetry} className="mt-4 rounded-lg bg-rose-600 px-4 py-2 text-xs font-semibold text-white hover:bg-rose-700">Try again</button>}
  </div>
);
