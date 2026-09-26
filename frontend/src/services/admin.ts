import { apiClient } from '@/services/api';
import type { CategorySummary, CourseDetail, CourseListItem, LessonSummary, ModuleSummary } from '@/types/catalog';

export interface AdminCategoryList { items: CategorySummary[] }
export interface AdminCourseList { items: CourseListItem[]; total: number }
export interface CoursePayload { category_id: string; title: string; slug: string; description: string; level: string; status: string }
export interface ModulePayload { title: string; description?: string; order_index: number }
export interface LessonPayload { title: string; slug: string; content: string; order_index: number; duration_minutes: number; is_published: boolean }

export const adminService = {
  categories: async () => (await apiClient.get<AdminCategoryList>('/admin/categories')).data,
  courses: async () => (await apiClient.get<AdminCourseList>('/admin/courses')).data,
  course: async (id: string) => (await apiClient.get<CourseDetail>(`/admin/courses/${id}`)).data,
  createCourse: async (payload: CoursePayload) => (await apiClient.post<CourseDetail>('/admin/courses', payload)).data,
  updateCourse: async (id: string, payload: Partial<CoursePayload>) => (await apiClient.patch<CourseDetail>(`/admin/courses/${id}`, payload)).data,
  deleteCourse: async (id: string) => { await apiClient.delete(`/admin/courses/${id}`); },
  createModule: async (courseId: string, payload: ModulePayload) => (await apiClient.post<ModuleSummary>(`/admin/courses/${courseId}/modules`, payload)).data,
  updateModule: async (id: string, payload: Partial<ModulePayload>) => (await apiClient.patch<ModuleSummary>(`/admin/modules/${id}`, payload)).data,
  deleteModule: async (id: string) => { await apiClient.delete(`/admin/modules/${id}`); },
  createLesson: async (moduleId: string, payload: LessonPayload) => (await apiClient.post<LessonSummary>(`/admin/modules/${moduleId}/lessons`, payload)).data,
  updateLesson: async (id: string, payload: Partial<LessonPayload>) => (await apiClient.patch<LessonSummary>(`/admin/lessons/${id}`, payload)).data,
  deleteLesson: async (id: string) => { await apiClient.delete(`/admin/lessons/${id}`); },
};
