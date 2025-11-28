'use client'

import { useState } from 'react'
import ProtectedRoute from '@/components/ProtectedRoute'
import Navbar from '@/components/Navbar'
import UserUpload from '@/components/user/UserUpload'
import UserTasks from '@/components/user/UserTasks'
import { Upload, Activity } from 'lucide-react'

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<'upload' | 'tasks'>('upload')
  const [currentJobId, setCurrentJobId] = useState<string | null>(null)

  const tabs = [
    { id: 'upload', label: 'Tải lên', icon: Upload },
    { id: 'tasks', label: 'Tasks của tôi', icon: Activity },
  ]

  const handleUploadSuccess = (jobId: string) => {
    setCurrentJobId(jobId)
    setActiveTab('tasks')
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        <Navbar />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Tabs */}
          <div className="bg-white rounded-lg shadow-sm p-2 mb-6">
            <nav className="flex space-x-2">
              {tabs.map((tab) => {
                const Icon = tab.icon
                const isActive = activeTab === tab.id
                
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={`
                      flex items-center space-x-2 px-4 py-2 rounded-md font-medium transition-all
                      ${isActive 
                        ? 'bg-primary text-white shadow-md' 
                        : 'text-gray-700 hover:bg-gray-100'
                      }
                    `}
                  >
                    <Icon size={18} />
                    <span>{tab.label}</span>
                  </button>
                )
              })}
            </nav>
          </div>

          {/* Content */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            {activeTab === 'upload' && (
              <UserUpload onUploadSuccess={handleUploadSuccess} />
            )}
            {activeTab === 'tasks' && (
              <UserTasks highlightJobId={currentJobId} />
            )}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  )
}
