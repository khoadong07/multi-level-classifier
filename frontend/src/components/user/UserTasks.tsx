'use client'

import { useState, useEffect } from 'react'
import { RefreshCw, Download, XCircle, Loader2, CheckCircle, Clock } from 'lucide-react'
import api from '@/lib/api'

interface UserTasksProps {
  highlightJobId?: string | null
}

export default function UserTasks({ highlightJobId }: UserTasksProps) {
  const [tasks, setTasks] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<string>('all')

  const fetchTasks = async () => {
    try {
      const url = filter === 'all' 
        ? '/api/tasks'
        : `/api/tasks?status=${filter}`
      
      const response = await api.get(url)
      setTasks(response.data.tasks)
    } catch (err) {
      console.error('Failed to fetch tasks:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTasks()
    const interval = setInterval(fetchTasks, 3000)
    return () => clearInterval(interval)
  }, [filter])

  const handleDownload = async (jobId: string, filename: string) => {
    try {
      const response = await api.get(`/api/download/${jobId}`, { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${filename.replace('.xlsx', '')}_classified.xlsx`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (err) {
      alert('Lỗi khi tải file')
    }
  }

  const handleCancel = async (jobId: string) => {
    if (!confirm('Bạn có chắc muốn hủy task này?')) return
    
    try {
      await api.delete(`/api/tasks/${jobId}`)
      fetchTasks()
    } catch (err) {
      alert('Lỗi khi hủy task')
    }
  }

  const handleStartProcessing = async (jobId: string) => {
    try {
      await api.post(`/api/classify/${jobId}`)
      fetchTasks()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Lỗi khi bắt đầu xử lý')
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle className="text-green-500" size={20} />
      case 'processing': return <Loader2 className="text-blue-500 animate-spin" size={20} />
      case 'pending': return <Clock className="text-yellow-500" size={20} />
      case 'failed': return <XCircle className="text-red-500" size={20} />
      default: return <Clock className="text-gray-500" size={20} />
    }
  }

  const getStatusBadge = (status: string) => {
    const colors = {
      completed: 'bg-green-100 text-green-800',
      processing: 'bg-blue-100 text-blue-800',
      pending: 'bg-yellow-100 text-yellow-800',
      failed: 'bg-red-100 text-red-800',
      uploaded: 'bg-gray-100 text-gray-800',
      cancelled: 'bg-gray-100 text-gray-800'
    }
    
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status as keyof typeof colors] || colors.uploaded}`}>
        {status}
      </span>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Tasks của tôi</h2>
        <button
          onClick={fetchTasks}
          className="flex items-center space-x-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-md"
        >
          <RefreshCw size={16} />
          <span>Làm mới</span>
        </button>
      </div>

      {/* Filter */}
      <div className="flex space-x-2">
        {['all', 'pending', 'processing', 'completed', 'failed'].map((status) => (
          <button
            key={status}
            onClick={() => setFilter(status)}
            className={`px-4 py-2 rounded-md font-medium transition-colors ${
              filter === status
                ? 'bg-primary text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {status === 'all' ? 'Tất cả' : status}
          </button>
        ))}
      </div>

      {/* Tasks List */}
      {loading ? (
        <div className="text-center py-12">
          <Loader2 className="animate-spin mx-auto text-gray-400" size={48} />
        </div>
      ) : tasks.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <p className="text-gray-600">Chưa có task nào</p>
        </div>
      ) : (
        <div className="space-y-4">
          {tasks.map((task) => (
            <div
              key={task.job_id}
              className={`p-6 bg-white border rounded-lg shadow-sm hover:shadow-md transition-shadow ${
                highlightJobId === task.job_id ? 'ring-2 ring-primary' : ''
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    {getStatusIcon(task.status)}
                    <h3 className="text-lg font-semibold text-gray-900">{task.filename}</h3>
                    {getStatusBadge(task.status)}
                  </div>
                  
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 text-sm">
                    <div>
                      <p className="text-gray-600">Topic</p>
                      <p className="font-semibold">{task.topic_name || 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Số dòng</p>
                      <p className="font-semibold">{task.rows}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Tiến trình</p>
                      <p className="font-semibold">{task.progress}%</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Tạo lúc</p>
                      <p className="font-semibold text-xs">
                        {new Date(task.created_at).toLocaleString('vi-VN')}
                      </p>
                    </div>
                  </div>

                  {/* Progress Bar */}
                  {task.status === 'processing' && (
                    <div className="mt-4">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-primary h-2 rounded-full transition-all"
                          style={{ width: `${task.progress}%` }}
                        />
                      </div>
                    </div>
                  )}

                  {/* Stats */}
                  {task.stats && (
                    <div className="grid grid-cols-4 gap-2 mt-4">
                      <div className="text-center p-2 bg-gray-50 rounded">
                        <p className="text-xs text-gray-600">Total</p>
                        <p className="font-bold">{task.stats.total_tasks}</p>
                      </div>
                      <div className="text-center p-2 bg-green-50 rounded">
                        <p className="text-xs text-green-600">Cache</p>
                        <p className="font-bold text-green-700">{task.stats.cache_hits}</p>
                      </div>
                      <div className="text-center p-2 bg-blue-50 rounded">
                        <p className="text-xs text-blue-600">API</p>
                        <p className="font-bold text-blue-700">{task.stats.api_calls}</p>
                      </div>
                      <div className="text-center p-2 bg-purple-50 rounded">
                        <p className="text-xs text-purple-600">Success</p>
                        <p className="font-bold text-purple-700">{task.stats.success_rate}%</p>
                      </div>
                    </div>
                  )}

                  {/* Error */}
                  {task.error && (
                    <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
                      <p className="text-sm text-red-700">{task.error}</p>
                    </div>
                  )}
                </div>

                {/* Actions */}
                <div className="flex space-x-2 ml-4">
                  {task.status === 'uploaded' && (
                    <button
                      onClick={() => handleStartProcessing(task.job_id)}
                      className="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90 font-medium"
                      title="Bắt đầu xử lý"
                    >
                      Xử lý
                    </button>
                  )}
                  
                  {task.status === 'completed' && (
                    <button
                      onClick={() => handleDownload(task.job_id, task.filename)}
                      className="p-2 bg-green-500 text-white rounded-md hover:bg-green-600"
                      title="Tải xuống"
                    >
                      <Download size={20} />
                    </button>
                  )}
                  
                  {task.status !== 'processing' && task.status !== 'completed' && (
                    <button
                      onClick={() => handleCancel(task.job_id)}
                      className="p-2 bg-red-500 text-white rounded-md hover:bg-red-600"
                      title="Hủy"
                    >
                      <XCircle size={20} />
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
