'use client'

import { useState } from 'react'
import ProtectedRoute from '@/components/ProtectedRoute'
import Navbar from '@/components/Navbar'
import UserManagement from '@/components/admin/UserManagement'
import TopicManagement from '@/components/admin/TopicManagement'
import AllTasks from '@/components/admin/AllTasks'
import { Users, FolderKanban, Activity } from 'lucide-react'

export default function AdminPage() {
  const [activeTab, setActiveTab] = useState<'users' | 'topics' | 'tasks'>('users')

  const tabs = [
    { id: 'users', label: 'Quản lý Users', icon: Users },
    { id: 'topics', label: 'Quản lý Topics', icon: FolderKanban },
    { id: 'tasks', label: 'Tất cả Tasks', icon: Activity },
  ]

  return (
    <ProtectedRoute requireAdmin>
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
            {activeTab === 'users' && <UserManagement />}
            {activeTab === 'topics' && <TopicManagement />}
            {activeTab === 'tasks' && <AllTasks />}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  )
}
