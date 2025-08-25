import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface UploadResponse {
  status: string;
  invoice_id: number;
  extracted_data: any;
  confidence_score: number;
}

class InvoiceService {
  private getAuthHeaders() {
    const token = localStorage.getItem('docbot_token');
    return {
      Authorization: `Bearer ${token}`,
    };
  }

  async uploadInvoice(file: File): Promise<UploadResponse> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(`${API_BASE_URL}/api/v1/invoices/upload`, formData, {
        headers: {
          ...this.getAuthHeaders(),
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data;
    } catch (error: any) {
      if (error.response?.status === 401) {
        throw new Error('Authentication required');
      }
      throw new Error(error.response?.data?.detail || 'Failed to upload invoice');
    }
  }

  async getInvoices(params?: {
    skip?: number;
    limit?: number;
    status_filter?: string;
  }) {
    try {
      const queryParams = new URLSearchParams();
      if (params?.skip) queryParams.append('skip', params.skip.toString());
      if (params?.limit) queryParams.append('limit', params.limit.toString());
      if (params?.status_filter) queryParams.append('status_filter', params.status_filter);

      const response = await axios.get(`${API_BASE_URL}/api/v1/invoices?${queryParams}`, {
        headers: this.getAuthHeaders(),
      });

      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to get invoices');
    }
  }

  async getInvoice(invoiceId: number) {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/invoices/${invoiceId}`, {
        headers: this.getAuthHeaders(),
      });

      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to get invoice');
    }
  }

  async approveInvoice(invoiceId: number) {
    try {
      const response = await axios.put(`${API_BASE_URL}/api/v1/invoices/${invoiceId}/approve`, {}, {
        headers: this.getAuthHeaders(),
      });

      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to approve invoice');
    }
  }
}

export const invoiceService = new InvoiceService();