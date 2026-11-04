import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'

function HomePage() {
  const [deals, setDeals] = useState([])
  const [meals, setMeals] = useState(1)

  // Separate loading states for deals and meal plans
  const [dealsLoading, setDealsLoading] = useState(false)
  const [mealPlanLoading, setMealPlanLoading] = useState(false)

  const [postalCode, setPostalCode] = useState("")
  const [nearbyStores, setNearbyStores] = useState([])
  const [selectedStore, setSelectedStore] = useState(null)

  const navigate = useNavigate()

  // Find nearby stores using the ZIP code
  const findNearbyStores = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/stores/nearby?postal_code=${postalCode}`
      )

      if (!response.ok) {
        throw new Error("Failed to find nearby stores")
      }

      const data = await response.json()

      setNearbyStores(data)
      localStorage.setItem("postalCode", postalCode)
    } catch (error) {
      console.error("Failed to find nearby stores:", error)
    }
  }

  // Save the selected store so it persists after refreshing
  const selectStore = (store) => {
    setSelectedStore(store)
    setDeals([])
    localStorage.setItem("selectedStore", JSON.stringify(store))
  }

  // Clear the current store and show nearby stores again
  const changeStore = () => {
    setSelectedStore(null)
    setDeals([])
    localStorage.removeItem("selectedStore")

    if (postalCode) {
      findNearbyStores()
    }
  }

  // Restore the selected store and ZIP code when the page loads
  useEffect(() => {
    const savedStore = localStorage.getItem("selectedStore")
    const savedPostalCode = localStorage.getItem("postalCode")

    if (savedStore) {
      setSelectedStore(JSON.parse(savedStore))
    }

    if (savedPostalCode) {
      setPostalCode(savedPostalCode)
    }
  }, [])

  // Load deals whenever the selected store changes
  useEffect(() => {
    if (!selectedStore) {
      return
    }

    setDealsLoading(true)
    setDeals([])

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
      .finally(() => {
        setDealsLoading(false)
      })

  }, [selectedStore])

  // Generate a meal plan using the currently selected store
  function generateMealPlan() {
    if (!selectedStore || meals <= 0 || dealsLoading) {
      return
    }

    setMealPlanLoading(true)

    fetch(
      `http://127.0.0.1:8000/stores/${selectedStore.store_id}/meal-plan?meals=${meals}`
    )
      .then(response => {
        if (!response.ok) {
          throw new Error("Failed to generate meal plan")
        }

        return response.json()
      })
      .then(data => {
        navigate('/meal-plan', {
          state: {
            mealPlan: data,
            store: selectedStore
          }
        })
      })
      .catch(error => {
        console.error("Failed to generate meal plan:", error)
      })
      .finally(() => {
        setMealPlanLoading(false)
      })
  }

  return (
    <div className="app">

      {selectedStore ? (
        <section className="store-info">
          <p>Shopping at:</p>

          <h2>{selectedStore.name}</h2>

          <p>
            {selectedStore.city}, {selectedStore.state}
          </p>

          {dealsLoading ? (
            <p>Loading this week's deals...</p>
          ) : (
            <p>
              {deals.length === 1
                ? "1 deal found"
                : `${deals.length} deals found`}
            </p>
          )}

          <button
            onClick={changeStore}
            disabled={dealsLoading}
          >
            Change Store
          </button>
        </section>
      ) : (
        <section className="store-search">
          <p>Find a store near you</p>

          <input
            type="text"
            value={postalCode}
            maxLength={5}
            placeholder="ZIP code"
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
                  (store) =>
                    store.store_id === Number(event.target.value)
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
        </section>
      )}

      <section className="weekly-deals-preview">
        <div className="section-header">
          <h2>Weekly Deals</h2>

          {selectedStore && !dealsLoading && (
            <Link to="/deals">
              View All Deals
            </Link>
          )}
        </div>

        {!selectedStore ? (
          <p>Select a store to see this week's deals.</p>
        ) : dealsLoading ? (
          <p>Loading this week's deals...</p>
        ) : deals.length === 0 ? (
          <p>No deals are currently available for this store.</p>
        ) : (
          <div className="deal-grid">
            {deals.slice(0, 6).map((deal) => (
              <div
                className="deal-card"
                key={deal.source_product_id ?? deal.id ?? deal.item}
              >
                <h3>{deal.item}</h3>
                <p>${deal.price}</p>
              </div>
            ))}
          </div>
        )}
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
              onChange={(event) =>
                setMeals(Number(event.target.value))
              }
            />
          </label>
        </div>

        <button
          className="generate-button"
          onClick={generateMealPlan}
          disabled={
            mealPlanLoading ||
            dealsLoading ||
            !selectedStore ||
            deals.length === 0
          }
        >
          {dealsLoading
            ? "Loading Deals..."
            : mealPlanLoading
              ? "Building Your Meal Plan..."
              : "Build My Meal Plan"}
        </button>

      </section>

    </div>
  )
}

export default HomePage