import { apiClient } from '@/services/api';
import type { AuthResponse, LoginPayload, RegisterPayload, User } from '@/types/catalog';

const TOKEN_KEY = 'litera_token';

export const authService = {
  register: async (payload: RegisterPayload): Promise<User> => {
    const response = await apiClient.post<User>('/auth/register', payload);
    return response.data;
  },
  login: async (payload: LoginPayload): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>('/auth/login', payload);
    localStorage.setItem(TOKEN_KEY, response.data.access_token);
    return response.data;
  },
  me: async (): Promise<User> => {
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  },
  logout: async (): Promise<void> => {
    if (localStorage.getItem(TOKEN_KEY)) {
      await apiClient.post('/auth/logout');
    }
    localStorage.removeItem(TOKEN_KEY);
  },
  hasToken: (): boolean => Boolean(localStorage.getItem(TOKEN_KEY)),
  clearToken: (): void => localStorage.removeItem(TOKEN_KEY),
};

export { TOKEN_KEY };
