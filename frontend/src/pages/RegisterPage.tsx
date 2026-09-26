import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { UserPlus } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';

export const RegisterPage: React.FC = () => {
  const { register, login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: '', username: '', full_name: '', password: '' });
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const update = (key: keyof typeof form) => (event: React.ChangeEvent<HTMLInputElement>) => setForm((current) => ({ ...current, [key]: event.target.value }));
  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError('');
    if (form.password.length < 8) { setError('Password must be at least 8 characters.'); return; }
    setIsSubmitting(true);
    try {
      await register(form);
      await login({ email: form.email, password: form.password });
      navigate('/courses', { replace: true });
    } catch (reason) {
      setError((reason as { response?: { data?: { error?: { message?: string } } } })?.response?.data?.error?.message || 'Registration failed. Please check your details.');
    } finally { setIsSubmitting(false); }
  };

  return (
    <div className="mx-auto flex min-h-[calc(100vh-8rem)] max-w-md items-center px-4 py-12">
      <form onSubmit={submit} className="w-full space-y-5 rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
        <div><div className="mb-4 inline-flex rounded-xl bg-emerald-50 p-3 text-emerald-600"><UserPlus /></div><h1 className="text-2xl font-bold text-slate-900">Create your account</h1><p className="mt-1 text-sm text-slate-500">Start your learning journey with LITERA.</p></div>
        {error && <div className="rounded-xl border border-rose-200 bg-rose-50 p-3 text-sm text-rose-700">{error}</div>}
        <label className="block text-sm font-medium text-slate-700">Full name<input required minLength={2} value={form.full_name} onChange={update('full_name')} className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-indigo-500" /></label>
        <label className="block text-sm font-medium text-slate-700">Username<input required minLength={3} value={form.username} onChange={update('username')} className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-indigo-500" /></label>
        <label className="block text-sm font-medium text-slate-700">Email<input required type="email" value={form.email} onChange={update('email')} className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-indigo-500" /></label>
        <label className="block text-sm font-medium text-slate-700">Password<input required type="password" minLength={8} value={form.password} onChange={update('password')} className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-indigo-500" /></label>
        <button disabled={isSubmitting} className="w-full rounded-xl bg-indigo-600 px-4 py-3 text-sm font-semibold text-white hover:bg-indigo-700 disabled:opacity-60">{isSubmitting ? 'Creating account...' : 'Create account'}</button>
        <p className="text-center text-sm text-slate-500">Already registered? <Link to="/login" className="font-semibold text-indigo-600">Sign in</Link></p>
      </form>
    </div>
  );
};
