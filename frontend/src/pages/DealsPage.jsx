import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

function DealsPage() {
  const [deals, setDeals] = useState([])
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("All")

  const [selectedStore] = useState(() => {
    const savedStore = localStorage.getItem("selectedStore")

    return savedStore
      ? JSON.parse(savedStore)
      : null
  })

  const [dealsLoading, setDealsLoading] = useState(
    () => selectedStore !== null
  )

  const [dealsError, setDealsError] = useState("")

  // Load deals for the selected store
  useEffect(() => {
    if (!selectedStore) {
      return
    }

    fetch(
      `http://127.0.0.1:8000/stores/${selectedStore.store_id}/deals`
    )
      .then(async response => {
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.detail)
        }

        return response.json()
      })
      .then(data => {
        setDeals(data)
      })
      .catch(error => {
        console.error("Failed to load deals:", error)
        setDealsError(error.message)
      })
      .finally(() => {
        setDealsLoading(false)
      })

  }, [selectedStore])

  // Build a list of categories from the loaded deals
  const categories = [
    "All",
    ...new Set(
      deals
        .map(deal => deal.category_path?.[2])
        .filter(Boolean)
    )
  ]

  // Filter deals using the search term and selected category
  const filteredDeals = deals.filter(deal => {
    const matchesSearch = deal.item
      .toLowerCase()
      .includes(searchTerm.toLowerCase())

    const dealCategory = deal.category_path?.[2]

    const matchesCategory =
      selectedCategory === "All" ||
      dealCategory === selectedCategory

    return matchesSearch && matchesCategory
  })

  if (!selectedStore) {
    return (
      <div className="app">
        <Link to="/">← Back</Link>

        <h1>Weekly Deals</h1>

        <p>
          Select a store from the home page to see this week's deals.
        </p>

        <Link to="/">Choose a Store</Link>
      </div>
    )
  }

  return (
    <div className="app">
      <Link to="/">← Back</Link>

      <div className="deals-page-header">
        <h1>Weekly Deals</h1>

        <p>
          {selectedStore.name}
          {selectedStore.city &&
            ` · ${selectedStore.city}, ${selectedStore.state}`}
        </p>
      </div>

      <section className="deal-filters">
        <input
          type="text"
          placeholder="Search deals"
          value={searchTerm}
          onChange={(event) =>
            setSearchTerm(event.target.value)
          }
        />

        <select
          value={selectedCategory}
          onChange={(event) =>
            setSelectedCategory(event.target.value)
          }
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

      ) : filteredDeals.length === 0 ? (
        <p>No deals found.</p>

      ) : (
        <div className="deal-grid">
          {filteredDeals.map(deal => (
            <div
              className="deal-card"
              key={deal.id}
            >
              <h3>{deal.item}</h3>

              <p>${deal.price}</p>

              {deal.promotion && (
                <p>{deal.promotion}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default DealsPage