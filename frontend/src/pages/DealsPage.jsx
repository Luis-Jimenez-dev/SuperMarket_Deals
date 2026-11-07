import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

const API_URL = 'http://127.0.0.1:8000'

function DealsPage() {
  const [deals, setDeals] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('All')

  const [selectedStore] = useState(() => {
    const savedStore = localStorage.getItem('selectedStore')

    return savedStore
      ? JSON.parse(savedStore)
      : null
  })

  const [dealsLoading, setDealsLoading] = useState(
    () => selectedStore !== null
  )

  const [dealsError, setDealsError] = useState('')

  useEffect(() => {
    if (!selectedStore) {
      return
    }

    fetch(
      `${API_URL}/stores/${selectedStore.store_id}/deals`
    )
      .then(async response => {
        if (!response.ok) {
          let message = 'Unable to load deals.'

          try {
            const errorData = await response.json()
            message = errorData.detail || message
          } catch {
            // Use the fallback message.
          }

          throw new Error(message)
        }

        return response.json()
      })
      .then(data => {
        setDeals(data)
      })
      .catch(error => {
        console.error('Failed to load deals:', error)

        setDealsError(
          error instanceof Error
            ? error.message
            : 'Unable to load deals.'
        )
      })
      .finally(() => {
        setDealsLoading(false)
      })

  }, [selectedStore])

  const categories = [
    'All',
    ...new Set(
      deals
        .map(deal => deal.category)
        .filter(Boolean)
    ),
  ].sort((a, b) => {
    if (a === 'All') {
      return -1
    }

    if (b === 'All') {
      return 1
    }

    return a.localeCompare(b)
  })

  const normalizedSearchTerm = searchTerm
    .trim()
    .toLowerCase()

  const filteredDeals = deals.filter(deal => {
    const matchesSearch = deal.item
      .toLowerCase()
      .includes(normalizedSearchTerm)

    const matchesCategory =
      selectedCategory === 'All' ||
      deal.category === selectedCategory

    return matchesSearch && matchesCategory
  })

  if (!selectedStore) {
    return (
      <div className="app empty-page">
        <Link className="back-link" to="/">
          ← Back
        </Link>

        <h1>Weekly Deals</h1>

        <p>
          Select a store from the home page to see this week's deals.
        </p>

        <Link className="primary-link" to="/">
          Choose a Store
        </Link>
      </div>
    )
  }

  return (
    <div className="app">
      <Link className="back-link" to="/">
        ← Back
      </Link>

      <header className="deals-page-header">
        <p className="page-eyebrow">
          {selectedStore.name}
        </p>

        <h1>Weekly Deals</h1>

        {selectedStore.city && (
          <p className="page-description">
            {selectedStore.city}
            {selectedStore.state &&
              `, ${selectedStore.state}`}
          </p>
        )}

        {!dealsLoading && !dealsError && (
          <p className="deal-count">
            {deals.length === 1
              ? '1 deal available'
              : `${deals.length} deals available`}
          </p>
        )}
      </header>

      <section className="deal-filters">
        <input
          className="deal-search"
          type="search"
          placeholder="Search deals"
          aria-label="Search deals"
          value={searchTerm}
          onChange={(event) => {
            setSearchTerm(event.target.value)
          }}
        />

        <select
          className="category-filter"
          aria-label="Filter deals by category"
          value={selectedCategory}
          onChange={(event) => {
            setSelectedCategory(event.target.value)
          }}
        >
          {categories.map(category => (
            <option
              key={category}
              value={category}
            >
              {category}
            </option>
          ))}
        </select>
      </section>

      {dealsLoading ? (
        <p>Loading this week's deals...</p>
      ) : dealsError ? (
        <p className="error-message">
          {dealsError}
        </p>
      ) : deals.length === 0 ? (
        <p>
          No deals are currently available for this store.
        </p>
      ) : filteredDeals.length === 0 ? (
        <p>
          No deals match your current search or category.
        </p>
      ) : (
        <div className="deal-grid">
          {filteredDeals.map(deal => (
            <article
              className="deal-card"
              key={deal.id}
            >
              {deal.category && (
                <p className="deal-category">
                  {deal.category}
                </p>
              )}

              <h3 className="deal-name">
                {deal.item}
              </h3>

              {deal.price != null && (
                <p className="deal-price">
                  ${Number(deal.price).toFixed(2)}
                </p>
              )}

              {deal.promotion && (
                <p className="deal-promotion">
                  {deal.promotion}
                </p>
              )}
            </article>
          ))}
        </div>
      )}
    </div>
  )
}

export default DealsPage