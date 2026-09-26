import React from 'react';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, BookOpen, Clock, PlayCircle } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { catalogService } from '@/services/catalog';
import { ErrorState, LoadingState } from '@/components/ApiState';

export const CourseDetailPage: React.FC = () => {
  const { slug = '' } = useParams();
  const query = useQuery({ queryKey: ['course', slug], queryFn: () => catalogService.getCourse(slug), enabled: Boolean(slug) });
  if (query.isLoading) return <LoadingState label="Loading course..." />;
  if (query.isError || !query.data) return <div className="mx-auto max-w-3xl px-4 py-12"><ErrorState message="This course could not be found or is not published." onRetry={() => query.refetch()} /></div>;
  const course = query.data;
  return <div className="mx-auto max-w-5xl space-y-8 px-4 py-10 sm:px-6 lg:px-8"><Link to="/courses" className="inline-flex items-center gap-2 text-sm font-semibold text-indigo-600"><ArrowLeft className="h-4 w-4" />Back to courses</Link><section className="overflow-hidden rounded-3xl bg-gradient-to-br from-indigo-700 via-violet-600 to-emerald-500 p-8 text-white shadow-lg md:p-12"><div className="max-w-3xl"><span className="rounded-full bg-white/15 px-3 py-1 text-xs font-semibold">{course.category.name} · {course.level}</span><h1 className="mt-5 text-3xl font-bold md:text-5xl">{course.title}</h1><p className="mt-4 text-base leading-relaxed text-indigo-50">{course.description}</p></div></section><section className="space-y-5"><div><p className="text-sm font-semibold uppercase tracking-widest text-indigo-600">Syllabus</p><h2 className="mt-1 text-2xl font-bold text-slate-900">Course modules</h2></div>{course.modules.map((module) => <div key={module.id} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><div className="flex items-start justify-between gap-4"><div><p className="text-xs font-semibold uppercase text-slate-400">Module {module.order_index}</p><h3 className="mt-1 text-lg font-bold text-slate-900">{module.title}</h3><p className="mt-1 text-sm text-slate-500">{module.description}</p></div><BookOpen className="h-5 w-5 text-indigo-500" /></div><div className="mt-5 divide-y divide-slate-100">{module.lessons.map((lesson) => <Link key={lesson.id} to={`/lessons/${lesson.id}`} className="flex items-center justify-between gap-4 py-3 first:pt-0 last:pb-0 group"><span className="flex items-center gap-3"><PlayCircle className="h-5 w-5 text-indigo-500" /><span className="text-sm font-medium text-slate-700 group-hover:text-indigo-600">{lesson.title}</span></span><span className="flex items-center gap-1 text-xs text-slate-400"><Clock className="h-3.5 w-3.5" />{lesson.duration_minutes} min</span></Link>)}</div></div>)}</section></div>;
};
