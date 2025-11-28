'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { LogOut, User } from 'lucide-react'
import { getUser, clearAuth, User as UserType } from '@/lib/auth'

export default function Navbar() {
  const router = useRouter()
  const [user, setUser] = useState<UserType | null>(null)

  useEffect(() => {
    // Get user only on client side
    setUser(getUser())
  }, [])

  const handleLogout = () => {
    clearAuth()
    router.push('/login')
  }

  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-3">
            <img 
              src="https://kompa.ai/assets/images/logo.svg" 
              alt="Kompa Logo" 
              className="h-8"
            />
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                Kompa MultiLevel Classifier
              </h1>
              <p className="text-xs text-gray-600">
                {user?.role === 'admin' ? 'Admin Dashboard' : 'User Dashboard'}
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {user && (
              <div className="flex items-center space-x-2 px-3 py-2 bg-gray-100 rounded-md">
                <User size={16} className="text-gray-600" />
                <span className="text-sm font-medium text-gray-900">{user.username}</span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${
                  user.role === 'admin' 
                    ? 'bg-primary text-white' 
                    : 'bg-gray-300 text-gray-700'
                }`}>
                  {user.role}
                </span>
              </div>
            )}

            <button
              onClick={handleLogout}
              className="flex items-center space-x-2 px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
            >
              <LogOut size={16} />
              <span className="text-sm">Đăng xuất</span>
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
