export interface HealthCheckResponse {
  status: string;
  service: string;
  version: string;
  environment: string;
  timestamp: string;
}

export interface DatabaseHealthCheckResponse {
  status: 'ok' | 'unavailable';
  database_url_prefix: string;
  detail: string;
  timestamp: string;
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    details: unknown[];
  };
}
