import React from 'react';
import { Link, useParams } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { ArrowLeft, Clock, FileText } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { catalogService } from '@/services/catalog';
import { ErrorState, LoadingState } from '@/components/ApiState';

export const LessonPage: React.FC = () => {
  const { lessonId = '' } = useParams();
  const query = useQuery({ queryKey: ['lesson', lessonId], queryFn: () => catalogService.getLesson(lessonId), enabled: Boolean(lessonId) });
  if (query.isLoading) return <LoadingState label="Loading lesson..." />;
  if (query.isError || !query.data) return <div className="mx-auto max-w-3xl px-4 py-12"><ErrorState message="This lesson could not be found or is not published." onRetry={() => query.refetch()} /></div>;
  const lesson = query.data;
  return <div className="mx-auto max-w-4xl space-y-6 px-4 py-10 sm:px-6 lg:px-8"><Link to={`/courses/${lesson.course.slug}`} className="inline-flex items-center gap-2 text-sm font-semibold text-indigo-600"><ArrowLeft className="h-4 w-4" />Back to {lesson.course.title}</Link><header className="rounded-3xl border border-slate-200 bg-white p-7 shadow-sm md:p-10"><div className="flex flex-wrap items-center gap-3 text-xs font-semibold uppercase tracking-wider text-indigo-600"><span className="inline-flex items-center gap-1"><FileText className="h-4 w-4" />Lesson {lesson.order_index}</span><span className="inline-flex items-center gap-1 text-slate-400"><Clock className="h-4 w-4" />{lesson.duration_minutes} minutes</span></div><h1 className="mt-4 text-3xl font-bold text-slate-900 md:text-4xl">{lesson.title}</h1></header><article className="prose prose-slate max-w-none rounded-3xl border border-slate-200 bg-white p-7 shadow-sm md:p-10"><ReactMarkdown>{lesson.content}</ReactMarkdown></article></div>;
};
