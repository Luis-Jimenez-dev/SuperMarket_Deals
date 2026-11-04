import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

function DealsPage() {
  const [deals, setDeals] = useState([])
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("All")
  const [selectedStore, setSelectedStore] = useState(null)

  // Restore the store selected on the homepage
  useEffect(() => {
    const savedStore = localStorage.getItem("selectedStore")

    if (savedStore) {
      setSelectedStore(JSON.parse(savedStore))
    }
  }, [])

  // Load deals after the selected store is available
  useEffect(() => {
    if (!selectedStore) {
      return
    }

    fetch(
      `http://127.0.0.1:8000/stores/${selectedStore.store_id}/deals`
    )
      .then(response => {
        if (!response.ok) {
          throw new Error("Failed to load deals")
        }

        return response.json()
      })
      .then(data => {
        setDeals(data)
      })
      .catch(error => {
        console.error("Failed to load deals:", error)
      })

  }, [selectedStore])

  const filteredDeals = deals.filter(deal =>
    deal.item.toLowerCase().includes(searchTerm.toLowerCase()) &&
    (
      selectedCategory === "All" ||
      deal.category_path?.[2] === selectedCategory
    )
  )

  const categories = [
    ...new Set(
      deals
        .map(deal => deal.category_path?.[2])
        .filter(Boolean)
    )
  ]

  return (
    <div className="app">

      <Link to="/">← Back</Link>

      <div className="deals-header">
        <h1>Weekly Deals</h1>

        {selectedStore && (
          <p>
            {selectedStore.name}
            {selectedStore.city && ` · ${selectedStore.city}, ${selectedStore.state}`}
          </p>
        )}
      </div>

      <input
        type="text"
        value={searchTerm}
        onChange={event => setSearchTerm(event.target.value)}
        placeholder="Search weekly deals..."
      />

      <select
        value={selectedCategory}
        onChange={event => setSelectedCategory(event.target.value)}
      >
        <option value="All">All Categories</option>

        {categories.map(category => (
          <option key={category} value={category}>
            {category}
          </option>
        ))}
      </select>

      {filteredDeals.length > 0 ? (
        <p>
          {filteredDeals.length === 1
            ? "1 deal found"
            : `${filteredDeals.length} deals found`}
        </p>
      ) : (
        <p>No results found</p>
      )}

      <div className="deal-grid">
        {filteredDeals.map(deal => (
          <div
            className="deal-card"
            key={deal.source_product_id ?? deal.id ?? deal.item}
          >
            <h3>{deal.item}</h3>
            <p>${deal.price}</p>
          </div>
        ))}
      </div>

    </div>
  )
}

export default DealsPage