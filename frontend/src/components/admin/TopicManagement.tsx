'use client'

import { useState, useEffect } from 'react'
import { FolderPlus, Edit, Trash2, RefreshCw } from 'lucide-react'
import api from '@/lib/api'

export default function TopicManagement() {
  const [topics, setTopics] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editingTopic, setEditingTopic] = useState<any>(null)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    llm_provider: 'openai',
    model: '',
    api_base_url: '',
    api_key: '',
    prompt_template: '',
    temperature: 0.0,
    max_tokens: 150
  })

  const fetchTopics = async () => {
    try {
      const response = await api.get('/api/topics')
      setTopics(response.data.topics)
    } catch (err) {
      console.error('Failed to fetch topics:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTopics()
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      if (editingTopic) {
        await api.put(`/api/topics/${editingTopic.topic_id}`, formData)
        alert('Topic updated successfully!')
      } else {
        await api.post('/api/topics', formData)
        alert('Topic created successfully!')
      }
      
      setShowModal(false)
      setEditingTopic(null)
      resetForm()
      fetchTopics()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Operation failed')
    }
  }

  const handleEdit = (topic: any) => {
    setEditingTopic(topic)
    setFormData({
      name: topic.name,
      description: topic.description || '',
      llm_provider: topic.llm_provider,
      model: topic.model,
      api_base_url: topic.api_base_url,
      api_key: topic.api_key || '',
      prompt_template: topic.prompt_template,
      temperature: topic.temperature,
      max_tokens: topic.max_tokens
    })
    setShowModal(true)
  }

  const handleDelete = async (topicId: string, name: string) => {
    if (!confirm(`Bạn có chắc muốn xóa topic "${name}"?`)) return
    
    try {
      await api.delete(`/api/topics/${topicId}`)
      fetchTopics()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to delete topic')
    }
  }

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      llm_provider: 'openai',
      model: '',
      api_base_url: '',
      api_key: '',
      prompt_template: '',
      temperature: 0.0,
      max_tokens: 150
    })
  }

  const openCreateModal = () => {
    setEditingTopic(null)
    resetForm()
    setShowModal(true)
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Quản lý Topics</h2>
        <div className="flex space-x-2">
          <button
            onClick={fetchTopics}
            className="flex items-center space-x-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-md"
          >
            <RefreshCw size={16} />
            <span>Làm mới</span>
          </button>
          <button
            onClick={openCreateModal}
            className="flex items-center space-x-2 px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90"
          >
            <FolderPlus size={16} />
            <span>Tạo Topic</span>
          </button>
        </div>
      </div>

      {/* Topics Grid */}
      {loading ? (
        <p>Đang tải...</p>
      ) : topics.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <p className="text-gray-600">Chưa có topic nào. Tạo topic đầu tiên!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {topics.map((topic) => (
            <div key={topic.topic_id} className="p-6 border rounded-lg hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{topic.name}</h3>
                  <p className="text-sm text-gray-600">{topic.description}</p>
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleEdit(topic)}
                    className="p-2 text-blue-600 hover:bg-blue-50 rounded"
                  >
                    <Edit size={16} />
                  </button>
                  <button
                    onClick={() => handleDelete(topic.topic_id, topic.name)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
              
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Provider:</span>
                  <span className="font-medium">{topic.llm_provider}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Model:</span>
                  <span className="font-medium">{topic.model}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Temperature:</span>
                  <span className="font-medium">{topic.temperature}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Max Tokens:</span>
                  <span className="font-medium">{topic.max_tokens}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Created by:</span>
                  <span className="font-medium">{topic.created_by}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create/Edit Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h3 className="text-xl font-bold mb-4">
              {editingTopic ? 'Chỉnh sửa Topic' : 'Tạo Topic Mới'}
            </h3>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="col-span-2">
                  <label className="block text-sm font-medium mb-1">Tên Topic *</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    className="w-full px-3 py-2 border rounded-md"
                    required
                  />
                </div>
                
                <div className="col-span-2">
                  <label className="block text-sm font-medium mb-1">Mô tả</label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    className="w-full px-3 py-2 border rounded-md"
                    rows={2}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">LLM Provider *</label>
                  <select
                    value={formData.llm_provider}
                    onChange={(e) => setFormData({...formData, llm_provider: e.target.value})}
                    className="w-full px-3 py-2 border rounded-md"
                  >
                    <option value="openai">OpenAI</option>
                    <option value="anthropic">Anthropic</option>
                    <option value="custom">Custom</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Model *</label>
                  <input
                    type="text"
                    value={formData.model}
                    onChange={(e) => setFormData({...formData, model: e.target.value})}
                    className="w-full px-3 py-2 border rounded-md"
                    placeholder="gpt-4, claude-3, etc"
                    required
                  />
                </div>

                <div className="col-span-2">
                  <label className="block text-sm font-medium mb-1">API Base URL *</label>
                  <input
                    type="text"
                    value={formData.api_base_url}
                    onChange={(e) => setFormData({...formData, api_base_url: e.target.value})}
                    className="w-full px-3 py-2 border rounded-md"
                    placeholder="https://api.openai.com/v1"
                    required
                  />
                </div>

                <div className="col-span-2">
                  <label className="block text-sm font-medium mb-1">API Key *</label>
                  <input
                    type="password"
                    value={formData.api_key}
                    onChange={(e) => setFormData({...formData, api_key: e.target.value})}
                    className="w-full px-3 py-2 border rounded-md"
                    placeholder="sk-..."
                    required={!editingTopic}
                  />
                  {editingTopic && (
                    <p className="text-xs text-gray-500 mt-1">Để trống nếu không muốn thay đổi</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Temperature</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="2"
                    value={formData.temperature}
                    onChange={(e) => setFormData({...formData, temperature: parseFloat(e.target.value)})}
                    className="w-full px-3 py-2 border rounded-md"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Max Tokens</label>
                  <input
                    type="number"
                    value={formData.max_tokens}
                    onChange={(e) => setFormData({...formData, max_tokens: parseInt(e.target.value)})}
                    className="w-full px-3 py-2 border rounded-md"
                  />
                </div>

                <div className="col-span-2">
                  <label className="block text-sm font-medium mb-1">Prompt Template *</label>
                  <textarea
                    value={formData.prompt_template}
                    onChange={(e) => setFormData({...formData, prompt_template: e.target.value})}
                    className="w-full px-3 py-2 border rounded-md font-mono text-sm"
                    rows={6}
                    placeholder="Your prompt template here..."
                    required
                  />
                </div>
              </div>

              <div className="flex space-x-2 pt-4">
                <button
                  type="submit"
                  className="flex-1 py-2 bg-primary text-white rounded-md hover:bg-primary/90"
                >
                  {editingTopic ? 'Cập nhật' : 'Tạo'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false)
                    setEditingTopic(null)
                    resetForm()
                  }}
                  className="flex-1 py-2 bg-gray-200 rounded-md hover:bg-gray-300"
                >
                  Hủy
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
