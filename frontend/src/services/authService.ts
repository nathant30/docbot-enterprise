import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://docbot-enterprise-backend.onrender.com';

interface LoginResponse {
  access_token: string;
  token_type: string;
  user_id: number;
}

interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  is_admin: boolean;
  is_active: boolean;
  last_login: string | null;
  created_at: string;
  updated_at: string;
}

class AuthService {
  private getAuthHeaders(token: string) {
    return {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    };
  }

  async login(email: string, password: string): Promise<LoginResponse> {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/v1/auth/login`, {
        email,
        password,
      });
      return response.data;
    } catch (error: any) {
      if (error.response?.status === 401) {
        throw new Error('Invalid email or password');
      }
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  }

  async getCurrentUser(token: string): Promise<User> {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/users/me`, {
        headers: this.getAuthHeaders(token),
      });
      return response.data;
    } catch (error: any) {
      if (error.response?.status === 401) {
        throw new Error('Invalid or expired token');
      }
      throw new Error(error.response?.data?.detail || 'Failed to get user data');
    }
  }

  async refreshToken(token: string): Promise<LoginResponse> {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/v1/auth/refresh`, {}, {
        headers: this.getAuthHeaders(token),
      });
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Token refresh failed');
    }
  }

  async register(userData: {
    email: string;
    password: string;
    first_name: string;
    last_name: string;
  }): Promise<User> {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/v1/auth/register`, userData);
      return response.data;
    } catch (error: any) {
      if (error.response?.status === 400) {
        throw new Error(error.response.data?.detail || 'Registration failed');
      }
      throw new Error('Registration failed');
    }
  }

  async forgotPassword(email: string): Promise<void> {
    try {
      await axios.post(`${API_BASE_URL}/api/v1/auth/forgot-password`, { email });
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to send reset email');
    }
  }

  async resetPassword(token: string, password: string): Promise<void> {
    try {
      await axios.post(`${API_BASE_URL}/api/v1/auth/reset-password`, {
        token,
        password,
      });
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to reset password');
    }
  }

  async updateProfile(token: string, userData: {
    first_name?: string;
    last_name?: string;
    email?: string;
  }): Promise<User> {
    try {
      const response = await axios.put(`${API_BASE_URL}/api/v1/users/me`, userData, {
        headers: this.getAuthHeaders(token),
      });
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to update profile');
    }
  }

  async changePassword(token: string, currentPassword: string, newPassword: string): Promise<void> {
    try {
      await axios.post(`${API_BASE_URL}/api/v1/auth/change-password`, {
        current_password: currentPassword,
        new_password: newPassword,
      }, {
        headers: this.getAuthHeaders(token),
      });
    } catch (error: any) {
      if (error.response?.status === 400) {
        throw new Error('Current password is incorrect');
      }
      throw new Error(error.response?.data?.detail || 'Failed to change password');
    }
  }
}

export const authService = new AuthService();