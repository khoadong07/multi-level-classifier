'use client'

import { useState, useEffect } from 'react'
import { Download, CheckCircle, TrendingUp } from 'lucide-react'
import axios from 'axios'

interface ResultsPanelProps {
  jobId: string
}

export default function ResultsPanel({ jobId }: ResultsPanelProps) {
  const [status, setStatus] = useState<any>(null)
  const [downloading, setDownloading] = useState(false)

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/status/${jobId}`)
        setStatus(response.data)
      } catch (err) {
        console.error('Failed to fetch status:', err)
      }
    }
    fetchStatus()
  }, [jobId])

  const handleDownload = async () => {
    setDownloading(true)
    try {
      const response = await axios.get(
        `http://localhost:8000/api/download/${jobId}`,
        { responseType: 'blob' }
      )
      
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${status.filename.replace('.xlsx', '')}_classified.xlsx`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (err) {
      alert('Lỗi khi tải file')
    } finally {
      setDownloading(false)
    }
  }

  if (!status) {
    return <div>Đang tải...</div>
  }

  if (status.status !== 'completed') {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">Chưa có kết quả. Vui lòng hoàn thành xử lý trước.</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Kết quả phân loại</h2>
        <CheckCircle className="text-green-500" size={32} />
      </div>

      {/* Success Message */}
      <div className="p-6 bg-green-50 border border-green-200 rounded-lg">
        <h3 className="text-lg font-semibold text-green-900 mb-2">
          ✅ Phân loại hoàn thành!
        </h3>
        <p className="text-green-700">
          File <span className="font-semibold">{status.filename}</span> đã được phân loại thành công.
        </p>
      </div>

      {/* Statistics */}
      {status.stats && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
            <TrendingUp size={20} />
            <span>Thống kê</span>
          </h3>
          
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="p-4 bg-gray-50 rounded-lg border text-center">
              <p className="text-sm text-gray-600 mb-1">Tổng số dòng</p>
              <p className="text-3xl font-bold text-gray-900">{status.stats.total_tasks}</p>
            </div>
            
            <div className="p-4 bg-green-50 rounded-lg border border-green-200 text-center">
              <p className="text-sm text-green-600 mb-1">Cache hits</p>
              <p className="text-3xl font-bold text-green-700">{status.stats.cache_hits}</p>
            </div>
            
            <div className="p-4 bg-blue-50 rounded-lg border border-blue-200 text-center">
              <p className="text-sm text-blue-600 mb-1">API calls</p>
              <p className="text-3xl font-bold text-blue-700">{status.stats.api_calls}</p>
            </div>
            
            <div className="p-4 bg-red-50 rounded-lg border border-red-200 text-center">
              <p className="text-sm text-red-600 mb-1">Thất bại</p>
              <p className="text-3xl font-bold text-red-700">{status.stats.failed}</p>
            </div>
            
            <div className="p-4 bg-purple-50 rounded-lg border border-purple-200 text-center">
              <p className="text-sm text-purple-600 mb-1">Tỷ lệ thành công</p>
              <p className="text-3xl font-bold text-purple-700">{status.stats.success_rate}%</p>
            </div>
          </div>
        </div>
      )}

      {/* Download Button */}
      <button
        onClick={handleDownload}
        disabled={downloading}
        className="w-full flex items-center justify-center space-x-2 px-6 py-4 bg-primary text-white rounded-lg hover:bg-primary/90 shadow-lg hover:shadow-xl transition-all disabled:bg-gray-400"
      >
        <Download size={24} />
        <span className="text-lg font-medium">
          {downloading ? 'Đang tải xuống...' : 'Tải xuống file đã phân loại'}
        </span>
      </button>

      {/* Info */}
      <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-900">
          <strong>Lưu ý:</strong> File đã được phân loại sẽ có thêm 5 cột mới: 
          <span className="font-mono"> label_en, label_1, label_2, label_3, label_4</span>
        </p>
      </div>
    </div>
  )
}
