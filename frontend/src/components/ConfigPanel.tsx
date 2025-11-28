'use client'

import { Server, Cpu, Database, Trash2 } from 'lucide-react'
import axios from 'axios'
import { useState } from 'react'

interface ConfigPanelProps {
  config: any
  onConfigUpdate: (config: any) => void
}

export default function ConfigPanel({ config, onConfigUpdate }: ConfigPanelProps) {
  const [clearing, setClearing] = useState(false)

  const handleClearCache = async () => {
    if (!confirm('Bạn có chắc muốn xóa cache?')) return
    
    setClearing(true)
    try {
      await axios.delete('http://localhost:8000/api/cache')
      const response = await axios.get('http://localhost:8000/api/config')
      onConfigUpdate(response.data)
      alert('Đã xóa cache thành công!')
    } catch (err) {
      alert('Lỗi khi xóa cache')
    } finally {
      setClearing(false)
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Cấu hình hệ thống</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* API Config */}
        <div className="p-6 bg-gray-50 rounded-lg border">
          <div className="flex items-center space-x-3 mb-4">
            <Server className="text-primary" size={24} />
            <h3 className="text-lg font-semibold">API Configuration</h3>
          </div>
          <dl className="space-y-2 text-sm">
            <div>
              <dt className="text-gray-600">Model:</dt>
              <dd className="font-mono text-gray-900">{config.model}</dd>
            </div>
            <div>
              <dt className="text-gray-600">Base URL:</dt>
              <dd className="font-mono text-gray-900 truncate">{config.base_url}</dd>
            </div>
          </dl>
        </div>

        {/* Processing Config */}
        <div className="p-6 bg-gray-50 rounded-lg border">
          <div className="flex items-center space-x-3 mb-4">
            <Cpu className="text-primary" size={24} />
            <h3 className="text-lg font-semibold">Processing</h3>
          </div>
          <dl className="space-y-2 text-sm">
            <div>
              <dt className="text-gray-600">Max Workers:</dt>
              <dd className="font-mono text-gray-900">{config.max_workers}</dd>
            </div>
          </dl>
        </div>

        {/* Cache Config */}
        <div className="p-6 bg-gray-50 rounded-lg border md:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <Database className="text-primary" size={24} />
              <h3 className="text-lg font-semibold">Cache</h3>
            </div>
            <button
              onClick={handleClearCache}
              disabled={clearing}
              className="flex items-center space-x-2 px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 disabled:bg-gray-400"
            >
              <Trash2 size={16} />
              <span>{clearing ? 'Đang xóa...' : 'Xóa cache'}</span>
            </button>
          </div>
          <dl className="space-y-2 text-sm">
            <div>
              <dt className="text-gray-600">Cache Size:</dt>
              <dd className="font-mono text-gray-900">{config.cache_size} entries</dd>
            </div>
          </dl>
        </div>
      </div>
    </div>
  )
}
