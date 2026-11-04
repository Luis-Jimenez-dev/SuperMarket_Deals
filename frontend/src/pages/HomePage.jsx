import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'

function HomePage() {
  const [deals, setDeals] = useState([])
  const [meals, setMeals] = useState(1)
  const [loading, setLoading] = useState(false)
  const [postalCode, setPostalCode] = useState("")
  const [nearbyStores, setNearbyStores] = useState([])
  const [selectedStore, setSelectedStore] = useState(null)

  const navigate = useNavigate()

  const findNearbyStores = async () => {
      const response = await fetch(
          `http://localhost:8000/stores/nearby?postal_code=${postalCode}`
      )

      const data = await response.json()

      setNearbyStores(data)
      localStorage.setItem("postalCode", postalCode)
  }

  const selectStore = (store) => {
    setSelectedStore(store)
    localStorage.setItem("selectedStore", JSON.stringify(store))
  }

  const changeStore = () => {
    setSelectedStore(null)
    localStorage.removeItem("selectedStore")
    findNearbyStores()
  }

  useEffect(() => {
    if (!selectedStore){
      return
    }
    fetch(`http://127.0.0.1:8000/stores/${selectedStore.store_id}/deals`)
      .then(response => response.json())
      .then(data => setDeals(data))
  }, [selectStore])

  useEffect(() => {
  const savedStore = localStorage.getItem("selectedStore")
  const savedPostalCode = localStorage.getItem("postalCode")

  if (savedStore) {
    setSelectedStore(JSON.parse(savedStore))
  }
  if (savedPostalCode){
    setPostalCode(savedPostalCode)
  }
}, [])

  function generateMealPlan() {
    if (meals <= 0) {
      return
    }

    setLoading(true)

    fetch(
      `http://127.0.0.1:8000/stores/${selectedStore.store_id}/meal-plan?meals=${meals}`
    )
      .then(response => response.json())
      .then(data => {
        navigate('/meal-plan', {
          state: {
            mealPlan: data,
            store: 'Safeway Broadway'
          }
        })
      })
      .catch(error => {
        console.error('Failed to generate meal plan:', error)
      })
      .finally(() => {
        setLoading(false)
      })
  }

  return (
    <div className="app">

      <section className="store-info">
        <h2>Safeway Broadway</h2>
        <p>Oakland, CA</p>
        <p>{deals.length} deals found</p>
      </section>
      
{selectedStore ? (
  <div>
    <p>Shopping at:</p>
    <p>{selectedStore.name}</p>

    <button onClick={changeStore}>
      Change Store
    </button>
  </div>
) : (
  <div>
    <p>Find a store near you</p>

    <input
      type="text"
      value={postalCode}
      maxLength={5}
      onChange={(event) => setPostalCode(event.target.value)}
    />

    <button onClick={findNearbyStores}>
      Find Stores
    </button>

    {nearbyStores.length > 0 && (
      <select
        defaultValue=""
        onChange={(event) => {
          const store = nearbyStores.find(
            (store) => store.store_id === Number(event.target.value)
          )

          if (store) {
            selectStore(store)
          }
        }}
      >
        <option value="" disabled>
          Choose a store
        </option>

        {nearbyStores.map((store) => (
          <option
            key={store.store_id}
            value={store.store_id}
          >
            {store.name} — {store.distance} miles
          </option>
        ))}
      </select>
    )}
  </div>
)}

      <section className="weekly-deals-preview">
        <div className="section-header">
          <h2>Weekly Deals</h2>
          <Link to="/deals">View All Deals</Link>
        </div>

        <div className="deal-grid">
          {deals.slice(0, 6).map((deal, index) => (
            <div className="deal-card" key={index}>
              <h3>{deal.item}</h3>
              <p>${deal.price}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="planner">
        <h2>Turn these deals into meals</h2>

        <div className="planner-controls">
          <label>
            Number of meals:
            <input
              type="number"
              min="1"
              value={meals}
              onChange={event => setMeals(event.target.value)}
            />
          </label>
        </div>

        <button
          className="generate-button"
          onClick={generateMealPlan}
          disabled={loading}
        >
          {loading ? 'Building Your Meal Plan...' : 'Build My Meal Plan'}
        </button>
      </section>

    </div>
  )
}

export default HomePage