import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://docbot-enterprise-backend.onrender.com';

interface DashboardStats {
  total_invoices: number;
  pending_review: number;
  approved_invoices: number;
  processing_accuracy: number;
  avg_processing_time: number;
}

interface RecentInvoice {
  id: number;
  invoice_number: string;
  vendor_name: string;
  total_amount: number;
  status: string;
  created_at: string;
}

class DashboardService {
  private getAuthHeaders() {
    const token = localStorage.getItem('docbot_token');
    return {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    };
  }

  async getStats(): Promise<DashboardStats> {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/stats/dashboard`, {
        headers: this.getAuthHeaders(),
      });
      return response.data;
    } catch (error: any) {
      if (error.response?.status === 401) {
        throw new Error('Authentication required');
      }
      throw new Error(error.response?.data?.detail || 'Failed to get dashboard stats');
    }
  }

  async getRecentInvoices(limit: number = 10): Promise<RecentInvoice[]> {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/invoices?limit=${limit}`, {
        headers: this.getAuthHeaders(),
      });
      return response.data.invoices || [];
    } catch (error: any) {
      if (error.response?.status === 401) {
        throw new Error('Authentication required');
      }
      throw new Error(error.response?.data?.detail || 'Failed to get recent invoices');
    }
  }
}

export const dashboardService = new DashboardService();