import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, ChevronLeft, ChevronRight, Search, SlidersHorizontal } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { catalogService } from '@/services/catalog';
import type { CourseLevel } from '@/types/catalog';
import { ErrorState, LoadingState } from '@/components/ApiState';

const levelLabel: Record<CourseLevel, string> = { BEGINNER: 'Beginner', INTERMEDIATE: 'Intermediate', ADVANCED: 'Advanced' };

export const CoursesPage: React.FC = () => {
  const [search, setSearch] = useState('');
  const [level, setLevel] = useState<CourseLevel | ''>('');
  const [category, setCategory] = useState('');
  const [page, setPage] = useState(1);
  const query = useQuery({ queryKey: ['courses', { search, level, category, page }], queryFn: () => catalogService.listCourses({ search, level, category, page }), });
  const data = query.data;

  return <div className="mx-auto max-w-7xl space-y-8 px-4 py-10 sm:px-6 lg:px-8">
    <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end"><div><p className="text-sm font-semibold uppercase tracking-widest text-indigo-600">Explore learning</p><h1 className="mt-2 text-3xl font-bold text-slate-900 md:text-4xl">Course catalog</h1><p className="mt-2 max-w-2xl text-slate-500">Build practical digital literacy and critical thinking skills through structured lessons.</p></div><Link to="/" className="text-sm font-semibold text-indigo-600 hover:text-indigo-700">Back to home</Link></div>
    <div className="grid gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm md:grid-cols-[1fr_180px_180px_auto]"><label className="relative block"><Search className="absolute left-3 top-3 h-4 w-4 text-slate-400" /><input value={search} onChange={(e) => { setSearch(e.target.value); setPage(1); }} placeholder="Search courses..." className="w-full rounded-xl border border-slate-200 py-2.5 pl-9 pr-3 text-sm outline-none focus:border-indigo-500" /></label><select value={level} onChange={(e) => { setLevel(e.target.value as CourseLevel | ''); setPage(1); }} className="rounded-xl border border-slate-200 px-3 py-2.5 text-sm text-slate-600 outline-none focus:border-indigo-500"><option value="">All levels</option><option value="BEGINNER">Beginner</option><option value="INTERMEDIATE">Intermediate</option><option value="ADVANCED">Advanced</option></select><input value={category} onChange={(e) => { setCategory(e.target.value); setPage(1); }} placeholder="Category slug" className="rounded-xl border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-indigo-500" /><button onClick={() => { setSearch(''); setLevel(''); setCategory(''); setPage(1); }} className="inline-flex items-center justify-center gap-2 rounded-xl bg-slate-100 px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-200"><SlidersHorizontal className="h-4 w-4" />Reset</button></div>
    {query.isLoading ? <LoadingState label="Loading courses..." /> : query.isError ? <ErrorState message="Could not load courses from the API." onRetry={() => query.refetch()} /> : data?.items.length === 0 ? <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center"><BookOpen className="mx-auto h-8 w-8 text-slate-300" /><p className="mt-3 font-semibold text-slate-700">No published courses found</p><p className="mt-1 text-sm text-slate-500">Try clearing your filters or run the demo seed.</p></div> : <>
      <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">{data?.items.map((course) => <Link key={course.id} to={`/courses/${course.slug}`} className="group overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:-translate-y-1 hover:border-indigo-200 hover:shadow-lg"><div className="flex h-32 items-end bg-gradient-to-br from-indigo-600 via-violet-500 to-emerald-400 p-5"><span className="rounded-full bg-white/20 px-3 py-1 text-xs font-semibold text-white backdrop-blur">{levelLabel[course.level]}</span></div><div className="space-y-3 p-5"><p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">{course.category.name}</p><h2 className="text-lg font-bold text-slate-900 group-hover:text-indigo-600">{course.title}</h2><p className="line-clamp-2 text-sm leading-relaxed text-slate-500">{course.description}</p><span className="inline-block text-sm font-semibold text-indigo-600">View course →</span></div></Link>)}</div>
      {data && data.total_pages > 1 && <div className="flex items-center justify-between rounded-2xl border border-slate-200 bg-white px-4 py-3"><span className="text-sm text-slate-500">Page {data.page} of {data.total_pages}</span><div className="flex gap-2"><button disabled={page <= 1} onClick={() => setPage((current) => current - 1)} className="rounded-lg border border-slate-200 p-2 disabled:opacity-40"><ChevronLeft className="h-4 w-4" /></button><button disabled={page >= data.total_pages} onClick={() => setPage((current) => current + 1)} className="rounded-lg border border-slate-200 p-2 disabled:opacity-40"><ChevronRight className="h-4 w-4" /></button></div></div>}
    </>}
  </div>;
};
