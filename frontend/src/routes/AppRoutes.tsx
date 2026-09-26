import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { HomePage } from '@/pages/HomePage';
import { NotFoundPage } from '@/pages/NotFoundPage';
import { LoginPage } from '@/pages/LoginPage';
import { RegisterPage } from '@/pages/RegisterPage';
import { CoursesPage } from '@/pages/CoursesPage';
import { CourseDetailPage } from '@/pages/CourseDetailPage';
import { LessonPage } from '@/pages/LessonPage';
import { ProfilePage } from '@/pages/ProfilePage';
import { AdminPage } from '@/pages/AdminPage';

export const AppRoutes: React.FC = () => <Routes><Route path="/" element={<HomePage />} /><Route path="/login" element={<LoginPage />} /><Route path="/register" element={<RegisterPage />} /><Route path="/courses" element={<CoursesPage />} /><Route path="/courses/:slug" element={<CourseDetailPage />} /><Route path="/lessons/:lessonId" element={<LessonPage />} /><Route path="/profile" element={<ProfilePage />} /><Route path="/admin" element={<AdminPage />} /><Route path="*" element={<NotFoundPage />} /></Routes>;
