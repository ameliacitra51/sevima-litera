import { apiClient } from '@/services/api';
import type { CourseDetail, CourseLevel, CourseListResponse, LessonDetail } from '@/types/catalog';

export interface CourseFilters {
  page?: number;
  page_size?: number;
  category?: string;
  level?: CourseLevel | '';
  search?: string;
}

export const catalogService = {
  listCourses: async (filters: CourseFilters = {}): Promise<CourseListResponse> => {
    const response = await apiClient.get<CourseListResponse>('/courses', {
      params: {
        page: filters.page ?? 1,
        page_size: filters.page_size ?? 12,
        category: filters.category || undefined,
        level: filters.level || undefined,
        search: filters.search || undefined,
      },
    });
    return response.data;
  },
  getCourse: async (slug: string): Promise<CourseDetail> => {
    const response = await apiClient.get<CourseDetail>(`/courses/${slug}`);
    return response.data;
  },
  getLesson: async (lessonId: string): Promise<LessonDetail> => {
    const response = await apiClient.get<LessonDetail>(`/lessons/${lessonId}`);
    return response.data;
  },
};
