import React from 'react';

const VendorList: React.FC = () => {
  return (
    <div className="max-w-7xl mx-auto py-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Vendor Management</h1>
        <p className="text-gray-600">Manage vendor information and relationships</p>
      </div>
      
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Vendor Directory</h3>
        </div>
        <div className="p-6">
          <p className="text-gray-500">Vendor management will be available once the backend is connected.</p>
        </div>
      </div>
    </div>
  );
};

export default VendorList;