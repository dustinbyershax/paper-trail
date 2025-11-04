/**
 * Environment configuration for API base URL
 *
 * In development: Vite proxy handles /api requests to Flask backend
 * In production: Flask serves both frontend and API from same origin
 * Empty string means relative URLs, which works in both scenarios
 */
export const API_BASE_URL = '';
