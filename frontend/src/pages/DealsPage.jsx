import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

function DealsPage() {
  const [deals, setDeals] = useState([])
  const [searchTerm, setSearchTerm] = useState("")
  const filteredDeals = deals.filter(deal =>
    deal.item.toLowerCase().includes(searchTerm.toLowerCase())
  )

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

      <p>{filteredDeals.length === 1 
          ? filteredDeals.length + " deal found" 
          : filteredDeals.length + " deals found" }
      </p>

      {filteredDeals.length === 0 && searchTerm.trim() !== "" &&(
        <p>No results found for: {searchTerm}</p>
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