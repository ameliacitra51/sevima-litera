import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { healthService } from '@/services/api';
import { CheckCircle2, AlertCircle, RefreshCw, Layers, ShieldCheck, Database, Code2 } from 'lucide-react';

export const HomePage: React.FC = () => {
  const { data: health, isLoading, isError, error, refetch, isFetching } = useQuery({
    queryKey: ['backend-health'],
    queryFn: healthService.checkHealth,
    retry: 1,
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
      {/* Hero Section */}
      <section className="text-center space-y-4 max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          Phase 2: Project Foundation Active
        </div>
        <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-slate-900">
          LITERA Learning Platform
        </h1>
        <p className="text-base sm:text-lg text-slate-600 leading-relaxed">
          Digital literacy, information evaluation, and critical thinking platform for high-school and university students.
        </p>
      </section>

      {/* Backend Connectivity Status Card */}
      <section className="max-w-2xl mx-auto bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-lg bg-indigo-50 text-indigo-600">
              <Layers className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-semibold text-slate-900">Backend Connectivity Check</h2>
              <p className="text-xs text-slate-500">Querying FastAPI health endpoint via TanStack Query & Axios</p>
            </div>
          </div>
          <button
            onClick={() => refetch()}
            disabled={isFetching}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isFetching ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>

        {isLoading ? (
          <div className="py-6 flex flex-col items-center justify-center space-y-2 text-slate-500">
            <RefreshCw className="w-6 h-6 animate-spin text-indigo-600" />
            <span className="text-xs">Connecting to backend at http://localhost:8000/api/v1/health...</span>
          </div>
        ) : isError ? (
          <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-amber-600 mt-0.5 shrink-0" />
            <div className="space-y-1 text-xs">
              <p className="font-semibold text-amber-900">Backend Server Not Detected</p>
              <p className="text-amber-800">
                {(error as Error)?.message || 'Failed to connect to FastAPI backend.'}
              </p>
              <p className="text-amber-700 mt-1">
                Make sure the backend is running with: <code className="bg-amber-100 px-1 py-0.5 rounded font-mono">uvicorn app.main:app --reload</code>
              </p>
            </div>
          </div>
        ) : (
          <div className="space-y-3">
            <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center gap-3">
              <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
              <div className="text-xs text-emerald-900">
                <span className="font-semibold">FastAPI Backend Connected: </span>
                <span>{health?.service} v{health?.version} ({health?.environment})</span>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="p-3 rounded-lg bg-slate-50 border border-slate-100">
                <span className="text-slate-500 block">Service Status</span>
                <span className="font-semibold text-slate-800 uppercase">{health?.status}</span>
              </div>
              <div className="p-3 rounded-lg bg-slate-50 border border-slate-100">
                <span className="text-slate-500 block">Server Time (UTC)</span>
                <span className="font-mono text-slate-800">
                  {health?.timestamp ? new Date(health.timestamp).toLocaleTimeString() : 'N/A'}
                </span>
              </div>
            </div>
          </div>
        )}
      </section>

      {/* Architecture Highlights */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto pt-6">
        <div className="p-5 rounded-xl bg-white border border-slate-200 shadow-sm space-y-2">
          <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
            <Code2 className="w-4 h-4" />
          </div>
          <h3 className="text-sm font-semibold text-slate-900">React + Vite + TypeScript</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Strict type safety, TanStack Query server caching, Tailwind CSS styling, and Axios interceptor architecture.
          </p>
        </div>

        <div className="p-5 rounded-xl bg-white border border-slate-200 shadow-sm space-y-2">
          <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center">
            <ShieldCheck className="w-4 h-4" />
          </div>
          <h3 className="text-sm font-semibold text-slate-900">FastAPI Modular API</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Layered architecture with Pydantic validation, CORS middleware, centralized error handling, and health monitoring.
          </p>
        </div>

        <div className="p-5 rounded-xl bg-white border border-slate-200 shadow-sm space-y-2">
          <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <Database className="w-4 h-4" />
          </div>
          <h3 className="text-sm font-semibold text-slate-900">PostgreSQL Ready</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            SQLAlchemy 2.0 and Alembic migration foundation prepared for Phase 3 database modeling.
          </p>
        </div>
      </section>
    </div>
  );
};
