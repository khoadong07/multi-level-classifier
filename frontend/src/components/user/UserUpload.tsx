'use client'

import { useState, useEffect, useRef } from 'react'
import { Upload, FileSpreadsheet, AlertCircle, CheckCircle } from 'lucide-react'
import api from '@/lib/api'

interface UserUploadProps {
  onUploadSuccess: (jobId: string) => void
}

export default function UserUpload({ onUploadSuccess }: UserUploadProps) {
  const [topics, setTopics] = useState<any[]>([])
  const [selectedTopic, setSelectedTopic] = useState<string>('')
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [uploadInfo, setUploadInfo] = useState<any>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    fetchTopics()
  }, [])

  const fetchTopics = async () => {
    try {
      const response = await api.get('/api/topics')
      setTopics(response.data.topics)
      if (response.data.topics.length > 0) {
        setSelectedTopic(response.data.topics[0].topic_id)
      }
    } catch (err) {
      console.error('Failed to fetch topics:', err)
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      if (!selectedFile.name.endsWith('.xlsx')) {
        setError('Chỉ hỗ trợ file .xlsx')
        return
      }
      setFile(selectedFile)
      setError(null)
      setUploadInfo(null)
    }
  }

  const handleUpload = async () => {
    if (!file || !selectedTopic) {
      setError('Vui lòng chọn topic và file')
      return
    }

    setUploading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('topic_id', selectedTopic)

    try {
      const response = await api.post('/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      setUploadInfo(response.data)
      onUploadSuccess(response.data.job_id)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Lỗi khi tải file lên')
    } finally {
      setUploading(false)
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile && droppedFile.name.endsWith('.xlsx')) {
      setFile(droppedFile)
      setError(null)
    } else {
      setError('Chỉ hỗ trợ file .xlsx')
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Tải lên file Excel</h2>
        <p className="text-gray-600">
          File phải chứa các cột: <span className="font-semibold">Title</span>, 
          <span className="font-semibold"> Content</span>, 
          <span className="font-semibold"> Description</span>
        </p>
      </div>

      {/* Topic Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Chọn Topic xử lý *
        </label>
        <select
          value={selectedTopic}
          onChange={(e) => setSelectedTopic(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary"
          required
        >
          {topics.map((topic) => (
            <option key={topic.topic_id} value={topic.topic_id}>
              {topic.name} ({topic.model})
            </option>
          ))}
        </select>
        {topics.length === 0 && (
          <p className="text-sm text-red-600 mt-1">Chưa có topic nào. Liên hệ admin để tạo topic.</p>
        )}
      </div>

      {/* Upload Area */}
      <div
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        className={`
          border-2 border-dashed rounded-lg p-12 text-center transition-all
          ${file ? 'border-green-400 bg-green-50' : 'border-gray-300 hover:border-primary'}
        `}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".xlsx"
          onChange={handleFileChange}
          className="hidden"
        />

        {!file ? (
          <div className="space-y-4">
            <FileSpreadsheet className="mx-auto text-gray-400" size={64} />
            <div>
              <p className="text-lg font-medium text-gray-700">
                Kéo thả file vào đây hoặc
              </p>
              <button
                onClick={() => fileInputRef.current?.click()}
                className="mt-2 px-6 py-2 bg-primary text-white rounded-md hover:bg-primary/90"
              >
                Chọn file
              </button>
            </div>
            <p className="text-sm text-gray-500">Chỉ hỗ trợ file .xlsx</p>
          </div>
        ) : (
          <div className="space-y-4">
            <CheckCircle className="mx-auto text-green-500" size={64} />
            <div>
              <p className="text-lg font-medium text-gray-900">{file.name}</p>
              <p className="text-sm text-gray-500">
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
            <button
              onClick={() => {
                setFile(null)
                setUploadInfo(null)
              }}
              className="text-sm text-gray-600 hover:text-gray-900"
            >
              Chọn file khác
            </button>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="flex items-center space-x-2 p-4 bg-red-50 border border-red-200 rounded-lg">
          <AlertCircle className="text-red-500" size={20} />
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {/* Upload Info */}
      {uploadInfo && (
        <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
          <h3 className="font-semibold text-green-900 mb-2">✅ Tải lên thành công!</h3>
          <div className="text-sm text-green-700 space-y-1">
            <p>File: {uploadInfo.filename}</p>
            <p>Topic: {uploadInfo.topic}</p>
            <p>Số dòng: {uploadInfo.rows}</p>
          </div>
        </div>
      )}

      {/* Upload Button */}
      {file && !uploadInfo && (
        <button
          onClick={handleUpload}
          disabled={uploading || !selectedTopic}
          className={`
            w-full flex items-center justify-center space-x-2 px-6 py-3 rounded-lg font-medium
            ${uploading || !selectedTopic
              ? 'bg-gray-400 cursor-not-allowed' 
              : 'bg-primary hover:bg-primary/90 text-white shadow-md'
            }
          `}
        >
          <Upload size={20} />
          <span>{uploading ? 'Đang tải lên...' : 'Tải lên và bắt đầu xử lý'}</span>
        </button>
      )}
    </div>
  )
}
