import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

function DealsPage() {
  const [deals, setDeals] = useState([])
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("All")

  const filteredDeals = deals.filter(deal =>
    deal.item.toLowerCase().includes(searchTerm.toLowerCase()) &&
    (
      selectedCategory === "All" || 
      deal.category_path[2] === selectedCategory
    )
  )
  const categories = [
    ...new Set(
      deals
      .map(deal => deal.category_path[2])
      .filter(Boolean)
    )
  ]

  useEffect(() => {
    fetch('http://127.0.0.1:8000/stores/Safeway Broadway/deals')
      .then(response => response.json())
      .then(data => setDeals(data))
  }, [])

  return (
    <div className="app">

      <Link to="/">← Back</Link>

      <div className="deals-header">
        <h1>Weekly Deals</h1>
        <p>Safeway Broadway · Oakland, CA</p>
      </div>

      <input
        type = "text"
        value = {searchTerm}
        onChange={event => setSearchTerm(event.target.value)}
        placeholder='Search weekly deals...'
      />

      <select
        value={selectedCategory}
        onChange={event => setSelectedCategory(event.target.value)}
      >
        <option value = 'All'>All Categories</option>
        {categories.map((category, index) => (
          <option key={index} value={category}>
            {category}
          </option>
        ))}
      </select>

      {filteredDeals.length > 0 && (
        <p>
          {filteredDeals.length === 1
            ? filteredDeals.length + " deal found"
            : filteredDeals.length + " deals found"}
        </p>
      )}

      {filteredDeals.length === 0 && (
        <p>No results found</p>
      )}

      <div className="deal-grid">
        {filteredDeals.map((deal, index) => (
          <div className="deal-card" key={index}>
            <h3>{deal.item}</h3>
            <p>${deal.price}</p>
          </div>
        ))}
      </div>

    </div>
  )
}

export default DealsPage