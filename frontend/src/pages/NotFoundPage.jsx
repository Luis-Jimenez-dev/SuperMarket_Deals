import { Link } from 'react-router-dom'

function NotFoundPage() {
  return (
    <div className="app">
      <h1>Page Not Found</h1>

      <p>
        The page you're looking for doesn't exist.
      </p>

      <Link to="/">
        Back to Home
      </Link>
    </div>
  )
}

export default NotFoundPage