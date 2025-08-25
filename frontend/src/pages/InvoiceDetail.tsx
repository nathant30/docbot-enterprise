import React from 'react';
import { useParams } from 'react-router-dom';

const InvoiceDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  return (
    <div className="max-w-7xl mx-auto py-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Invoice Details</h1>
        <p className="text-gray-600">Invoice ID: {id}</p>
      </div>
      
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Invoice Information</h3>
        </div>
        <div className="p-6">
          <p className="text-gray-500">Invoice details will be available once the backend is connected.</p>
        </div>
      </div>
    </div>
  );
};

export default InvoiceDetail;