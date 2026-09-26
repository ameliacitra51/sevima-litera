import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-200 bg-white py-8 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
        <p>© {new Date().getFullYear()} LITERA — Digital Literacy & Learning Platform.</p>
        <p className="flex items-center gap-4">
          <span>React + Vite + TypeScript</span>
          <span>•</span>
          <span>FastAPI</span>
          <span>•</span>
          <span>PostgreSQL</span>
        </p>
      </div>
    </footer>
  );
};
