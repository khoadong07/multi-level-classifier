'use client'

export default function TestPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">
          ✅ Test Page Working!
        </h1>
        <p className="text-gray-600">
          If you see this, Next.js is working correctly.
        </p>
        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded">
          <p className="text-sm text-green-800">
            Frontend is operational. The error might be in a specific component.
          </p>
        </div>
      </div>
    </div>
  )
}
