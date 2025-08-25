import React from 'react';

const Settings: React.FC = () => {
  return (
    <div className="max-w-7xl mx-auto py-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600">Configure your DocBot Enterprise system</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Account Settings</h3>
          </div>
          <div className="p-6">
            <p className="text-gray-500">Account configuration options will be available here.</p>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">System Configuration</h3>
          </div>
          <div className="p-6">
            <p className="text-gray-500">System settings and preferences will be available here.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;