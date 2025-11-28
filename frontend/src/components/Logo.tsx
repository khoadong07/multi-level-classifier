interface LogoProps {
  size?: 'sm' | 'md' | 'lg'
  showText?: boolean
}

export default function Logo({ size = 'md', showText = false }: LogoProps) {
  const sizeClasses = {
    sm: 'h-6',
    md: 'h-8',
    lg: 'h-16'
  }

  return (
    <div className="flex items-center space-x-3">
      <img 
        src="https://kompa.ai/assets/images/logo.svg" 
        alt="Kompa Logo" 
        className={sizeClasses[size]}
      />
      {showText && (
        <span className="text-xl font-bold text-gray-900">
          Kompa MultiLevel Classifier
        </span>
      )}
    </div>
  )
}
