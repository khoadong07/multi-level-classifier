'use client'

import { useState, useEffect } from 'react'
import { RefreshCw, Download, Trash2, XCircle, Loader2, CheckCircle, Clock } from 'lucide-react'
import api from '@/lib/api'

export default function AllTasks() {
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

  const handleDelete = async (jobId: string) => {
    if (!confirm('Bạn có chắc muốn xóa task này?')) return
    
    try {
      await api.delete(`/api/tasks/${jobId}`)
      fetchTasks()
    } catch (err) {
      alert('Lỗi khi xóa task')
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
        <h2 className="text-2xl font-bold text-gray-900">Tất cả Tasks</h2>
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

      {/* Tasks Table */}
      {loading ? (
        <div className="text-center py-12">
          <Loader2 className="animate-spin mx-auto text-gray-400" size={48} />
        </div>
      ) : tasks.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <p className="text-gray-600">Không có task nào</p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Topic</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">File</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Progress</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rows</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Created</th>
                <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {tasks.map((task) => (
                <tr key={task.job_id} className="hover:bg-gray-50">
                  <td className="px-4 py-4 whitespace-nowrap font-medium">{task.user}</td>
                  <td className="px-4 py-4 whitespace-nowrap text-sm">{task.topic_name || 'N/A'}</td>
                  <td className="px-4 py-4 whitespace-nowrap text-sm">{task.filename}</td>
                  <td className="px-4 py-4 whitespace-nowrap">
                    <div className="flex items-center space-x-2">
                      {getStatusIcon(task.status)}
                      {getStatusBadge(task.status)}
                    </div>
                  </td>
                  <td className="px-4 py-4 whitespace-nowrap">
                    <div className="flex items-center space-x-2">
                      <div className="w-24 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-primary h-2 rounded-full"
                          style={{ width: `${task.progress}%` }}
                        />
                      </div>
                      <span className="text-sm">{task.progress}%</span>
                    </div>
                  </td>
                  <td className="px-4 py-4 whitespace-nowrap text-sm">{task.rows}</td>
                  <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(task.created_at).toLocaleString('vi-VN')}
                  </td>
                  <td className="px-4 py-4 whitespace-nowrap text-right">
                    <div className="flex justify-end space-x-2">
                      {task.status === 'completed' && (
                        <button
                          onClick={() => handleDownload(task.job_id, task.filename)}
                          className="p-2 text-green-600 hover:bg-green-50 rounded"
                          title="Download"
                        >
                          <Download size={16} />
                        </button>
                      )}
                      {task.status !== 'processing' && (
                        <button
                          onClick={() => handleDelete(task.job_id)}
                          className="p-2 text-red-600 hover:bg-red-50 rounded"
                          title="Delete"
                        >
                          <Trash2 size={16} />
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
