import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { LoadingState } from '@/components/ApiState';

export const ProfilePage: React.FC = () => {
  const { user, isLoading } = useAuth();
  if (isLoading) return <LoadingState label="Loading profile..." />;
  if (!user) return <Navigate to="/login" replace state={{ from: '/profile' }} />;
  return <div className="mx-auto max-w-2xl px-4 py-12"><div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm"><p className="text-sm font-semibold uppercase tracking-widest text-indigo-600">Your account</p><h1 className="mt-2 text-3xl font-bold text-slate-900">{user.full_name}</h1><div className="mt-8 grid gap-4 sm:grid-cols-2"><div className="rounded-2xl bg-slate-50 p-4"><p className="text-xs text-slate-500">Username</p><p className="mt-1 font-semibold text-slate-800">@{user.username}</p></div><div className="rounded-2xl bg-slate-50 p-4"><p className="text-xs text-slate-500">Role</p><p className="mt-1 font-semibold text-slate-800">{user.role}</p></div><div className="rounded-2xl bg-slate-50 p-4 sm:col-span-2"><p className="text-xs text-slate-500">Email</p><p className="mt-1 font-semibold text-slate-800">{user.email}</p></div></div></div></div>;
};
