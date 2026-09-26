export interface HealthCheckResponse {
  status: string;
  service: string;
  version: string;
  environment: string;
  timestamp: string;
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    details: unknown[];
  };
}
