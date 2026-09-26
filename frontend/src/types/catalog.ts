export type UserRole = 'STUDENT' | 'ADMIN';
export type CourseLevel = 'BEGINNER' | 'INTERMEDIATE' | 'ADVANCED';
export type CourseStatus = 'DRAFT' | 'PUBLISHED' | 'ARCHIVED';

export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface RegisterPayload {
  email: string;
  username: string;
  full_name: string;
  password: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface CategorySummary {
  id: string;
  name: string;
  slug: string;
}

export interface LessonSummary {
  id: string;
  title: string;
  slug: string;
  order_index: number;
  duration_minutes: number;
  is_published: boolean;
}

export interface ModuleSummary {
  id: string;
  title: string;
  description: string | null;
  order_index: number;
  lessons: LessonSummary[];
}

export interface CourseListItem {
  id: string;
  title: string;
  slug: string;
  description: string;
  thumbnail_url: string | null;
  level: CourseLevel;
  status: CourseStatus;
  category: CategorySummary;
}

export interface CourseDetail extends CourseListItem {
  modules: ModuleSummary[];
}

export interface CourseListResponse {
  items: CourseListItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface LessonDetail {
  id: string;
  title: string;
  slug: string;
  content: string;
  order_index: number;
  duration_minutes: number;
  is_published: boolean;
  module_id: string;
  course: CourseListItem;
}
